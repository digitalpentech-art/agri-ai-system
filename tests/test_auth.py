import unittest
from factory import create_app, db
from models.models import User
from sqlalchemy.pool import StaticPool

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        print("DEBUG: Setting up app...")
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'poolclass': StaticPool,
        }
        self.client = self.app.test_client()
        print("DEBUG: Creating DB...")
        with self.app.app_context():
            db.create_all()
        print("DEBUG: Setup complete.")

    def tearDown(self):
        print("DEBUG: Tearing down...")
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration(self):
        print("DEBUG: Running test_registration...")
        response = self.client.post('/register', data={
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
        print("DEBUG: test_registration complete.")

if __name__ == '__main__':
    unittest.main()
