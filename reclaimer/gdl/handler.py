from os.path import splitext

from supyr_struct.test import TagTestHandler
from .field_types import *
from .defs.objs.tag import GdlTag

class GdlHandler(TagTestHandler):
    default_tag_cls   = GdlTag
    default_defs_path = "reclaimer.gdl.defs"

    def get_def_id(self, filepath):
        filepath = filepath.replace('/', '\\')
        try:
            filename = filepath.split('\\')[-1].lower()
        except:
            filename = ''
            
        filename, ext = splitext(filename)
        filename, ext = filename.lower(), ext.lower()
        
        if ext in ('.xbe','.rom'):
            return ext[1:]
        elif ext == '.ps2':
            return filename
        elif ext == '.wad':
            if filename in ('jac','jes','kni','med','min','ogr',
                            'sor','tig','uni','val','war','wiz'):
                return 'pdata'
            elif filename in ('battle','castle','desert','dream',
                              'forest','hell','ice','mount','secret',
                              'sky','temple','test','tower','town'):
                return 'wdata'
            elif filename in ('lich','dragon','pboss', 'chimera',
                              'gar_eagl','gar_lion','gar_serp',
                              'drider','djinn','yeti','wraith',
                              'skorne1','skorne2','garm',
                              'general','golem','golemf', 'golemi'):
                return 'critter'
        elif filename in self.defs:
            return filename
        elif ext in self.id_ext_map.values():
            for def_id in self.id_ext_map:
                if self.id_ext_map[def_id].lower() == ext:
                    return def_id
