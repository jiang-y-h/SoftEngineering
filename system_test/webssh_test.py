import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from your_module import app

class TestSSHFunctions(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_ssh_login_success(self):
        data = {
            'host': 'example.com',
            'port': '22',
            'username': 'testuser',
            'pwd': 'testpassword'
        }

        with patch('your_module.paramiko.SSHClient.connect') as mock_ssh_connect:
            mock_ssh_connect.return_value = True

            response = self.app.post('/ssh', data=data)

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)
            self.assertIn('ids', result)

    def test_ssh_login_bad_authentication_type(self):
        data = {
            'host': 'example.com',
            'port': '22',
            'username': 'testuser',
            'pwd': 'testpassword'
        }

        with patch('your_module.paramiko.SSHClient.connect') as mock_ssh_connect:
            mock_ssh_connect.side_effect = paramiko.BadAuthenticationType

            response = self.app.post('/ssh', data=data)

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 1)
            self.assertEqual(result['result'], '登录失败,错误的连接类型')

    def test_ssh_input(self):
        ids = '1234567890'
        data = {
            'input': 'ls -l',
            'ids': ids
        }

        with patch.dict('your_module.sshListDict', {ids: mock.Mock()}):
            response = self.app.post('/SSHInput', data=data)

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)

    def test_get_ssh(self):
        ids = '1234567890'

        with patch.dict('your_module.sshListDict', {ids: mock.Mock()}):
            response = self.app.post('/GetSsh', data={'ids': ids})

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)

    def test_get_ssh_invalid_ids(self):
        ids = 'invalid_ids'

        response = self.app.post('/GetSsh', data={'ids': ids})

        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertEqual(result['resultCode'], 1)

if __name__ == '__main__':
    unittest.main()

