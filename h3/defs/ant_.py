from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


ant_vertice = Struct("vertices",
    float_rad("angle_y"),
    float_rad("angle_p"),
    Float("length"),
    SInt16("sequence_index"),
    SInt16("unknown"),
    color_argb_float("color"),
    color_argb_float("lod_color"),
    Pad(16),
    ENDIAN=">", SIZE=64
    )


ant__meta_def = BlockDef("ant!",
    string_id_meta("attachment_marker_name"),
    dependency("bitmaps"),
    dependency("physics"),
    Pad(28),
    reflexive("vertices", ant_vertice),
    TYPE=Struct, ENDIAN=">", SIZE=76
    )
