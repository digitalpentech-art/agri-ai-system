from factory import create_app
from factory import db
from models.models import Crop

app = create_app()

def seed_crops():
    with app.app_context():
        # Define crops
        crops_data = ['Pepper', 'Potato', 'Tomato']

        for name in crops_data:
            if not Crop.query.filter_by(crop_name=name).first():
                crop = Crop(crop_name=name)
                db.session.add(crop)
                print(f"Created crop: {name}")
            else:
                print(f"Crop already exists: {name}")
        
        db.session.commit()
        print("Crops seeding completed.")

if __name__ == '__main__':
    seed_crops()
