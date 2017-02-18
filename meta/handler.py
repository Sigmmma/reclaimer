import os

from os.path import abspath, basename, normpath

from binilla.handler import Handler
from ..field_types import *


class MapLoader(Handler):
    default_defs_path = "reclaimer.meta.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
