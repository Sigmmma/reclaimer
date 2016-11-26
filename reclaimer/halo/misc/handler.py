from os.path import basename, normpath

from supyr_struct.tests.test import TagTestHandler
from ..field_types import *


class MiscHaloLoader(TagTestHandler):
    default_defs_path = "reclaimer.halo.misc.defs"
