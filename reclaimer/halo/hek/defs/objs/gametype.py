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

CE_CRC32_OFF = 0x98
PC_CRC32_OFF = 0xD8

class GametypeTag(HekTag):

    is_xbox = False
    
    def calc_crc32(self, buffer=None, offset=-1):
        '''Returns the crc32 checksum of the data in 'buffer' up
        to the 'offset' specified. If offset is not specified, the
        entire buffer is used. If buffer is not specified, the tag
        will be written and the returned buffer will be used.'''
        if buffer is None:
            buffer = self.data.write(buffer=BytearrayBuffer())
        return 0xFFFFFFFF - (binascii.crc32(buffer[:offset]) & 0xFFFFFFFF)

    def validate_checksum(self, buffer=None, offset=-1):
        '''Returns True if the checksum of the gametype is valid'''
        checksum = unpack('<I', buffer[offset:offset+4])[0]
        return self.calc_crc32(buffer, offset) == checksum

    def read(self, **kwargs):
        ''''''
        if kwargs.get('filepath') is None and kwargs.get('rawdata') is None:
            kwargs['filepath'] = self.filepath

        rawdata = BytearrayBuffer(blocks.Block.get_raw_data(self, **kwargs))
        kwargs['rawdata'] = rawdata
        if 'filepath' in kwargs:
            del kwargs['filepath']
            
        is_ce = self.validate_checksum(rawdata, CE_CRC32_OFF)
        is_pc = self.validate_checksum(rawdata, PC_CRC32_OFF)

        self.is_xbox = not(is_ce or is_pc)
        
        #if the gametype isnt a valid PC gametype, make it a hybrid of both
        if is_ce and not is_pc:
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
        if not self.is_xbox:
            footer = self.data.gametype_footer
            footer.crc_32 = self.calc_crc32(None, CE_CRC32_OFF)
            
            footer.hybrid_settings = BytearrayBuffer()
            self.data.gametype_settings.write(buffer=footer.hybrid_settings)
            
            footer.crc_32_ce = self.calc_crc32(None, PC_CRC32_OFF)
        
        return HekTag.write(self, **kwargs)
