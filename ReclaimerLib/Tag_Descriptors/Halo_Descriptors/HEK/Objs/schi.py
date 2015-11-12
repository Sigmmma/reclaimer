from os.path import splitext
from .Tag_Obj import *

class SCHI_Tag(Halo_Tag_Obj):
    
    def Convert_to_Other_Chicago(self):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        self.Tag_Extension = '.shader_transparent_chicago_extended'
        self.Tag_Data.Blam_Header.Type_FourCC = 'scex'
        self.Tag_Path = splitext(self.Tag_Path)[0] + self.Tag_Extension
        
        Data = self.Tag_Data.Data
        Data.Numeric_Shader_ID = 7
        Data.ATTR_OFFSETS['Extra_Flags'] = 110
        Data.Set_Size(120)
