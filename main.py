# coding=utf-8
import io

from components.MainWindow import UiMainWindow
from components.SettingWindow import UiSettingWindow
from components.BarrageWindow import UiBarrageWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget

if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

    # application 对象
    app = QApplication(sys.argv)

    """ main window """
    main_window = QMainWindow()
    ui_main = UiMainWindow()
    ui_main.setupUi(main_window)

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

    # 显示
    main_window.show()
    ui_main.init_info()

    sys.exit(app.exec_())
