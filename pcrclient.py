from msgpack import packb, unpackb
from random import randint
from Crypto.Cipher import AES
from base64 import b64decode
from hashlib import md5
import socket

apiroot = 'http://le1-prod-all-gs-gzlj.bilibiligame.net'

defaultHeaders = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux, U, Android 5.1.1, PCRT00 Build/LMY48Z)',
    'X-Unity-Version': '2021.3.36f1c1',
    'APP-VER': '10.7.1',
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '2',
    'DEVICE-NAME': 'Samsung SM-G973F',
    'EXCEL-VER': '1.0.0',
    'GRAPHICS-DEVICE-NAME': 'Mali-G76 MP12',
    'IP-ADDRESS': '100.98.233.111',
    'KEYCHAIN': '',
    'LOCALE': 'CN',
    'PLATFORM-OS-VERSION': 'Android OS 9 / API-28 (PPR1.180610.011/G973FXXU8FUE1)',
    'REGION-CODE': '',
    'RES-KEY': 'ab00a0a6dd915a052a2ef7fd649083e5',
    'RES-VER': '10002200',
    'SHORT-UDID': '0'
}

gk_iv = b'7Fk9Lm3Np8Qr4Sv2'
gk_hostname = socket.gethostname()

class ApiException(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


class pcrclient:
    '''
        acccountinfo = {
            'uid': '',
            'access_key': '',
            'platform': 2, # indicates android platform
            'channel': 1, #indicates bilibili channel
        }
    '''

    def __init__(self, accountinfo: dict):
        self.viewer_id = 0
        self.uid = accountinfo['uid']
        self.access_key = accountinfo['access_key']
        self.platform = accountinfo['platform']
        self.channel = accountinfo['channel']

        self.headers = {}
        for key in defaultHeaders.keys():
            self.headers[key] = defaultHeaders[key]
        self.headers['PLATFORM'] = str(self.platform)
        self.headers['PLATFORM-ID'] = str(self.platform)
        self.headers['CHANNEL-ID'] = str(self.channel)
        # md5() produces 128-bit (16-byte) output, hexdigest() converts it to 32 hexadecimal characters. Therefore, the output is always 32 characters regardless of input.
        self.headers['DEVICE-ID'] = md5(gk_hostname.encode('utf-8')).hexdigest()

        self.shouldLogin = True

    @staticmethod
    def createkey() -> bytes:
        return bytes([ord('0123456789abcdef'[randint(0, 15)]) for _ in range(32)])

    @staticmethod
    def add_to_16(b: bytes) -> bytes:
        n = len(b) % 16
        n = n // 16 * 16 - n + 16
        return b + (n * bytes([n]))

    @staticmethod
    def pack(data: object, key: bytes) -> bytes:
        aes = AES.new(key, AES.MODE_CBC, gk_iv)
        return aes.encrypt(pcrclient.add_to_16(packb(data,
                                                     use_bin_type=False
                                                     ))) + key

    @staticmethod
    def encrypt(data: str, key: bytes) -> bytes:
        aes = AES.new(key, AES.MODE_CBC, gk_iv)
        return aes.encrypt(pcrclient.add_to_16(data.encode('utf8'))) + key

    @staticmethod
    def decrypt(data: bytes):
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, gk_iv)
        return aes.decrypt(data[:-32]), data[-32:]

    @staticmethod
    def unpack(data: bytes):
        aes = AES.new(data[-32:], AES.MODE_CBC, gk_iv)
        dec = aes.decrypt(data[:-32])
        return unpackb(dec[:-dec[-1]],
                       strict_map_key=False
                       ), data[-32:]

    @staticmethod
    def unpackRsp(data: bytes):
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, gk_iv)
        dec = aes.decrypt(data[:-32])
        return unpackb(dec[:-dec[-1]],
                       strict_map_key=False
                       ), data[-32:]
