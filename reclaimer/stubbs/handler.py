import os

from reclaimer.hek.handler import HaloHandler
from reclaimer.stubbs.defs import __all__ as all_def_names
from supyr_struct.defs.constants import PATHDIV


class StubbsHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.stubbs.defs"
    treat_mode_as_mod2 = False

    tagsdir = "%s%stags%s" % (os.path.abspath(os.curdir), PATHDIV, PATHDIV)
