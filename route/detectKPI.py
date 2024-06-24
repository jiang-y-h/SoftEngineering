from flask import request,render_template,redirect,send_file, send_from_directory,url_for,session,make_response, jsonify
import time
from index import app,url
import json
import os
import time,random
from .login import cklogin
import threading  # 用于多线程处理

url.append({
    "title": "KPI异常检测",
    "href": "/KPI",
})

# 模拟一个训练函数
@app.route('/StartTraining', methods=['POST'])
@cklogin()
def start_training():
    train_data = request.form.get('model')
    print(f"Starting training : {train_data}")
    
    try:
        # 获取当前脚本所在目录
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(current_directory)
        # 保存当前工作目录
        original_directory = os.getcwd()
        # 切换工作目录到 data_preprocess.py 所在目录
        os.chdir(os.path.join(parent_directory, 'OmniAnomaly'))
        # 构建相对路径调用 data_preprocess.py
        os.system(f"python data_preprocess.py {train_data}")
        os.system(f"python main.py 1")
        # 恢复原始工作目录
        os.chdir(original_directory)
        
        return jsonify({'resultCode': '0', 'result': '训练成功'})
    
    except Exception as e:
        return jsonify({'resultCode': '1', 'result': f'训练失败：{str(e)}'})


@app.route('/KPI', methods=['GET', 'POST'])
@cklogin()
def KPIhome():
    if request.method == 'POST':
        selected_model = request.form.get('model')
        if selected_model:
            # 开始训练的后台任务
            thread = threading.Thread(target=start_training, args=(selected_model,))
            thread.start()
            return jsonify({'resultCode': '0', 'result': '训练已启动'})
        else:
            return jsonify({'resultCode': '1', 'result': '未选择训练集'})

    return render_template('kPI.html')


@app.route('/UploadKPIFile', methods=['POST'])
def upload_kpi_file():
    if 'kpiFile' not in request.files:
        return jsonify({'resultCode': '1', 'result': '未上传文件'})

    kpi_file = request.files['kpiFile']
    if kpi_file.filename == '':
        return jsonify({'resultCode': '1', 'result': '未选择文件'})

    if kpi_file:
        filename = kpi_file.filename
        save_path = os.path.join('uploads', filename)
        kpi_file.save(save_path)
        test = os.path.splitext(filename)[0]

        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            parent_directory = os.path.dirname(current_directory)
            original_directory = os.getcwd()
            os.chdir(os.path.join(parent_directory, 'OmniAnomaly'))
            os.system(f"python main.py 0 {test}")
            os.chdir(original_directory)


            return jsonify({
                'resultCode': '0',
                'result': f'文件上传成功: {filename}',
                'imagePath': url_for('static', filename='result/anomaly_detection_plot.png')
            })

        except Exception as e:
            return jsonify({'resultCode': '1', 'result': f'文件处理失败：{str(e)}'})

    return jsonify({'resultCode': '1', 'result': '文件上传失败'})

