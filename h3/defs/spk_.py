from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


spk__meta_def = BlockDef("spk!",
    Float("almost_never"),
    Float("rarely"),
    Float("somewhat"),
    Float("often"),
    Pad(24),
    TYPE=Struct, ENDIAN=">", SIZE=40
    )
