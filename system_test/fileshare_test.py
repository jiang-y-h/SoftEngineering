import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, render_template, make_response, send_from_directory
import json
import os

# Assuming your Flask app is defined in index.py or accessible through import
from index import app, sql  # Assuming 'app' is your Flask application object and 'sql' is imported

class TestFileShareFunctions(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch.object(sql, 'creatFileShare')
    def test_creatFileShare(self, mock_creatFileShare):
        mock_creatFileShare.return_value = None

        response = self.app.post('/creatFileShare', data={'filepath': 'bG9va3MvZmlsZQ==', 'needvie': 'yes'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), '0')

    @patch.object(sql, 'deleteFileShare')
    def test_deleteFileShare(self, mock_deleteFileShare):
        mock_deleteFileShare.return_value = None

        response = self.app.post('/deleteFileShare', data={'ids': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), '0')

    @patch.object(sql, 'getFileShare')
    def test_getFileShare(self, mock_getFileShare):
        mock_getFileShare.return_value = [(1, 'test/file/path', 'yes')]

        response = self.app.get('/getFileShare')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(len(data['result']), 1)
        self.assertEqual(data['result'][0]['filename'], 'path')
        self.assertEqual(data['result'][0]['filepath'], 'test\\\\file\\\\path')
        self.assertEqual(data['result'][0]['ids'], 1)
        self.assertEqual(data['result'][0]['vie'], 'yes')

    def test_FileShare(self):
        response = self.app.get('/FileShare?ids=123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<title>File Share</title>', response.data.decode())

    @patch('index.sql.getShareFileInfo')
    @patch('index.os.path.split')
    @patch('index.os.path.exists')
    def test_DownFileShare(self, mock_exists, mock_split, mock_getShareFileInfo):
        mock_exists.return_value = True
        mock_split.return_value = ('path', 'filename')
        mock_getShareFileInfo.return_value = (123, '/test/file/path', '123456')

        response = self.app.get('/DownFileShare?ids=123&filevie=123456')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'attachment; filename=filename', response.headers['Content-Disposition'])

if __name__ == '__main__':
    unittest.main()

