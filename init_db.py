from app import create_app, db
from models.models import User, Crop, Disease, Diagnosis, AgriInfo

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
    
    # Check if crops exist, if not, seed them
    if not Crop.query.first():
        crops = [
            Crop(crop_name='Pepper'),
            Crop(crop_name='Potato'),
            Crop(crop_name='Tomato')
        ]
        db.session.add_all(crops)
        db.session.commit()
        print("Database seeded with initial crops.")
