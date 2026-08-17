from factory import create_app, db
from models.models import User, Crop
from werkzeug.security import generate_password_hash
import os

app = create_app()

def initialize_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Seed crops if not present
        crops_data = ['Pepper', 'Potato', 'Tomato']
        for name in crops_data:
            if not Crop.query.filter_by(crop_name=name).first():
                crop = Crop(crop_name=name)
                db.session.add(crop)
                print(f"Created crop: {name}")
        
        # Check if admin exists
        admin_email = 'admin@example.com'
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            print("Creating default admin account...")
            password = 'adminpassword'
            admin = User(
                full_name='Administrator',
                email=admin_email,
                phone='0000000000',
                password_hash=generate_password_hash(password),
                role='admin'
            )
            db.session.add(admin)
            print("-----------------------------------")
            print(f"Default Admin Created:")
            print(f"Email: {admin_email}")
            print(f"Password: {password}")
            print("-----------------------------------")
        
        db.session.commit()
        print("Database initialized and seeded.")

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
