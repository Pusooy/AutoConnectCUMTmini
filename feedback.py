from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QDialog

from ui_feedback import Ui_Dialog
from utils import send_email


class FeedbackWindow(QDialog, Ui_Dialog):
    mesSignal = QtCore.Signal(str)

    def __init__(self):
        super(FeedbackWindow, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.send.clicked.connect(self.send_feedback)

    def send_feedback(self):
        try:
            send_email(content=self.feedbackText.toPlainText())
            self.mesSignal.emit("提交反馈成功")
        except Exception as exceptionResult:
            print("邮件发送失败，抛出 %s 异常" % exceptionResult)
            self.mesSignal.emit("提交反馈失败")
        self.hide()
