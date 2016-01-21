from os.path import splitext
from .Tag import *

class SCHI_Tag(HEK_Tag):
    
    def Convert_to_Other_Chicago(self):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        self.Tag_Extension = '.shader_transparent_chicago_extended'
        self.Tag_Data.Blam_Header.Tag_4CC_ID.Set_Data('shader_transparent_chicago_extended')
        self.Tag_Path = splitext(self.Tag_Path)[0] + self.Tag_Extension
        
        Data = self.Tag_Data.Data
        Data.Numeric_Shader_ID.Data = 7
        Data.ATTR_OFFS[Data.NAME_MAP['Extra_Flags']] = 108
        Data.Set_Size(120)
