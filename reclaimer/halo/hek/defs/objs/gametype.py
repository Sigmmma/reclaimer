'''
    Adapted from source files located here
    https://github.com/Halogen002/Flare-Qt

    My thanks go to Halogen002 for providing me with
    the information I needed to write this definition.
    I extended it to include xbox gametypes as well
'''

import binascii

from struct import unpack

from .tag import *
from supyr_struct.buffer import BytearrayBuffer

class GametypeTag(HekTag):

    is_xbox = False

    def calc_crc32(self, buffer=None):
        if buffer is None:
            buffer = self.data.write(buffer=BytearrayBuffer())
        return 0xFFFFFFFF - (binascii.crc32(buffer[:0x98]) & 0xFFFFFFFF)

    def calc_ce_crc32(self, buffer=None):
        if buffer is None:
            buffer = self.data.write(buffer=BytearrayBuffer())
        return 0xFFFFFFFF - (binascii.crc32(buffer[:0xD8]) & 0xFFFFFFFF)

    def read(self, **kwargs):
        if kwargs.get('filepath') is None and kwargs.get('rawdata') is None:
            kwargs['filepath'] = self.filepath

        rawdata = BytearrayBuffer(blocks.Block.get_raw_data(self, **kwargs))
        kwargs['rawdata'] = rawdata
        if 'filepath' in kwargs:
            del kwargs['filepath']

        try:
            is_ce = self.calc_crc32(rawdata)    == unpack('<I',rawdata[0x98:0x9C])[0]
            is_pc = self.calc_ce_crc32(rawdata) == unpack('<I',rawdata[0xD8:0xDC])[0]
        except Exception:
            is_ce = is_pc = False
            
        self.is_xbox = not(is_ce or is_pc)
        
        #if the gametype isnt a valid PC gametype, make it a hybrid of both
        if is_ce and not self.is_xbox:
            #copy the checksum to the PC Halo specific location
            rawdata[0x94:0x9C] = rawdata[0xD4:0xDC]
            #copy the gametype settings to the PC Halo specific location
            rawdata[0x7C:0x94] = rawdata[0x9C:0xB4]
        
        return HekTag.read(self, **kwargs)
        
    def write(self, **kwargs):
        '''Writes this tag to the set path like normal, but makes
        sure to calculate and set the checksums before doing so.
        Checksums are only valid for PC and CE gametypes, so for
        xbox gametypes this function is the same as Tag.write'''
        try:
            footer = self.data.gametype_footer
            footer.crc_32 = self.calc_crc32()
            
            footer.hybrid_settings = BytearrayBuffer()
            self.data.gametype_settings.write(buffer=footer.hybrid_settings)
            
            footer.crc_32_ce = self.calc_ce_crc32()
        except AttributeError:
            pass
        
        return HekTag.write(self, **kwargs)
