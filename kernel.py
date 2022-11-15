import datetime

import requests
from PySide6 import QtCore
from PySide6.QtCore import QThread

from utils import init_and_loadconfig


class Kernel(QThread):
    logSignal = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.authData = {
            "c": "Portal",
            "a": "login",
            "login_method": "1",
            "user_account": "081800
            "user_password": "123456"
        }
        self.testUrl = "http://www.baidu.com"
        self.s = requests.session()
        self.s.keep_alive = False  # 关闭多余连接
        # 验证网址
        self.authUrl = "http://10.2.5.251:801/eportal/?"
        # 验证关键字
        self.authKeyword = ["上网登录页", "http://10.2.5.251/"]
        self.configs = init_and_loadconfig()

    def check_and_init(self):
        self.configs = init_and_loadconfig()
        # 移动 @cmcc 联通 @unicom   电信@telecom   校园网null
        self.authData["user_account"] = self.configs["account"]
        self.authData["user_password"] = self.configs["password"]
        if self.configs["internet"] == '校园网':
            self.authData["user_account"] = self.configs["account"]
        if self.configs["internet"] == '中国移动':
            self.authData["user_account"] += "@cmcc"
        if self.configs["internet"] == '中国联通':
            self.authData["user_account"] += "@unicom"
        if self.configs["internet"] == '中国电信':
            self.authData["user_account"] += "@telecom"

    def is_need_stop(self):  # 判断当前时间是否在范围时间内
        d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:25', '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '6:35', '%Y-%m-%d%H:%M')
        n_time = datetime.datetime.now()
        if d_time < n_time or n_time < d_time1:
            return True
        else:
            return False

    def run(self):
        status_emit = True
        error_emit = True
        stop_emit = True
        while True:
            self.check_and_init()
            if self.configs['isNeedStopTime'] == 'True' and self.is_need_stop():
                if stop_emit:
                    stop_emit = False
                    status_emit = True
                    error_emit = True
                    self.logSignal.emit("指定时间停止运行")
            else:
                stop_emit = True
                try:
                    html = self.s.get(self.testUrl, timeout=5, verify=False).text
                    isConnected = (self.authUrl in html) | (self.authKeyword[0] in html) | (self.authKeyword[1] in html)
                    error_emit = True
                    if isConnected:
                        status_emit = True
                        self.logSignal.emit("需要验证,提交登录请求")
                        self.logSignal.emit("authData:" + str(self.authData))
                        self.s.get(self.authUrl, params=self.authData, timeout=5)
                        self.sleep(3)
                    elif status_emit:
                        status_emit = False
                        self.logSignal.emit("网络连接正常")
                except:
                    if error_emit:
                        error_emit = False
                        status_emit = True
                        self.logSignal.emit("无法访问网络，检查是否已连接WiFi")
            self.sleep(5)
