import unittest
from ..lib.vieCode import vieCode  # 替换为你的实际模块名
import PIL.Image

class TestVieCode(unittest.TestCase):
    
    def setUp(self):
        self.vie_code = vieCode()

    def tearDown(self):
        pass

    def test_get_code_image(self):
        img, code = self.vie_code.GetCodeImage(size=80, length=4)
        # 检查返回的验证码字符串长度是否正确
        self.assertEqual(len(code), 4)
        # 检查生成的图片是否是 PIL Image 实例
        self.assertIsInstance(img, PIL.Image.Image)

    def test_get_code_image_base64(self):
        img_base64, code = self.vie_code.GetCodeImageBase64()
        # 检查返回的 Base64 编码是否有效
        self.assertTrue(img_base64.startswith('data:image/png;base64,'))
        # 检查返回的验证码字符串长度是否正确
        self.assertEqual(len(code), 4)

    def test_create_filter(self):
        self.vie_code.__img = Image.new('RGB', (120, 45))  # 模拟创建了一个图片实例
        filtered_img = self.vie_code._vieCode__cerateFilter()
        # 检查返回的图片是否是 PIL Image 实例
        self.assertIsInstance(filtered_img, PIL.Image.Image)

    def test_create_code(self):
        self.vie_code._vieCode__str = '1234567890'  # 模拟设置验证码字符集
        self.vie_code._vieCode__length = 4  # 模拟设置验证码长度
        self.vie_code._vieCode__createCode()
        # 检查生成的验证码长度是否正确
        self.assertEqual(len(self.vie_code._vieCode__code), 4)
        # 检查生成的验证码字符是否在指定的字符集中
        for char in self.vie_code._vieCode__code:
            self.assertIn(char, '1234567890')

if __name__ == '__main__':
    unittest.main()

