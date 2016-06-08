from os.path import splitext
from .tag import *
from supyr_struct.fields import Void

class ScexTag(HekTag):

    def convert_to_schi(self, mod_desc=False):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        ext = 'shader_transparent_chicago'
        self.data.blam_header.tag_class.set_data(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        tagdata = self.data.tagdata
        tagdata.numeric_shader_id.data = 6
        if mod_desc:
            tagdata.two_stage_maps.set_desc('TYPE', Void)
            tagdata.ATTR_OFFS[tagdata.NAME_MAP['extra_flags']] = 96
            tagdata.set_size(108)
