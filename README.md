# 南开大学软件工程团队作业--智能运维系统
本运维系统运行再windows或linux环境下，前端采用了多种现代化的技术栈，旨在提供用户友好的界面和丰富的交互功能，使用了layui的模块快速构建前端网页。具体包括：HTML、CSS、JavaScript。同时，使用了ECharts实现数据可视化，提供了丰富的图表类型和配置项，使得数据展示更加直观，利用jQuery简化了JavaScript的DOM操作和Ajax请求。本项目的后端使用Python和Flask框架进行开发，具有高效、稳定和易于扩展的特点。

## 安装依赖库
本次项目需要运行在python 3.6环境下，需要安装以下依赖库：
```
chardet==3.0.4
paramiko==2.4.2
requests>=2.20.0
psutil==5.6.6
Flask==1.0.2
pillow
pyautogui
six == 1.11.0
matplotlib == 3.0.2
numpy == 1.15.4
pandas == 0.23.4
scipy == 1.2.0
scikit_learn == 0.20.2
tensorflow-gpu == 1.12.0
tensorflow_probability == 0.5.0
tqdm == 4.28.1
imageio == 2.4.1
fs == 2.3.0
click == 7.0
```

可以通过以下命令一键安装：
```shell
pip install -r requirements.txt
```

## 运行说明
1. 运行`index.py`文件，启动服务。
2. 然后在浏览器中相应的地址即可访问系统。
 