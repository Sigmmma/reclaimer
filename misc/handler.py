from pathlib import Path
import os

from binilla.handler import Handler
from reclaimer.misc.defs import __all__ as all_def_names


class MiscHaloLoader(Handler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.misc.defs"

    tagsdir = tagsdir = str(Path.cwd().join("tags"))

    def get_def_id(self, filepath):
        '''docstring'''
        def_id = Handler.get_def_id(self, filepath)

        if def_id == 'xbox_gametype' and 'pc_gametype' in self.id_ext_map:
            return 'pc_gametype'
        return def_id
