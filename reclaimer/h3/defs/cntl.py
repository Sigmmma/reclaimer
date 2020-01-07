#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Standardizing.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


cntl_contrail_system_unknown_14 = Struct("unknown_14",
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


cntl_contrail_system_import_data_function = Struct("function",
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


cntl_contrail_system_import_data = Struct("import_data",
    h3_string_id("material_type"),
    SInt32("unknown_0", VISIBLE=False),
    h3_dependency("bitmap"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_reflexive("functions", cntl_contrail_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


cntl_contrail_system_shader_propertie_shader_map = Struct("shader_map",
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


cntl_contrail_system_shader_propertie_argument = Struct("argument",
    Array("arg_array", SUB_STRUCT=Float("arg"), SIZE=4),
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system_shader_propertie_unknown_0 = Struct("unknown_0",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


cntl_contrail_system_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


cntl_contrail_system_shader_propertie_unknown_3 = Struct("unknown_3",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=6
    )


cntl_contrail_system_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


cntl_contrail_system_shader_propertie_function = Struct("function",
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


cntl_contrail_system_shader_propertie = Struct("shader_propertie",
    h3_dependency("template"),
    h3_reflexive("shader_maps", cntl_contrail_system_shader_propertie_shader_map),
    h3_reflexive("arguments", cntl_contrail_system_shader_propertie_argument),
    h3_reflexive("unknown_0", cntl_contrail_system_shader_propertie_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_2", cntl_contrail_system_shader_propertie_unknown_2),
    h3_reflexive("unknown_3", cntl_contrail_system_shader_propertie_unknown_3),
    h3_reflexive("unknown_4", cntl_contrail_system_shader_propertie_unknown_4),
    h3_reflexive("functions", cntl_contrail_system_shader_propertie_function),
    SInt32("unknown_5", VISIBLE=False),
    SInt32("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


cntl_contrail_system_unknown_29 = Struct("unknown_29",
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system_compiled_function = Struct("compiled_function",
    BytesRaw("unknown", SIZE=64, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=64
    )


cntl_contrail_system_compiled_color_function = Struct("compiled_color_function",
    color_rgb_float("color"),
    Float("magnitude"),
    ENDIAN=">", SIZE=16
    )


cntl_contrail_system = Struct("contrail_system",
    h3_string_id("name"),
    BytesRaw("unknown_0", SIZE=32, VISIBLE=False),
    SInt8("input_0"),
    SInt8("input_range_0"),
    SEnum8("output_kind_0", *cntl_contrail_system_output_kind_0),
    SInt8("output_0"),
    h3_rawdata_ref("unknown_1"),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *cntl_contrail_system_output_kind_0),
    SInt8("output_1"),
    h3_rawdata_ref("unknown_3"),
    Pad(8),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *cntl_contrail_system_output_kind_0),
    SInt8("output_2"),
    h3_rawdata_ref("unknown_4"),
    BytesRaw("unknown_5", SIZE=32, VISIBLE=False),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *cntl_contrail_system_output_kind_0),
    SInt8("output_3"),
    h3_rawdata_ref("unknown_6"),
    BytesRaw("unknown_7", SIZE=8, VISIBLE=False),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *cntl_contrail_system_output_kind_0),
    SInt8("output_4"),
    h3_rawdata_ref("unknown_8"),
    BytesRaw("unknown_9", SIZE=24, VISIBLE=False),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *cntl_contrail_system_output_kind_0),
    SInt8("output_5"),
    h3_rawdata_ref("unknown_10"),
    BytesRaw("unknown_11", SIZE=8, VISIBLE=False),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *cntl_contrail_system_output_kind_0),
    SInt8("output_6"),
    h3_rawdata_ref("unknown_12"),
    BytesRaw("unknown_13", SIZE=12, VISIBLE=False),
    h3_dependency("base_render_method"),
    h3_reflexive("unknown_14", cntl_contrail_system_unknown_14),
    h3_reflexive("import_data", cntl_contrail_system_import_data),
    h3_reflexive("shader_properties", cntl_contrail_system_shader_propertie),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_15", SIZE=4, VISIBLE=False),
    SInt32("unknown_16", VISIBLE=False),
    Pad(16),
    SInt8("input_7"),
    SInt8("input_range_7"),
    SEnum8("output_kind_7", *cntl_contrail_system_output_kind_0),
    SInt8("output_7"),
    h3_rawdata_ref("unknown_17"),
    BytesRaw("unknown_18", SIZE=8, VISIBLE=False),
    SInt8("input_8"),
    SInt8("input_range_8"),
    SEnum8("output_kind_8", *cntl_contrail_system_output_kind_0),
    SInt8("output_8"),
    h3_rawdata_ref("unknown_19"),
    BytesRaw("unknown_20", SIZE=8, VISIBLE=False),
    SInt8("input_9"),
    SInt8("input_range_9"),
    SEnum8("output_kind_9", *cntl_contrail_system_output_kind_0),
    SInt8("output_9"),
    h3_rawdata_ref("unknown_21"),
    BytesRaw("unknown_22", SIZE=8, VISIBLE=False),
    SInt8("input_10"),
    SInt8("input_range_10"),
    SEnum8("output_kind_10", *cntl_contrail_system_output_kind_0),
    SInt8("output_10"),
    h3_rawdata_ref("unknown_23"),
    BytesRaw("unknown_24", SIZE=8, VISIBLE=False),
    SInt8("input_11"),
    SInt8("input_range_11"),
    SEnum8("output_kind_11", *cntl_contrail_system_output_kind_0),
    SInt8("output_11"),
    h3_rawdata_ref("unknown_25"),
    BytesRaw("unknown_26", SIZE=8, VISIBLE=False),
    SInt8("input_12"),
    SInt8("input_range_12"),
    SEnum8("output_kind_12", *cntl_contrail_system_output_kind_0),
    SInt8("output_12"),
    h3_rawdata_ref("unknown_27"),
    BytesRaw("unknown_28", SIZE=16, VISIBLE=False),
    h3_reflexive("unknown_29", cntl_contrail_system_unknown_29),
    h3_reflexive("compiled_functions", cntl_contrail_system_compiled_function),
    h3_reflexive("compiled_color_functions", cntl_contrail_system_compiled_color_function),
    ENDIAN=">", SIZE=620
    )


cntl_body = Struct("tagdata",
    h3_reflexive("contrail_system", cntl_contrail_system),
    ENDIAN=">", SIZE=12
    )


def get():
    return cntl_def

cntl_def = TagDef("cntl",
    h3_blam_header('cntl'),
    cntl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["cntl"], endian=">", tag_cls=H3Tag
    )
