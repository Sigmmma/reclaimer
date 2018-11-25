from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


decs_decal_system_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


decs_decal_system_import_data_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


decs_decal_system_import_data = Struct("import_data",
    string_id_meta("material_type"),
    SInt32("unknown"),
    dependency("bitmap"),
    Pad(4),
    SInt32("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    SInt16("unknown_7"),
    SInt16("unknown_8"),
    Pad(4),
    reflexive("functions", decs_decal_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


decs_decal_system_shader_propertie_shader_map = Struct("shader_maps",
    dependency("bitmap"),
    SInt8("unknown"),
    SInt8("bitmap_index"),
    SInt8("unknown_1"),
    Bool8("bitmap_flags",
        ),
    SInt8("unknown_bitmap_index_enable"),
    SInt8("uv_argument_index"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    ENDIAN=">", SIZE=24
    )


decs_decal_system_shader_propertie_argument = Struct("arguments",
    Float("arg_1"),
    Float("arg_2"),
    Float("arg_3"),
    Float("arg_4"),
    ENDIAN=">", SIZE=16
    )


decs_decal_system_shader_propertie_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


decs_decal_system_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


decs_decal_system_shader_propertie_unknown_3 = Struct("unknown_3",
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    ENDIAN=">", SIZE=6
    )


decs_decal_system_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


decs_decal_system_shader_propertie_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


decs_decal_system_shader_propertie = Struct("shader_properties",
    dependency("template"),
    reflexive("shader_maps", decs_decal_system_shader_propertie_shader_map),
    reflexive("arguments", decs_decal_system_shader_propertie_argument),
    reflexive("unknown", decs_decal_system_shader_propertie_unknown),
    Pad(4),
    reflexive("unknown_2", decs_decal_system_shader_propertie_unknown_2),
    reflexive("unknown_3", decs_decal_system_shader_propertie_unknown_3),
    reflexive("unknown_4", decs_decal_system_shader_propertie_unknown_4),
    reflexive("functions", decs_decal_system_shader_propertie_function),
    SInt32("unknown_5"),
    SInt32("unknown_6"),
    Pad(4),
    SInt16("unknown_8"),
    SInt16("unknown_9"),
    SInt16("unknown_10"),
    SInt16("unknown_11"),
    SInt16("unknown_12"),
    SInt16("unknown_13"),
    SInt16("unknown_14"),
    SInt16("unknown_15"),
    ENDIAN=">", SIZE=132
    )


decs_decal_system = Struct("decal_system",
    string_id_meta("name"),
    Pad(4),
    dependency("base_render_method"),
    reflexive("unknown_1", decs_decal_system_unknown_1),
    reflexive("import_data", decs_decal_system_import_data),
    reflexive("shader_properties", decs_decal_system_shader_propertie),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    Pad(4),
    SInt32("unknown_7"),
    Pad(44),
    ENDIAN=">", SIZE=116
    )


decs_meta_def = BlockDef("decs",
    Pad(8),
    Float("radius"),
    Pad(8),
    reflexive("decal_system", decs_decal_system),
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )