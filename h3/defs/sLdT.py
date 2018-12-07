############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Labelled Raw Identifier
# revision: 3		author: Lord Zedd
# 	Standardized model data and updated
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


sLdT_lightmap_instanced_meshe = Struct("instanced_meshe", 
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    SInt32("unknown_index"),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap_unknown_1 = Struct("unknown_1", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


sLdT_lightmap_instanced_geometry = Struct("instanced_geometry", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("instanced_mesh_index"),
    SInt16("unknown_b_index", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


sLdT_lightmap_unknown_b = Struct("unknown_b", 
    BytesRaw("unknown", SIZE=72, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=72
    )


sLdT_lightmap_meshe_part = Struct("part", 
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


sLdT_lightmap_meshe_subpart = Struct("subpart", 
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sLdT_lightmap_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_content", 
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_meshe_instanced_geometry_indice = Struct("instanced_geometry_indice", 
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    h3_reflexive("instanced_geometry_mesh_contents", sLdT_lightmap_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap_meshe_unknown_water = Struct("unknown_water", 
    SInt16("unknown"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_meshe = Struct("meshe", 
    h3_reflexive("parts", sLdT_lightmap_meshe_part),
    h3_reflexive("subparts", sLdT_lightmap_meshe_subpart),
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
    h3_reflexive("instanced_geometry_indices", sLdT_lightmap_meshe_instanced_geometry_indice),
    h3_reflexive("unknown_water", sLdT_lightmap_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


sLdT_lightmap_compression_info = Struct("compression_info", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    QStruct("position_bounds_x", INCLUDE=from_to),
    QStruct("position_bounds_y", INCLUDE=from_to),
    QStruct("position_bounds_z", INCLUDE=from_to),
    QStruct("texcoord_bounds_x", INCLUDE=from_to),
    QStruct("texcoord_bounds_y", INCLUDE=from_to),
    ENDIAN=">", SIZE=44
    )


sLdT_lightmap_unknown_nodey = Struct("unknown_nodey", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Array("node_index_array", SUB_STRUCT=SInt8("node_index"), SIZE=4, VISIBLE=False),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sLdT_lightmap_unknown_3 = Struct("unknown_3", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_rawdata_ref("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


sLdT_lightmap_unknown_meshe_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_unknown_meshe = Struct("unknown_meshe", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", sLdT_lightmap_unknown_meshe_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


sLdT_lightmap_node_map_unknown = Struct("unknown", 
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sLdT_lightmap_node_map = Struct("node_map", 
    h3_reflexive("unknown", sLdT_lightmap_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


sLdT_lightmap_unknown_5_unknown = Struct("unknown", 
    BytesRaw("unknown", SIZE=48, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


sLdT_lightmap_unknown_5 = Struct("unknown_5", 
    h3_reflexive("unknown", sLdT_lightmap_unknown_5_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


sLdT_lightmap_unknown_yo = Struct("unknown_yo", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_index"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap = Struct("lightmap", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("bsp_index"),
    SInt32("structure_checksum"),
    Pad(216),
    h3_dependency("primary_map"),
    h3_dependency("intensity_map"),
    h3_reflexive("instanced_meshes", sLdT_lightmap_instanced_meshe),
    h3_reflexive("unknown_1", sLdT_lightmap_unknown_1),
    h3_reflexive("instanced_geometry", sLdT_lightmap_instanced_geometry),
    h3_reflexive("unknown_b", sLdT_lightmap_unknown_b),
    SInt32("unknown_2", VISIBLE=False),
    h3_reflexive("meshes", sLdT_lightmap_meshe),
    h3_reflexive("compression_info", sLdT_lightmap_compression_info),
    h3_reflexive("unknown_nodey", sLdT_lightmap_unknown_nodey),
    h3_reflexive("unknown_3", sLdT_lightmap_unknown_3),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_meshes", sLdT_lightmap_unknown_meshe),
    h3_reflexive("node_maps", sLdT_lightmap_node_map),
    h3_reflexive("unknown_5", sLdT_lightmap_unknown_5),
    BytesRaw("unknown_6", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_yo", sLdT_lightmap_unknown_yo),
    zone_asset("asset_data"),
    ENDIAN=">", SIZE=436
    )


sLdT_airprobe = Struct("airprobe", 
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    h3_string_id("unknown_3", VISIBLE=False),
    Bool16("unknown_4", *unknown_flags_16),
    SInt16("unknown_5", VISIBLE=False),
    BytesRaw("unknown_6", SIZE=72, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=92
    )


sLdT_unknown_2 = Struct("unknown_2", 
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown", SIZE=72, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=80
    )


sLdT_unknown_3_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=84, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=84
    )


sLdT_unknown_3 = Struct("unknown_3", 
    BytesRaw("unknown_0", SIZE=32, VISIBLE=False),
    h3_reflexive("unknown_1", sLdT_unknown_3_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=44
    )


sLdT_body = Struct("tagdata", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("lightmap", sLdT_lightmap),
    BytesRaw("unknown_1", SIZE=24, VISIBLE=False),
    h3_reflexive("airprobes", sLdT_airprobe),
    h3_reflexive("unknown_2", sLdT_unknown_2),
    h3_reflexive("unknown_3", sLdT_unknown_3),
    BytesRaw("unknown_4", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=88
    )


def get():
    return sLdT_def

sLdT_def = TagDef("sLdT",
    h3_blam_header('sLdT'),
    sLdT_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sLdT"], endian=">", tag_cls=H3Tag
    )
