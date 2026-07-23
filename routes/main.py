from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from factory import db, Config
from models.models import Diagnosis, Crop
from models.predictor import DiseasePredictor
from forms import DiagnosisForm, ClearHistoryForm
from sqlalchemy import func

main = Blueprint('main', __name__)

# Initialize predictor as None, instantiate lazily
_predictor = None

def get_predictor():
    global _predictor
    if _predictor is None:
        classes_path = os.path.join(os.path.dirname(Config.MODEL_PATH), 'classes.json')
        if os.path.exists(Config.MODEL_PATH):
            _predictor = DiseasePredictor(Config.MODEL_PATH, classes_path)
    return _predictor

@main.route('/')
def index():
    # Temporary bypass: redirect to upload to test core functionality directly
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Metrics
    diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).all()
    total_diagnoses = len(diagnoses)
    
    avg_confidence = db.session.query(func.avg(Diagnosis.confidence_score)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Disease Distribution
    disease_dist = db.session.query(Diagnosis.predicted_disease, func.count(Diagnosis.diagnosis_id)).filter_by(user_id=current_user.id).group_by(Diagnosis.predicted_disease).all()
    
    return render_template('dashboard.html', 
                           total=total_diagnoses, 
                           confidence=round(avg_confidence * 100, 2),
                           disease_dist=disease_dist,
                           recent=diagnoses[-5:][::-1],
                           clear_form=ClearHistoryForm())

@main.route('/dashboard/clear', methods=['POST'])
@login_required
def clear_history():
    form = ClearHistoryForm()
    if form.validate_on_submit():
        Diagnosis.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Prediction history cleared.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_diagnosis():
    form = DiagnosisForm()
    form.crop.choices = [(c.crop_id, c.crop_name) for c in Crop.query.all()]
    
    if form.validate_on_submit():
        predictor = get_predictor()
        if not predictor:
            flash('Model not found. Please contact administrator.')
            return redirect(url_for('main.upload_diagnosis'))
        
        if current_user.is_anonymous:
            flash('Please log in to upload.', 'danger')
            return redirect(url_for('auth.login'))
            
        file = form.image.data
        filename = secure_filename(file.filename)
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(upload_path)
        
        # Use the real model prediction and get heatmap
        predicted_disease, confidence, heatmap_filename = predictor.predict(upload_path)
        
        diagnosis = Diagnosis(user_id=current_user.id, crop_id=form.crop.data, image_path=filename,
                              predicted_disease=predicted_disease, confidence_score=confidence)
        db.session.add(diagnosis)
        db.session.commit()
        
        return render_template('result.html', disease=predicted_disease, 
                               confidence=confidence, heatmap=heatmap_filename)
    return render_template('upload.html', form=form)
