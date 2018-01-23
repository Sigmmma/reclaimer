import os

from os.path import abspath

from ..hek.handler import *
from .defs import __all__ as all_def_names


class StubbsHandler(HaloHandler):
    frozen_imp_paths = all_def_names
    default_defs_path = "reclaimer.stubbs.defs"
    treat_mode_as_mod2 = False

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
