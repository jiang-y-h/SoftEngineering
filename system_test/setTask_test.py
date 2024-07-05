import unittest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient
from your_module import app

class TestTaskFunctions(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_creat_task(self):
        data = {
            'type': 'day',
            'hour': '12',
            'mint': '30',
            'senc': '15',
            'day': '01',
            'creatTime': '2023-01-01 12:00:00',
            'taskID': '1234567890',
            'nextRunTime': '2023-01-01 12:00:00',
            'value': 'echo 666'
        }

        with patch('your_module.task.CreatTask') as mock_creat_task:
            mock_creat_task.side_effect = lambda data: True

            response = self.app.post('/CreatTask', data=data)

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)

    def test_select_task(self):
        with patch('your_module.task.GetTaskList') as mock_get_task_list:
            mock_get_task_list.return_value = [{'taskID': '1234567890', 'type': 'day', 'hour': '12', 'mint': '30', 'senc': '15', 'creatTime': '2023-01-01 12:00:00', 'nextRunTime': '2023-01-01 12:00:00', 'value': 'echo 666'}]

            response = self.app.post('/SelectTask')

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)
            self.assertEqual(len(result['result']), 1)

    def test_delete_task(self):
        task_id = '1234567890'

        with patch('your_module.task.DeleteTask') as mock_delete_task:
            mock_delete_task.side_effect = lambda taskid: True

            response = self.app.post('/DeleteTask', data={'taskid': task_id})

            self.assertEqual(response.status_code, 200)
            result = response.get_json()
            self.assertEqual(result['resultCode'], 0)

if __name__ == '__main__':
    unittest.main()

