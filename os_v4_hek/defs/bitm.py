from ...os_v3_hek.defs.bitm import *

def get(): return bitm_def

# replace the model animations dependency with an open sauce one
bitm_body = dict(bitm_body)
bitm_body[3] = Bool16("flags",
    "enable diffusion dithering",
    "disable height map compression",
    "uniform sprite sequences",
    "sprite bug fix",
    ("never share resources", 1<<13)
    )

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=BitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
