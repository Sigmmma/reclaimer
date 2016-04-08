from os.path import splitext
from .tag import *

class SchiTag(HekTag):
    
    def convert_to_scex(self, mod_desc=False):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        ext = 'shader_transparent_chicago_extended'
        self.data.Blam_Header.Tag_Class.set_data(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        Data = self.data.Data
        Data.numeric_shader_id.data = 7
        if mod_desc:
            Data.ATTR_OFFS[Data.NAME_MAP['extra_flags']] = 108
            Data.set_size(120)
