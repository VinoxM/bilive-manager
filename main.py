# coding=utf-8
from components.MainWindow import UiMainWindow
from components.SettingWindow import UiSettingWindow
from components.BarrageWindow import UiBarrageWindow
from components.SystemTray import UiSystemTray
from components.ChangeableMainWindow import ChangeableMainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
from PyQt5.QtCore import QByteArray
from PyQt5.QtGui import QIcon, QPixmap
import icon

if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

    # application 对象
    app = QApplication(sys.argv)

    """ main window """
    main_window = ChangeableMainWindow()
    ui_main = UiMainWindow()
    ui_main.setupUi(main_window)
    main_window.minimized.connect(ui_main.toggle_main_minimized)

    """ setting window """
    setting_window = QDialog()
    ui_setting = UiSettingWindow()
    ui_setting.setupUi(setting_window)
    ui_main._signal_open_setting_window.connect(ui_setting._show)
    ui_setting.close_and_refresh.connect(ui_main.call_setting)

    """ barrage window """
    barrage_window = QWidget()
    ui_barrage = UiBarrageWindow()
    ui_barrage.setupUi(barrage_window)
    ui_main._signal_toggle_barrage_window.connect(ui_barrage._toggle)
    ui_main._signal_bili_ws_receive.connect(ui_barrage.add_barrage)
    ui_main._signal_bili_ws_join.connect(ui_barrage.add_join)
    ui_main._signal_bili_ws_gift.connect(ui_barrage.add_gift)
    ui_main._signal_bili_ws_update.connect(ui_barrage.update_live_info)
    ui_main._signal_bili_ws_pop.connect(ui_barrage.update_heartbeat)
    ui_main._signal_bili_ws_close.connect(ui_barrage.ws_closed)

    """ system tray """
    pixMap = QPixmap()
    pixMap.loadFromData(QByteArray.fromBase64(icon.icon_stop))
    sys_icon = QIcon(pixMap)
    sys_tray = UiSystemTray(sys_icon, main_window)
    sys_tray.show()
    # Double Clicked Action
    sys_tray._signal_double_clicked.connect(ui_main.toggle_window_visible)
    # Main Panel Action
    sys_tray.a_main.triggered.connect(ui_main.show_main_window)
    # Barrage Panel Action
    sys_tray.a_barrage.triggered.connect(ui_main.toggle_barrage_window)
    ui_barrage._signal_update_barrage_visible.connect(sys_tray.toggle_barrage_status)
    # Live Start Action
    sys_tray.a_live.triggered.connect(ui_main.toggle_live_status)
    ui_main._signal_update_sys_tray_live_status.connect(sys_tray.toggle_live_status)
    # Barrage Connect Action
    sys_tray.a_connect.triggered.connect(ui_main.toggle_ws_status)
    ui_main._signal_update_sys_tray_ws_connect.connect(sys_tray.toggle_barrage_connect)
    # Minimized Action
    sys_tray._signal_update_minimized_status.connect(ui_main.toggle_minimized)

    # 显示
    main_window.show()
    ui_main.init_info()

    sys.exit(app.exec_())
