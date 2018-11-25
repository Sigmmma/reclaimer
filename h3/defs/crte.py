from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


crte_unknown_6_unknown = Struct("unknown",
    Pad(32),
    ENDIAN=">", SIZE=32
    )


crte_unknown_6_unknown_1_unknown_1_unknown = Struct("unknown",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


crte_unknown_6_unknown_1_unknown_1 = Struct("unknown_1",
    reflexive("unknown", crte_unknown_6_unknown_1_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


crte_unknown_6_unknown_1 = Struct("unknown_1",
    Pad(28),
    reflexive("unknown_1", crte_unknown_6_unknown_1_unknown_1),
    ENDIAN=">", SIZE=40
    )


crte_unknown_6 = Struct("unknown_6",
    reflexive("unknown", crte_unknown_6_unknown),
    reflexive("unknown_1", crte_unknown_6_unknown_1),
    ENDIAN=">", SIZE=24
    )


crte_unknown_7_unknown_unknown_1_unknown = Struct("unknown",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


crte_unknown_7_unknown_unknown_1 = Struct("unknown_1",
    reflexive("unknown", crte_unknown_7_unknown_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown = Struct("unknown",
    Pad(28),
    reflexive("unknown_1", crte_unknown_7_unknown_unknown_1),
    Pad(12),
    ENDIAN=">", SIZE=52
    )


crte_unknown_7_unknown_1 = Struct("unknown_1",
    Pad(52),
    ENDIAN=">", SIZE=52
    )


crte_unknown_7_unknown_2_unknown_1_unknown = Struct("unknown",
    Pad(12),
    ENDIAN=">", SIZE=12
    )


crte_unknown_7_unknown_2_unknown_1 = Struct("unknown_1",
    reflexive("unknown", crte_unknown_7_unknown_2_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown_2 = Struct("unknown_2",
    Pad(24),
    reflexive("unknown_1", crte_unknown_7_unknown_2_unknown_1),
    Pad(12),
    ENDIAN=">", SIZE=48
    )


crte_unknown_7_unknown_3_unknown_1_unknown = Struct("unknown",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


crte_unknown_7_unknown_3_unknown_1 = Struct("unknown_1",
    reflexive("unknown", crte_unknown_7_unknown_3_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown_3 = Struct("unknown_3",
    Pad(28),
    reflexive("unknown_1", crte_unknown_7_unknown_3_unknown_1),
    Pad(12),
    ENDIAN=">", SIZE=52
    )


crte_unknown_7 = Struct("unknown_7",
    reflexive("unknown", crte_unknown_7_unknown),
    reflexive("unknown_1", crte_unknown_7_unknown_1),
    reflexive("unknown_2", crte_unknown_7_unknown_2),
    reflexive("unknown_3", crte_unknown_7_unknown_3),
    ENDIAN=">", SIZE=48
    )


crte_unknown_9_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


crte_unknown_9_unknown_1_unknown_1_unknown = Struct("unknown",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


crte_unknown_9_unknown_1_unknown_1 = Struct("unknown_1",
    reflexive("unknown", crte_unknown_9_unknown_1_unknown_1_unknown),
    rawdata_ref("unknown_1"),
    ENDIAN=">", SIZE=32
    )


crte_unknown_9_unknown_1 = Struct("unknown_1",
    Pad(28),
    reflexive("unknown_1", crte_unknown_9_unknown_1_unknown_1),
    Pad(12),
    ENDIAN=">", SIZE=52
    )


crte_unknown_9_unknown_2 = Struct("unknown_2",
    Pad(12),
    ENDIAN=">", SIZE=12
    )


crte_unknown_9 = Struct("unknown_9",
    reflexive("unknown", crte_unknown_9_unknown),
    reflexive("unknown_1", crte_unknown_9_unknown_1),
    reflexive("unknown_2", crte_unknown_9_unknown_2),
    ENDIAN=">", SIZE=36
    )


crte_meta_def = BlockDef("crte",
    string_id_meta("unknown"),
    Pad(16),
    rawdata_ref("unknown_2"),
    rawdata_ref("unknown_3"),
    dependency("unknown_4"),
    string_id_meta("unknown_5"),
    reflexive("unknown_6", crte_unknown_6),
    reflexive("unknown_7", crte_unknown_7),
    Pad(12),
    reflexive("unknown_9", crte_unknown_9),
    TYPE=Struct, ENDIAN=">", SIZE=128
    )