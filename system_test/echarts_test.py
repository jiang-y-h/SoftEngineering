import sys
import os
import unittest
import json

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上级目录，即项目根目录
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# 将项目根目录添加到 Python 的模块搜索路径
sys.path.append(parent_dir)

# 现在可以导入项目根目录中的 index.py 中的模块
from index import app

class TestSystemInfoRoutes(unittest.TestCase):

    def setUp(self):
        # 设置测试客户端
        self.app = app.test_client()
        self.app.testing = True

    def test_GetPie(self):
        # 发送 POST 请求到 /GetPie 路由
        response = self.app.post('/GetPie')

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的 JSON 数据
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['resultCode'], 0)

        # 验证返回的数据结构
        self.assertIn('result', data)
        self.assertIsInstance(data['result'], list)
        self.assertGreater(len(data['result']), 0)

    def test_GetLine(self):
        # 发送 POST 请求到 /GetLine 路由
        response = self.app.post('/GetLine')

        # 检查状态码
        self.assertEqual(response.status_code, 200)

        # 检查返回的 JSON 数据
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['resultCode'], 0)

        # 验证返回的数据结构
        self.assertIn('realTimeSent', data)
        self.assertIn('realTimeRcvd', data)
        self.assertIn('BytesSent', data)
        self.assertIn('BytesRcvd', data)
        self.assertIn('tim', data)

if __name__ == '__main__':
    unittest.main()
