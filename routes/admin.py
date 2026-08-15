from flask import Blueprint, render_template
from flask_login import login_required
from utils.decorators import admin_required
import os
import json

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Comparative metrics data loading logic
    results_dir = 'ml/results'
    models = ['mobilenetv2', 'cnn', 'dnn']
    comparative_data = {}
    
    for model in models:
        metrics_path = os.path.join(results_dir, model, 'metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                comparative_data[model] = json.load(f)
                
    return render_template('admin/dashboard.html', comparative_data=comparative_data)
