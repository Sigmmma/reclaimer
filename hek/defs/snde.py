from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

snde_body = QStruct("tagdata",
    Pad(4),
    UInt16("priority"),
    Pad(2),
    Float("room intensity"),
    Float("room intensity hf"),
    Float("room rolloff", MIN=0.0, MAX=10.0),
    float_sec("decay time", MIN=0.1, MAX=20.0),
    Float("decay hf ratio", MIN=0.1, MAX=2.0),
    Float("reflections intensity"),
    float_sec("reflections delay", MIN=0.0, MAX=0.3),
    Float("reverb intensity"),
    float_sec("reverb delay", MIN=0.0, MAX=0.1),
    Float("diffusion"),
    Float("density"),
    Float("hf reference", MIN=20.0, MAX=20000.0, SIDETIP="Hz"),
    SIZE=72,
    )

def get():
    return snde_def

snde_def = TagDef("snde",
    blam_header('snde'),
    snde_body,

    ext=".sound_environment", endian=">", tag_cls=HekTag
    )
