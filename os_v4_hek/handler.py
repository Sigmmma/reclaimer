import os

from os.path import abspath

from ..hek.handler import *
from .defs import __all__ as all_def_names


class OsV4HaloHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.os_v4_hek.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
