import os

from os.path import abspath

from ..hek.handler import *


class OsHaloHandler(HaloHandler):
    default_defs_path = "reclaimer.halo.os_hek.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
