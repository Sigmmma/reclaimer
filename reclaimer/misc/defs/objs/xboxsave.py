import hashlib, hmac

from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.tag import *

DEFAULT_XBOX_KEY = (b'\x5C\x07\x33\xAE\x04\x01\xF7\xE8'+
                    b'\xBA\x79\x93\xFD\xCD\x2F\x1F\xE0')

class XboxSaveTag(Tag):
    sigkey  = None
    authkey = None
    xboxkey = DEFAULT_XBOX_KEY

    data_start = 20
    data_end   = 0
    
    def __init__(self, **kwargs):
        if 'sigkey' in kwargs:
            self.sigkey = kwargs['sigkey']
        if 'authkey' in kwargs:
            self.authkey = kwargs['authkey']
        if 'xboxkey' in kwargs:
            self.xboxkey = kwargs['xboxkey']
            
        if 'data_start' in kwargs:
            self.data_start = kwargs['data_start']
        if 'data_len' in kwargs:
            self.data_len = kwargs['data_len']
            
        Tag.__init__(self, **kwargs)

    def calc_authkey(self, sigkey=None):
        if sigkey is None:
            sigkey = self.sigkey
        authkey = hmac.new(self.xboxkey, sigkey[:16], hashlib.sha1)
        authkey = authkey.digest()[:16]
        if self.authkey is None:
            self.authkey = authkey
        return authkey

    def calc_hmac_sig(self, rawdata, authkey=None):
        if authkey is None:
            if self.authkey is None:
                authkey = self.calc_authkey(self.sigkey)
            else:
                authkey = self.authkey
        return hmac.new(authkey, rawdata, hashlib.sha1).digest()

    def xbox_sign(self, rawdata=None, authkey=None):
        if rawdata is None:
            rawdata = self.data.write(buffer=BytearrayBuffer())
            if self.data_end != 0:
                rawdata = rawdata[self.data_start:self.data_end]
            else:
                rawdata = rawdata[self.data_start:]
        hmac_sig = self.calc_hmac_sig(rawdata, authkey)
        self.data.hmac_sig = hmac_sig

    def write(self, **kwargs):
        self.xbox_sign()
        return Tag.write(self, **kwargs)
