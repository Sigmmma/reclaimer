from os.path import splitext
from .tag import *

class SchiTag(HekTag):
    
    def convert_to_scex(self):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        self.ext = ext = 'shader_transparent_chicago_extended'
        self.data.blam_header.tag_class.set_to(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        tagdata = self.data.tagdata
        tagdata.shdr_attrs.shader_type.data = 7
