import unittest
from unittest.mock import patch, MagicMock
import socket
import threading
import time

# 将 slaver 模块路径添加到 sys.path
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))

from slaver import Slaver, run_slaver

class TestSlaver(unittest.TestCase):

    @patch('slaver.socket.socket')
    def test_connect_master(self, mock_socket):
        # Mock the socket object
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        communicate_addr = ('127.0.0.1', 10000)
        target_addr = ('127.0.0.1', 22)
        slaver = Slaver(communicate_addr, target_addr)

        # Test _connect_master
        sock = slaver._connect_master()
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock.connect.assert_called_with(communicate_addr)
        self.assertIn(sock.getsockname(), slaver.spare_slaver_pool)
    
    @patch('slaver.socket.socket')
    def test_connect_target(self, mock_socket):
        # Mock the socket object
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        
        communicate_addr = ('127.0.0.1', 10000)
        target_addr = ('127.0.0.1', 22)
        slaver = Slaver(communicate_addr, target_addr)

        # Test _connect_target
        sock = slaver._connect_target()
        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock.connect.assert_called_with(target_addr)
    
    @patch('slaver.Slaver._connect_master')
    @patch('slaver.Slaver._slaver_working')
    def test_serve_forever(self, mock_slaver_working, mock_connect_master):
        mock_sock = MagicMock()
        mock_connect_master.return_value = mock_sock

        communicate_addr = ('127.0.0.1', 10000)
        target_addr = ('127.0.0.1', 22)
        slaver = Slaver(communicate_addr, target_addr)

        def stop_serving():
            
            time.sleep(1)
            
            slaver.socket_bridge.running = False

        stop_thread = threading.Thread(target=stop_serving)
        stop_thread.start()

        slaver.serve_forever()

        mock_connect_master.assert_called()
        mock_slaver_working.assert_called()

    @patch('slaver.Slaver._connect_master')
    @patch('slaver.Slaver._slaver_working')
    def test_run_slaver(self, mock_slaver_working, mock_connect_master):
        communicate_addr = ('127.0.0.1', 10000)
        target_addr = ('127.0.0.1', 22)
        slaver = Slaver(communicate_addr, target_addr)
        def stop_serving():
            time.sleep(1)
            
            slaver.socket_bridge.running = False

        stop_thread = threading.Thread(target=stop_serving)
        stop_thread.start()

        run_slaver(communicate_addr, target_addr)

        mock_connect_master.assert_called()
        mock_slaver_working.assert_called()


def test():
    unittest.main()
    return True

if __name__ == '__main__':
    test()