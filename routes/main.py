from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from app import db, Config
from models.models import Diagnosis
from models.predictor import DiseasePredictor
from forms import DiagnosisForm

main = Blueprint('main', __name__)
# Assume classes.json is in the same directory as the model
classes_path = os.path.join(os.path.dirname(Config.MODEL_PATH), 'classes.json')
predictor = DiseasePredictor(Config.MODEL_PATH, classes_path)

@main.route('/')
@login_required
def index():
    diagnoses = Diagnosis.query.filter_by(user_id=current_user.id).order_by(Diagnosis.diagnosis_date.desc()).all()
    return render_template('index.html', diagnoses=diagnoses)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_diagnosis():
    form = DiagnosisForm()
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(upload_path)
        
        # Use the real model prediction and get heatmap
        predicted_disease, confidence, heatmap_filename = predictor.predict(upload_path)
        
        diagnosis = Diagnosis(user_id=current_user.id, crop_id=1, image_path=filename,
                              predicted_disease=predicted_disease, confidence_score=confidence)
        db.session.add(diagnosis)
        db.session.commit()
        
        return render_template('result.html', disease=predicted_disease, 
                               confidence=confidence, heatmap=heatmap_filename)
    return render_template('upload.html', form=form)
