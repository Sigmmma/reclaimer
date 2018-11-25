from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rmop_unknown = Struct("unknown",
    string_id_meta("type"),
    Pad(8),
    dependency("unknown_1"),
    Pad(44),
    ENDIAN=">", SIZE=72
    )


rmop_meta_def = BlockDef("rmop",
    reflexive("unknown", rmop_unknown),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )