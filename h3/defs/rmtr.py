from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rmtr_unknown = Struct("unknown",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


rmtr_import_data_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


rmtr_import_data = Struct("import_data",
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
    reflexive("functions", rmtr_import_data_function),
    ENDIAN=">", SIZE=60
    )


rmtr_shader_propertie_shader_map = Struct("shader_maps",
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


rmtr_shader_propertie_argument = Struct("arguments",
    Float("arg_1"),
    Float("arg_2"),
    Float("arg_3"),
    Float("arg_4"),
    ENDIAN=">", SIZE=16
    )


rmtr_shader_propertie_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


rmtr_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


rmtr_shader_propertie_unknown_3 = Struct("unknown_3",
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    ENDIAN=">", SIZE=6
    )


rmtr_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


rmtr_shader_propertie_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


rmtr_shader_propertie = Struct("shader_properties",
    dependency("template"),
    reflexive("shader_maps", rmtr_shader_propertie_shader_map),
    reflexive("arguments", rmtr_shader_propertie_argument),
    reflexive("unknown", rmtr_shader_propertie_unknown),
    Pad(4),
    reflexive("unknown_2", rmtr_shader_propertie_unknown_2),
    reflexive("unknown_3", rmtr_shader_propertie_unknown_3),
    reflexive("unknown_4", rmtr_shader_propertie_unknown_4),
    reflexive("functions", rmtr_shader_propertie_function),
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


rmtr_meta_def = BlockDef("rmtr",
    dependency("base_render_method"),
    reflexive("unknown", rmtr_unknown),
    reflexive("import_data", rmtr_import_data),
    reflexive("shader_properties", rmtr_shader_propertie),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    Pad(4),
    SInt32("unknown_6"),
    string_id_meta("material_1"),
    string_id_meta("material_2"),
    string_id_meta("material_3"),
    string_id_meta("material_4"),
    SInt16("global_material_index_1"),
    SInt16("global_material_index_2"),
    SInt16("global_material_index_3"),
    SInt16("global_material_index_4"),
    Pad(4),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )