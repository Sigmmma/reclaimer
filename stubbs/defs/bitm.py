from ...hek.defs.bitm import *
from .objs.bitm import StubbsBitmTag

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=StubbsBitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
