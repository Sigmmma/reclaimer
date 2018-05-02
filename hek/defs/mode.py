from .mod2 import *
from .objs.mode import ModeTag

def get():
    return mode_def

permutation = Struct('permutation',
    ascii_str32("name"),
    Bool32('flags',
        'cannot be chosen randomly'
        ),
    Pad(28),

    dyn_senum16('superlow geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('low geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('medium geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('high geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    dyn_senum16('superhigh geometry block',
        DYN_NAME_PATH="tagdata.geometries.geometries_array[DYN_I].NAME"),
    Pad(2),
    SIZE=88
    )

part = Struct('part',
    Bool32('flags',
        'stripped',
        'ZONER',
        ),
    dyn_senum16('shader index',
        DYN_NAME_PATH="tagdata.shaders.shaders_array[DYN_I].shader.filepath"),
    SInt8('previous part index'),
    SInt8('next part index'),

    SInt16('centroid primary node'),
    SInt16('centroid secondary node'),
    Float('centroid primary weight'),
    Float('centroid secondary weight'),

    QStruct('centroid translation', INCLUDE=xyz_float),

    #reflexive("uncompressed vertices", uncompressed_vertex_union, 65535),
    #reflexive("compressed vertices", compressed_vertex_union, 65535),
    #reflexive("triangles", triangle_union, 65535),
    reflexive("uncompressed vertices", fast_uncompressed_vertex, 65535),
    reflexive("compressed vertices", fast_compressed_vertex, 65535),
    reflexive("triangles", triangle, 65535),

    #Pad(36),
    Struct("model meta info",
        UEnum32("index type",  # name is a guess.  always 1?
            ("uncompressed", 1),
            ),
        UInt32("index count"),
        UInt32("indices offset"),
        UInt32("indices reflexive offset"),

        UEnum32("vertex type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        UInt32("vertex count"),
        Pad(4),  # always 0?
        UInt32("vertices offset"),
        UInt32("vertices reflexive offset"),
        VISIBLE=False, SIZE=36
        ),

    SIZE=104
    )

fast_part = dict(part)
fast_part[9]  = raw_reflexive("uncompressed vertices", fast_uncompressed_vertex)
fast_part[10] = raw_reflexive("compressed vertices", fast_compressed_vertex)
fast_part[11] = raw_reflexive("triangles", triangle)

node = Struct('node',
    ascii_str32("name"),
    dyn_senum16('next sibling node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('first child node', DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16('parent node', DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    Float('distance from parent'),
    Pad(32),

    # xbox specific values
    LFloat('unknown', ENDIAN='<', DEFAULT=1.0),
    QStruct("rot_jj_kk", GUI_NAME="[1-2j^2-2k^2]   2[ij+kw]   2[ik-jw]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct("rot_kk_ii", GUI_NAME="2[ij-kw]   [1-2k^2-2i^2]   2[jk+iw]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct("rot_ii_jj", GUI_NAME="2[ik+jw]   2[jk-iw]   [1-2i^2-2j^2]",
        INCLUDE=ijk_float, ENDIAN='<'),
    QStruct('translation to root', INCLUDE=xyz_float, ENDIAN='<'),
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


mode_body = Struct('tagdata',
    Bool32('flags',
        'blend shared normals',
        ),
    SInt32('node list checksum'),

    # xbox has these values swapped around in order
    Float('superlow lod cutoff', SIDETIP="pixels"),
    Float('low lod cutoff', SIDETIP="pixels"),
    Float('medium lod cutoff', SIDETIP="pixels"),
    Float('high lod cutoff', SIDETIP="pixels"),
    Float('superhigh lod cutoff', SIDETIP="pixels"),

    SInt16('superlow lod nodes', SIDETIP="nodes"),
    SInt16('low lod nodes', SIDETIP="nodes"),
    SInt16('medium lod nodes', SIDETIP="nodes"),
    SInt16('high lod nodes', SIDETIP="nodes"),
    SInt16('superhigh lod nodes', SIDETIP="nodes"),

    Pad(10),

    Float('base map u scale'),
    Float('base map v scale'),

    Pad(116),

    reflexive("markers", marker, 256, DYN_NAME_PATH=".name"),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath"),

    SIZE=232
    )

fast_mode_body = dict(mode_body)
fast_mode_body[19] = reflexive("geometries", fast_geometry, 256)

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
