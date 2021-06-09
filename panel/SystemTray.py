# coding=utf-8
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5.QtCore import pyqtSignal, QByteArray

import icon


class UiSystemTray(QSystemTrayIcon):
    _signal_double_clicked = pyqtSignal()
    _signal_update_minimized_status = pyqtSignal(int)

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.setToolTip('Bilive Manager [未开播]')
        # Show Main
        self.a_main = QAction('主界面')
        menu.addAction(self.a_main)
        # Show Barrage
        self.a_barrage = QAction('弹幕姬')
        self.a_barrage.setCheckable(True)
        menu.addAction(self.a_barrage)

        menu.addSeparator()
        # Start Live
        self.a_live = QAction('开播')
        self.a_live.setCheckable(True)
        menu.addAction(self.a_live)
        # Connect Barrage
        self.a_connect = QAction('连接弹幕')
        self.a_connect.setCheckable(True)
        menu.addAction(self.a_connect)

        menu.addSeparator()
        # Toggle Minimized
        self.a_minimized = QAction('最小化到托盘')
        self.a_minimized.setCheckable(True)
        self.a_minimized.setChecked(True)
        self.a_minimized.triggered.connect(self.toggle_minimized_status)
        menu.addAction(self.a_minimized)

        menu.addSeparator()
        # Exit
        self.a_exit = QAction('退出')
        self.a_exit.triggered.connect(qApp.quit)
        menu.addAction(self.a_exit)
        self.setContextMenu(menu)
        self.activated.connect(self.act)

    def act(self, reason):
        if reason == 2:
            self._signal_double_clicked.emit()

    def toggle_barrage_status(self, status):
        self.a_barrage.setChecked(status == 1)

    def toggle_live_status(self, status):
        self.a_live.setChecked(status == 1)
        self.a_live.setText('开播' if status == 0 else '下播')
        pixMap = QPixmap()
        pixMap.loadFromData(QByteArray.fromBase64(icon.icon if status == 1 else icon.icon_stop))
        sys_icon = QIcon(pixMap)
        self.setIcon(sys_icon)
        self.setToolTip('Bilive Manager [直播中]' if status == 1 else 'Bilive Manager [未开播]')

    def toggle_barrage_connect(self, status):
        self.a_connect.setChecked(status == 1)
        self.a_connect.setText('连接弹幕姬' if status == 0 else '断开弹幕姬')

    def toggle_minimized_status(self, status):
        self._signal_update_minimized_status.emit(1 if status else 0)
