# coding=utf-8
import json
import zlib
import numpy as np


def read_int(buffer, start, len_):
    result = 0
    for i in range(len_ - 1, 0, -1):
        result += pow(256, len_ - i - 1) * buffer[start + i]
    return result


def write_int(buffer, start, len_, val):
    i = 0
    while i < len_:
        buffer[start + i] = val / pow(256, len_ - i - 1)
        i += 1


def decoder(blob):
    result = {
        'packet_len': int(blob[0:4].hex(), 16),
        'header_len': int(blob[4:6].hex(), 16),
        'ver': int(blob[6:8].hex(), 16),
        'op': int(blob[8:12].hex(), 16),
        'body': None
    }
    if result['op'] == 5:
        result['body'] = []
        offset = 0
        while offset < len(blob):
            packet_len = int(blob[offset:4 + offset].hex(), 16)
            header_len = 16
            data = blob[offset + header_len:offset + packet_len]
            if result['ver'] == 2:
                data = zlib.decompress(data)
                res = decoder(data)
                body = res['body']
                len_ = len(result['body'])
                result['body'][len_:len_] = body if type(body) == list else [body]
            else:
                if data:
                    len_ = len(result['body'])
                    result['body'][len_:len_] = [json.loads(data.decode('utf-8', errors='ignore'))]
            offset += packet_len
    elif result['op'] == 3:
        result['body'] = {
            'count': int(blob[16: 20].hex(), 16)
        }
    return result


def encode(type_='heartbeat', str_=None):
    header = [0, 0, 0, 16, 0, 16, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1]
    if type_ == 'join':
        body = bytes(json.dumps(str_), encoding='utf-8')
        data = list(body)
        if len(data) > 10:
            data.pop(10)
        header[3] = 16 + len(data)
        header[11] = 7
        header.extend(data)
    return bytes(header)
