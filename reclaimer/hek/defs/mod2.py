#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.mod2 import Mod2Tag
from supyr_struct.defs.tag_def import TagDef

def get():
    return mod2_def

local_marker = Struct('local_marker',
    ascii_str32("name"),
    dyn_senum16('node_index',
        DYN_NAME_PATH="tagdata.nodes.nodes_array[DYN_I].name"),
    Pad(2),

    QStruct('rotation', INCLUDE=ijkw_float),
    QStruct('translation', INCLUDE=xyz_float),
    SIZE=80
    )

fast_uncompressed_vertex = QStruct('uncompressed_vertex',
    Float('position_x'), Float('position_y'), Float('position_z'),
    Float('normal_i'),   Float('normal_j'),   Float('normal_k'),
    Float('binormal_i'), Float('binormal_j'), Float('binormal_k'),
    Float('tangent_i'),  Float('tangent_j'),  Float('tangent_k'),

    Float('u'), Float('v'),

    SInt16('node_0_index'), SInt16('node_1_index'),
    Float('node_0_weight'), Float('node_1_weight'),
    SIZE=68
    )

fast_compressed_vertex = QStruct('compressed_vertex',
    Float('position_x'), Float('position_y'), Float('position_z'),
    UInt32('normal'),
    UInt32('binormal'),
    UInt32('tangent'),

    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),

    SInt8('node_0_index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt8('node_1_index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt16('node_0_weight', UNIT_SCALE=1/32767, MIN=0, WIDGET_WIDTH=10),
    SIZE=32
    )

uncompressed_vertex = Struct('uncompressed_vertex',
    QStruct("position", INCLUDE=xyz_float),
    QStruct("normal", INCLUDE=ijk_float),
    QStruct("binormal", INCLUDE=ijk_float),
    QStruct("tangent", INCLUDE=ijk_float),

    Float('u'),
    Float('v'),

    SInt16('node_0_index',
        TOOLTIP="If local nodes are used, this is a local index"),
    SInt16('node_1_index',
        TOOLTIP="If local nodes are used, this is a local index"),
    Float('node_0_weight'),
    Float('node_1_weight'),
    SIZE=68
    )

compressed_vertex = Struct('compressed_vertex',
    QStruct("position", INCLUDE=xyz_float),

    BBitStruct('normal',   INCLUDE=compressed_normal_32, SIZE=4),
    BBitStruct('binormal', INCLUDE=compressed_normal_32, SIZE=4),
    BBitStruct('tangent',  INCLUDE=compressed_normal_32, SIZE=4),

    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),

    SInt8('node_0_index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt8('node_1_index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt16('node_0_weight', UNIT_SCALE=1/32767, MIN=0, WIDGET_WIDTH=10),
    SIZE=32
    )

triangle = QStruct('triangle',
    SInt16('v0_index'), SInt16('v1_index'), SInt16('v2_index'),
    SIZE=6, ORIENT='h'
    )

uncompressed_vertex_union = Union('uncompressed_vertex',
    CASES={'uncompressed_vertex': uncompressed_vertex},
    )

compressed_vertex_union = Union('compressed_vertex',
    CASES={'compressed_vertex': compressed_vertex},
    )

triangle_union = Union('triangle',
    CASES={'triangle': triangle},
    )


marker_instance = Struct('marker_instance',
    dyn_senum8('region_index',
        DYN_NAME_PATH="tagdata.regions.regions_array[DYN_I].name"),
    SInt8('permutation_index', MIN=-1),
    dyn_senum8('node_index',
        DYN_NAME_PATH="tagdata.nodes.nodes_array[DYN_I].name"),
    Pad(1),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    SIZE=32
    )

permutation = Struct('permutation',
    ascii_str32("name"),
    Bool32('flags',
        'cannot_be_chosen_randomly'
        ),
    # permutations ending with -XXX where XXX is a number will belong to
    # the permutation set XXX. Trailing non-numeric characters are ignored.
    # Example:
    #     head_marcus_cap-101asdf
    #     Will have its permutation_set be set to 101
    # For all parts of a permutation to be properly chosen across
    # all regions, they must share a permutation set number.
    # Anything not ending in -XXX will have this set to 0.
    FlUInt16("permutation_set", VISIBLE=False),  # meta only field
    Pad(26),

    dyn_senum16('superlow_geometry_block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('low_geometry_block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('medium_geometry_block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('high_geometry_block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('superhigh_geometry_block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    Pad(2),

    reflexive("local_markers", local_marker, 32, DYN_NAME_PATH=".name"),
    SIZE=88
    )

part = Struct('part',
    Bool32('flags',
        'stripped',
        'ZONER',
        ),
    dyn_senum16('shader_index',
        DYN_NAME_PATH="tagdata.shaders.shaders_array[DYN_I].shader.filepath"),
    SInt8('previous_part_index'),
    SInt8('next_part_index'),

    SInt16('centroid_primary_node'),
    SInt16('centroid_secondary_node'),
    Float('centroid_primary_weight'),
    Float('centroid_secondary_weight'),

    QStruct('centroid_translation', INCLUDE=xyz_float),

    #reflexive("uncompressed_vertices", uncompressed_vertex_union, 32767),
    #reflexive("compressed_vertices", compressed_vertex_union, 32767),
    #reflexive("triangles", triangle_union, 32767),
    reflexive("uncompressed_vertices", fast_uncompressed_vertex, 32767),
    reflexive("compressed_vertices", fast_compressed_vertex, 32767),
    reflexive("triangles", triangle, 32767),
    #Pad(36),
    Struct("model_meta_info",
        UEnum16("index_type",  # name is a guess.  always 1?
            ("uncompressed", 1),
            ),
        Pad(2),
        UInt32("index_count"),
        # THESE TWO VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("indices_magic_offset"),
        UInt32("indices_offset"),

        UEnum16("vertex_type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        Pad(2),
        UInt32("vertex_count"),
        Pad(4),  # always 0?
        # THESE TWO VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("vertices_magic_offset"),
        UInt32("vertices_offset"),
        VISIBLE=False, SIZE=36
        ),

    Pad(3),
    SInt8('local_node_count', MIN=0, MAX=22),
    #UInt8Array('local_nodes', SIZE=22),
    Array("local_nodes", SUB_STRUCT=UInt8("local_node_index"), SIZE=22),

    # this COULD be 2 more potential local nodes, but I've seen tool
    # split models when they reach 22 nodes, so im assuming 22 is the max
    Pad(2),
    SIZE=132
    )

fast_part = dict(part)
fast_part[9]  = raw_reflexive("uncompressed_vertices", fast_uncompressed_vertex, 65535)
fast_part[10] = raw_reflexive("compressed_vertices", fast_compressed_vertex, 65535)
fast_part[11] = raw_reflexive("triangles", triangle, 65535)

marker = Struct('marker',
    ascii_str32("name"),
    UInt16('magic_identifier'),
    Pad(18),

    reflexive("marker_instances", marker_instance, 32),
    SIZE=64
    )

node = Struct('node',
    ascii_str32("name"),
    dyn_senum16('next_sibling_node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('first_child_node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('parent_node', DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    Float('distance_from_parent'),
    Pad(32),

    # xbox specific values
    LFloat('scale', ENDIAN='<', DEFAULT=1.0, VISIBLE=False),
    QStruct("rot_jj_kk", GUI_NAME="[1-2j^2-2k^2]   2[ij+kw]   2[ik-jw]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct("rot_kk_ii", GUI_NAME="2[ij-kw]   [1-2k^2-2i^2]   2[jk+iw]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct("rot_ii_jj", GUI_NAME="2[ik+jw]   2[jk-iw]   [1-2i^2-2j^2]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct('translation_to_root',
        INCLUDE=xyz_float, ENDIAN='<', VISIBLE=False),
    SIZE=156,
    )

region = Struct('region',
    ascii_str32("name"),
    Pad(32),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH=".name"),
    SIZE=76
    )

geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", part, 32),
    SIZE=48
    )

fast_geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", fast_part, 32),
    SIZE=48
    )

shader = Struct('shader',
    dependency("shader", valid_shaders),
    SInt16('permutation_index'),
    SIZE=32,
    )


mod2_body = Struct('tagdata',
    Bool32('flags',
        'blend_shared_normals',
        'parts_have_local_nodes',
        'ignore_skinning'
        ),
    SInt32('node_list_checksum'),

    Float('superhigh_lod_cutoff', SIDETIP="pixels"),
    Float('high_lod_cutoff', SIDETIP="pixels"),
    Float('medium_lod_cutoff', SIDETIP="pixels"),
    Float('low_lod_cutoff', SIDETIP="pixels"),
    Float('superlow_lod_cutoff', SIDETIP="pixels"),

    SInt16('superlow_lod_nodes', SIDETIP="nodes"),
    SInt16('low_lod_nodes', SIDETIP="nodes"),
    SInt16('medium_lod_nodes', SIDETIP="nodes"),
    SInt16('high_lod_nodes', SIDETIP="nodes"),
    SInt16('superhigh_lod_nodes', SIDETIP="nodes"),

    Pad(10),

    Float('base_map_u_scale'),
    Float('base_map_v_scale'),

    Pad(116),

    reflexive("markers", marker, 256, DYN_NAME_PATH=".name"),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath"),

    SIZE=232
    )

fast_mod2_body = dict(mod2_body)
fast_mod2_body[19] = reflexive("geometries", fast_geometry, 256)

mod2_def = TagDef("mod2",
    blam_header('mod2', 5),
    mod2_body,

    ext=".gbxmodel", endian=">", tag_cls=Mod2Tag
    )

fast_mod2_def = TagDef("mod2",
    blam_header('mod2', 5),
    fast_mod2_body,

    ext=".gbxmodel", endian=">", tag_cls=Mod2Tag
    )
