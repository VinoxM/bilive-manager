# coding=utf-8
import requests as request
import json


def get_live_area():
    live_area = {}
    res = request.get(url='https://api.live.bilibili.com/room/v1/Area/getList',
                      params={'show_pinyin': 1})
    if res.status_code == 200:
        result = json.loads(res.text)
        if result['code'] == 0:
            data = result['data']
            for item in data:
                for elem in item['list']:
                    live_area[elem['id']] = item['name'] + '-' + elem['name']
        else:
            live_area['err'] = result['message']
    return live_area


def get_user_info_by_cookie(uid, cookie):
    user_info = {'user_name': 'User Name', 'level': 0, 'face': None}
    if uid != '' and cookie != '':
        res = request.get(url='https://api.bilibili.com/x/space/acc/info', params={
            'mid': uid, 'jsonp': 'jsonp'
        }, headers={'cookie': cookie, 'Content-type': 'application/json'})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                data = result['data']
                user_info['user_name'] = data['name']
                user_info['level'] = data['level']
                face = data['face']
                if face is not None or face == '':
                    res = request.get(face)
                    if res.status_code == 200:
                        user_info['face'] = res.content
            else:
                user_info['err'] = result['message']
    return user_info


def get_user_stat_by_cookie(uid, cookie):
    user_stat = {'follower': '?', 'following': '?'}
    if uid != '' and cookie != '':
        res = request.get(url='https://api.bilibili.com/x/relation/stat', headers={'cookie': cookie},
                          params={'vmid': uid, 'jsonp': 'jsonp'})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                data = result['data']
                user_stat['follower'] = data['follower']
                user_stat['following'] = data['following']
            else:
                user_stat['err'] = result['message']
    return user_stat


def get_live_info_by_cookie(cookie):
    live_info = {'link': '', 'title': '', 'area_id': 0, 'area_name': '', 'status': 0, 'room_id': 0}
    if cookie != '':
        res = request.get(url='https://api.live.bilibili.com/xlive/web-ucenter/user/live_info',
                          headers={'cookie': cookie, 'Content-type': 'application/json'})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                data = result['data']
                live_info['room_id'] = data['room_id']
            else:
                live_info['err'] = result['message']
        room_id = live_info['room_id']
        if room_id != 0:
            res1 = request.get(url='https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo',
                               params={'req_biz': 'link-center', 'room_ids': room_id},
                               headers={'Content-type': 'application/json'})
            if res1.status_code == 200:
                result = json.loads(res1.text)
                if result['code'] == 0:
                    data = result['data'].get('by_room_ids')[str(room_id)]
                    live_info['link'] = data['live_url']
                    live_info['title'] = data['title']
                    live_info['area_id'] = data['area_id']
                    live_info['area_name'] = data['area_name']
                    live_info['status'] = data['live_status']
                else:
                    live_info['err'] = result['message']
    return live_info


def get_live_rtmp_by_cookie(room_id, cookie):
    live_rtmp = {'rtmp': '', 'code': ''}
    if room_id != 0 and cookie != '':
        res = request.get(url='https://api.live.bilibili.com/live_stream/v1/StreamList/get_stream_by_roomId', params={
            'room_id': room_id
        }, headers={'cookie': cookie, 'Content-type': 'application/json'}, )
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                data = result['data'].get('rtmp', None)
                if data is not None:
                    live_rtmp['rtmp'] = data['addr']
                    live_rtmp['code'] = data['code']
            else:
                live_rtmp['err'] = result['message']
    return live_rtmp


def update_live_title(room_id, title, token, cookie):
    info = {'err': None}
    if room_id != 0 and token != '' and cookie != '' and title != '':
        res = request.post(
            url='https://api.live.bilibili.com/room/v1/Room/update',
            data={
                'room_id': room_id,
                'title': title,
                'csrf_token': token,
                'csrf': token
            },
            headers={'cookie': cookie})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] != 0:
                info['err'] = result['message']
    return info


def update_live_area(room_id, area_id, token, cookie):
    info = {'err': None}
    if room_id != 0 and token != '' and cookie != '':
        res = request.post(
            url='https://api.live.bilibili.com/room/v1/Room/update',
            data={
                'room_id': room_id,
                'area_id': area_id,
                'csrf_token': token,
                'csrf': token
            },
            headers={'cookie': cookie})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] != 0:
                info['err'] = result['message']
    return info


def update_live_status(room_id, status, area_id, token, cookie):
    info = {'err': None}
    if room_id != 0 and area_id != 0 and token != '' and cookie != '':
        is_live = status == 1
        res = request.post(
            url='https://api.live.bilibili.com/room/v1/Room/{}'.format('startLive' if not is_live else 'stopLive'),
            data={
                'room_id': room_id,
                'platform': 'pc',
                'area_v2': area_id,
                'csrf_token': token,
                'csrf': token
            }, headers={'cookie': cookie})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] != 0:
                info['err'] = result['message']
    return info


def send_bili_barrage(message, room_id, token, cookie):
    info = {'err': None}
    if room_id != 0 and token != '' and cookie != '':
        res = request.post(
            url='https://api.live.bilibili.com/msg/send',
            data={
                'bubble': 0,
                'msg': message,
                'color': 16777215,
                'mode': 1,
                'fontsize': 25,
                'rnd': 1621495631,
                'roomid': room_id,
                'csrf': token,
                'csrf_token': token
            }, headers={'cookie': cookie})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] != 0:
                info['err'] = result['message']
    return info


def get_real_room_id(room_id, cookie):
    live_info = {'real_room_id': 0, 'uid': 0}
    if room_id != 0 and cookie != '':
        res = request.get(
            url='https://api.live.bilibili.com/room/v1/Room/room_init',
            params={
                'id': room_id
            }, headers={'cookie': cookie})
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                live_info['real_room_id'] = result['data']['room_id']
                room_id = result['data']['room_id']
                if live_info['real_room_id'] != 0:
                    res1 = request.get(url='https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo',
                                       params={'req_biz': 'link-center', 'room_ids': room_id},
                                       headers={'Content-type': 'application/json'})
                    if res1.status_code == 200:
                        result = json.loads(res1.text)
                        if result['code'] == 0:
                            data = result['data'].get('by_room_ids')[str(room_id)]
                            live_info['link'] = data['live_url']
                            live_info['title'] = data['title']
                            live_info['status'] = data['live_status']
                            live_info['uid'] = data['uid']
                            live_info['uname'] = data['uname']
            else:
                live_info['err'] = result['message']
    return live_info


def get_user_detail(uid):
    user_info = {'uname': '', 'uid': uid, 'face': None, 'link': None}
    if uid != 0:
        res = request.get(
            url='https://api.bilibili.com/x/space/acc/info',
            params={
                'mid': uid,
                'jsonp': 'jsonp'
            })
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['code'] == 0:
                data = result['data']
                user_info['uname'] = data['name']
                face = data['face']
                user_info['link'] = data['live_room']['url']
                if face is not None or face == '':
                    res = request.get(face)
                    if res.status_code == 200:
                        user_info['face'] = res.content
            else:
                user_info['err'] = result['message']
    return user_info
