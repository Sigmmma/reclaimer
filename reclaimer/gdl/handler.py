from os.path import splitext

from supyr_struct.test import TagTestHandler
from .fields import *
from .defs.objs.tag import GdlTag

class GdlHandler(TagTestHandler):
    default_tag_cls   = GdlTag
    default_defs_path = "reclaimer.gdl.defs"

    def get_tag_id(self, filepath):
        filepath = filepath.replace('/', '\\')
        try:
            tag_id = filepath.split('\\')[-1].lower()
        except:
            tag_id = ''
        
        if splitext(tag_id)[-1].lower() == '.xbe':
            tag_id = 'xbe'
            
        if tag_id in self.defs:
            return tag_id
