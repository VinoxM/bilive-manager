# coding=utf-8
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath


class AvatarLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(AvatarLabel, self).__init__(*args, **kwargs)

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
