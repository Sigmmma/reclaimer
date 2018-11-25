from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


colo_color_table = Struct("color_table",
    StrLatin1("string", SIZE=32),
    color_argb_float("color"),
    ENDIAN=">", SIZE=48
    )


colo_meta_def = BlockDef("colo",
    reflexive("color_table", colo_color_table),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )