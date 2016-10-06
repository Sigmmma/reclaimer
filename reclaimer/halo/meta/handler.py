from os.path import basename, normpath

from supyr_struct.tests.test import TagTestHandler
from ..field_types import *
from .defs.objs.tag import MetaTag


class MapLoader(TagTestHandler):
    default_defs_path = "reclaimer.halo.meta.defs"
