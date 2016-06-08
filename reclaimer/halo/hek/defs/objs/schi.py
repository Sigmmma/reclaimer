from os.path import splitext
from .tag import *

class SchiTag(HekTag):
    
    def convert_to_scex(self, mod_desc=False):
        '''Call this function to convert a SCHI tag to a SCEX tag'''
        ext = 'shader_transparent_chicago_extended'
        self.data.blam_header.tag_class.set_data(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        tagdata = self.data.tagdata
        tagdata.numeric_shader_id.data = 7
        if mod_desc:
            tagdata.ATTR_OFFS[tagdata.NAME_MAP['extra_flags']] = 108
            tagdata.set_size(120)
