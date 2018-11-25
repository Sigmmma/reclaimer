from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

sLdT_lightmap_meshe_index_buffer_type = (
    "point_list",
    "line_list",
    "line_strip",
    "triange_list",
    "triange_fan",
    "triange_strip",
    )

sLdT_lightmap_meshe_prt_type = (
    "none",
    "ambient",
    "linear",
    "quadratic",
    )

sLdT_lightmap_meshe_vertex_type = (
    "world",
    "rigid",
    "skinned",
    "particle_model",
    "flat_world",
    "flat_rigid",
    "flat_skinned",
    "screen",
    "debug",
    "transparent",
    "particle",
    "contrail",
    "light_volume",
    "chud_simple",
    "chud_fancy",
    "decorator",
    "tiny_position",
    "patchy_fog",
    "water",
    "ripple",
    "implicit",
    "beam",
    )


sLdT_lightmap_instanced_meshe = Struct("instanced_meshes",
    Pad(12),
    SInt32("unknown_index"),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


sLdT_lightmap_instanced_geometry = Struct("instanced_geometry",
    SInt16("unknown"),
    SInt16("instanced_mesh_index"),
    SInt16("unknown_b_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


sLdT_lightmap_unknown_b = Struct("unknown_b",
    Pad(72),
    ENDIAN=">", SIZE=72
    )


sLdT_lightmap_meshe_part = Struct("parts",
    SInt16("material_index"),
    SInt16("unknown_nodey_index"),
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("subpart_index"),
    SInt16("subpart_count"),
    SInt8("unknown_enum"),
    Bool8("flags",
        ("water", 1 << 3),
        ),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap_meshe_subpart = Struct("subparts",
    SInt16("index_buffer_start"),
    SInt16("index_buffer_count"),
    SInt16("part_index"),
    SInt16("vertex_count"),
    ENDIAN=">", SIZE=8
    )


sLdT_lightmap_meshe_instanced_geometry_indice_instanced_geometry_mesh_content = Struct("instanced_geometry_mesh_contents",
    SInt16("instanced_geometry_index"),
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_meshe_instanced_geometry_indice = Struct("instanced_geometry_indices",
    SInt16("instanced_geometry_mesh_index_1"),
    SInt16("instanced_geometry_mesh_index_2"),
    reflexive("instanced_geometry_mesh_contents", sLdT_lightmap_meshe_instanced_geometry_indice_instanced_geometry_mesh_content),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap_meshe_unknown_water = Struct("unknown_water",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_meshe = Struct("meshes",
    reflexive("parts", sLdT_lightmap_meshe_part),
    reflexive("subparts", sLdT_lightmap_meshe_subpart),
    SInt16("vertex_buffer_index_1"),
    SInt16("vertex_buffer_index_2"),
    SInt16("vertex_buffer_index_3"),
    SInt16("vertex_buffer_index_4"),
    SInt16("vertex_buffer_index_5"),
    SInt16("vertex_buffer_index_6"),
    SInt16("vertex_buffer_index_7"),
    SInt16("vertex_buffer_index_8"),
    SInt16("index_buffer_index_1"),
    SInt16("index_buffer_index_2"),
    Bool8("flags",
        "has_vertex_colors",
        ),
    SInt8("rigid_node"),
    SEnum8("vertex_type", *sLdT_lightmap_meshe_vertex_type),
    SEnum8("prt_type", *sLdT_lightmap_meshe_prt_type),
    SEnum8("index_buffer_type", *sLdT_lightmap_meshe_index_buffer_type),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    reflexive("instanced_geometry_indices", sLdT_lightmap_meshe_instanced_geometry_indice),
    reflexive("unknown_water", sLdT_lightmap_meshe_unknown_water),
    ENDIAN=">", SIZE=76
    )


sLdT_lightmap_compression_info = Struct("compression_info",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("position_bounds_x_min"),
    Float("position_bounds_x_max"),
    Float("position_bounds_y_min"),
    Float("position_bounds_y_max"),
    Float("position_bounds_z_min"),
    Float("position_bounds_z_max"),
    Float("texcoord_bounds_x_min"),
    Float("texcoord_bounds_x_max"),
    Float("texcoord_bounds_y_min"),
    Float("texcoord_bounds_y_max"),
    ENDIAN=">", SIZE=44
    )


sLdT_lightmap_unknown_nodey = Struct("unknown_nodey",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    SInt8("node_index"),
    SInt8("node_index_1"),
    SInt8("node_index_2"),
    SInt8("node_index_3"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    ENDIAN=">", SIZE=48
    )


sLdT_lightmap_unknown_3 = Struct("unknown_3",
    SInt16("unknown"),
    SInt16("unknown_1"),
    rawdata_ref("unknown_2"),
    ENDIAN=">", SIZE=24
    )


sLdT_lightmap_unknown_meshe_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


sLdT_lightmap_unknown_meshe = Struct("unknown_meshes",
    rawdata_ref("unknown"),
    reflexive("unknown_1", sLdT_lightmap_unknown_meshe_unknown_1),
    ENDIAN=">", SIZE=32
    )


sLdT_lightmap_node_map_unknown = Struct("unknown",
    UInt8("node_index"),
    ENDIAN=">", SIZE=1
    )


sLdT_lightmap_node_map = Struct("node_maps",
    reflexive("unknown", sLdT_lightmap_node_map_unknown),
    ENDIAN=">", SIZE=12
    )


sLdT_lightmap_unknown_5_unknown = Struct("unknown",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


sLdT_lightmap_unknown_5 = Struct("unknown_5",
    reflexive("unknown", sLdT_lightmap_unknown_5_unknown),
    ENDIAN=">", SIZE=12
    )


sLdT_lightmap_unknown_yo = Struct("unknown_yo",
    Pad(12),
    SInt16("unknown_index"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=16
    )


sLdT_lightmap = Struct("lightmap",
    SInt16("unknown"),
    SInt16("bsp_index"),
    SInt32("structure_checksum"),
    Pad(216),
    dependency("primary_map"),
    dependency("intensity_map"),
    reflexive("instanced_meshes", sLdT_lightmap_instanced_meshe),
    reflexive("unknown_1", sLdT_lightmap_unknown_1),
    reflexive("instanced_geometry", sLdT_lightmap_instanced_geometry),
    reflexive("unknown_b", sLdT_lightmap_unknown_b),
    SInt32("unknown_2"),
    reflexive("meshes", sLdT_lightmap_meshe),
    reflexive("compression_info", sLdT_lightmap_compression_info),
    reflexive("unknown_nodey", sLdT_lightmap_unknown_nodey),
    reflexive("unknown_3", sLdT_lightmap_unknown_3),
    Pad(12),
    reflexive("unknown_meshes", sLdT_lightmap_unknown_meshe),
    reflexive("node_maps", sLdT_lightmap_node_map),
    reflexive("unknown_5", sLdT_lightmap_unknown_5),
    Pad(12),
    reflexive("unknown_yo", sLdT_lightmap_unknown_yo),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding"),
    ENDIAN=">", SIZE=436
    )


sLdT_airprobe = Struct("airprobes",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    string_id_meta("unknown_3"),
    Bool16("unknown_4",
        ),
    SInt16("unknown_5"),
    Pad(72),
    ENDIAN=">", SIZE=92
    )


sLdT_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    Pad(72),
    ENDIAN=">", SIZE=80
    )


sLdT_unknown_3_unknown_1 = Struct("unknown_1",
    Pad(84),
    ENDIAN=">", SIZE=84
    )


sLdT_unknown_3 = Struct("unknown_3",
    Pad(32),
    reflexive("unknown_1", sLdT_unknown_3_unknown_1),
    ENDIAN=">", SIZE=44
    )


sLdT_meta_def = BlockDef("sLdT",
    Pad(4),
    reflexive("lightmap", sLdT_lightmap),
    Pad(24),
    reflexive("airprobes", sLdT_airprobe),
    reflexive("unknown_2", sLdT_unknown_2),
    reflexive("unknown_3", sLdT_unknown_3),
    Pad(12),
    TYPE=Struct, ENDIAN=">", SIZE=88
    )