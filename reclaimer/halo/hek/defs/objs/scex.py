from os.path import splitext
from .tag import *
from supyr_struct.fields import Void

class ScexTag(HekTag):

    def convert_to_schi(self, mod_desc=False):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        ext = 'shader_transparent_chicago'
        self.data.Blam_Header.Tag_Class.set_data(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        Data = self.data.Data
        Data.numeric_shader_id.data = 6
        if mod_desc:
            Data.two_stage_maps.set_desc('TYPE', Void)
            Data.ATTR_OFFS[Data.NAME_MAP['extra_flags']] = 96
            Data.set_size(108)
