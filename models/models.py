from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='farmer')  # farmer, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Crop(db.Model):
    crop_id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Disease(db.Model):
    disease_id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    disease_name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prevention = db.Column(db.Text)

class Diagnosis(db.Model):
    diagnosis_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id'), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    predicted_disease = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    diagnosis_date = db.Column(db.DateTime, default=datetime.utcnow)

class AgriInfo(db.Model):
    info_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
