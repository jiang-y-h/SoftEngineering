import paramiko
import threading
import time, random, json
from flask import request, redirect, render_template
from index import app, sql, url
from .login import cklogin

url.append({"title": "web shell", "href": "/ssh"})

sshListDict = {}
sshTimeout = {}

def checkSSH():
    t = []
    for k, v in sshTimeout.items():
        if time.time() > (v + 180):
            t.append(k)
    for i in t:
        sshListDict[i].close()
        del sshListDict[i]
        del sshTimeout[i]

# 此方法用于处理ssh登陆,并返回id号码
@app.route('/ssh', methods=['GET', 'POST'])
def ssh():
    if request.method == 'GET':
        return render_template('webssh.html')
    else:
        checkSSH()
        # 获取前端输入的服务器地址信息等
        host = request.values.get('host')
        port = request.values.get('port')
        username = request.values.get('username')
        pwd = request.values.get('pwd')
        # 创建ssh链接
        sshclient = paramiko.SSHClient()
        sshclient.load_system_host_keys()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 不限制白名单以外的连接
        try:
            sshclient.connect(host, port, username, pwd)
            chan = sshclient.invoke_shell(term='xterm')  # 创建交互终端
            chan.settimeout(0)
            ids = str(int(time.time() + random.randint(1, 999999999)))
            sshListDict[ids] = chan
        except paramiko.BadAuthenticationType:
            return json.dumps({'resultCode': 1, 'result': '登录失败,错误的连接类型'})
        except paramiko.AuthenticationException:
            return json.dumps({'resultCode': 1, 'result': '登录失败'})
        except paramiko.BadHostKeyException:
            return json.dumps({'resultCode': 1, 'result': '登录失败,请检查IP'})
        except:
            return json.dumps({'resultCode': 1, 'result': '登录失败'})
        else:
            sshTimeout[ids] = time.time()
            return json.dumps({'resultCode': 0, 'ids': ids})

# 此方法用于获取前端监听的键盘动作,输入到远程ssh
@app.route('/SSHInput', methods=['POST'])
def SSHInput():
    WebInput = request.values.get('input')
    ids = request.values.get('ids')
    chan = sshListDict.get(ids)
    sshTimeout[ids] = time.time()
    if not chan:
        return json.dumps({'resultCode': 1})
    chan.send(WebInput)
    return json.dumps({'resultCode': 0})

# 根据id号,获取远程ssh结果,方法比较low,用的轮询而没有用socket
@app.route('/GetSsh', methods=['POST'])
def GetSsh():
    ids = request.values.get('ids')
    chan = sshListDict.get(ids)
    if not chan:
        return json.dumps({'resultCode': 1})
    if not chan.exit_status_ready():
        try:
            data = chan.recv(1024).decode()
        except:
            data = ''
        return json.dumps({'resultCode': 0, 'data': data})
    else:
        chan.close()
        del sshListDict[ids]
        return json.dumps({'resultCode': 1})