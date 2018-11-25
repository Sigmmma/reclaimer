from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


cine_scene_unknown = Struct("scene_unknown",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


cine_cinematic_scene = Struct("cinematic_scenes",
    dependency("scene"),
    ENDIAN=">", SIZE=16
    )


cine_meta_def = BlockDef("cine",
    SInt32("unknown"),
    reflexive("scene_unknown", cine_scene_unknown),
    dependency("import_scenario"),
    SInt32("unknown_1"),
    string_id_meta("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt32("unknown_5"),
    Pad(20),
    SInt32("unknown_7"),
    Pad(12),
    SInt32("unknown_9"),
    dependency("unknown_10"),
    rawdata_ref("import_script"),
    reflexive("cinematic_scenes", cine_cinematic_scene),
    rawdata_ref("import_script_1"),
    rawdata_ref("import_script_2"),
    TYPE=Struct, ENDIAN=">", SIZE=176
    )