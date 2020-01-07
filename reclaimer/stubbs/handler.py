#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path

from reclaimer.hek.handler import HaloHandler
from reclaimer.stubbs.defs import __all__ as all_def_names


class StubbsHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.stubbs.defs"
    treat_mode_as_mod2 = False
