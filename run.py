from factory import create_app
from flask_migrate import upgrade
import os

app = create_app()

# Run migrations on startup for Free Tier compatibility
with app.app_context():
    try:
        print("Running migrations...")
        upgrade()
        print("Migrations complete.")
        
        # Optionally seed if needed, but be careful with duplication
        # from seed_admin import seed_admin
        # seed_admin()
        
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)
