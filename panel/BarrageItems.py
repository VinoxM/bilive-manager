# coding=utf-8
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPainter, QPalette, QPainterPath

from components.Avatar import AvatarLabel


class SuperChatItem(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SuperChatItem, self).__init__(*args, **kwargs)
        self.uid = None
        self.setStyleSheet('font-family: "微软雅黑", sans-serif;')

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QtGui.QColor()
        pen.setRgb(0, 0, 0, 0)
        painter.setPen(pen)
        color = QtGui.QColor()
        color.setRgb(165, 207, 216, 80)
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), 8, 15, QtCore.Qt.RelativeSize)

    def setup_elem(self, obj):
        uname = obj['data']['user_info']['uname']
        face = obj['data']['user_info']['face']
        self.uid = obj['data']['uid']
        message = obj['data']['message'] if obj['data']['message'] != '' else obj['data']['message_jpn']
        self.setFixedSize(380, 72)
        avatar = AvatarLabel(self)
        avatar.setCursor(QtCore.Qt.PointingHandCursor)
        avatar.setup_image_by_url(size_=28, url=face)
        avatar.setGeometry(QtCore.QRect(10, 2, 28, 28))
        avatar.clicked.connect(self.open_url)
        avatar.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        name = QtWidgets.QLabel(self)
        name.setGeometry(QtCore.QRect(50, 0, 270, 30))
        name.setAlignment(QtCore.Qt.AlignVCenter)
        name.setText('<span style="color: #ADBCD9; font-weight: bold">' + uname + '</span>')
        name.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        price = QtWidgets.QLabel(self)
        price.setGeometry(QtCore.QRect(300, 0, 70, 30))
        price.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        price.setText('<span style="color: #ffdd61">￥' + str(obj['data']['price']) + '</span>')
        price.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        split = QtWidgets.QWidget(self)
        split.setGeometry(QtCore.QRect(5, 32, 370, 1))
        split.setStyleSheet('background: rgba(0,0,0,0.2)')
        label = QtWidgets.QLabel(self)
        label.setObjectName('label')
        label.setText('<span style="color: white">' + message + '</span>')
        label.setMaximumWidth(380)
        label.setCursor(QtCore.Qt.IBeamCursor)
        label.setGeometry(QtCore.QRect(5, 32, 370, 40))
        label.setWordWrap(True)
        label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    def open_url(self):
        if self.uid:
            url = 'https://space.bilibili.com/{}/'.format(str(self.uid))
            webbrowser.open(url)
