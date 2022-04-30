import configparser
import email
import os
import shutil
import smtplib
import sys
from email.mime import text
from email.mime.multipart import MIMEMultipart

import winshell

startupPath = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\\"
installPath = "C:\Program Files\AutoConnectCUMTmini"
configPath = installPath + '\config.ini'


# configPath = 'config.ini'

def mkdir(path):  # 创建目录
    path = path.strip()  # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部 \ 符号
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


# create_desktop_shortcut("C:/LeiXueWei/Python.framework/Versions/3.8/bin/rxq.exe", "RenXianQi", "学委特制清点小程序")
def create_desktop_shortcut(bin_path: str, name: str, desc: str):
    try:
        shortcut = os.path.join(winshell.desktop(), name + ".lnk")
        winshell.CreateShortcut(
            Path=shortcut,
            Target=bin_path,
            Icon=(bin_path, 0),
            Description=desc
        )
        return True
    except ImportError as err:
        print("Well, do nothing as 'winshell' lib may not available on current os")
        print("error detail %s" % str(err))
    return False


# 移动安装包至安装目录同时生成桌面快捷方式
def install_and_createLinks():
    runningAppPath = os.path.realpath(
        sys.argv[0])  # 当前程序自身路径 如 ”C:\Users\chang\PycharmProjects\pythonProject\dist\gui.exe“
    mkdir(installPath)
    if runningAppPath != installPath + "AutoConnectCUMTmini.exe":
        shutil.copyfile(runningAppPath, installPath + "\AutoConnectCUMTmini.exe")  # hello.txt内容复制给hello2.txt

    create_desktop_shortcut(installPath + "\AutoConnectCUMTmini.exe", "AutoConnectCUMTmini", "AutoConnectCUMTmini")


# 实现开机自启
def start_whenLaunch():
    try:
        desktop_shortcut_path = os.path.join(winshell.desktop(), "AutoConnectCUMTmini.lnk")
        shutil.copyfile(desktop_shortcut_path,
                        startupPath + "AutoConnectCUMT.lnk")  # hello.txt内容复制给hello2.txt
    except:
        return False


# 检查是否是第一次使用&返回配置信息
def init_and_loadconfig():
    config = configparser.ConfigParser()  # 类中一个方法 #实例化一个对象
    config.read(configPath)
    try:
        config["DEFAULT"]['internet']
    except:
        # 第一次运行
        print("第一次运行")
        config["DEFAULT"] = {'account': '',
                             'password': '',
                             'internet': '中国移动',
                             'isNeedStopTime': 'False',
                             }  # 类似于操作字典的形式

        with open(configPath, 'w+') as configfile:
            config.write(configfile)  # 将对象写入文件
        configfile.close()
        config["DEFAULT"]['isFirstRun'] = 'True'

    return config["DEFAULT"]


# 发送email
def send_email(smtpHost='smtp.163.com', sendAddr='autoconnectcumt@163.com', password='ISWCPFKUWZYQQPMY',
               recipientAddrs='1643460951@qq.com', subject='AutoConnectCUMTmini', content=''):
    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sendAddr
    msg['to'] = recipientAddrs
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content, 'plain', 'utf-8')
    msg.attach(txt)
    smtp = smtplib.SMTP()
    smtp.connect(smtpHost, '25')
    smtp.login(sendAddr, password)
    smtp.sendmail(sendAddr, recipientAddrs, str(msg))
    smtp.quit()
