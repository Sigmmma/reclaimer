from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

bloom_global = Struct("bloom global",
    Bool16("shader model",
        "enabled",
        "apply after hud",
        ),
    Pad(2),
    Float("bloom size"),
    Float("bloom exposure"),
    Float("bloom mix amount", MIN=0.0, MAX=1.0),
    QStruct("bloom minimum color", INCLUDE=rgb_float),
    QStruct("bloom maximum color", INCLUDE=rgb_float),
    SIZE=40,
    )

sppg_body = Struct("tagdata",
    Pad(4),
    reflexive("bloom globals", bloom_global, 1),
    SIZE=244
    )

def get():
    return sppg_def

sppg_def = TagDef("sppg",
    blam_header_os('sppg'),
    sppg_body,

    ext=".shader_postprocess_globals", endian=">", tag_cls=HekTag
    )
