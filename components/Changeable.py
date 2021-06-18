# coding=utf-8
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QTextEdit


class ChangeableMainWindow(QMainWindow):
    minimized = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeableMainWindow, self).__init__()

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                self.minimized.emit()


class ChangeableWidget(QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeableWidget, self).__init__()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.closed.emit()


class ChangeableTextEdit(QTextEdit):
    text_changed = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(ChangeableTextEdit, self).__init__(*args, **kwargs)
        self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self):
        self.text_changed.emit(len(self.toPlainText()))
