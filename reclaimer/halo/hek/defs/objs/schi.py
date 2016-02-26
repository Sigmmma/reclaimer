from os.path import splitext
from .tag import *

class SchiTag(HekTag):
    
    def convert_to_scex(self, mod_desc=False):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        ext = 'shader_transparent_chicago_extended'
        self.tagdata.Blam_Header.Tag_Class.set_data(ext)
        self.tagpath = splitext(self.tagpath)[0] + '.' + ext
        
        Data = self.tagdata.Data
        Data.Numeric_Shader_ID.data = 7
        if mod_desc:
            Data.ATTR_OFFS[Data.NAME_MAP['Extra_Flags']] = 108
            Data.set_size(120)
