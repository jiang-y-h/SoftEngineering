import unittest
from sqlitedb.sqlitedb import sqlClass  # 替换为你的模块名

class TestSQLClass(unittest.TestCase):
    
    def setUp(self):
        self.db = sqlClass()
        
    def tearDown(self):
        del self.db
        
    def test_insert_info(self):
        info = {"message": "test message", "value": 123}
        self.db.insertInfo(info)
        result = self.db.selectInfo(1)
        self.assertTrue(len(result[1]) > 0)
        
    def test_insert_remote_host(self):
        IP = "192.168.1.100"
        PORT = "22"
        CTYPE = "SSH"
        USERNAME = "testuser"
        GROUPS = "admin"
        NOTE = "Test host"
        ROOTPWD = "rootpass"
        result = self.db.insertRemoteHost(IP, PORT, CTYPE, USERNAME, GROUPS, NOTE, ROOTPWD)
        self.assertTrue(result[0])
        
    def test_insert_task(self):
        task_info = {"taskID": "12345", "task_name": "Test Task"}
        self.db.insertTask(task_info)
        result = self.db.selectTask()
        self.assertTrue(len(result[1]) > 0)
        
    def test_create_link_button(self):
        button_info = {
            "BUTTONNAME": "Test Button",
            "TYPE": "action",
            "NOTE": "Test Button Description",
            "SHELL": "/bin/bash",
            "CATEGORY": "test"
        }
        result = self.db.createLinkButton(button_info)
        self.assertTrue(result[0])
        
    def test_file_share_operations(self):
        filepath = "/path/to/testfile.txt"
        self.db.creatFileShare(filepath, "yes")
        files = self.db.getFileShare()
        self.assertTrue(len(files) > 0)
        
    def test_delete_remote_host(self):
        IP = "192.168.1.100"
        result = self.db.deleteRemoteHost(IP)
        self.assertTrue(result[0])
        
if __name__ == "__main__":
    unittest.main()

