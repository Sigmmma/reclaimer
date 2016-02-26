from os.path import splitext
from .tag import *
from supyr_struct.fields import Void

class ScexTag(HekTag):

    def convert_to_schi(self, mod_desc=False):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        ext = 'shader_transparent_chicago'
        self.tagdata.Blam_Header.Tag_Class.set_data(ext)
        self.tagpath = splitext(self.tagpath)[0] + '.' + ext
        
        Data = self.tagdata.Data
        Data.Numeric_Shader_ID.data = 6
        if mod_desc:
            Data.Two_Stage_Maps.set_desc('TYPE', Void)
            Data.ATTR_OFFS[Data.NAME_MAP['Extra_Flags']] = 96
            Data.set_size(108)
