from os.path import splitext
from .tag import *

class ScexTag(HekTag):

    def convert_to_schi(self):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        self.ext = ext = 'shader_transparent_chicago'
        self.data.blam_header.tag_class.set_to(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        tagdata = self.data.tagdata
        tagdata.shdr_attrs.shader_type.data = 6
