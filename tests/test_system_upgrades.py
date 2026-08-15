import unittest
from flask import Flask, url_for
from factory import create_app, db
from config import Config
import os

class TestSystemUpgrades(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_model_config(self):
        """Ensure model path is updated correctly."""
        self.assertIn('ml/models/mobilenetv2.h5', Config.MODEL_PATH)

    def test_admin_dashboard_access(self):
        """Ensure admin dashboard requires admin role."""
        response = self.client.get('/admin/dashboard')
        # Expect 403 or redirect to login depending on how @admin_required handles auth
        self.assertIn(response.status_code, [302, 403])

if __name__ == '__main__':
    unittest.main()
