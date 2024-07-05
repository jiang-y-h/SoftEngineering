import unittest
from flask import Flask
from flask_testing import TestCase
from plugins import app

class TestMysqlPlugins(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_mysql_status(self):
        with self.client:
            response = self.client.get('/plugins/mysql')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'mysqlMange.html', response.data)

    def test_mysql_operations(self):
        with self.client:
            response = self.client.post('/plugins/mysql', data={'types': '4'})
            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertEqual(data['resultCode'], 0)
            self.assertIn('result', data)

    def test_mysql_install(self):
        with self.client:
            response = self.client.get('/plugins/install/mysql')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'安装MySQL', response.data)

if __name__ == '__main__':
    unittest.main()
