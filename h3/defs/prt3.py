from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

prt3_output_kind = (
    "none",
    "plus",
    "times",
    )


prt3_unknown_1 = Struct("unknown_1",
    dependency("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=20
    )


prt3_unknown_3 = Struct("unknown_3",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


prt3_import_data_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


prt3_import_data = Struct("import_data",
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
    reflexive("functions", prt3_import_data_function),
    ENDIAN=">", SIZE=60
    )


prt3_shader_propertie_shader_map = Struct("shader_maps",
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


prt3_shader_propertie_argument = Struct("arguments",
    Float("arg_1"),
    Float("arg_2"),
    Float("arg_3"),
    Float("arg_4"),
    ENDIAN=">", SIZE=16
    )


prt3_shader_propertie_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


prt3_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


prt3_shader_propertie_unknown_3 = Struct("unknown_3",
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    ENDIAN=">", SIZE=6
    )


prt3_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


prt3_shader_propertie_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


prt3_shader_propertie = Struct("shader_properties",
    dependency("template"),
    reflexive("shader_maps", prt3_shader_propertie_shader_map),
    reflexive("arguments", prt3_shader_propertie_argument),
    reflexive("unknown", prt3_shader_propertie_unknown),
    Pad(4),
    reflexive("unknown_2", prt3_shader_propertie_unknown_2),
    reflexive("unknown_3", prt3_shader_propertie_unknown_3),
    reflexive("unknown_4", prt3_shader_propertie_unknown_4),
    reflexive("functions", prt3_shader_propertie_function),
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


prt3_unknown_25 = Struct("unknown_25",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


prt3_unknown_26 = Struct("unknown_26",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


prt3_meta_def = BlockDef("prt3",
    Pad(4),
    reflexive("unknown_1", prt3_unknown_1),
    Pad(44),
    dependency("base_render_method"),
    reflexive("unknown_3", prt3_unknown_3),
    reflexive("import_data", prt3_import_data),
    reflexive("shader_properties", prt3_shader_propertie),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
    Pad(4),
    SInt32("unknown_9"),
    SInt8("input"),
    SInt8("input_range"),
    SEnum8("output_kind", *prt3_output_kind),
    SInt8("output"),
    rawdata_ref("unknown_10"),
    Pad(8),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *prt3_output_kind),
    SInt8("output_1"),
    rawdata_ref("unknown_12"),
    Pad(8),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *prt3_output_kind),
    SInt8("output_2"),
    rawdata_ref("unknown_14"),
    Pad(8),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *prt3_output_kind),
    SInt8("output_3"),
    rawdata_ref("unknown_16"),
    Pad(12),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *prt3_output_kind),
    SInt8("output_4"),
    rawdata_ref("unknown_18"),
    Pad(8),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *prt3_output_kind),
    SInt8("output_5"),
    rawdata_ref("unknown_20"),
    Pad(8),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *prt3_output_kind),
    SInt8("output_6"),
    rawdata_ref("unknown_22"),
    Pad(8),
    dependency("particle_model"),
    Pad(12),
    reflexive("unknown_25", prt3_unknown_25),
    reflexive("unknown_26", prt3_unknown_26),
    TYPE=Struct, ENDIAN=">", SIZE=404
    )