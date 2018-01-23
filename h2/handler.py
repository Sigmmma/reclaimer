import os
from .defs import __all__ as all_def_names
from ..hek.handler import HaloHandler
from os.path import abspath, basename, exists, isfile, normpath, splitext

class Halo2Handler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.h2.defs"

    def get_def_id(self, filepath):
        if not filepath.startswith('.') and '.' in filepath:
            ext = splitext(filepath)[-1].lower()
        else:
            ext = filepath.lower()

        if ext in self.ext_id_map:
            return self.ext_id_map[ext]

        '''It is more reliable to determine a Halo tag
        based on its 4CC def_id than by file extension'''
        try:
            with open(filepath, 'r+b') as tagfile:
                tagfile.seek(36)
                def_id = str(tagfile.read(4), 'latin-1')
            tagfile.seek(60);
            engine_id = tagfile.read(4)
            if def_id in self.defs and engine_id in (
                b'!MLB', b'BMAL', b'BALM', b'lbma'):
                return def_id
        except:
            return None
