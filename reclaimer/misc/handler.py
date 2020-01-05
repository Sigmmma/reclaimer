#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
import os

from binilla.handler import Handler
from reclaimer.misc.defs import __all__ as all_def_names


class MiscHaloLoader(Handler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.misc.defs"

    tagsdir = tagsdir = str(Path.cwd().joinpath("tags"))

    def get_def_id(self, filepath):
        '''docstring'''
        def_id = Handler.get_def_id(self, filepath)

        if def_id == 'xbox_gametype' and 'pc_gametype' in self.id_ext_map:
            return 'pc_gametype'
        return def_id
