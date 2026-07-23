from factory import create_app
from flask_migrate import upgrade
import os

# Create the database directory explicitly if it doesn't exist
db_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)
    # Attempt to set permissions if possible
    try:
        os.chmod(db_dir, 0o777)
    except Exception:
        pass

app = create_app()

# Run migrations on startup for Free Tier compatibility
with app.app_context():
    try:
        print("Running migrations...")
        upgrade()
        print("Migrations complete.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    app.run(debug=True)
