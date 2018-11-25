from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


mffn_location = Struct("locations",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


mffn_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Pad(4),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    rawdata_ref("unknown_6"),
    Float("unknown_7"),
    rawdata_ref("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Float("unknown_15"),
    Float("unknown_16"),
    dependency("effect"),
    ENDIAN=">", SIZE=112
    )


mffn_meta_def = BlockDef("mffn",
    dependency("render_model"),
    Pad(12),
    SInt32("unknown_1"),
    reflexive("locations", mffn_location),
    reflexive("unknown_2", mffn_unknown_2),
    TYPE=Struct, ENDIAN=">", SIZE=56
    )