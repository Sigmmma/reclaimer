import os

from os.path import abspath

from ..hek.handler import *


class StubbsHandler(HaloHandler):
    default_defs_path = "reclaimer.halo.stubbs.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
