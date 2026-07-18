from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Automatically create tables and seed initial data
    from models.models import Crop, User
    from werkzeug.security import generate_password_hash
    with app.app_context():
        db.create_all()
        # Seed Crops
        if not Crop.query.first():
            crops = [
                Crop(crop_name='Pepper'),
                Crop(crop_name='Potato'),
                Crop(crop_name='Tomato')
            ]
            db.session.add_all(crops)
            db.session.commit()
        # Seed Admin User
        if not User.query.filter_by(role='admin').first():
            admin = User(
                full_name='Administrator',
                email='admin@agriai.com',
                phone='0000000000',
                password_hash=generate_password_hash('adminpassword'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from flask import send_from_directory
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
