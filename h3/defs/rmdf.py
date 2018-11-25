from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rmdf_method_shader_option = Struct("shader_options",
    string_id_meta("type"),
    dependency("option"),
    string_id_meta("unknown"),
    string_id_meta("unknown_1"),
    ENDIAN=">", SIZE=28
    )


rmdf_method = Struct("methods",
    string_id_meta("type"),
    reflexive("shader_options", rmdf_method_shader_option),
    string_id_meta("unknown"),
    string_id_meta("unknown_1"),
    ENDIAN=">", SIZE=24
    )


rmdf_unknown_1_unknown_1_unknown_1 = Struct("unknown_1",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


rmdf_unknown_1_unknown_1 = Struct("unknown_1",
    Pad(4),
    reflexive("unknown_1", rmdf_unknown_1_unknown_1_unknown_1),
    ENDIAN=">", SIZE=16
    )


rmdf_unknown_1 = Struct("unknown_1",
    Pad(4),
    reflexive("unknown_1", rmdf_unknown_1_unknown_1),
    ENDIAN=">", SIZE=16
    )


rmdf_unknown_2 = Struct("unknown_2",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


rmdf_meta_def = BlockDef("rmdf",
    dependency("unknown"),
    reflexive("methods", rmdf_method),
    reflexive("unknown_1", rmdf_unknown_1),
    reflexive("unknown_2", rmdf_unknown_2),
    dependency("unknown_3"),
    dependency("unknown_4"),
    Pad(8),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )