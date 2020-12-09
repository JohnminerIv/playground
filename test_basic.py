from app import app
from unittest import TestCase, main as unittest_main, mock



class AppTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)