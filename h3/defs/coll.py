############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DarkShallFall
# 	Mapped out and named reflexives and values
# revision: 3		author: Lord Zedd
# 	Updates.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


coll_material = Struct("material", 
    h3_string_id("name"),
    ENDIAN=">", SIZE=4
    )


coll_region_permutation_bsp_bsp_3d_node = Struct("bsp_3d_node", 
    UInt8("unknown_0", VISIBLE=False),
    SInt16("second_child"),
    UInt8("unknown_1", VISIBLE=False),
    SInt16("first_child"),
    SInt16("plane"),
    ENDIAN=">", SIZE=8
    )


coll_region_permutation_bsp_plane = Struct("plane", 
    QStruct("plane", INCLUDE=ijk_float),
    Float("plane_d"),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp_leave = Struct("leave", 
    SInt16("flags"),
    SInt16("bsp_2d_reference_count"),
    SInt16("unknown", VISIBLE=False),
    SInt16("first_bsp_2d_reference"),
    ENDIAN=">", SIZE=8
    )


coll_region_permutation_bsp_bsp_2d_reference = Struct("bsp_2d_reference", 
    SInt16("plane"),
    SInt16("bsp_2d_node"),
    ENDIAN=">", SIZE=4
    )


coll_region_permutation_bsp_bsp_2d_node = Struct("bsp_2d_node", 
    QStruct("plane", INCLUDE=ij_float),
    Float("plane_d"),
    SInt16("left_child"),
    SInt16("right_child"),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp_surface = Struct("surface", 
    SInt16("plane"),
    SInt16("first_edge"),
    SInt16("material"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("breakable_surface"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=12
    )


coll_region_permutation_bsp_edge = Struct("edge", 
    SInt16("start_vertex"),
    SInt16("end_vertex"),
    SInt16("forward_edge"),
    SInt16("reverse_edge"),
    SInt16("left_surface"),
    SInt16("right_surface"),
    ENDIAN=">", SIZE=12
    )


coll_region_permutation_bsp_vertice = Struct("vertice", 
    Pad(12),
    SInt16("first_edge"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


coll_region_permutation_bsp = Struct("bsp", 
    SInt16("node_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("bsp_3d_nodes", coll_region_permutation_bsp_bsp_3d_node),
    h3_reflexive("planes", coll_region_permutation_bsp_plane),
    h3_reflexive("leaves", coll_region_permutation_bsp_leave),
    h3_reflexive("bsp_2d_references", coll_region_permutation_bsp_bsp_2d_reference),
    h3_reflexive("bsp_2d_nodes", coll_region_permutation_bsp_bsp_2d_node),
    h3_reflexive("surfaces", coll_region_permutation_bsp_surface),
    h3_reflexive("edges", coll_region_permutation_bsp_edge),
    h3_reflexive("vertices", coll_region_permutation_bsp_vertice),
    ENDIAN=">", SIZE=100
    )


coll_region_permutation_bsp_physic = Struct("bsp_physic", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=16, VISIBLE=False),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    BytesRaw("unknown_6", SIZE=4, VISIBLE=False),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    BytesRaw("unknown_10", SIZE=4, VISIBLE=False),
    dependency_uint32("model", VISIBLE=False),
    BytesRaw("unknown_11", SIZE=4, VISIBLE=False),
    SInt16("unknown_12", VISIBLE=False),
    SInt16("unknown_13", VISIBLE=False),
    BytesRaw("unknown_14", SIZE=8, VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_15", VISIBLE=False),
    SInt32("unknown_16", VISIBLE=False),
    BytesRaw("unknown_17", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=112
    )


coll_region_permutation_bsp_mopp_code_data = Struct("data", 
    UInt8("data_byte"),
    ENDIAN=">", SIZE=1
    )


coll_region_permutation_bsp_mopp_code = Struct("bsp_mopp_code", 
    SInt32("size_0"),
    SInt32("size_1"),
    SInt32("offset_0"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    QStruct("offset_1", INCLUDE=xyz_float),
    Float("offset_scale"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt32("data_size"),
    UInt32("data_capacity"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("data", coll_region_permutation_bsp_mopp_code_data),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


coll_region_permutation = Struct("permutation", 
    h3_string_id("name"),
    h3_reflexive("bsps", coll_region_permutation_bsp),
    h3_reflexive("bsp_physics", coll_region_permutation_bsp_physic),
    h3_reflexive("bsp_mopp_codes", coll_region_permutation_bsp_mopp_code),
    ENDIAN=">", SIZE=40
    )


coll_region = Struct("region", 
    h3_string_id("name"),
    h3_reflexive("permutations", coll_region_permutation),
    ENDIAN=">", SIZE=16
    )


coll_pathfinding_sphere = Struct("pathfinding_sphere", 
    SInt16("node"),
    Bool16("flags", 
        "remains_when_open",
        "vehicle_only",
        "with_sectors",
        ),
    QStruct("center", INCLUDE=xyz_float),
    Float("radius"),
    ENDIAN=">", SIZE=20
    )


coll_node = Struct("node", 
    h3_string_id("name"),
    SInt16("unknown"),
    SInt16("parent_node"),
    SInt16("next_sibling_node"),
    SInt16("first_child_node"),
    ENDIAN=">", SIZE=12
    )


coll_body = Struct("tagdata", 
    SInt32("collision_model_checksum"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    Bool32("flags", 
        "contains_open_edges",
        ),
    h3_reflexive("materials", coll_material),
    h3_reflexive("regions", coll_region),
    h3_reflexive("pathfinding_spheres", coll_pathfinding_sphere),
    h3_reflexive("nodes", coll_node),
    ENDIAN=">", SIZE=68
    )


def get():
    return coll_def

coll_def = TagDef("coll",
    h3_blam_header('coll'),
    coll_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["coll"], endian=">", tag_cls=H3Tag
    )