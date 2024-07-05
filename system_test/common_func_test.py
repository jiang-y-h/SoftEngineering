import unittest
import socket
from unittest.mock import MagicMock
from socket_bridge import SocketBridge, CtrlPkg, select_recv

class TestSocketBridge(unittest.TestCase):
    
    def setUp(self):

        pass

    def tearDown(self):

        pass

    def test_socket_bridge_add_conn_pair(self):

        mock_conn1 = MagicMock(spec=socket.socket)
        mock_conn2 = MagicMock(spec=socket.socket)
        
        bridge = SocketBridge()
        bridge.add_conn_pair(mock_conn1, mock_conn2)
        
        self.assertIn(mock_conn1, bridge.conn_rd)
        self.assertIn(mock_conn2, bridge.conn_rd)
        self.assertEqual(bridge.map.get(mock_conn1), mock_conn2)
        self.assertEqual(bridge.map.get(mock_conn2), mock_conn1)

    def test_ctrl_pkg_build_bytes(self):

        pkg = CtrlPkg(pkg_ver=1, pkg_type=CtrlPkg.PTYPE_HEART_BEAT, prgm_ver=0x0D)
        self.assertIsNotNone(pkg.raw)
        self.assertEqual(len(pkg.raw), CtrlPkg.PACKAGE_SIZE)

    def test_select_recv_timeout(self):

        mock_conn = MagicMock(spec=socket.socket)
        

        with self.assertRaises(RuntimeError) as cm:
            select_recv(mock_conn, 1024, timeout=0.1)
        
        self.assertEqual(str(cm.exception), "recv timeout")

    def test_select_recv_zero_bytes(self):

        mock_conn = MagicMock(spec=socket.socket)
        mock_conn.recv.return_value = b""
        
        with self.assertRaises(RuntimeError) as cm:
            select_recv(mock_conn, 1024)
        
        self.assertEqual(str(cm.exception), "received zero bytes, socket was closed")


if __name__ == '__main__':
    unittest.main()
