from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rmt2_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


rmt2_unknown_2 = Struct("unknown_2",
    Pad(28),
    ENDIAN=">", SIZE=28
    )


rmt2_unknown_3 = Struct("unknown_3",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


rmt2_argument = Struct("arguments",
    string_id_meta("name"),
    ENDIAN=">", SIZE=4
    )


rmt2_unknown_4 = Struct("unknown_4",
    string_id_meta("unknown"),
    ENDIAN=">", SIZE=4
    )


rmt2_unknown_5 = Struct("unknown_5",
    string_id_meta("unknown"),
    ENDIAN=">", SIZE=4
    )


rmt2_shader_map = Struct("shader_maps",
    string_id_meta("name"),
    ENDIAN=">", SIZE=4
    )


rmt2_meta_def = BlockDef("rmt2",
    dependency("vertex_shader"),
    dependency("pixel_shader"),
    Pad(4),
    reflexive("unknown_1", rmt2_unknown_1),
    reflexive("unknown_2", rmt2_unknown_2),
    reflexive("unknown_3", rmt2_unknown_3),
    reflexive("arguments", rmt2_argument),
    reflexive("unknown_4", rmt2_unknown_4),
    reflexive("unknown_5", rmt2_unknown_5),
    reflexive("shader_maps", rmt2_shader_map),
    Pad(12),
    TYPE=Struct, ENDIAN=">", SIZE=132
    )