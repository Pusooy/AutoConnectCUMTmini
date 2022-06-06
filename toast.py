from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import QTimer


class Toast(QtWidgets.QWidget):
    background_color = QtGui.QColor("#666")
    text_color = QtCore.Qt.white
    font = QtGui.QFont('fangsong', 10)
    text = ''
    times = 3
    parent = None
    min_height = 10
    min_width = 10
    pos = QtCore.QPointF(0, 0)

    def __init__(self, parent=None, ):
        super(Toast, self).__init__(parent)
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def init_UI(self):
        # 计算气泡长宽及移动气泡到指定位置
        self.height = self.get_font_size() * 2.5
        self.width = len(self.text) * self.height
        if self.height < self.min_height:
            self.height = self.min_height
        # else:
        #     self.height = self.min_height * 2
        if self.width < self.min_width:
            self.width = self.min_width
        self.resize(self.width, self.height)
        if self.pos.x() != 0 or self.pos.y() != 0:
            self.move(self.pos.x() - self.width / 2, self.pos.y() - self.height / 2)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        rect_line_path = QtGui.QPainterPath()
        rectangle = QtCore.QRectF(0, 0, self.width, self.height)
        rect_line_path.addRoundedRect(rectangle, self.height / 2, self.height / 2, QtCore.Qt.AbsoluteSize)
        painter.fillPath(rect_line_path, QtGui.QColor(self.background_color))

        pen = QtGui.QPen(QtGui.QColor(self.text_color))
        painter.setPen(pen)
        painter.setFont(self.font)
        self.draw_text(painter)

    def get_font_size(self):
        return self.font.pointSizeF()

    def draw_text(self, painter):
        painter.drawText(QtCore.QRectF(0, 0, self.width, self.height),
                         QtCore.Qt.AlignCenter, self.text)

    def make_text(self, pos, text, times=None, background_color=None):
        if pos:
            self.pos = pos
        if text:
            self.text = text
        if times:
            self.times = times
        if background_color:
            self.background_color = background_color
        self.init_UI()
        self.repaint()
        self.show()

        QTimer.singleShot(3000000, self.close)

    def toast_timeout(self):
        self.close()
