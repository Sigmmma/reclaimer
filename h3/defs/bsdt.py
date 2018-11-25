from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


bsdt_unknown0 = Struct("unknown0",
    Pad(8),
    rawdata_ref("unknown_1"),
    Pad(8),
    ENDIAN=">", SIZE=36
    )


bsdt_unknown1 = Struct("unknown1",
    Pad(8),
    rawdata_ref("unknown_1"),
    Pad(8),
    ENDIAN=">", SIZE=36
    )


bsdt_meta_def = BlockDef("bsdt",
    Float("maximum_vitality"),
    dependency("effect"),
    dependency("sound"),
    Pad(16),
    dependency("crack_bitmap"),
    dependency("hole_bitmap"),
    Pad(36),
    reflexive("unknown0", bsdt_unknown0),
    Pad(12),
    reflexive("unknown1", bsdt_unknown1),
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=160
    )