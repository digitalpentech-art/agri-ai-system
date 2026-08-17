from factory import create_app, db
from models.models import Disease, Crop

app = create_app()

def seed_diseases():
    with app.app_context():
        # Map crop names to IDs
        crops = {c.crop_name: c.crop_id for c in Crop.query.all()}
        
        disease_data = [
            {
                'crop': 'Tomato',
                'name': 'Tomato_Late_blight',
                'symptoms': 'Dark, water-soaked spots on leaves that turn brown/black; white fungal growth on undersides.',
                'treatment': 'Apply copper-based fungicides; remove and destroy infected plant parts.',
                'prevention': 'Ensure good air circulation; avoid overhead watering; use resistant varieties.'
            },
            {
                'crop': 'Potato',
                'name': 'Potato___Late_blight',
                'symptoms': 'Brown lesions on leaves; white fuzzy growth under humid conditions.',
                'treatment': 'Fungicide applications; practice crop rotation.',
                'prevention': 'Remove cull piles; use certified disease-free seed tubers.'
            },
            {
                'crop': 'Pepper',
                'name': 'Pepper__bell___Bacterial_spot',
                'symptoms': 'Small, circular, dark spots on leaves with yellow halos.',
                'treatment': 'Copper-based bactericides; remove severely infected plants.',
                'prevention': 'Use disease-free seeds; practice crop rotation; avoid working in wet fields.'
            }
        ]
        
        for data in disease_data:
            crop_id = crops.get(data['crop'])
            if crop_id and not Disease.query.filter_by(disease_name=data['name']).first():
                disease = Disease(
                    crop_id=crop_id,
                    disease_name=data['name'],
                    symptoms=data['symptoms'],
                    treatment=data['treatment'],
                    prevention=data['prevention']
                )
                db.session.add(disease)
                print(f"Seeded disease: {data['name']}")
        
        db.session.commit()
        print("Disease table seeded.")

if __name__ == '__main__':
    seed_diseases()
