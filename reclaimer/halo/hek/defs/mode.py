from .mod2 import *

def get():
    return mode_def

permutation = Struct('permutation',
    ascii_str32("name"),
    BBool32('flags',
        'cannot be chosen randomly'
        ),
    Pad(28),

    dyn_senum16('superlow geometry block'),
    dyn_senum16('low geometry block'),
    dyn_senum16('medium geometry block'),
    dyn_senum16('high geometry block'),
    dyn_senum16('superhigh geometry block'),
    Pad(2),
    SIZE=88
    )

part = Struct('part',
    Pad(5),
    dyn_senum8('shader index'),
    SInt8('previous part index'),
    SInt8('next part index'),

    BSInt16('centroid primary node'),
    BSInt16('centroid secondary node'),
    BFloat('centroid primary weight'),
    BFloat('centroid secondary weight'),

    QStruct('centroid translation', INCLUDE=xyz_float),
    Pad(12),

    #reflexive("compressed vertices", compressed_vertex_union, 65535),
    #reflexive("triangles", triangle_union, 65535),
    reflexive("compressed vertices", compressed_vertex, 65535),
    reflexive("triangles", triangle, 65535),

    SIZE=104
    )


node = Struct('node',
    ascii_str32("name"),
    dyn_senum16('next sibling node'),
    dyn_senum16('first child node'),
    dyn_senum16('parent node'),
    Pad(2),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    BFloat('distance from parent'),
    Pad(32),

    # xbox specific values
    LFloat('unknown', ENDIAN='<'),
    QStruct('unknown normal', INCLUDE=ijk_float, ENDIAN='<'),
    QStruct('unknown binormal', INCLUDE=ijk_float, ENDIAN='<'),
    QStruct('unknown tangent', INCLUDE=ijk_float, ENDIAN='<'),
    QStruct('unknown translation', INCLUDE=xyz_float, ENDIAN='<'),
    SIZE=156,
    )

region = Struct('region',
    ascii_str32("name"),
    Pad(32),
    reflexive("permutations", permutation, 32),
    SIZE=76
    )

geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", part, 32),
    SIZE=48
    )


mode_body = Struct('tagdata',
    BBool32('flags',
        'blend shared normals',
        'parts have local nodes',
        'ignore skinning'
        ),
    BSInt32('node list checksum'),

    BFloat('superlow lod cutoff', SIDETIP="pixels"),
    BFloat('low lod cutoff', SIDETIP="pixels"),
    BFloat('medium lod cutoff', SIDETIP="pixels"),
    BFloat('high lod cutoff', SIDETIP="pixels"),
    BFloat('superhigh lod cutoff', SIDETIP="pixels"),

    BSInt16('superlow lod nodes', SIDETIP="nodes"),
    BSInt16('low lod nodes', SIDETIP="nodes"),
    BSInt16('medium lod nodes', SIDETIP="nodes"),
    BSInt16('high lod nodes', SIDETIP="nodes"),
    BSInt16('superhigh lod nodes', SIDETIP="nodes"),

    Pad(10),

    BFloat('base map u scale'),
    BFloat('base map v scale'),

    Pad(116),

    reflexive("markers", marker, 256),
    reflexive("nodes", node, 64),
    reflexive("regions", region, 32),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256),

    SIZE=232
    )


mode_def = TagDef("mode",
    blam_header('mode', 4),
    mode_body,

    ext=".model", endian=">"
    )
