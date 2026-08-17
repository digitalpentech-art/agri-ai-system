from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from utils.decorators import admin_required
from factory import db
from models.models import User, Crop, Disease
import os
import json

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    results_dir = 'ml/results'
    models = ['mobilenetv2', 'cnn', 'dnn']
    comparative_data = {}
    
    for model in models:
        metrics_path = os.path.join(results_dir, model, 'metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                comparative_data[model] = json.load(f)
        elif model == 'dnn':
            # Fallback for DNN
            report_path = os.path.join(results_dir, model, 'classification_report.json')
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    report = json.load(f)
                    comparative_data[model] = {'accuracy': report['accuracy'], 'precision': 0.0, 'recall': 0.0, 'f1_score': 0.0}
                
    users = User.query.all()
    crops = Crop.query.all()
    diseases = Disease.query.all()
    
    return render_template('admin/dashboard.html', 
                           comparative_data=comparative_data,
                           users=users,
                           crops=crops,
                           diseases=diseases)

# Placeholder CRUD routes
@admin.route('/admin/crop/add', methods=['POST'])
@login_required
@admin_required
def add_crop():
    name = request.form.get('crop_name')
    if name:
        db.session.add(Crop(crop_name=name))
        db.session.commit()
        flash('Crop added.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/admin/disease/add', methods=['POST'])
@login_required
@admin_required
def add_disease():
    name = request.form.get('disease_name')
    crop_id = request.form.get('crop_id')
    if name and crop_id:
        db.session.add(Disease(disease_name=name, crop_id=crop_id))
        db.session.commit()
        flash('Disease added.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/admin/user/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin user.', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
