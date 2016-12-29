import os

from os.path import abspath, basename, normpath

from supyr_struct.apps.handler import Handler
from ..field_types import *


class MapLoader(Handler):
    default_defs_path = "reclaimer.halo.meta.defs"

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)
