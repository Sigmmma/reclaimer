from os.path import splitext
from .Tag import *
from supyr_struct.Field_Types import Void

class SCEX_Tag(HEK_Tag):

    def Convert_to_Other_Chicago(self):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        self.Tag_Extension = '.shader_transparent_chicago'
        self.Tag_Data.Blam_Header.Tag_4CC_ID.Set_Data('shader_transparent_chicago')
        self.Tag_Path = splitext(self.Tag_Path)[0] + self.Tag_Extension
        
        Data = self.Tag_Data.Data
        Data.Two_Stage_Maps.Set_Desc('TYPE', Void)
        Data.Numeric_Shader_ID.Data = 6
        Data.ATTR_OFFS[Data.NAME_MAP['Extra_Flags']] = 96
        Data.Set_Size(108)
