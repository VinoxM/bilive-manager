# coding=utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from requests.exceptions import ProxyError
import api.api as api


class RunThread(QtCore.QObject):
    signal = QtCore.pyqtSignal(object)

    def __init__(self, name):
        super(RunThread, self).__init__()
        self.flag = True
        self.name = name

    def run(self, *args):
        method = getattr(api, self.name)
        try:
            result = method(*args)
            self.signal.emit(result)
        except ConnectionError as e:
            self.signal.emit({"err": '网络连接错误'})
        except ProxyError as e:
            self.signal.emit({"err": '代理连接错误'})
