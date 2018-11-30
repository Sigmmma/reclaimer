############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	Made soft barriers visable for easy access
# revision: 3		author: Lord Zedd
# 	ctrl c ctrl v
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


sddt_design_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sddt_design_mopp_code = Struct("design_mopp_code", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SIZE=4, SUB_STRUCT=SInt8("unknown"), VISIBLE=False),
    h3_reflexive("data", sddt_design_mopp_code_data),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


sddt_design_shapes_2_unknown_2 = Struct("unknown_2", 
    Array("unknown_array", SIZE=17, SUB_STRUCT=Float("unknown")),
    VISIBLE=False,
    ENDIAN=">", SIZE=68
    )


sddt_design_shapes_2 = Struct("design_shapes_2", 
    h3_string_id("name"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", sddt_design_shapes_2_unknown_2),
    ENDIAN=">", SIZE=20
    )


sddt_water_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sddt_water_mopp_code = Struct("water_mopp_code", 
    SInt32("unknown_0", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SIZE=4, SUB_STRUCT=SInt8("unknown"), VISIBLE=False),
    h3_reflexive("data", sddt_water_mopp_code_data),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


sddt_water_name = Struct("water_name", 
    h3_string_id("name"),
    ENDIAN=">", SIZE=4
    )


sddt_underwater_definition_unknown_1 = Struct("unknown_1", 
    Array("unknown_array", SIZE=4, SUB_STRUCT=Float("unknown")),
    ENDIAN=">", SIZE=16
    )


sddt_underwater_definition_triangle = Struct("triangle", 
    BytesRaw("_1_x", SIZE=36, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


sddt_underwater_definition = Struct("underwater_definition", 
    SInt16("water_name_index"),
    SInt16("unknown_0", VISIBLE=False),
    QStruct("flow_force", INCLUDE=xyz_float),
    Float("flow_force_z_2"),
    h3_reflexive("unknown_1", sddt_underwater_definition_unknown_1),
    h3_reflexive("triangles", sddt_underwater_definition_triangle),
    ENDIAN=">", SIZE=44
    )


sddt_meta_def = BlockDef("sddt", 
    SInt32("unknown", VISIBLE=False),
    h3_reflexive("design_mopp_codes", sddt_design_mopp_code),
    h3_reflexive("design_shapes_2", sddt_design_shapes_2),
    h3_reflexive("water_mopp_codes", sddt_water_mopp_code),
    h3_reflexive("water_names", sddt_water_name),
    h3_reflexive("underwater_definitions", sddt_underwater_definition),
    TYPE=Struct, ENDIAN=">", SIZE=64
    )