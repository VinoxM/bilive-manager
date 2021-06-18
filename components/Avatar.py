# coding=utf-8
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

from api.apiThread import RunThread
import icon


class AvatarLabel(QLabel):
    clicked = pyqtSignal()
    _signal_get_avatar_content = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(AvatarLabel, self).__init__(*args, **kwargs)

        self.size_ = 200

        self.thread = QtCore.QThread(self)
        self.thread_get_avatar_content = RunThread('get_avatar_content')
        self.thread_get_avatar_content.moveToThread(self.thread)
        self._signal_get_avatar_content.connect(self.thread_get_avatar_content.run)
        self.thread_get_avatar_content.signal.connect(self.call_get_avatar_content)

    def setup_image(self, size_=200, img_=None):
        pixmap = QPixmap(size_, size_)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.begin(self)  # 要将绘制过程用begin(self)和end()包起来
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)  # 一个是平滑，一个是缩放保持比例
        path = QPainterPath()
        path.addEllipse(0, 0, size_, size_)  # 绘制椭圆
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, size_, size_, img_)
        painter.end()
        self.setPixmap(pixmap)

    def mouseReleaseEvent(self, event):
        if Qt.LeftButton == event.button():
            self.clicked.emit()

    def setup_image_by_url(self, size_=200, url=''):
        self.size_ = size_
        if not self.thread.isRunning():
            self.thread.start()
        self._signal_get_avatar_content.emit(url)

    def call_get_avatar_content(self, obj):
        face = obj.get('face', None)
        if obj.get('err', '') is None and face:
            img = QtGui.QImage.fromData(face)
            avatar = QtGui.QPixmap.fromImage(img)
            self.setup_image(size_=self.size_,
                             img_=avatar.scaled(self.size_, self.size_,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        else:
            pixMap = QtGui.QPixmap()
            pixMap.loadFromData(QtCore.QByteArray.fromBase64(icon.no_face))
            self.setup_image(size_=self.size_,
                             img_=pixMap.scaled(self.size_, self.size_,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        self.thread.terminate()
