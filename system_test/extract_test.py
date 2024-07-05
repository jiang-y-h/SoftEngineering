import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
from extract import main

class TestExtract(unittest.TestCase):
    def setUp(self):
        """创建测试文件夹和测试文件"""
        os.makedirs('tests/test_files/test_zip_files', exist_ok=True)
        os.makedirs('tests/test_files/test_tar_files', exist_ok=True)
        os.makedirs('tests/test_files/test_gz_files', exist_ok=True)

        with open('tests/test_files/test_zip_files/test.txt', 'w') as f:
            f.write('This is a test file for zip.')
        
        with open('tests/test_files/test_tar_files/test.txt', 'w') as f:
            f.write('This is a test file for tar.')
        
        with open('tests/test_files/test_gz_files/test.txt', 'w') as f:
            f.write('This is a test file for gz.')

        # Create .zip file
        import zipfile
        with zipfile.ZipFile('tests/test_files/test.zip', 'w') as zipf:
            zipf.write('tests/test_files/test_zip_files/test.txt', arcname='test.txt')

        # Create .tar file
        import tarfile
        with tarfile.open('tests/test_files/test.tar', 'w') as tarf:
            tarf.add('tests/test_files/test_tar_files/test.txt', arcname='test.txt')

        # Create .gz file
        import gzip
        with open('tests/test_files/test_gz_files/test.txt', 'rb') as f_in:
            with gzip.open('tests/test_files/test.gz', 'wb') as f_out:
                f_out.writelines(f_in)

    def tearDown(self):
        """删除测试文件夹和测试文件"""
        import shutil
        shutil.rmtree('tests/test_files/test_zip_files')
        shutil.rmtree('tests/test_files/test_tar_files')
        shutil.rmtree('tests/test_files/test_gz_files')
        os.remove('tests/test_files/test.zip')
        os.remove('tests/test_files/test.tar')
        os.remove('tests/test_files/test.gz')
        if os.path.exists('tests/test_files/test.zip_files'):
            shutil.rmtree('tests/test_files/test.zip_files')
        if os.path.exists('tests/test_files/test.tar_files'):
            shutil.rmtree('tests/test_files/test.tar_files')
        if os.path.exists('tests/test_files/test.gz'):
            os.remove('tests/test_files/test.gz')

    def test_zip(self):
        result = main('tests/test_files/test.zip')
        self.assertTrue(result[0])
        self.assertTrue(os.path.exists('tests/test_files/test.zip_files/test.txt'))

    def test_tar(self):
        result = main('tests/test_files/test.tar')
        self.assertTrue(result[0])
        self.assertTrue(os.path.exists('tests/test_files/test.tar_files/test.txt'))


def test():
    unittest.main()
    return True

if __name__ == '__main__':
    test()