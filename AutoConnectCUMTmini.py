import configparser
import datetime
import sys
import webbrowser

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QDateTime, QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox

from feedback import FeedbackWindow
from kernel import Kernel
from ui_AutoConnectCUMTmini import Ui_MainWindow
from utils import install_and_createLinks, start_whenLaunch, init_and_loadconfig, configPath, send_email


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.feedbackWindow = FeedbackWindow()
        self.feedbackWindow.mesSignal.connect(self.showMessage)
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.upgradeAction = QAction("更新", self)
        self.upgradeAction.setIcon(QtGui.QPixmap(":/menu/upgrade.png"))
        self.feedbackAction = QAction("反馈", self)
        self.feedbackAction.setIcon(QtGui.QPixmap(":/menu/feedback.png"))
        self.aboutAction = QAction("关于", self)
        self.aboutAction.setIcon(QtGui.QPixmap(":/menu/about.png"))
        self.quitAction = QAction("退出", self)
        self.quitAction.setIcon(QtGui.QPixmap(":/menu/exit.png"))

        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.upgradeAction)
        self.trayIconMenu.addAction(self.feedbackAction)
        self.trayIconMenu.addAction(self.aboutAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QPixmap(":/icon/app.ico"))
        self.trayIcon.setToolTip("AutoConnectCUMTmini")
        self.trayIcon.show()

        self.trayIcon.activated.connect(self.iconActivated)
        self.feedbackAction.triggered.connect(self.feedbackWindow.show)
        self.quitAction.triggered.connect(QCoreApplication.quit)
        self.aboutAction.triggered.connect(self.showAbout)
        self.upgradeAction.triggered.connect(self.upgradeClicked)

        self.configs = init_and_loadconfig()
        self.ui.account.setText(self.configs['account'])
        self.ui.password.setText(self.configs['password'])
        self.ui.internet.setCurrentText(self.configs['internet'])
        if self.configs['isNeedStopTime'] == 'True':
            self.ui.stoptime.setChecked(True)
        try:
            if self.configs['isFirstRun']:
                self.showLog("第一次运行，请配置")
                self.trayIcon.showMessage("AutoConnectCUMTmini", "第一次运行 AutoConnectCUMTmini ，请配置",
                                          QSystemTrayIcon.Information, 2000)
                send_email(content=str(datetime.datetime.now()) + ' new user.')
        except:
            self.trayIcon.showMessage("AutoConnectCUMTmini", "AutoConnectCUMTmini 启动成功", QSystemTrayIcon.Information,
                                      2000)
        self.ui.save.clicked.connect(self.saveButtonClicked)

        self.kernel = Kernel()
        self.kernel.logSignal.connect(self.showLog)
        self.kernel.start()

    def upgradeClicked(self):
        self.trayIcon.showMessage("AutoConnectCUMTmini", "请自行查看是否有新版本", QSystemTrayIcon.Information,
                                  2000)
        webbrowser.open('https://github.com/TrumpHe/AutoConnectCUMTmini', new=0, autoraise=True)

    def saveButtonClicked(self):
        config = configparser.ConfigParser()
        config.set('DEFAULT', 'account', self.ui.account.text())
        config.set('DEFAULT', 'password', self.ui.password.text())
        config.set('DEFAULT', 'internet', self.ui.internet.currentText())
        config.set('DEFAULT', 'isNeedStopTime', str(self.ui.stoptime.isChecked()))
        try:
            with open(configPath, 'w') as f:
                config.write(f)
            self.showLog('保存成功')
        except:
            self.showLog('保存失败')
        self.ui.save.setText('保存')

    def iconActivated(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.showNormal()

    def showAbout(self):
        aboutText = '''
            <p>软件名称：校园网连接助手迷你版</p>
            <p>软件版本：v0.0.1</p>
            <p>开发者：<a style="color:#333;" href="https://trumphe.github.io/about/">蒲苏 | Trump He</a></p>
            <p>开源地址：<a style="color:#333;" href="https://github.com/TrumpHe/AutoConnectCUMTmini">AutoConnectCUMTmini</a></p>
            <p>AutoConnectCUMTmini</p>
            <p>Copyright © 2021-2022 Trump.</p>
            <p>All Rights Reserved.</p>
        '''
        msg = QMessageBox(self)
        msg.setWindowTitle("关于")
        msg.setText(aboutText)
        msg.setIconPixmap(QtGui.QPixmap(":/icon/app.ico"))
        msg.addButton("确定", QMessageBox.ActionRole)
        msg.exec()

    def showMessage(self, message):
        self.trayIcon.showMessage("AutoConnectCUMTmini", message, QSystemTrayIcon.Information,
                                  2000)

    def showLog(self, text):
        currentDateTime = QDateTime.currentDateTime()
        time = currentDateTime.toString("yyyy/MM/dd HH:mm:ss")
        text = time + "：" + text
        self.ui.log.appendPlainText(text)

    def closeEvent(self, event):
        self.hide()
        event.ignore()


def main():
    try:
        if sys.platform[0:3] == 'win':
            install_and_createLinks()
            start_whenLaunch()
    except Exception as e:
        print(e)
        print("something error happend outset...")

    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# nuitka --mingw64 --windows-uac-admin --windows-disable-console --standalone --plugin-enable=pyside6 --show-progress --windows-icon-from-ico='app.ico' --onefile AutoConnectCUMTmini.py

# nuitka --mingw64 --standalone --plugin-enable=pyside6 --show-progress --windows-icon-from-ico='app.ico' --onefile AutoConnectCUMTmini.py
