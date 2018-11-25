from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

beam_beam_system_output_kind = (
    "none",
    "plus",
    "times",
    )


beam_beam_system_unknown = Struct("unknown",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


beam_beam_system_import_data_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


beam_beam_system_import_data = Struct("import_data",
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
    reflexive("functions", beam_beam_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


beam_beam_system_shader_propertie_shader_map = Struct("shader_maps",
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


beam_beam_system_shader_propertie_argument = Struct("arguments",
    Float("arg_1"),
    Float("arg_2"),
    Float("arg_3"),
    Float("arg_4"),
    ENDIAN=">", SIZE=16
    )


beam_beam_system_shader_propertie_unknown = Struct("unknown",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


beam_beam_system_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


beam_beam_system_shader_propertie_unknown_3 = Struct("unknown_3",
    Pad(4),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    ENDIAN=">", SIZE=6
    )


beam_beam_system_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


beam_beam_system_shader_propertie_function = Struct("functions",
    SInt32("unknown"),
    string_id_meta("name"),
    Pad(8),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


beam_beam_system_shader_propertie = Struct("shader_properties",
    dependency("template"),
    reflexive("shader_maps", beam_beam_system_shader_propertie_shader_map),
    reflexive("arguments", beam_beam_system_shader_propertie_argument),
    reflexive("unknown", beam_beam_system_shader_propertie_unknown),
    Pad(4),
    reflexive("unknown_2", beam_beam_system_shader_propertie_unknown_2),
    reflexive("unknown_3", beam_beam_system_shader_propertie_unknown_3),
    reflexive("unknown_4", beam_beam_system_shader_propertie_unknown_4),
    reflexive("functions", beam_beam_system_shader_propertie_function),
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


beam_beam_system_unknown_30 = Struct("unknown_30",
    Pad(16),
    ENDIAN=">", SIZE=16
    )


beam_beam_system_compiled_function = Struct("compiled_functions",
    Pad(64),
    ENDIAN=">", SIZE=64
    )


beam_beam_system_compiled_color_function = Struct("compiled_color_functions",
    Float("red"),
    Float("green"),
    Float("blue"),
    Float("magnitude"),
    ENDIAN=">", SIZE=16
    )


beam_beam_system = Struct("beam_system",
    string_id_meta("name"),
    dependency("base_render_method"),
    reflexive("unknown", beam_beam_system_unknown),
    reflexive("import_data", beam_beam_system_import_data),
    reflexive("shader_properties", beam_beam_system_shader_propertie),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    Pad(4),
    SInt32("unknown_6"),
    Pad(36),
    SInt8("input"),
    SInt8("input_range"),
    SEnum8("output_kind", *beam_beam_system_output_kind),
    SInt8("output"),
    rawdata_ref("unknown_8"),
    Pad(8),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *beam_beam_system_output_kind),
    SInt8("output_1"),
    rawdata_ref("unknown_10"),
    Pad(8),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *beam_beam_system_output_kind),
    SInt8("output_2"),
    rawdata_ref("unknown_12"),
    Pad(8),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *beam_beam_system_output_kind),
    SInt8("output_3"),
    rawdata_ref("unknown_14"),
    Pad(24),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *beam_beam_system_output_kind),
    SInt8("output_4"),
    rawdata_ref("unknown_16"),
    Pad(8),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *beam_beam_system_output_kind),
    SInt8("output_5"),
    rawdata_ref("unknown_18"),
    Pad(8),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *beam_beam_system_output_kind),
    SInt8("output_6"),
    rawdata_ref("unknown_20"),
    Pad(8),
    SInt8("input_7"),
    SInt8("input_range_7"),
    SEnum8("output_kind_7", *beam_beam_system_output_kind),
    SInt8("output_7"),
    rawdata_ref("unknown_22"),
    Pad(8),
    SInt8("input_8"),
    SInt8("input_range_8"),
    SEnum8("output_kind_8", *beam_beam_system_output_kind),
    SInt8("output_8"),
    rawdata_ref("unknown_24"),
    Pad(8),
    SInt8("input_9"),
    SInt8("input_range_9"),
    SEnum8("output_kind_9", *beam_beam_system_output_kind),
    SInt8("output_9"),
    rawdata_ref("unknown_26"),
    Pad(8),
    SInt8("input_10"),
    SInt8("input_range_10"),
    SEnum8("output_kind_10", *beam_beam_system_output_kind),
    SInt8("output_10"),
    rawdata_ref("unknown_28"),
    Pad(20),
    reflexive("unknown_30", beam_beam_system_unknown_30),
    reflexive("compiled_functions", beam_beam_system_compiled_function),
    reflexive("compiled_color_functions", beam_beam_system_compiled_color_function),
    ENDIAN=">", SIZE=520
    )


beam_meta_def = BlockDef("beam",
    reflexive("beam_system", beam_beam_system),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )