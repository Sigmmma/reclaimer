from os.path import splitext
from .Tag_Obj import *

class SCEX_Tag(Halo_Tag_Obj):

    def Convert_to_Other_Chicago(self):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        self.Tag_Extension = '.shader_transparent_chicago'
        self.Tag_Data.Blam_Header.Type_FourCC = 'schi'
        self.Tag_Path = splitext(self.Tag_Path)[0] + self.Tag_Extension
        
        Data = self.Tag_Data.Data
        del Data.Two_Stage_Maps
        Data.Numeric_Shader_ID = 6
        Data.ATTR_OFFS['Extra_Flags'] = 98
        Data.Set_Size(108)
