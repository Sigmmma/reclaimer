############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Labelled raw identifier
# revision: 3		author: Lord Zedd
# 	Standardized model data and updated
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


pmdf_meshe_part = Struct("part", 
    SInt16("material_index"),
    SInt16("unknown_nodey_index", VISIBLE=False),
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("subpart_index"),
    SInt16("subpart_count"),
    SInt8("unknown_enum", VISIBLE=False),
    Bool8("flags", 
        ("water", 1 << 3),
        ),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=16
    )


pmdf_meshe_subpart = Struct("subpart", 
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


pmdf_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_content", 
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


pmdf_meshe_instanced_geometry_indice = Struct("instanced_geometry_indice", 
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    h3_reflexive("instanced_geometry_mesh_contents", pmdf_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


pmdf_meshe_unknown_water = Struct("unknown_water", 
    SInt16("unknown"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


pmdf_meshe = Struct("meshe", 
    h3_reflexive("parts", pmdf_meshe_part),
    h3_reflexive("subparts", pmdf_meshe_subpart),
    Array("vertex_buffer_index_array", SUB_STRUCT=SInt16("vertex_buffer_index"), SIZE=8),
    SInt16("index_buffer_index_1"),
    SInt16("index_buffer_index_2"),
    Bool8("flags", 
        "has_vertex_colors",
        ),
    SInt8("rigid_node"),
    SEnum8("vertex_type", *pmdf_meshe_vertex_type),
    SEnum8("prt_type", *pmdf_meshe_prt_type),
    SEnum8("index_buffer_type", *pmdf_meshe_index_buffer_type),
    SInt8("unknown_0", VISIBLE=False),
    SInt8("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    h3_reflexive("instanced_geometry_indices", pmdf_meshe_instanced_geometry_indice),
    h3_reflexive("unknown_water", pmdf_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


pmdf_compression_info = Struct("compression_info", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    QStruct("position_bounds_x", INCLUDE=from_to),
    QStruct("position_bounds_y", INCLUDE=from_to),
    QStruct("position_bounds_z", INCLUDE=from_to),
    QStruct("texcoord_bounds_x", INCLUDE=from_to),
    QStruct("texcoord_bounds_y", INCLUDE=from_to),
    ENDIAN=">", SIZE=44
    )


pmdf_unknown_nodey = Struct("unknown_nodey", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Array("node_index_array", SUB_STRUCT=SInt8("node_index"), SIZE=4, VISIBLE=False),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


pmdf_unknown_1 = Struct("unknown_1", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_rawdata_ref("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


pmdf_unknown_meshe_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


pmdf_unknown_meshe = Struct("unknown_meshe", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", pmdf_unknown_meshe_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


pmdf_node_map_unknown = Struct("unknown", 
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


pmdf_node_map = Struct("node_map", 
    h3_reflexive("unknown", pmdf_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


pmdf_unknown_3_unknown = Struct("unknown", 
    BytesRaw("unknown", SIZE=48, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


pmdf_unknown_3 = Struct("unknown_3", 
    h3_reflexive("unknown", pmdf_unknown_3_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


pmdf_unknown_yo = Struct("unknown_yo", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_index"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


pmdf_unknown_5 = Struct("unknown_5", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


pmdf_body = Struct("tagdata", 
    SInt32("unknown_0", VISIBLE=False),
    h3_reflexive("meshes", pmdf_meshe),
    h3_reflexive("compression_info", pmdf_compression_info),
    h3_reflexive("unknown_nodey", pmdf_unknown_nodey),
    h3_reflexive("unknown_1", pmdf_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_meshes", pmdf_unknown_meshe),
    h3_reflexive("node_maps", pmdf_node_map),
    h3_reflexive("unknown_3", pmdf_unknown_3),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_yo", pmdf_unknown_yo),
    zone_asset("asset_data"),
    h3_reflexive("unknown_5", pmdf_unknown_5),
    ENDIAN=">", SIZE=144
    )


def get():
    return pmdf_def

pmdf_def = TagDef("pmdf",
    h3_blam_header('pmdf'),
    pmdf_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["pmdf"], endian=">", tag_cls=H3Tag
    )
