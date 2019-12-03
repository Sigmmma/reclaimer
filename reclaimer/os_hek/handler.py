from pathlib import Path
import os

from reclaimer.hek.handler import HaloHandler
from reclaimer.os_hek.defs import __all__ as all_def_names


class OsHaloHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.os_hek.defs"

    tagsdir = str(Path.cwd().join("tags"))
