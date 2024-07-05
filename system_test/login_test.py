import unittest
from flask import Flask, session
from flask_testing import TestCase
from login import app

class TestLogin(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.secret_key = 'test_secret_key'
        return app

    def test_login_correct_credentials(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='test_username',
                password='test_password'
            ), follow_redirects=True)
            self.assertIn(b'Logged in successfully', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(session['username'], 'test_username')
            self.assertEqual(session['password'], 'test_password')

    def test_login_incorrect_credentials(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                username='wrong_username',
                password='wrong_password'
            ), follow_redirects=True)
            self.assertIn(b'账号或密码错误!', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('username', session)
            self.assertNotIn('password', session)

    def test_logout(self):
        with self.client:
            with self.client.session_transaction() as sess:
                sess['username'] = 'test_username'
                sess['password'] = 'test_password'
            response = self.client.get('/loginout', follow_redirects=True)
            self.assertIn(b'Logged out successfully', response.data)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('username', session)
            self.assertNotIn('password', session)

if __name__ == '__main__':
    unittest.main()