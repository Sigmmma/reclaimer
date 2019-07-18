import os

from reclaimer.hek.handler import HaloHandler
from reclaimer.os_v3_hek.defs import __all__ as all_def_names
from supyr_struct.defs.constants import PATHDIV


class OsV3HaloHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.os_v3_hek.defs"

    tagsdir = "%s%stags%s" % (os.path.abspath(os.curdir), PATHDIV, PATHDIV)
