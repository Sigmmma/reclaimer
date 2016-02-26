from os.path import basename, normpath

from supyr_struct.test import TagTestHandler
from ..fields import *
from .defs.objs.tag import MetaTag


class MapLoader(TagTestHandler):
    default_tag_cls   = MetaTag
    default_defs_path = "reclaimer.halo.meta.defs"
