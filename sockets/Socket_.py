# coding=utf-8
import os
import threading
import time

import websocket
from PyQt5 import QtWidgets, QtCore

from sockets.SokectHandler import encode, decoder

handlers = {
    'INTERACT_WORD': 'handle_interact',
    'DANMU_MSG:4:0:2:2:2:0': 'handle_dan_mu',
    'DANMU_MSG': 'handle_dan_mu',
    'SEND_GIFT': 'handle_send_gift',
    'COMBO_SEND': 'handle_combo_send',
    'WELCOME': 'handle_welcome',
    'SUPER_CHAT_MESSAGE': 'handle_super_chat',
    'SUPER_CHAT_MESSAGE_JPN': 'handle_super_chat',
    'ENTRY_EFFECT': 'handle_entry_effect',
    'LIVE': 'handle_live',
    'PREPARING': 'handle_preparing'
}


class SocketWidget(QtCore.QObject):
    open = QtCore.pyqtSignal(str)
    close = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    join = QtCore.pyqtSignal(object)
    pop = QtCore.pyqtSignal(int)
    gift = QtCore.pyqtSignal(object)
    receive = QtCore.pyqtSignal(object)
    live = QtCore.pyqtSignal()
    preparing = QtCore.pyqtSignal()

    def __init__(self):
        super(SocketWidget, self).__init__()
        self.ws = None
        self.wst = None
        self.room = '0'
        self.heart_beat = None

    def _on_open(self, *args):
        room_id = self.room
        msg = encode('join', {'roomid': int(room_id)})
        self.ws.send(msg)
        self.open.emit('进入直播间:{}'.format(self.room))
        self.heart_beat = StoppableThread(target=self.send_heart_beat)
        self.heart_beat.daemon = True
        self.heart_beat.start()

    def _on_close(self, *args):
        self.close.emit('弹幕连接关闭')
        self.heart_beat.terminate()
        self.heart_beat = None

    def _on_error(self, *args):
        self.error.emit('弹幕连接出错')

    def _on_message(self, obj, str_):
        threading.Thread(target=self.handle_msg, args=(str_,)).start()

    def handle_msg(self, str_):
        result = decoder(str_)
        # print(len(result['body']),result)
        if result['op'] == 3:
            self.pop.emit(result['body']['count'])
        elif result['op'] == 5:
            body = result['body']
            if type(body) == dict:
                body = [body]
            for elem in body:
                name_ = handlers.get(elem['cmd'], None)
                if name_:
                    method = getattr(self, name_)
                    method(elem)
                else:
                    print(elem)
        elif result['op'] == 8:
            # self.join.emit('加入直播间:{}'.format(self.room))
            pass

    def connect_ws(self, room_id):
        self.room = room_id
        self.ws = websocket.WebSocketApp("wss://broadcastlv.chat.bilibili.com/sub",
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close,
                                         on_open=self._on_open)
        self.ws.keep_running = True
        self.wst = threading.Thread(target=self.ws.run_forever)
        self.wst.daemon = True
        self.wst.start()

    def send_heart_beat(self):
        print('Send HeartBeat')
        if self.ws:
            self.ws.send(encode())

    def close_ws(self):
        if self.ws is not None:
            print('disconnect')
            self.ws.keep_running = False
            self.ws.close()
            self.ws = None

    def handle_interact(self, elem):
        data = elem['data']
        obj = {
            'welcome': False,
            'uname': data['uname']
        }
        self.join.emit(obj)

    def handle_dan_mu(self, elem):
        dm_info = {
            'uid': elem['info'][2][0],
            'uname': elem['info'][2][1],
            'msg': elem['info'][1]
        }
        self.receive.emit(dm_info)

    def handle_send_gift(self, elem):
        data = elem['data']
        gift_info = {
            'uid': data['uid'],
            'uname': data['uname'],
            'action': data['action'],
            'num': data['num'],
            'gift_name': data['giftName']
        }
        self.gift.emit(gift_info)

    def handle_combo_send(self, elem):
        data = elem['data']
        gift_info = {
            'uid': data['uid'],
            'uname': data['uname'],
            'action': data['action'],
            'num': data['combo_num'],
            'gift_name': data['gift_name']
        }
        self.gift.emit(gift_info)

    def handle_welcome(self, elem):
        data = elem['data']
        obj = {
            'welcome': True,
            'uname': data['uname']
        }
        self.join.emit(obj)

    # 开播
    def handle_live(self, elem):
        self.live.emit()

    # 下播
    def handle_preparing(self, elem):
        self.preparing.emit()

    def handle_super_chat(self, elem):
        print(elem)

    def handle_entry_effect(self, elem):
        print(elem)


class StoppableThread(threading.Thread):

    def __init__(self, daemon=None, target=None):
        super(StoppableThread, self).__init__(daemon=daemon, target=target)
        self.__is_running = True
        self.daemon = daemon
        self._target = target

    def terminate(self):
        self.__is_running = False

    def run(self):
        try:
            while self.__is_running:
                if self._target:
                    self._target()
                time.sleep(30)
        finally:
            del self._target
