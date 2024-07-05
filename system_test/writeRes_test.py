import unittest
from unittest.mock import patch, MagicMock
from write_res_task import writeResTask
from config.config import ResState, ResSaveDay, ResInv

class TestWriteResTask(unittest.TestCase):

    def setUp(self):
        self.write_res_task = writeResTask()

    def tearDown(self):
        pass

    @patch('write_res_task.psutil')
    @patch('write_res_task.sql')
    def test_write_method(self, mock_sql, mock_psutil):
        mock_sql.insertInfo = MagicMock()
        mock_sql.deleteInfo = MagicMock()

        mock_psutil.virtual_memory.return_value.total = 1024 * 1024 * 1024

        self.write_res_task.write()

        mock_sql.insertInfo.assert_called()
        mock_sql.deleteInfo.assert_called()

if __name__ == '__main__':
    unittest.main()

