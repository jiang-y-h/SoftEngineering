import asyncio
from pyppeteer import launch
from PIL import Image, ImageChops

async def take_screenshot(url, filename):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector('body')
    await page.screenshot({'path': filename})
    await browser.close()

def compare_images(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)
    diff = ImageChops.difference(image1, image2)
    return diff.getbbox() is None

async def main():
    url = 'http://localhost:9001/index.html'  # 替换成你要测试的页面地址
    reference_filename = 'reference.png'
    test_filename = 'test.png'

    # 生成参考快照
    await take_screenshot(url, reference_filename)

    # 模拟修改页面后，生成测试快照
    # 假设这里是修改了页面内容
    # await modify_page_content(url)  # 如果需要修改页面内容再生成测试快照，可添加此步骤

    await take_screenshot(url, test_filename)

    # 比较两个快照
    if compare_images(reference_filename, test_filename):
        print("页面快照测试通过！")
    else:
        print("页面快照测试失败！存在差异。")

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())