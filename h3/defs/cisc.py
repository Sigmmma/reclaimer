from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


cisc_puppet_unknown_6 = Struct("unknown_6",
    Pad(40),
    dependency("unknown_1"),
    ENDIAN=">", SIZE=56
    )


cisc_puppet = Struct("puppets",
    StrLatin1("import_name", SIZE=32),
    string_id_meta("name"),
    string_id_meta("variant"),
    dependency("puppet_animation"),
    dependency("puppet_object"),
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt32("unknown_5"),
    rawdata_ref("import_script"),
    reflexive("unknown_6", cisc_puppet_unknown_6),
    ENDIAN=">", SIZE=116
    )


cisc_shot_lighting = Struct("lighting",
    dependency("cinematic_light"),
    SInt32("owner_puppet_index"),
    string_id_meta("marker"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_unknown_3_unknown_1 = Struct("unknown_1",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


cisc_shot_unknown_3 = Struct("unknown_3",
    Pad(32),
    reflexive("unknown_1", cisc_shot_unknown_3_unknown_1),
    ENDIAN=">", SIZE=44
    )


cisc_shot_sound = Struct("sounds",
    dependency("sound"),
    SInt32("frame"),
    Float("unknown"),
    string_id_meta("unknown_1"),
    Pad(4),
    string_id_meta("unknown_3"),
    ENDIAN=">", SIZE=36
    )


cisc_shot_background_sound = Struct("background_sounds",
    Pad(4),
    dependency("sound"),
    SInt32("frame"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_effect = Struct("effects",
    dependency("effect"),
    SInt32("frame"),
    string_id_meta("marker"),
    SInt32("owner_puppet_index"),
    ENDIAN=">", SIZE=28
    )


cisc_shot_function_value = Struct("values",
    Pad(4),
    SInt32("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    ENDIAN=">", SIZE=16
    )


cisc_shot_function = Struct("functions",
    SInt32("owner_puppet_index"),
    string_id_meta("target_function_name"),
    reflexive("values", cisc_shot_function_value),
    ENDIAN=">", SIZE=20
    )


cisc_shot_cortana_effect = Struct("cortana_effects",
    dependency("effect"),
    Pad(4),
    ENDIAN=">", SIZE=20
    )


cisc_shot_import_script = Struct("import_scripts",
    SInt32("frame"),
    rawdata_ref("import_script"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_frame = Struct("frames",
    Float("x"),
    Float("y"),
    Float("z"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("fov"),
    Bool32("flags",
        "enable_depth_of_field",
        ),
    Float("near_plane"),
    Float("far_plane"),
    Float("focal_depth"),
    Float("blur_amount"),
    ENDIAN=">", SIZE=68
    )


cisc_shot = Struct("shots",
    rawdata_ref("opening_import_script"),
    SInt32("unknown"),
    Pad(4),
    Float("unknown_2"),
    reflexive("lighting", cisc_shot_lighting),
    reflexive("unknown_3", cisc_shot_unknown_3),
    reflexive("sounds", cisc_shot_sound),
    reflexive("background_sounds", cisc_shot_background_sound),
    reflexive("effects", cisc_shot_effect),
    reflexive("functions", cisc_shot_function),
    reflexive("cortana_effects", cisc_shot_cortana_effect),
    reflexive("import_scripts", cisc_shot_import_script),
    rawdata_ref("import_script"),
    SInt32("loaded_frame_count"),
    reflexive("frames", cisc_shot_frame),
    ENDIAN=">", SIZE=164
    )


cisc_texture_camera_shot_frame = Struct("frames",
    SInt32("unknown"),
    Float("x"),
    Float("y"),
    Float("z"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("fov"),
    Bool32("flags",
        "enable_depth_of_field",
        ),
    Float("near_plane"),
    Float("far_plane"),
    Float("focal_depth"),
    Float("blur_amount"),
    ENDIAN=">", SIZE=72
    )


cisc_texture_camera_shot = Struct("shots",
    reflexive("frames", cisc_texture_camera_shot_frame),
    ENDIAN=">", SIZE=12
    )


cisc_texture_camera = Struct("texture_cameras",
    string_id_meta("name"),
    string_id_meta("unknown"),
    reflexive("shots", cisc_texture_camera_shot),
    ENDIAN=">", SIZE=20
    )


cisc_meta_def = BlockDef("cisc",
    string_id_meta("name"),
    StrLatin1("anchor_name", SIZE=32),
    Pad(4),
    rawdata_ref("import_script"),
    reflexive("puppets", cisc_puppet),
    reflexive("shots", cisc_shot),
    reflexive("texture_cameras", cisc_texture_camera),
    rawdata_ref("import_script_1"),
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )