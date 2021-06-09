# coding=utf-8

from PyQt5 import QtCore, QtWidgets, QtGui


class ChangeableWidget(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super(ChangeableWidget, self).__init__()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.closed.emit()
