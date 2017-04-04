import os

from os.path import abspath

from ..hek.handler import *


class StubbsHandler(HaloHandler):
    default_defs_path = "reclaimer.stubbs.defs"
    treat_mode_as_mod2 = False

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
