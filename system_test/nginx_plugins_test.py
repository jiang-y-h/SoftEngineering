import unittest
from flask import Flask
from flask_testing import TestCase
from plugins import app

class TestNginxPlugins(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_nginx_status(self):
        with self.client:
            response = self.client.get('/plugins/nginx')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'nginxMange.html', response.data)

    def test_nginx_operations(self):
        with self.client:
            response = self.client.post('/plugins/nginx', data={'types': '4'})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['resultCode'], 0)
            self.assertIn('result', data)

    def test_nginx_install(self):
        with self.client:
            response = self.client.get('/plugins/install/nginx')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'安装nginx', response.data)

if __name__ == '__main__':
    unittest.main()