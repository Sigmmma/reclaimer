from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


dsrc_data_integer_value = Struct("integer_values",
    string_id_meta("data_type"),
    SInt32("value"),
    ENDIAN=">", SIZE=8
    )


dsrc_data_string_value = Struct("string_values",
    string_id_meta("data_type"),
    StrLatin1("value", SIZE=20),
    ENDIAN=">", SIZE=36
    )


dsrc_data_stringid_value = Struct("stringid_values",
    string_id_meta("data_type"),
    string_id_meta("value"),
    ENDIAN=">", SIZE=8
    )


dsrc_data = Struct("data",
    reflexive("integer_values", dsrc_data_integer_value),
    reflexive("string_values", dsrc_data_string_value),
    reflexive("stringid_values", dsrc_data_stringid_value),
    string_id_meta("unknown"),
    ENDIAN=">", SIZE=40
    )


dsrc_meta_def = BlockDef("dsrc",
    string_id_meta("name"),
    Pad(12),
    reflexive("data", dsrc_data),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )