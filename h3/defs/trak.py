from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


trak_camera_point = Struct("camera_points",
    Float("position_i"),
    Float("position_j"),
    Float("position_k"),
    Float("orientation_i"),
    Float("orientation_j"),
    Float("orientation_k"),
    Float("orientation_w"),
    ENDIAN=">", SIZE=28
    )


trak_meta_def = BlockDef("trak",
    Pad(4),
    reflexive("camera_points", trak_camera_point),
    TYPE=Struct, ENDIAN=">", SIZE=16
    )