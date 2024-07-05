import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session, json
from index import app

class TestFileManagement(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_file_route(self):
        response = self.app.get('/file')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'file.html', response.data)  # Ensure 'file.html' is in the response

    @patch('index.os.listdir')
    @patch('index.os.stat')
    @patch('index.os.path.isdir')
    @patch('index.os.path.islink')
    def test_GetFile(self, mock_islink, mock_isdir, mock_stat, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'dir1', 'file2.txt']
        mock_stat.return_value.st_mtime = 1625542794.0  # Mocking modification time
        mock_islink.return_value = False
        mock_isdir.return_value = True

        response = self.app.post('/GetFile', data={'path': 'L2RlZmF1bHRzcGVj'})  # assuming 'L2RlZmF1bHRzcGVj' is base64 encoded path
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertIn('files', data['result'])

    @patch('index.shutil.move')
    def test_batch_cut(self, mock_move):
        mock_move.return_value = None
        selectedList = ['L2ZpbGUxLnR4dA==', 'L2ZpbGUyLnR4dA==']  # assuming these are base64 encoded file paths
        path = 'L3BhdGg='  # assuming this is base64 encoded path

        response = self.app.post('/batch', data={'type': 'cut', 'selectedList': json.dumps(selectedList), 'path': path})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.rename')
    def test_RenameFile(self, mock_rename):
        mock_rename.return_value = None

        response = self.app.post('/RenameFile', data={'newFileName': 'bGludXgudHh0', 'oldFileName': 'b2xkRmlsZQ=='})  # assuming these are base64 encoded file names
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.path.exists')
    @patch('index.os.mkdir')
    def test_CreateDir(self, mock_mkdir, mock_exists):
        mock_exists.return_value = False
        mock_mkdir.return_value = None

        response = self.app.post('/CreateDir', data={'dirName': 'bW9kZWw=', 'path': 'L3BhdGg='})  # assuming these are base64 encoded directory name and path
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.open', create=True)
    @patch('index.os.path.exists')
    def test_CreateFile(self, mock_exists, mock_open):
        mock_exists.return_value = False
        mock_file = MagicMock()
        mock_open.return_value = mock_file

        response = self.app.post('/CreateFile', data={'fileName': 'bW9kZWwudHh0', 'path': 'L3BhdGg='})  # assuming these are base64 encoded file name and path
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.send_from_directory')
    @patch('index.os.path.isdir')
    @patch('index.os.path.exists')
    def test_DownFile(self, mock_exists, mock_isdir, mock_send_from_directory):
        mock_exists.return_value = True
        mock_isdir.return_value = False
        mock_send_from_directory.return_value = 'fake response'

        response = self.app.post('/DownFile', data={'filename': 'bG9va3MvZmlsZTEudHh0'})  # assuming this is a base64 encoded file path
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'fake response')

    @patch('index.chardet.detect')
    @patch('index.open', create=True)
    @patch('index.os.path.getsize')
    def test_codeEdit(self, mock_getsize, mock_open, mock_detect):
        mock_getsize.return_value = 1000  # Mocking file size limit
        mock_detect.return_value = {'encoding': 'utf-8'}

        response = self.app.get('/codeEdit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'codeEdit.html', response.data)  # Ensure 'codeEdit.html' is in the response

        response = self.app.post('/codeEdit', data={'path': 'L3BhdGg='})  # assuming this is base64 encoded path
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertIn('fileCode', data)

    @patch('index.open', create=True)
    def test_saveEditCode(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value = mock_file

        response = self.app.post('/saveEditCode', data={'editValues': 'dGVzdCBmaWxlCg==', 'fileName': 'bW9kZWwudHh0'})  # assuming these are base64 encoded edit values and file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.delete_')
    def test_Delete(self, mock_delete):
        mock_delete.return_value = (True, 'deleted successfully')

        response = self.app.post('/Delete', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.chmod')
    def test_chmod(self, mock_chmod):
        mock_chmod.return_value = None

        response = self.app.post('/chmod', data={'filename': 'bG9va3MvZmlsZQ==', 'power': '777'})  # assuming these are base64 encoded file name and power
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    def test_picVisit(self):
        response = self.app.post('/picVisit', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.startswith(b'/9j/'))  # Ensure response starts with a valid image header

    @patch('index.request.files')
    def test_UploadFile(self, mock_files):
        mock_file = MagicMock()
        mock_file.filename = 'test_file.txt'
        mock_files.get.return_value = mock_file

        response = self.app.post('/UploadFile', data={'nowPath': 'bG9va3M=', 'File': (BytesIO(b'file content'), 'test_file.txt')})  # assuming these are base64 encoded nowPath and file content
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.extract.main')
    def test_Extract_(self, mock_extract):
        mock_extract.return_value = (True, 'extracted successfully')

        response = self.app.post('/Extract', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    def test_secectList(self):
        with self.app.session_transaction() as sess:
            sess['secectList'] = json.dumps(['item1', 'item2'])

        response = self.app.post('/secectList', data={'type': 'get'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], ['item1', 'item2'])

        response = self.app.post('/secectList', data={'type': 'add', 'listData': 'W10='})  # assuming this is base64 encoded list data
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

        response = self.app.post('/secectList', data={'type': 'delete', 'listData': 'W10='})  # assuming this is base64 encoded list data
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.shutil.copy2')
    def test_Copy(self, mock_copy2):
        mock_copy2.return_value = None

        response = self.app.post('/Copy', data={'copySrc': 'bG9va3MvZmlsZQ==', 'copyDst': 'bG9va3MvZmlsZTE='})  # assuming these are base64 encoded copy source and destination
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.shutil.rmtree')
    def test_rmtree(self, mock_rmtree):
        mock_rmtree.return_value = None

        response = self.app.post('/rmtree', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.shutil.move')
    def test_move(self, mock_move):
        mock_move.return_value = None

        response = self.app.post('/move', data={'copySrc': 'bG9va3MvZmlsZQ==', 'copyDst': 'bG9va3MvZmlsZTE='})  # assuming these are base64 encoded copy source and destination
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.zipfile.ZipFile')
    @patch('index.os.path.exists')
    def test_Zip(self, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None

        response = self.app.post('/Zip', data={'type': 'start', 'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

        response = self.app.post('/Zip', data={'type': 'end'})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.zipfile.ZipFile')
    @patch('index.os.path.exists')
    def test_7z(self, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None

        response = self.app.post('/7z', data={'type': 'start', 'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

        response = self.app.post('/7z', data={'type': 'end'})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.chmod')
    def test_chmodAll(self, mock_chmod):
        mock_chmod.return_value = None

        response = self.app.post('/chmodAll', data={'filenames': json.dumps(['bG9va3MvZmlsZQ==', 'bG9va3MvZmlsZTE=']), 'power': '777'})  # assuming these are base64 encoded file names and power
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.zipfile.ZipFile')
    @patch('index.os.path.exists')
    def test_ZipAll(self, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None

        response = self.app.post('/ZipAll', data={'filenames': json.dumps(['bG9va3MvZmlsZQ==', 'bG9va3MvZmlsZTE='])})  # assuming these are base64 encoded file names
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.zipfile.ZipFile')
    @patch('index.os.path.exists')
    def test_7zAll(self, mock_exists, mock_zipfile):
        mock_exists.return_value = True
        mock_zipfile.return_value.__enter__.return_value.extractall.return_value = None

        response = self.app.post('/7zAll', data={'filenames': json.dumps(['bG9va3MvZmlsZQ==', 'bG9va3MvZmlsZTE='])})  # assuming these are base64 encoded file names
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.listdir')
    @patch('index.os.path.islink')
    @patch('index.os.path.isdir')
    @patch('index.os.path.exists')
    def test_GetfolderSize(self, mock_exists, mock_isdir, mock_islink, mock_listdir):
        mock_exists.return_value = True
        mock_isdir.return_value = True
        mock_islink.return_value = False
        mock_listdir.return_value = ['file1.txt', 'dir1', 'file2.txt']

        response = self.app.post('/GetfolderSize', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertIsInstance(data['result'], int)

    @patch('index.os.stat')
    @patch('index.os.path.isdir')
    @patch('index.os.path.islink')
    @patch('index.os.path.exists')
    def test_GetAllFileInfo(self, mock_exists, mock_islink, mock_isdir, mock_stat):
        mock_exists.return_value = True
        mock_isdir.return_value = False
        mock_islink.return_value = False
        mock_stat.return_value.st_size = 1024
        mock_stat.return_value.st_mtime = 1625542794.0

        response = self.app.post('/GetAllFileInfo', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result']['size'], 1024)
        self.assertEqual(data['result']['mtime'], 1625542794.0)

    @patch('index.shutil.make_archive')
    def test_Make_archive(self, mock_make_archive):
        mock_make_archive.return_value = '/path/to/archive.zip'

        response = self.app.post('/Make_archive', data={'filename': 'bG9va3MvZmlsZQ==', 'format': 'zip'})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], '/path/to/archive.zip')

    @patch('index.time.sleep')
    def test_SystemUpdate(self, mock_sleep):
        mock_sleep.return_value = None

        response = self.app.post('/SystemUpdate')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.path.islink')
    @patch('index.os.path.exists')
    def test_link(self, mock_exists, mock_islink):
        mock_exists.return_value = True
        mock_islink.return_value = False

        response = self.app.post('/link', data={'filename': 'bG9va3MvZmlsZQ==', 'linkname': 'bG9va3MvZmlsZTE='})  # assuming these are base64 encoded file name and link name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

    @patch('index.os.remove')
    def test_rmFile(self, mock_remove):
        mock_remove.return_value = None

        response = self.app.post('/rmFile', data={'filename': 'bG9va3MvZmlsZQ=='})  # assuming this is a base64 encoded file name
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resultCode'], 0)
        self.assertEqual(data['result'], 'success')

if __name__ == '__main__':
    unittest.main()

