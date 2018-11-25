from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


cddf_meta_def = BlockDef("cddf",
    Float("apply_damage_scale"),
    Float("apply_recoil_damage_scale"),
    Float("damage_acceleration_min"),
    Float("damage_acceleration_max"),
    Float("damage_scale_min"),
    Float("damage_scale_min_1"),
    Float("recoil_damage_acceleration_min"),
    Float("recoil_damage_acceleration_max"),
    Float("recoil_damage_scale_min"),
    Float("recoil_damage_scale_max"),
    TYPE=Struct, ENDIAN=">", SIZE=40
    )