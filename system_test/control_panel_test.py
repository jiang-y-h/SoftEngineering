import unittest
from unittest.mock import patch, Mock
from index import app, ControlPanel, ControlPanelConfig  # 导入 index.py 中的内容

class TestControlPanel(unittest.TestCase):

    def setUp(self):
        # 设置测试客户端
        self.client = app.test_client()
        self.client.testing = True

    def test_ControlPanel_GET(self):
        # 发送 GET 请求到 /ControlPanel 路由
        response = self.client.get('/ControlPanel')

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的页面内容或 JSON 数据
        self.assertIn(b'ControlPanel', response.data)  # 确保返回的页面包含 ControlPanel 字符串

    @patch('index.sql')
    def test_ControlPanel_POST(self, mock_sql):
        # 创建模拟的 SQL 查询结果
        mock_sql.selectInfo.return_value = (True, [{'key': 'value'}])

        # 发送 POST 请求到 /ControlPanel 路由
        response = self.client.post('/ControlPanel')

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的 JSON 数据
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertIn('result', data)

    def test_ControlPanelConfig(self):
        # 准备 POST 请求的参数
        params = {
            'state': 'on',
            'saveDay': '7',
            'inv': '60',
            'visitDay': '30'
        }

        # 发送 POST 请求到 /ControlPanelConfig 路由
        response = self.client.post('/ControlPanelConfig', data=params)

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的 JSON 数据
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

if __name__ == '__main__':
    unittest.main()
