import unittest
from urllib.parse import urlparse
from werkzeug.wrappers.response import Response
from main import create_app
from dotenv import load_dotenv
from os import environ

# python -m unittest discover -s gratitude_app/tests -v
load_dotenv()
environ["FLASK_ENV"] = "testing"


class TestUsers(unittest.TestCase):
    """Test all endpoints concerning users"""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_users_can_be_read(self):
        response = self.client.get("/users/")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)

    def test_user_can_be_read_by_id(self):
        response = self.client.get("/users/1")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, dict)
    
    def test_read_user_404(self):
        response = self.client.get("/users/0")
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, None)

    def test_user_can_be_created(self):
        response = self.client.post("/signup/", data={"name": "test", "email": "123@email.com", "password": "1234567890"})
        self.assertEqual(response.status_code, 302)
        # Redirect to /users/
        # Code from https://newbedev.com/flask-unit-testing-getting-the-response-s-redirect-location
        self.assertEqual(urlparse(response.location).path, "/users/")

    def test_user_cannot_be_created_with_missing_password_field(self):
        response = self.client.post("/signup/", json={"name": "test", "email": "123@email.com"})
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_be_created_with_missing_name_field(self):
        response = self.client.post("/signup/", json={"email": "123@email.com", "password": "1234567890"})
        self.assertEqual(response.status_code, 400)
    
    def test_user_cannot_be_created_with_missing_email_field(self):
        response = self.client.post("/signup/", json={"name": "test", "password": "1234567890"})
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_be_created_with_invalid_password_field(self):
        response = self.client.post("/signup/", json={"name": "test", "email": "123@email.com", "password": "12345"})
        self.assertEqual(response.status_code, 400)

    def test_user_cannot_be_created_with_invalid_name_field(self):
        response = self.client.post("/signup/", json={"name": "te$t", "email": "123@email.com", "password": "1234567890"})
        self.assertEqual(response.status_code, 400)
    
    def test_user_cannot_be_created_with_invalid_email_field(self):
        response = self.client.post("/signup/", json={"name": "test", "email": "123email.com", "password": "1234567890"})
        self.assertEqual(response.status_code, 400)

    def test_user_can_be_deleted(self):
        pass

    def test_user_can_be_updated(self):
        pass


