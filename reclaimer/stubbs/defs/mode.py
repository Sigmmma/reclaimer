#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.mode import *
from ..common_descs import *

def get():
    return mode_def

# my guess at what the struct might be like
unknown_struct = Struct("unknown",
    ascii_str32("name"),
    LFloat('unknown1', ENDIAN='<', DEFAULT=1.0),
    LFloat('unknown2', ENDIAN='<', DEFAULT=1.0),
    BytesRaw("unknown_data", SIZE=64-32-4*2),
    SIZE=64
    )

#unknown_struct = Struct("unknown",
#    BytesRaw("unknown_data", SIZE=64),
#    SIZE=64
#    )

pc_part = Struct('part',
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

    #reflexive("uncompressed_vertices", uncompressed_vertex_union, 65535),
    #reflexive("compressed_vertices", compressed_vertex_union, 65535),
    #reflexive("triangles", triangle_union, 65535),
    reflexive("uncompressed_vertices", fast_uncompressed_vertex, 65535),
    reflexive("compressed_vertices", fast_compressed_vertex, 65535),
    reflexive("triangles", triangle, 65535),

    #Pad(36),
    Struct("model_meta_info",
        # the offset fields in model_meta_info struct are the only
        # thing different from halo model tags. if they weren't,
        # this whole new part definition wouldn't be necessary.
        UEnum16("index_type",  # name is a guess.  always 1?
            ("uncompressed", 1),
            ),
        Pad(2),
        UInt32("index_count"),
        # THESE VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("indices_magic_offset"),
        UInt32("indices_offset"),

        UEnum16("vertex_type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        Pad(2),
        UInt32("vertex_count"),
        Pad(4),  # always 0?
        # THESE VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("vertices_magic_offset"),
        UInt32("vertices_offset"),
        VISIBLE=False, SIZE=36
        ),

    SIZE=104
    )

fast_part = dict(part)
fast_part[9]  = raw_reflexive("uncompressed_vertices", fast_uncompressed_vertex)
fast_part[10] = raw_reflexive("compressed_vertices", fast_compressed_vertex)
fast_part[11] = raw_reflexive("triangles", triangle)

pc_geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", pc_part, 32),
    SIZE=48
    )

fast_geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", fast_part, 32),
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

    SInt16('superhigh_lod_nodes', SIDETIP="nodes"),
    SInt16('high_lod_nodes', SIDETIP="nodes"),
    SInt16('medium_lod_nodes', SIDETIP="nodes"),
    SInt16('low_lod_nodes', SIDETIP="nodes"),
    SInt16('superlow_lod_nodes', SIDETIP="nodes"),

    Pad(10),

    Float('base_map_u_scale'),
    Float('base_map_v_scale'),

    Pad(104),
    reflexive("unknown", unknown_struct, DYN_NAME_PATH=".name"),

    reflexive("markers", marker, 256, DYN_NAME_PATH=".name"),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath"),

    SIZE=232
    )

pc_mode_body = dict(mode_body)
pc_mode_body[20] = reflexive("geometries", pc_geometry, 256)

fast_mode_body = dict(mode_body)
fast_mode_body[20] = reflexive("geometries", fast_geometry, 256)

mode_def = TagDef("mode",
    blam_header_stubbs('mode', 6),  # increment to differentiate it from mode and mod2
    mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )

fast_mode_def = TagDef("mode",
    blam_header_stubbs('mode', 6),  # increment to differentiate it from mode and mod2
    fast_mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )

pc_mode_def = TagDef("mode",
    blam_header_stubbs('mode', 6),  # increment to differentiate it from mode and mod2
    pc_mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )
