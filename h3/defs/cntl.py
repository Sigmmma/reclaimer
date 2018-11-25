from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

cntl_contrail_system_output_kind = (
    "none",
    "plus",
    "times",
    )


cntl_contrail_system_unknown_14 = Struct("unknown_14",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


cntl_contrail_system_import_data_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


cntl_contrail_system_import_data = Struct("import_data",
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
    reflexive("functions", cntl_contrail_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


cntl_contrail_system_shader_propertie_shader_map = Struct("shader_maps",
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


cntl_contrail_system_shader_propertie_argument = Struct("arguments",
    Float("arg_1"),
    Float("arg_2"),
    Float("arg_3"),
    Float("arg_4"),
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system_shader_propertie_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


cntl_contrail_system_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


cntl_contrail_system_shader_propertie_unknown_3 = Struct("unknown_3",
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    ENDIAN=">", SIZE=6
    )


cntl_contrail_system_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


cntl_contrail_system_shader_propertie_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


cntl_contrail_system_shader_propertie = Struct("shader_properties",
    dependency("template"),
    reflexive("shader_maps", cntl_contrail_system_shader_propertie_shader_map),
    reflexive("arguments", cntl_contrail_system_shader_propertie_argument),
    reflexive("unknown", cntl_contrail_system_shader_propertie_unknown),
    Pad(4),
    reflexive("unknown_2", cntl_contrail_system_shader_propertie_unknown_2),
    reflexive("unknown_3", cntl_contrail_system_shader_propertie_unknown_3),
    reflexive("unknown_4", cntl_contrail_system_shader_propertie_unknown_4),
    reflexive("functions", cntl_contrail_system_shader_propertie_function),
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


cntl_contrail_system_unknown_33 = Struct("unknown_33",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system_compiled_function = Struct("compiled_functions",
    Pad(64),
    ENDIAN=">", SIZE=64
    )


cntl_contrail_system_compiled_color_function = Struct("compiled_color_functions",
    Float("red"),
    Float("green"),
    Float("blue"),
    Float("magnitude"),
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system = Struct("contrail_system",
    string_id_meta("name"),
    Pad(32),
    SInt8("input"),
    SInt8("input_range"),
    SEnum8("output_kind", *cntl_contrail_system_output_kind),
    SInt8("output"),
    rawdata_ref("unknown_1"),
    Pad(8),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *cntl_contrail_system_output_kind),
    SInt8("output_1"),
    rawdata_ref("unknown_3"),
    Pad(8),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *cntl_contrail_system_output_kind),
    SInt8("output_2"),
    rawdata_ref("unknown_4"),
    Pad(32),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *cntl_contrail_system_output_kind),
    SInt8("output_3"),
    rawdata_ref("unknown_6"),
    Pad(8),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *cntl_contrail_system_output_kind),
    SInt8("output_4"),
    rawdata_ref("unknown_8"),
    Pad(24),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *cntl_contrail_system_output_kind),
    SInt8("output_5"),
    rawdata_ref("unknown_10"),
    Pad(8),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *cntl_contrail_system_output_kind),
    SInt8("output_6"),
    rawdata_ref("unknown_12"),
    Pad(12),
    dependency("base_render_method"),
    reflexive("unknown_14", cntl_contrail_system_unknown_14),
    reflexive("import_data", cntl_contrail_system_import_data),
    reflexive("shader_properties", cntl_contrail_system_shader_propertie),
    SInt8("unknown_15"),
    SInt8("unknown_16"),
    SInt8("unknown_17"),
    SInt8("unknown_18"),
    Pad(4),
    SInt32("unknown_20"),
    Pad(16),
    SInt8("input_7"),
    SInt8("input_range_7"),
    SEnum8("output_kind_7", *cntl_contrail_system_output_kind),
    SInt8("output_7"),
    rawdata_ref("unknown_21"),
    Pad(8),
    SInt8("input_8"),
    SInt8("input_range_8"),
    SEnum8("output_kind_8", *cntl_contrail_system_output_kind),
    SInt8("output_8"),
    rawdata_ref("unknown_23"),
    Pad(8),
    SInt8("input_9"),
    SInt8("input_range_9"),
    SEnum8("output_kind_9", *cntl_contrail_system_output_kind),
    SInt8("output_9"),
    rawdata_ref("unknown_25"),
    Pad(8),
    SInt8("input_10"),
    SInt8("input_range_10"),
    SEnum8("output_kind_10", *cntl_contrail_system_output_kind),
    SInt8("output_10"),
    rawdata_ref("unknown_27"),
    Pad(8),
    SInt8("input_11"),
    SInt8("input_range_11"),
    SEnum8("output_kind_11", *cntl_contrail_system_output_kind),
    SInt8("output_11"),
    rawdata_ref("unknown_29"),
    Pad(8),
    SInt8("input_12"),
    SInt8("input_range_12"),
    SEnum8("output_kind_12", *cntl_contrail_system_output_kind),
    SInt8("output_12"),
    rawdata_ref("unknown_31"),
    Pad(16),
    reflexive("unknown_33", cntl_contrail_system_unknown_33),
    reflexive("compiled_functions", cntl_contrail_system_compiled_function),
    reflexive("compiled_color_functions", cntl_contrail_system_compiled_color_function),
    ENDIAN=">", SIZE=620
    )


cntl_meta_def = BlockDef("cntl",
    reflexive("contrail_system", cntl_contrail_system),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )