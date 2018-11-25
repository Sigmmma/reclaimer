from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


vtsh_unknown_1_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


vtsh_unknown_1 = Struct("unknown_1",
    reflexive("unknown", vtsh_unknown_1_unknown),
    ENDIAN=">", SIZE=12
    )


vtsh_vertex_shader_unknown_2 = Struct("unknown_2",
    string_id_meta("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


vtsh_vertex_shader = Struct("vertex_shaders",
    rawdata_ref("unknown"),
    rawdata_ref("unknown_1"),
    reflexive("unknown_2", vtsh_vertex_shader_unknown_2),
    Pad(24),
    UInt32("vertex_shader"),
    ENDIAN=">", SIZE=80
    )


vtsh_meta_def = BlockDef("vtsh",
    Pad(4),
    reflexive("unknown_1", vtsh_unknown_1),
    Pad(4),
    reflexive("vertex_shaders", vtsh_vertex_shader),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )