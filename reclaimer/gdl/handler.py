from os.path import splitext

from supyr_struct.test import TagTestHandler
from .fields import *
from .defs.objs.tag import GdlTag

class GdlHandler(TagTestHandler):
    default_tag_cls   = GdlTag
    default_defs_path = "reclaimer.gdl.defs"

    def get_def_id(self, filepath):
        filepath = filepath.replace('/', '\\')
        try:
            def_id = filepath.split('\\')[-1].lower()
        except:
            def_id = ''
            
        def_id, ext = splitext(def_id)
        def_id, ext = def_id.lower(), ext.lower()
        
        if ext in ('.xbe','.rom'):
            def_id = ext[1:]
            
        if def_id in self.defs:
            return def_id
