import os

from os.path import abspath

from ..hek.handler import *


class OsV3HaloHandler(HaloHandler):
    default_defs_path = "reclaimer.os_v3_hek.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
