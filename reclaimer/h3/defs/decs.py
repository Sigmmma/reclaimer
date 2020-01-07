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


decs_decal_system_unknown_1 = Struct("unknown_1",
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


decs_decal_system_import_data_function = Struct("function",
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


decs_decal_system_import_data = Struct("import_data",
    h3_string_id("material_type"),
    SInt32("unknown_0", VISIBLE=False),
    h3_dependency("bitmap"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_reflexive("functions", decs_decal_system_import_data_function),
    ENDIAN=">", SIZE=60
    )


decs_decal_system_shader_propertie_shader_map = Struct("shader_map",
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


decs_decal_system_shader_propertie_argument = Struct("argument",
    Array("arg_array", SUB_STRUCT=Float("arg"), SIZE=4),
    ENDIAN=">", SIZE=16
    )


decs_decal_system_shader_propertie_unknown_0 = Struct("unknown_0",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


decs_decal_system_shader_propertie_unknown_2 = Struct("unknown_2",
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


decs_decal_system_shader_propertie_unknown_3 = Struct("unknown_3",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=6
    )


decs_decal_system_shader_propertie_unknown_4 = Struct("unknown_4",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


decs_decal_system_shader_propertie_function = Struct("function",
    SInt32("unknown_0", VISIBLE=False),
    h3_string_id("name"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


decs_decal_system_shader_propertie = Struct("shader_propertie",
    h3_dependency("template"),
    h3_reflexive("shader_maps", decs_decal_system_shader_propertie_shader_map),
    h3_reflexive("arguments", decs_decal_system_shader_propertie_argument),
    h3_reflexive("unknown_0", decs_decal_system_shader_propertie_unknown_0),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_2", decs_decal_system_shader_propertie_unknown_2),
    h3_reflexive("unknown_3", decs_decal_system_shader_propertie_unknown_3),
    h3_reflexive("unknown_4", decs_decal_system_shader_propertie_unknown_4),
    h3_reflexive("functions", decs_decal_system_shader_propertie_function),
    SInt32("unknown_5", VISIBLE=False),
    SInt32("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


decs_decal_system = Struct("decal_system",
    h3_string_id("name"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_dependency("base_render_method"),
    h3_reflexive("unknown_1", decs_decal_system_unknown_1),
    h3_reflexive("import_data", decs_decal_system_import_data),
    h3_reflexive("shader_properties", decs_decal_system_shader_propertie),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("unknown_3", VISIBLE=False),
    BytesRaw("unknown_4", SIZE=44, VISIBLE=False),
    ENDIAN=">", SIZE=116
    )


decs_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    Float("radius"),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_reflexive("decal_system", decs_decal_system),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


def get():
    return decs_def

decs_def = TagDef("decs",
    h3_blam_header('decs'),
    decs_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["decs"], endian=">", tag_cls=H3Tag
    )
