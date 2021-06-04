# coding=utf-8

from PyQt5 import QtCore, QtGui, QtWidgets


class ChangeableTextEdit(QtWidgets.QTextEdit):
    text_changed = QtCore.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(ChangeableTextEdit, self).__init__(*args, **kwargs)
        self.textChanged.connect(self.handleTextChanged)

    def handleTextChanged(self):
        self.text_changed.emit(len(self.toPlainText()))
