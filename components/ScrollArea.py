# coding=utf-8
import threading

from PyQt5 import QtCore, QtWidgets, QtGui


class ScrollArea(QtWidgets.QScrollArea):

    def __init__(self, *args, **kwargs):
        super(ScrollArea, self).__init__(*args, **kwargs)
        self.is_on_bottom = True
        self.auto_remove = False
        self.max_count = 100
        self.item_style_sheet = '#label{padding: 0px 3px 0px 3px;font-family: "微软雅黑", sans-serif;}'
        widget = ResizeableWidget()
        widget.adjustSize()
        widget.resize.connect(self.scroll_to_bottom)
        widget.setObjectName("widget")
        widget.setStyleSheet("#widget{padding: 0px;}")
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)
        widget.setLayout(self.layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)
        self.auto_hide = False
        self.is_mouse_over = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.hide_and_scroll_bottom)

    def setProperties(self, auto_remove=True, max_count=100,
                      item_style_sheet='#label{padding: 0px 3px 0px 3px;font-family: "微软雅黑", sans-serif;}'):
        self.auto_remove = auto_remove
        self.max_count = max_count
        self.item_style_sheet = item_style_sheet

    def add_item(self, message):
        self.is_on_bottom = self.verticalScrollBar().value() == self.verticalScrollBar().maximum()
        if self.auto_remove and self.layout.count() > self.max_count:
            for i in range(self.layout.count() - self.max_count):
                self.layout.itemAt(i).widget().deleteLater()
        if type(message) != str:
            self.layout.addWidget(message)
        else:
            label = QtWidgets.QLabel()
            label.setMaximumWidth(self.width() - 10)
            label.setWordWrap(True)
            label.setText(message)
            label.setCursor(QtCore.Qt.IBeamCursor)
            label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            label.setObjectName('label')
            label.setStyleSheet(self.item_style_sheet)
            label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.layout.addWidget(label)

    def clear_items(self):
        if self.layout.count() <= 0:
            return
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().deleteLater()

    def scroll_to_bottom(self):
        if self.is_on_bottom and self.widget().height() > self.height():
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
            if self.auto_hide and not self.is_mouse_over:
                self.verticalScrollBar().hide()

    def enterEvent(self, event: QtCore.QEvent) -> None:
        self.is_mouse_over = True

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.auto_hide:
            if self.verticalScrollBar().isHidden():
                self.verticalScrollBar().show()
        super(ScrollArea, self).wheelEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.is_mouse_over = False
        if self.auto_hide:
            self.timer.start(2000)

    def hide_and_scroll_bottom(self):
        if not self.is_mouse_over:
            self.verticalScrollBar().hide()
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class ResizeableWidget(QtWidgets.QWidget):
    resize = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ResizeableWidget, self).__init__(*args, **kwargs)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.resize.emit()
