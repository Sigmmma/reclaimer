from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


sddt_design_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sddt_design_mopp_code = Struct("design_mopp_codes",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    reflexive("data", sddt_design_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


sddt_design_shapes_2_unknown_2 = Struct("unknown_2",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Float("unknown_15"),
    Float("unknown_16"),
    ENDIAN=">", SIZE=68
    )


sddt_design_shapes_2 = Struct("design_shapes_2",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    reflexive("unknown_2", sddt_design_shapes_2_unknown_2),
    ENDIAN=">", SIZE=20
    )


sddt_water_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


sddt_water_mopp_code = Struct("water_mopp_codes",
    SInt32("unknown"),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    reflexive("data", sddt_water_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


sddt_water_name = Struct("water_names",
    string_id_meta("name"),
    ENDIAN=">", SIZE=4
    )


sddt_underwater_definition_unknown_1 = Struct("unknown_1",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    ENDIAN=">", SIZE=16
    )


sddt_underwater_definition_triangle = Struct("triangles",
    Pad(36),
    ENDIAN=">", SIZE=36
    )


sddt_underwater_definition = Struct("underwater_definitions",
    SInt16("water_name_index"),
    SInt16("unknown"),
    Float("flow_force_x"),
    Float("flow_force_y"),
    Float("flow_force_z"),
    Float("flow_force_z_2"),
    reflexive("unknown_1", sddt_underwater_definition_unknown_1),
    reflexive("triangles", sddt_underwater_definition_triangle),
    ENDIAN=">", SIZE=44
    )


sddt_meta_def = BlockDef("sddt",
    SInt32("unknown"),
    reflexive("design_mopp_codes", sddt_design_mopp_code),
    reflexive("design_shapes_2", sddt_design_shapes_2),
    reflexive("water_mopp_codes", sddt_water_mopp_code),
    reflexive("water_names", sddt_water_name),
    reflexive("underwater_definitions", sddt_underwater_definition),
    TYPE=Struct, ENDIAN=">", SIZE=64
    )