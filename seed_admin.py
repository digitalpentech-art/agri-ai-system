import os
from factory import create_app
from factory import db
from models.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def seed_admin():
    with app.app_context():
        # Get password from environment variable
        password = os.getenv('ADMIN_PASSWORD', 'default_test_password')
        
        # Seed Admin User
        if not User.query.filter_by(role='admin').first():
            admin = User(
                full_name='Administrator',
                email='admin@agriai.com',
                phone='0000000000',
                password_hash=generate_password_hash(password),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user seeded.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    seed_admin()
