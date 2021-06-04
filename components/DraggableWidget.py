# coding=utf-8

from PyQt5 import QtCore, QtGui, QtWidgets


class DraggableWidget(QtWidgets.QWidget):
    drag_move = QtCore.pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super(DraggableWidget, self).__init__(*args, **kwargs)
        self.drag_flag = False
        self.window_x = 0
        self.window_y = 0

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if QtCore.Qt.LeftButton == event.button():
            self.drag_flag = True
            self.window_x = event.windowPos().x()
            self.window_y = event.windowPos().y()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if QtCore.Qt.LeftButton == event.button():
            self.drag_flag = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        x = event.screenPos().x() - self.window_x
        y = event.screenPos().y() - self.window_y
        self.drag_move.emit(x, y)


class DraggableLabel(QtWidgets.QLabel):
    drag_move = QtCore.pyqtSignal(int, int)

    def __init__(self, *args, **kwargs):
        super(DraggableLabel, self).__init__(*args, **kwargs)
        self.drag_flag = False
        self.window_x = 0
        self.window_y = 0

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if QtCore.Qt.LeftButton == event.button():
            self.drag_flag = True
            self.window_x = event.windowPos().x()
            self.window_y = event.windowPos().y()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if QtCore.Qt.LeftButton == event.button():
            self.drag_flag = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        x = event.screenPos().x() - self.window_x
        y = event.screenPos().y() - self.window_y
        self.drag_move.emit(x, y)
