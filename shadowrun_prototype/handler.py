import os

from os.path import abspath

from ..hek.handler import *


class ShadowrunPrototypeHandler(HaloHandler):
    default_defs_path = "reclaimer.shadowrun_prototype.defs"
    treat_mode_as_mod2 = False

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
