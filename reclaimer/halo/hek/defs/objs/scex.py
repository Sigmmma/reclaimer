from os.path import splitext
from .tag import *

class ScexTag(HekTag):

    def convert_to_schi(self, mod_desc=False):    
        '''Call this function to convert a SCEX tag to a SCHI tag'''
        self.ext = ext = 'shader_transparent_chicago'
        self.data.blam_header.tag_class.set_to(ext)
        self.filepath = splitext(self.filepath)[0] + '.' + ext
        
        tagdata = self.data.tagdata
        tagdata.shdr_attrs.shader_type.data = 6
        if mod_desc:
            dict.__setitem__(tagdata.scex_attrs.two_stage_maps.desc,
                             'TYPE', Void)
            tagdata.scex_attrs.ATTR_OFFS[
                tagdata.scex_attrs.NAME_MAP['extra_flags']] = 96
            tagdata.set_size(108)
            tagdata.scex_attrs.set_size(68)
