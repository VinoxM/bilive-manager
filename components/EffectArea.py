# coding=utf-8
import webbrowser

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QPixmap

from components.Avatar import AvatarLabel
from components.ScrollArea import ResizeableWidget
import icon


class EffectArea(QtWidgets.QScrollArea):

    def __init__(self, *args, **kwargs):
        super(EffectArea, self).__init__(*args, **kwargs)
        self.setStyleSheet('border: none;background: rgba(0,0,0,0)')
        widget = ResizeableWidget()
        widget.resize.connect(self.scroll_to_bottom)
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        widget.adjustSize()
        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.setAlignment(QtCore.Qt.AlignBottom)
        self.layout_.setSpacing(0)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.layout_)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hide()

    def add_item(self, obj: dict):
        item = EffectItem()
        item.destroyed.connect(self.none_item_hide)
        item.setup_elem(obj)
        self.layout_.addWidget(item)
        self.show()

    def none_item_hide(self):
        count = self.layout_.count()
        if count == 1:
            self.hide()

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        pass

    def scroll_to_bottom(self):
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class EffectItem(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(EffectItem, self).__init__(*args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.deleteLater())
        self.timer.start(3000)
        self.uid = None

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        img = QtGui.QImage()
        img.loadFromData(QtCore.QByteArray.fromBase64(icon.effect_back))
        img_ = img.copy(15, 75, 925, 128)
        pixmap = QPixmap().fromImage(img_)
        painter.drawPixmap(self.rect(), pixmap)

    def setup_elem(self, obj):
        self.uid = obj['data']['uid']
        face = obj['data']['face']
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 40)
        str_ = '<span style="color: white">' + str(obj['data']['copy_writing'])
        message = str_.replace('<%', '</span><span style="font-weight: bold;color: #ffdd61">') \
                      .replace('%>', '</span><span style="color: white">') + '</span>'
        avatar = AvatarLabel(self)
        avatar.setCursor(QtCore.Qt.PointingHandCursor)
        avatar.setup_image_by_url(size_=36, url=face)
        avatar.setGeometry(QtCore.QRect(9, 2, 36, 36))
        avatar.clicked.connect(self.open_url)
        label = QtWidgets.QLabel(self)
        label.setGeometry(QtCore.QRect(60, 8, 260, 30))
        label.setText(message)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.timer.isActive():
            self.timer.stop()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        if not self.timer.isActive():
            self.timer.start(3000)

    def open_url(self):
        if self.uid:
            url = 'https://space.bilibili.com/{}/'.format(str(self.uid))
            webbrowser.open(url)