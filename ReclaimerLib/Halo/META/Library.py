from os.path import basename, normpath

from supyr_struct.Test import Tag_Test_Library
from ..Field_Types import *
from .Defs.Objs.Tag import META_Tag


class Map_Loader(Tag_Test_Library):
    Default_Tag_Cls   = META_Tag
    Default_Defs_Path = "ReclaimerLib.Halo.META.Defs"
