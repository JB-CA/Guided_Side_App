import unittest
from main import create_app
from dotenv import load_dotenv
from os import environ

# python -m unittest discover -s gratitude_app/tests -v
load_dotenv()
environ["FLASK_ENV"] = "testing"


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def test_users_can_be_read(self):
        response = self.client.get("/users/")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_users_can_be_read_by_id(self):
        pass
    def test_users_can_be_created(self):
        pass

    def test_users_can_be_deleted(self):
        pass

    def test_users_can_be_updated(self):
        pass


