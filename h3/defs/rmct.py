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


rmct_unknown_0 = Struct("unknown_0", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


rmct_import_data_function = Struct("function", 
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


rmct_import_data = Struct("import_data", 
    h3_string_id("material_type"),
    SInt32("unknown_0", VISIBLE=False),
    h3_dependency("bitmap"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_reflexive("functions", rmct_import_data_function),
    ENDIAN=">", SIZE=60
    )


rmct_shader_propertie_shader_map = Struct("shader_map", 
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


rmct_shader_propertie_argument = Struct("argument", 
    Array("arg_array", SUB_STRUCT=Float("arg"), SIZE=4),
    ENDIAN=">", SIZE=16
    )


rmct_shader_propertie_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmct_shader_propertie_unknown_2 = Struct("unknown_2", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


rmct_shader_propertie_unknown_3 = Struct("unknown_3", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=6
    )


rmct_shader_propertie_unknown_4 = Struct("unknown_4", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


rmct_shader_propertie_function = Struct("function", 
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


rmct_shader_propertie = Struct("shader_propertie", 
    h3_dependency("template"),
    h3_reflexive("shader_maps", rmct_shader_propertie_shader_map),
    h3_reflexive("arguments", rmct_shader_propertie_argument),
    h3_reflexive("unknown_0", rmct_shader_propertie_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_2", rmct_shader_propertie_unknown_2),
    h3_reflexive("unknown_3", rmct_shader_propertie_unknown_3),
    h3_reflexive("unknown_4", rmct_shader_propertie_unknown_4),
    h3_reflexive("functions", rmct_shader_propertie_function),
    SInt32("unknown_5", VISIBLE=False),
    SInt32("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


rmct_body = Struct("tagdata", 
    h3_dependency("base_render_method"),
    h3_reflexive("unknown_0", rmct_unknown_0),
    h3_reflexive("import_data", rmct_import_data),
    h3_reflexive("shader_properties", rmct_shader_propertie),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=68
    )


def get():
    return rmct_def

rmct_def = TagDef("rmct",
    h3_blam_header('rmct'),
    rmct_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rmct"], endian=">", tag_cls=H3Tag
    )