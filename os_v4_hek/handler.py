import os

from os.path import abspath

from ..hek.handler import *


class OsV4HaloHandler(HaloHandler):
    default_defs_path = "reclaimer.os_v4_hek.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
