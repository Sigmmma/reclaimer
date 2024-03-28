#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .mod2 import *
from .objs.mode import ModeTag
from supyr_struct.util import desc_variant

def get():
    return mode_def

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

    reflexive("local_markers", local_marker, 32, DYN_NAME_PATH=".name", EXT_MAX=SINT16_MAX),
    SIZE=88
    )

# dip == double-indirect pointer
dip_model_meta_info = Struct("model_meta_info",
    UEnum16("index_type", *H1_TRIANGLE_BUFFER_TYPES),
    Pad(2),
    UInt32("index_count"),
    UInt32("indices_offset"),
    UInt32("indices_reflexive_offset"),

    UEnum16("vertex_type",  *H1_VERTEX_BUFFER_TYPES),
    Pad(2),
    UInt32("vertex_count"),
    Pad(4),  # always 0?
    UInt32("vertices_offset"),
    UInt32("vertices_reflexive_offset"),
    VISIBLE=False, SIZE=36
    )

part = Struct('part',
    Bool32('flags',
        'stripped',
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

    #reflexive("uncompressed_vertices", uncompressed_vertex_union, SINT16_MAX),
    #reflexive("compressed_vertices", compressed_vertex_union, SINT16_MAX),
    #reflexive("triangles", triangle_union, SINT16_MAX),
    reflexive("uncompressed_vertices", fast_uncompressed_vertex, SINT16_MAX),
    reflexive("compressed_vertices", fast_compressed_vertex, SINT16_MAX),
    reflexive("triangles", triangle, SINT16_MAX),

    #Pad(36),
    dip_model_meta_info,

    SIZE=104
    )

fast_part = desc_variant(part,
    raw_reflexive("uncompressed_vertices", fast_uncompressed_vertex, SINT16_MAX),
    raw_reflexive("compressed_vertices", fast_compressed_vertex, SINT16_MAX),
    raw_reflexive("triangles", triangle, SINT16_MAX),
    )

region = Struct('region',
    ascii_str32("name"),
    Pad(32),
    reflexive("permutations", permutation, 32, DYN_NAME_PATH=".name", EXT_MAX=UINT8_MAX),
    SIZE=76
    )

geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", part, 32, EXT_MAX=SINT16_MAX),
    SIZE=48
    )

fast_geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", fast_part, 32, EXT_MAX=SINT16_MAX),
    SIZE=48
    )

mode_body = Struct('tagdata',
    Bool32('flags',
        'blend_shared_normals',
        ),
    SInt32('node_list_checksum'),

    Float('superhigh_lod_cutoff', SIDETIP="pixels"),
    Float('high_lod_cutoff', SIDETIP="pixels"),
    Float('medium_lod_cutoff', SIDETIP="pixels"),
    Float('low_lod_cutoff', SIDETIP="pixels"),
    Float('superlow_lod_cutoff', SIDETIP="pixels"),

    SInt16('superlow_lod_nodes', SIDETIP="nodes", VISIBLE=False),
    SInt16('low_lod_nodes', SIDETIP="nodes", VISIBLE=False),
    SInt16('medium_lod_nodes', SIDETIP="nodes", VISIBLE=False),
    SInt16('high_lod_nodes', SIDETIP="nodes", VISIBLE=False),
    SInt16('superhigh_lod_nodes', SIDETIP="nodes", VISIBLE=False),

    Pad(10),

    Float('base_map_u_scale'),
    Float('base_map_v_scale'),

    Pad(104),
    Pad(12), # replaced with unknown reflexive in stubbs

    # NOTE: the extended max for nodes and regions can't be set higher due
    #       to data structure limits. there is an object struct used at
    #       runtime that only has enough room to reference 8 regions. for
    #       nodes, there is only enough room in each animation to flag 64
    #       nodes as animated. theoretically you could add another 32 if
    #       if used neighboring padding, but this is untested, and a strech.
    reflexive("markers", marker, 256, DYN_NAME_PATH=".name", VISIBLE=False),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256, EXT_MAX=SINT16_MAX),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath", EXT_MAX=SINT16_MAX),

    SIZE=232
    )

fast_mode_body = desc_variant(mode_body,
    reflexive("geometries", fast_geometry, 256, EXT_MAX=SINT16_MAX),
    )

mode_def = TagDef("mode",
    blam_header('mode', 4),
    mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )

fast_mode_def = TagDef("mode",
    blam_header('mode', 4),
    fast_mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )
