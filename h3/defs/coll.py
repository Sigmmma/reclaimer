from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


coll_material = Struct("materials",
    string_id_meta("name"),
    ENDIAN=">", SIZE=4
    )


coll_region_permutation_bsp_bsp_3d_node = Struct("bsp_3d_nodes",
    UInt8("unknown"),
    SInt16("second_child"),
    UInt8("unknown_1"),
    SInt16("first_child"),
    SInt16("plane"),
    ENDIAN=">", SIZE=8
    )


coll_region_permutation_bsp_plane = Struct("planes",
    Float("plane_i"),
    Float("plane_j"),
    Float("plane_k"),
    Float("plane_d"),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp_leave = Struct("leaves",
    SInt16("flags"),
    SInt16("bsp_2d_reference_count"),
    SInt16("unknown"),
    SInt16("first_bsp_2d_reference"),
    ENDIAN=">", SIZE=8
    )


coll_region_permutation_bsp_bsp_2d_reference = Struct("bsp_2d_references",
    SInt16("plane"),
    SInt16("bsp_2d_node"),
    ENDIAN=">", SIZE=4
    )


coll_region_permutation_bsp_bsp_2d_node = Struct("bsp_2d_nodes",
    Float("plane_i"),
    Float("plane_j"),
    Float("plane_d"),
    SInt16("left_child"),
    SInt16("right_child"),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp_surface = Struct("surfaces",
    SInt16("plane"),
    SInt16("first_edge"),
    SInt16("material"),
    SInt16("unknown"),
    SInt16("breakable_surface"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=12
    )


coll_region_permutation_bsp_edge = Struct("edges",
    SInt16("start_vertex"),
    SInt16("end_vertex"),
    SInt16("forward_edge"),
    SInt16("reverse_edge"),
    SInt16("left_surface"),
    SInt16("right_surface"),
    ENDIAN=">", SIZE=12
    )


coll_region_permutation_bsp_vertice = Struct("vertices",
    Pad(12),
    SInt16("first_edge"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp = Struct("bsps",
    SInt16("node_index"),
    SInt16("unknown"),
    reflexive("bsp_3d_nodes", coll_region_permutation_bsp_bsp_3d_node),
    reflexive("planes", coll_region_permutation_bsp_plane),
    reflexive("leaves", coll_region_permutation_bsp_leave),
    reflexive("bsp_2d_references", coll_region_permutation_bsp_bsp_2d_reference),
    reflexive("bsp_2d_nodes", coll_region_permutation_bsp_bsp_2d_node),
    reflexive("surfaces", coll_region_permutation_bsp_surface),
    reflexive("edges", coll_region_permutation_bsp_edge),
    reflexive("vertices", coll_region_permutation_bsp_vertice),
    ENDIAN=">", SIZE=100
    )


coll_region_permutation_bsp_physic = Struct("bsp_physics",
    Pad(4),
    SInt16("size"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_1"),
    Pad(16),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Pad(4),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Pad(4),
    UInt32("model"),
    Pad(4),
    SInt16("unknown_12"),
    SInt16("unknown_13"),
    Pad(8),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_15"),
    SInt32("unknown_16"),
    Pad(12),
    ENDIAN=">", SIZE=112
    )


coll_region_permutation_bsp_mopp_code_data = Struct("data",
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


coll_region_permutation_bsp_mopp_code = Struct("bsp_mopp_codes",
    SInt32("size"),
    SInt32("size_1"),
    SInt32("offset"),
    Pad(4),
    Float("offset_x"),
    Float("offset_y"),
    Float("offset_z"),
    Float("offset_scale"),
    Pad(4),
    SInt32("data_size"),
    UInt32("data_capacity"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    SInt8("unknown_5"),
    reflexive("data", coll_region_permutation_bsp_mopp_code_data),
    Pad(4),
    ENDIAN=">", SIZE=64
    )


coll_region_permutation = Struct("permutations",
    string_id_meta("name"),
    reflexive("bsps", coll_region_permutation_bsp),
    reflexive("bsp_physics", coll_region_permutation_bsp_physic),
    reflexive("bsp_mopp_codes", coll_region_permutation_bsp_mopp_code),
    ENDIAN=">", SIZE=40
    )


coll_region = Struct("regions",
    string_id_meta("name"),
    reflexive("permutations", coll_region_permutation),
    ENDIAN=">", SIZE=16
    )


coll_pathfinding_sphere = Struct("pathfinding_spheres",
    SInt16("node"),
    Bool16("flags",
        "remains_when_open",
        "vehicle_only",
        "with_sectors",
        ),
    Float("center_x"),
    Float("center_y"),
    Float("center_z"),
    Float("radius"),
    ENDIAN=">", SIZE=20
    )


coll_node = Struct("nodes",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("parent_node"),
    SInt16("next_sibling_node"),
    SInt16("first_child_node"),
    ENDIAN=">", SIZE=12
    )


coll_meta_def = BlockDef("coll",
    SInt32("collision_model_checksum"),
    Pad(12),
    Bool32("flags",
        "contains_open_edges",
        ),
    reflexive("materials", coll_material),
    reflexive("regions", coll_region),
    reflexive("pathfinding_spheres", coll_pathfinding_sphere),
    reflexive("nodes", coll_node),
    TYPE=Struct, ENDIAN=">", SIZE=68
    )