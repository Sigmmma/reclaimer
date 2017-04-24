from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

snde_body = QStruct("tagdata",
    Pad(4),
    BUInt16("priority"),
    Pad(2),
    BFloat("room intensity"),
    BFloat("room intensity hf"),
    BFloat("room rolloff", MIN=0.0, MAX=10.0),
    float_sec("decay time", MIN=0.1, MAX=20.0),
    BFloat("decay hf ratio", MIN=0.1, MAX=2.0),
    BFloat("reflections intensity"),
    float_sec("reflections delay", MIN=0.0, MAX=0.3),
    BFloat("reverb intensity"),
    float_sec("reverb delay", MIN=0.0, MAX=0.1),
    BFloat("diffusion"),
    BFloat("density"),
    BFloat("hf reference", MIN=20.0, MAX=20000.0, SIDETIP="Hz"),
    SIZE=72,
    )

def get():
    return snde_def

snde_def = TagDef("snde",
    blam_header('snde'),
    snde_body,

    ext=".sound_environment", endian=">", tag_cls=HekTag
    )
