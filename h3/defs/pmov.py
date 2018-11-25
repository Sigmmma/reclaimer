from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

pmov_movement_type = (
    "physics",
    "collider",
    "swarm",
    "wind",
    )


pmov_movement_parameter = Struct("parameters",
    SInt32("parameter_id"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("function"),
    Float("unknown_2"),
    UInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    ENDIAN=">", SIZE=36
    )


pmov_movement = Struct("movements",
    SEnum16("type", *pmov_movement_type),
    SInt16("unknown"),
    reflexive("parameters", pmov_movement_parameter),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt32("unknown_3"),
    ENDIAN=">", SIZE=24
    )


pmov_meta_def = BlockDef("pmov",
    dependency("template"),
    Bool32("flags",
        "physics",
        "collide_with_structure",
        "collide_with_media",
        "collide_with_scenery",
        "collide_with_vehicles",
        "collide_with_bipeds",
        "swarm",
        "wind",
        ),
    reflexive("movements", pmov_movement),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )