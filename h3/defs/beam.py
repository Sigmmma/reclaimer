############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Named Some Values...
# revision: 3		author: Lord Zedd
# 	Standardizing.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


beam_beam_system_unknown_0 = Struct("unknown_0", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


beam_beam_system_import_data_function = Struct("function", 
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


beam_beam_system_import_data = Struct("import_data", 
    h3_string_id("material_type"),
    SInt32("unknown_0", VISIBLE=False),
    h3_dependency("bitmap"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_reflexive("functions", beam_beam_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


beam_beam_system_shader_propertie_shader_map = Struct("shader_map", 
    h3_dependency("bitmap"),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("bitmap_index"),
    SInt8("unknown_1", VISIBLE=False),
    Bool8("bitmap_flags", *unknown_flags_8),
    SInt8("unknown_bitmap_index_enable"),
    SInt8("uv_argument_index"),
    SInt8("unknown_2", VISIBLE=False),
    SInt8("unknown_3", VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


beam_beam_system_shader_propertie_argument = Struct("argument", 
    Array("arg_array", SUB_STRUCT=Float("arg"), SIZE=4),
    ENDIAN=">", SIZE=16
    )


beam_beam_system_shader_propertie_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


beam_beam_system_shader_propertie_unknown_2 = Struct("unknown_2", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


beam_beam_system_shader_propertie_unknown_3 = Struct("unknown_3", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=6
    )


beam_beam_system_shader_propertie_unknown_4 = Struct("unknown_4", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


beam_beam_system_shader_propertie_function = Struct("function", 
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


beam_beam_system_shader_propertie = Struct("shader_propertie", 
    h3_dependency("template"),
    h3_reflexive("shader_maps", beam_beam_system_shader_propertie_shader_map),
    h3_reflexive("arguments", beam_beam_system_shader_propertie_argument),
    h3_reflexive("unknown_0", beam_beam_system_shader_propertie_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_2", beam_beam_system_shader_propertie_unknown_2),
    h3_reflexive("unknown_3", beam_beam_system_shader_propertie_unknown_3),
    h3_reflexive("unknown_4", beam_beam_system_shader_propertie_unknown_4),
    h3_reflexive("functions", beam_beam_system_shader_propertie_function),
    SInt32("unknown_5", VISIBLE=False),
    SInt32("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


beam_beam_system_unknown_26 = Struct("unknown_26", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


beam_beam_system_compiled_function = Struct("compiled_function", 
    BytesRaw("unknown", SIZE=64, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=64
    )


beam_beam_system_compiled_color_function = Struct("compiled_color_function", 
    color_rgb_float("color"),
    Float("magnitude"),
    ENDIAN=">", SIZE=16
    )


beam_beam_system = Struct("beam_system", 
    h3_string_id("name"),
    h3_dependency("base_render_method"),
    h3_reflexive("unknown_0", beam_beam_system_unknown_0),
    h3_reflexive("import_data", beam_beam_system_import_data),
    h3_reflexive("shader_properties", beam_beam_system_shader_propertie),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=36, VISIBLE=False),
    SInt8("input_0"),
    SInt8("input_range_0"),
    SEnum8("output_kind_0", *cntl_contrail_system_output_kind_0),
    SInt8("output_0"),
    h3_rawdata_ref("unknown_4"),
    BytesRaw("unknown_5", SIZE=8, VISIBLE=False),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *cntl_contrail_system_output_kind_0),
    SInt8("output_1"),
    h3_rawdata_ref("unknown_6"),
    BytesRaw("unknown_7", SIZE=8, VISIBLE=False),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *cntl_contrail_system_output_kind_0),
    SInt8("output_2"),
    h3_rawdata_ref("unknown_8"),
    BytesRaw("unknown_9", SIZE=8, VISIBLE=False),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *cntl_contrail_system_output_kind_0),
    SInt8("output_3"),
    h3_rawdata_ref("unknown_10"),
    BytesRaw("unknown_11", SIZE=24, VISIBLE=False),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *cntl_contrail_system_output_kind_0),
    SInt8("output_4"),
    h3_rawdata_ref("unknown_12"),
    BytesRaw("unknown_13", SIZE=8, VISIBLE=False),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *cntl_contrail_system_output_kind_0),
    SInt8("output_5"),
    h3_rawdata_ref("unknown_14"),
    BytesRaw("unknown_15", SIZE=8, VISIBLE=False),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *cntl_contrail_system_output_kind_0),
    SInt8("output_6"),
    h3_rawdata_ref("unknown_16"),
    BytesRaw("unknown_17", SIZE=8, VISIBLE=False),
    SInt8("input_7"),
    SInt8("input_range_7"),
    SEnum8("output_kind_7", *cntl_contrail_system_output_kind_0),
    SInt8("output_7"),
    h3_rawdata_ref("unknown_18"),
    BytesRaw("unknown_19", SIZE=8, VISIBLE=False),
    SInt8("input_8"),
    SInt8("input_range_8"),
    SEnum8("output_kind_8", *cntl_contrail_system_output_kind_0),
    SInt8("output_8"),
    h3_rawdata_ref("unknown_20"),
    BytesRaw("unknown_21", SIZE=8, VISIBLE=False),
    SInt8("input_9"),
    SInt8("input_range_9"),
    SEnum8("output_kind_9", *cntl_contrail_system_output_kind_0),
    SInt8("output_9"),
    h3_rawdata_ref("unknown_22"),
    BytesRaw("unknown_23", SIZE=8, VISIBLE=False),
    SInt8("input_10"),
    SInt8("input_range_10"),
    SEnum8("output_kind_10", *cntl_contrail_system_output_kind_0),
    SInt8("output_10"),
    h3_rawdata_ref("unknown_24"),
    BytesRaw("unknown_25", SIZE=20, VISIBLE=False),
    h3_reflexive("unknown_26", beam_beam_system_unknown_26),
    h3_reflexive("compiled_functions", beam_beam_system_compiled_function),
    h3_reflexive("compiled_color_functions", beam_beam_system_compiled_color_function),
    ENDIAN=">", SIZE=520
    )


beam_body = Struct("tagdata", 
    h3_reflexive("beam_system", beam_beam_system),
    ENDIAN=">", SIZE=12
    )


def get():
    return beam_def

beam_def = TagDef("beam",
    h3_blam_header('beam'),
    beam_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["beam"], endian=">", tag_cls=H3Tag
    )