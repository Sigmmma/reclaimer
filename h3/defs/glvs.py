from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


glvs_unknown_unknown_unknown_unknown_1 = Struct("unknown_1",
    UInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


glvs_unknown_unknown_unknown = Struct("unknown",
    UInt32("unknown"),
    reflexive("unknown_1", glvs_unknown_unknown_unknown_unknown_1),
    ENDIAN=">", SIZE=16
    )


glvs_unknown_unknown = Struct("unknown",
    reflexive("unknown", glvs_unknown_unknown_unknown),
    Pad(4),
    ENDIAN=">", SIZE=16
    )


glvs_unknown = Struct("unknown",
    reflexive("unknown", glvs_unknown_unknown),
    ENDIAN=">", SIZE=12
    )


glvs_vertex_shader_unknown_2 = Struct("unknown_2",
    string_id_meta("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


glvs_vertex_shader = Struct("vertex_shaders",
    rawdata_ref("unknown"),
    rawdata_ref("unknown_1"),
    reflexive("unknown_2", glvs_vertex_shader_unknown_2),
    Pad(24),
    UInt32("vertex_shader"),
    ENDIAN=">", SIZE=80
    )


glvs_meta_def = BlockDef("glvs",
    reflexive("unknown", glvs_unknown),
    Pad(4),
    reflexive("vertex_shaders", glvs_vertex_shader),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )