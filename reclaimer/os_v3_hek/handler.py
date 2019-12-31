from pathlib import Path
import os

from reclaimer.hek.handler import HaloHandler
from reclaimer.os_v3_hek.defs import __all__ as all_def_names


class OsV3HaloHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.os_v3_hek.defs"
