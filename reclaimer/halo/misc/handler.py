import os

from os.path import abspath, basename, normpath

from supyr_struct.tests.test import TagTestHandler
from ..field_types import *


class MiscHaloLoader(TagTestHandler):
    default_defs_path = "reclaimer.halo.misc.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
