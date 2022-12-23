from msgpack import packb, unpackb
from random import randint
from Crypto.Cipher import AES
from base64 import b64decode

apiroot = 'http://le1-prod-all-gs-gzlj.bilibiligame.net'

defaultHeaders = {
    'Accept-Encoding': 'gzip',
    'User-Agent': 'Dalvik/2.1.0 (Linux, U, Android 5.1.1, PCRT00 Build/LMY48Z)',
    'X-Unity-Version': '2018.4.30f1',
    'APP-VER': '4.9.7',
    'BATTLE-LOGIC-VERSION': '4',
    'BUNDLE-VER': '',
    'DEVICE': '2',
    'DEVICE-ID': '7b1703a5d9b394e24051d7a5d4818f17',
    'DEVICE-NAME': 'OPPO PCRT00',
    'EXCEL-VER': '1.0.0',
    'GRAPHICS-DEVICE-NAME': 'Adreno (TM) 640',
    'IP-ADDRESS': '10.0.2.15',
    'KEYCHAIN': '',
    'LOCALE': 'CN',
    'PLATFORM-OS-VERSION': 'Android OS 5.1.1 / API-22 (LMY48Z/rel.se.infra.20200612.100533)',
    'REGION-CODE': '',
    'RES-KEY': 'ab00a0a6dd915a052a2ef7fd649083e5',
    'RES-VER': '10002200',
    'SHORT-UDID': '0'
}


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
        aes = AES.new(key, AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        return aes.encrypt(pcrclient.add_to_16(packb(data,
                                                     use_bin_type=False
                                                     ))) + key

    @staticmethod
    def encrypt(data: str, key: bytes) -> bytes:
        aes = AES.new(key, AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        return aes.encrypt(pcrclient.add_to_16(data.encode('utf8'))) + key

    @staticmethod
    def decrypt(data: bytes):
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        return aes.decrypt(data[:-32]), data[-32:]

    @staticmethod
    def unpack(data: bytes):
        aes = AES.new(data[-32:], AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        dec = aes.decrypt(data[:-32])
        return unpackb(dec[:-dec[-1]],
                       strict_map_key=False
                       ), data[-32:]

    @staticmethod
    def unpackRsp(data: bytes):
        data = b64decode(data.decode('utf8'))
        aes = AES.new(data[-32:], AES.MODE_CBC, b'ha4nBYA2APUD6Uv1')
        dec = aes.decrypt(data[:-32])
        return unpackb(dec[:-dec[-1]],
                       strict_map_key=False
                       ), data[-32:]
