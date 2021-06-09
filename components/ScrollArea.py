# coding=utf-8

from PyQt5 import QtCore, QtWidgets, QtGui


class ScrollArea(QtWidgets.QScrollArea):

    def __init__(self, *args, **kwargs):
        super(ScrollArea, self).__init__(*args, **kwargs)
        self.is_on_bottom = True
        self.auto_remove = False
        self.max_count = 100
        self.max_height = 360
        self.item_max_width = 230
        self.item_style_sheet = '#label{padding: 0px 3px 0px 3px;font-family: "微软雅黑", sans-serif;}'
        widget = ResizeableWidget()
        widget.adjustSize()
        widget.resize.connect(self.scroll_to_bottom)
        widget.setObjectName("widget")
        widget.setStyleSheet("#widget{padding: 3px 2px 3px 2px;}")
        self.layout = QtWidgets.QGridLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def setProperties(self, max_height=360, item_max_width=230, auto_remove=True, max_count=100,
                      item_style_sheet='#label{padding: 0px 3px 0px 3px;font-family: "微软雅黑", sans-serif;}'):
        self.auto_remove = auto_remove
        self.max_count = max_count
        self.max_height = max_height
        self.item_max_width = item_max_width
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
            label.setMaximumWidth(self.item_max_width)
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
        if self.is_on_bottom and self.widget().height() > self.max_height:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


class ResizeableWidget(QtWidgets.QWidget):
    resize = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ResizeableWidget, self).__init__(*args, **kwargs)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.resize.emit()
