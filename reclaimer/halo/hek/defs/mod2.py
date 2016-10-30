from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return mod2_def

local_marker = Struct('local marker',
    StrLatin1("name", SIZE=32),
    SInt16('node index'),
    Pad(2),

    BFloat('rotation i'),
    BFloat('rotation j'),
    BFloat('rotation k'),
    BFloat('rotation w'),

    BFloat('translation x'),
    BFloat('translation y'),
    BFloat('translation z'),
    SIZE=80
    )

uncompressed_vertex = QStruct('uncompressed vertex',
    BFloat('translation x'),
    BFloat('translation y'),
    BFloat('translation z'),

    BFloat('normal i'),
    BFloat('normal j'),
    BFloat('normal k'),

    BFloat('binormal i'),
    BFloat('binormal j'),
    BFloat('binormal k'),

    BFloat('tangent i'),
    BFloat('tangent j'),
    BFloat('tangent k'),

    BFloat('tex coord u'),
    BFloat('tex coord v'),

    BSInt16('node 0 index'),
    BSInt16('node 1 index'),
    BFloat('node 0 weight'),
    BFloat('node 1 weight'),
    SIZE=68
    )

compressed_vertex = QStruct('compressed vertex',
    BFloat('translation x'),
    BFloat('translation y'),
    BFloat('translation z'),

    # These wont work in a QStruct, so make sure not to use them with it.
    #BBitStruct('normal',   INCLUDE=compressed_normal_32, SIZE=4),
    #BBitStruct('binormal', INCLUDE=compressed_normal_32, SIZE=4),
    #BBitStruct('tangent',  INCLUDE=compressed_normal_32, SIZE=4),
    BUInt32('normal'),
    BUInt32('binormal'),
    BUInt32('tangent'),

    BSInt16('tex coord u'),
    BSInt16('tex coord v'),

    SInt8('node 0 index'),
    SInt8('node 1 index'),
    BSInt16('node 0 weight'),
    SIZE=32
    )

triangle = QStruct('triangle',
    BSInt16('vert 0 index'),
    BSInt16('vert 1 index'),
    BSInt16('vert 2 index'),
    SIZE=6
    )


uncompressed_vertex_union = Union('uncompressed vertex',
    CASES={'uncompressed_vertex': uncompressed_vertex},
    )

compressed_vertex_union = Union('compressed vertex',
    CASES={'compressed_vertex': compressed_vertex},
    )

triangle_union = Union('triangle',
    CASES={'triangle': triangle},
    )


marker_instance = QStruct('marker instance',
    SInt8('region index'),
    SInt8('permutation index'),
    SInt8('node index'),
    Pad(1),

    BFloat('translation x'),
    BFloat('translation y'),
    BFloat('translation z'),

    BFloat('rotation i'),
    BFloat('rotation j'),
    BFloat('rotation k'),
    BFloat('rotation w'),
    SIZE=32
    )

permutation = Struct('permutation',
    StrLatin1("name", SIZE=32),
    BBool32('flags',
        'cannot be chosen randomly'
        ),
    Pad(28),

    BSInt16('superlow geometry block'),
    BSInt16('low geometry block'),
    BSInt16('medium geometry block'),
    BSInt16('high geometry block'),
    BSInt16('superhigh geometry block'),
    Pad(2),

    reflexive("local markers", local_marker, 32),
    SIZE=88
    )

part = Struct('part',
    BBool32('flags',
        'stripped',
        'ZONER',
        ),
    Pad(1),
    SInt8('shader index'),
    SInt8('previous part index'),
    SInt8('next part index'),

    BSInt16('centroid primary node'),
    BSInt16('centroid secondary node'),
    BFloat('centroid primary weight'),
    BFloat('centroid secondary weight'),

    BFloat('centroid translation x'),
    BFloat('centroid translation y'),
    BFloat('centroid translation z'),

    #reflexive("uncompressed vertices", uncompressed_vertex_union),
    #reflexive("compressed vertices", compressed_vertex_union),
    #reflexive("triangles", triangle_union),
    reflexive("uncompressed vertices", uncompressed_vertex),
    reflexive("compressed vertices", compressed_vertex),
    reflexive("triangles", triangle),
    Pad(40),

    UInt8('local node count'),
    UInt8Array('local nodes', SIZE=20),
    SIZE=132
    )



marker = Struct('marker',
    StrLatin1("name", SIZE=32),
    BUInt16('magic identifier'),
    Pad(18),

    reflexive("marker instances", marker_instance, 32),
    SIZE=64
    )

node = Struct('node',
    StrLatin1("name", SIZE=32),
    BSInt16('next sibling node'),
    BSInt16('first child node'),
    BSInt16('parent node'),
    Pad(2),

    BFloat('translation x'),
    BFloat('translation y'),
    BFloat('translation z'),

    BFloat('rotation i'),
    BFloat('rotation j'),
    BFloat('rotation k'),
    BFloat('rotation w'),
    BFloat('distance from parent'),
    SIZE=156,
    )

region = Struct('region',
    StrLatin1("name", SIZE=32),
    Pad(32),
    reflexive("permutations", permutation),
    SIZE=76
    )

geometry = Struct('geometry',
    Pad(36),
    reflexive("parts", part, 32),
    SIZE=48
    )

shader = Struct('shader',
    dependency("shader", valid_shaders),
    BSInt16('permutation index'),
    SIZE=32,
    )


mod2_body = Struct('tagdata',
    BBool32('flags',
        'blend shared normals',
        'parts have local nodes',
        'ignore skinning'
        ),
    BSInt32('node list checksum'),

    BFloat('superlow lod cutoff'),
    BFloat('low lod cutoff'),
    BFloat('medium lod cutoff'),
    BFloat('high lod cutoff'),
    BFloat('superhigh lod cutoff'),

    BSInt16('superlow nodes count'),
    BSInt16('low nodes count'),
    BSInt16('medium nodes count'),
    BSInt16('high nodes count'),
    BSInt16('superhigh nodes count'),

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


mod2_def = TagDef("mod2",
    blam_header('mod2', 5),
    mod2_body,

    ext=".gbxmodel", endian=">"
    )
