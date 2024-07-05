import unittest
import json
from flask import Flask
from flask_testing import TestCase
from linkButton import app

class TestLinkButton(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_linkButton_get(self):
        with self.client:
            response = self.client.get('/linkButton')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<!DOCTYPE html>', response.data)

    def test_linkButton_post(self):
        with self.client:
            response = self.client.post('/linkButton')
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], 0)
            self.assertTrue('result' in json_data)

    def test_createLinkButton(self):
        with self.client:
            data = {
                'BUTTONNAME': 'TestButton',
                'TYPE': 'Type',
                'NOTE': 'Test Note',
                'SHELL': 'echo "Test shell"'
            }
            response = self.client.post('/linkButton/Create', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], 0)

    def test_deleteLinkButton(self):
        with self.client:
            data = {'BTID': '1'}  # Replace with an existing BTID for testing
            response = self.client.post('/linkButton/Delete', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], 0)

    def test_runLinkButton(self):
        with self.client:
            data = {
                'BTID': '1',  # Replace with an existing BTID for testing
                'SHELL': 'echo "Test shell"'
            }
            response = self.client.post('/linkButton/Run', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], 0)

    def test_runLinkButtonRunShell(self):
        with self.client:
            data = {'BTID': '1'}  # Replace with an existing BTID for testing
            response = self.client.get('/linkButton/RunShell', query_string=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'执行完成', response.data)

if __name__ == '__main__':
    unittest.main()