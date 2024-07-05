import unittest
import os
import tempfile
import json
from flask import Flask
from flask_testing import TestCase
from detectKPI import app

class TestKPIdetect(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_start_training_success(self):
        with self.client:
            data = {'model': 'model_name'}
            response = self.client.post('/StartTraining', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], '0')
            self.assertIn('训练成功', json_data['result'])

    def test_start_training_failure(self):
        with self.client:
            data = {'model': 'non_existing_model'}
            response = self.client.post('/StartTraining', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], '1')
            self.assertIn('训练失败', json_data['result'])

    def test_upload_kpi_file_success(self):
        with self.client:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix='.csv') as temp_file:
                temp_file.write(b'test data')
                temp_file.flush()
                
                # Simulate file upload
                data = {'kpiFile': (temp_file, 'test.csv')}
                response = self.client.post('/UploadKPIFile', data=data, content_type='multipart/form-data')
                
                self.assertEqual(response.status_code, 200)
                json_data = json.loads(response.data.decode('utf-8'))
                self.assertEqual(json_data['resultCode'], '0')
                self.assertIn('文件上传成功', json_data['result'])
                self.assertIn('anomaly_detection_plot.png', json_data['imagePath'])

    def test_upload_kpi_file_failure(self):
        with self.client:
            # Simulate file upload without file
            data = {'kpiFile': ''}
            response = self.client.post('/UploadKPIFile', data=data)
            self.assertEqual(response.status_code, 200)
            json_data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(json_data['resultCode'], '1')
            self.assertIn('文件上传失败', json_data['result'])

if __name__ == '__main__':
    unittest.main()