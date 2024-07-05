import unittest
from flask import Flask
from flask_testing import TestCase
from PenetrationSend import app

class TestPenetrationSend(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_penetration_send(self):
        with self.client:
            response = self.client.post('/PenetrationSend', headers={'Origin': 'http://localhost:5000'})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertIn('cpu', data)
            self.assertIn('memory', data)
            self.assertIn('disk', data)
            self.assertGreaterEqual(data['cpu'], 0.0)
            self.assertLessEqual(data['cpu'], 100.0)
            self.assertGreaterEqual(data['memory'], 0.0)
            self.assertLessEqual(data['memory'], 1.0)
            self.assertGreaterEqual(data['disk'], 0.0)
            self.assertLessEqual(data['disk'], 1.0)

if __name__ == '__main__':
    unittest.main()