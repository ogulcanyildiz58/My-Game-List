import unittest
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class MyGameListTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.app = app.test_client()

    def test_index_page_loads(self):

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Game List', response.data)

    def test_login_page_get_method(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_home_page_redirects_without_session(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 302)

    def test_logout_redirects(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()