from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import click
from flask.cli import with_appcontext

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

@click.command("seed-db")
@with_appcontext
def seed_db():
    from models.models import Crop, User
    from werkzeug.security import generate_password_hash
    # Seed Crops
    if not Crop.query.first():
        crops = [
            Crop(crop_name='Pepper'),
            Crop(crop_name='Potato'),
            Crop(crop_name='Tomato')
        ]
        db.session.add_all(crops)
        db.session.commit()
        click.echo("Crops seeded.")
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
        click.echo("Admin user seeded.")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.cli.add_command(seed_db)

    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from flask import send_from_directory
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
