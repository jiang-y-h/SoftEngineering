import unittest
import json
from index import app  

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass  # 可选：如果需要，清理每个测试后的数据

    def test_process_route(self):
        # 测试 '/Process' 路由
        response = self.client.get('/Process')
        self.assertEqual(response.status_code, 200)


    def test_get_network_list_route(self):
        # 测试 '/GetNetWorkList' 路由
        response = self.client.post('/GetNetWorkList')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resultCode', data)
        self.assertEqual(data['resultCode'], 0)


    def test_get_process_list_route(self):
        # 测试 '/GetProcessList' 路由
        response = self.client.post('/GetProcessList')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resultCode', data)
        self.assertEqual(data['resultCode'], 0)


    def test_kill_process_route(self):
        # 测试 '/KillPid' 路由
        # 假设需要一个存在的进程PID来进行测试
        existing_pid = 1234  # 替换为实际存在的PID
        response = self.client.post('/KillPid', data={'pid': existing_pid})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resultCode', data)
        self.assertEqual(data['resultCode'], 0)


    def test_process_details_route(self):
        # 测试 '/ProcessDetails' 路由
        # 假设需要一个存在的进程PID来进行测试
        existing_pid = 1234  # 替换为实际存在的PID
        response = self.client.post('/ProcessDetails', data={'pid': existing_pid})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('resultCode', data)
        self.assertEqual(data['resultCode'], 0)
        
if __name__ == '__main__':
    unittest.main()

