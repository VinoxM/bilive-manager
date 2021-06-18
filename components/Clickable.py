from PyQt5 import QtCore, QtGui, QtWidgets


class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    right_clicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)

    def mouseReleaseEvent(self, event):
        if QtCore.Qt.LeftButton == event.button():
            self.clicked.emit()
        elif QtCore.Qt.RightButton == event.button():
            self.right_clicked.emit()
            return
