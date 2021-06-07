# coding=utf-8
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow


class ChangeableMainWindow(QMainWindow):
    minimized = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeableMainWindow, self).__init__()

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                self.minimized.emit()
