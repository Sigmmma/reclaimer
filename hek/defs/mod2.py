from ...common_descs import *
from .objs.mod2 import Mod2Tag
from supyr_struct.defs.tag_def import TagDef

def get():
    return mod2_def

local_marker = Struct('local marker',
    ascii_str32("name"),
    dyn_senum16('node index',
        DYN_NAME_PATH="tagdata.nodes.nodes_array[DYN_I].name"),
    Pad(2),

    QStruct('rotation', INCLUDE=ijkw_float),
    QStruct('translation', INCLUDE=xyz_float),
    SIZE=80
    )

fast_uncompressed_vertex = QStruct('uncompressed vertex',
    Float('position x'), Float('position y'), Float('position z'),
    Float('normal i'),   Float('normal j'),   Float('normal k'),
    Float('binormal i'), Float('binormal j'), Float('binormal k'),
    Float('tangent i'),  Float('tangent j'),  Float('tangent k'),

    Float('u'), Float('v'),

    SInt16('node 0 index'), SInt16('node 1 index'),
    Float('node 0 weight'), Float('node 1 weight'),
    SIZE=68
    )

fast_compressed_vertex = QStruct('compressed vertex',
    Float('position x'), Float('position y'), Float('position z'),
    UInt32('normal'),
    UInt32('binormal'),
    UInt32('tangent'),

    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),

    SInt8('node 0 index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt8('node 1 index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt16('node 0 weight', UNIT_SCALE=1/32767, MIN=0, WIDGET_WIDTH=10),
    SIZE=32
    )

uncompressed_vertex = Struct('uncompressed vertex',
    QStruct("position", INCLUDE=xyz_float),
    QStruct("normal", INCLUDE=ijk_float),
    QStruct("binormal", INCLUDE=ijk_float),
    QStruct("tangent", INCLUDE=ijk_float),

    Float('u'),
    Float('v'),

    SInt16('node 0 index',
        TOOLTIP="If local nodes are used, this is a local index"),
    SInt16('node 1 index',
        TOOLTIP="If local nodes are used, this is a local index"),
    Float('node 0 weight'),
    Float('node 1 weight'),
    SIZE=68
    )

compressed_vertex = Struct('compressed vertex',
    QStruct("position", INCLUDE=xyz_float),

    # These wont work in a QStruct, so make sure not to use them with it.
    BBitStruct('normal',   INCLUDE=compressed_normal_32, SIZE=4),
    BBitStruct('binormal', INCLUDE=compressed_normal_32, SIZE=4),
    BBitStruct('tangent',  INCLUDE=compressed_normal_32, SIZE=4),

    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),

    SInt8('node 0 index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt8('node 1 index', UNIT_SCALE=1/3, MIN=0, WIDGET_WIDTH=10),
    SInt16('node 0 weight', UNIT_SCALE=1/32767, MIN=0, WIDGET_WIDTH=10),
    SIZE=32
    )

triangle = QStruct('triangle',
    SInt16('v0 index'), SInt16('v1 index'), SInt16('v2 index'),
    SIZE=6, ORIENT='h'
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


marker_instance = Struct('marker instance',
    dyn_senum8('region index',
        DYN_NAME_PATH="tagdata.regions.regions_array[DYN_I].name"),
    SInt8('permutation index', MIN=-1),
    dyn_senum8('node index',
        DYN_NAME_PATH="tagdata.nodes.nodes_array[DYN_I].name"),
    Pad(1),

    QStruct('translation', INCLUDE=xyz_float),
    QStruct('rotation', INCLUDE=ijkw_float),
    SIZE=32
    )

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

    reflexive("local markers", local_marker, 32, DYN_NAME_PATH=".name"),
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

    #reflexive("uncompressed vertices", uncompressed_vertex_union, 32767),
    #reflexive("compressed vertices", compressed_vertex_union, 32767),
    #reflexive("triangles", triangle_union, 32767),
    reflexive("uncompressed vertices", fast_uncompressed_vertex, 32767),
    reflexive("compressed vertices", fast_compressed_vertex, 32767),
    reflexive("triangles", triangle, 32767),
    #Pad(36),
    Struct("model meta info",
        UEnum32("index type",  # name is a guess.  always 1?
            ("uncompressed", 1),
            ),
        UInt32("index count"),
        # THESE TWO VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("indices magic offset"),
        UInt32("indices offset"),

        UEnum32("vertex type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        UInt32("vertex count"),
        Pad(4),  # always 0?
        # THESE TWO VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("vertices magic offset"),
        UInt32("vertices offset"),
        VISIBLE=False, SIZE=36
        ),

    Pad(3),
    SInt8('local node count', MIN=0, MAX=22),
    #UInt8Array('local nodes', SIZE=22),
    Array("local nodes", SUB_STRUCT=UInt8("local node index"), SIZE=22),

    # this COULD be 2 more potential local nodes, but I've seen tool
    # split models when they reach 22 nodes, so im assuming 22 is the max
    Pad(2),
    SIZE=132
    )

fast_part = dict(part)
fast_part[9]  = raw_reflexive("uncompressed vertices", fast_uncompressed_vertex)
fast_part[10] = raw_reflexive("compressed vertices", fast_compressed_vertex)
fast_part[11] = raw_reflexive("triangles", triangle)

marker = Struct('marker',
    ascii_str32("name"),
    UInt16('magic identifier'),
    Pad(18),

    reflexive("marker instances", marker_instance, 32),
    SIZE=64
    )

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
    LFloat('unknown', ENDIAN='<', DEFAULT=1.0, VISIBLE=False),
    QStruct("rot_jj_kk", GUI_NAME="[1-2j^2-2k^2]   2[ij+kw]   2[ik-jw]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct("rot_kk_ii", GUI_NAME="2[ij-kw]   [1-2k^2-2i^2]   2[jk+iw]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct("rot_ii_jj", GUI_NAME="2[ik+jw]   2[jk-iw]   [1-2i^2-2j^2]",
        INCLUDE=ijk_float, ENDIAN='<', VISIBLE=False),
    QStruct('translation to root', INCLUDE=xyz_float,
            ENDIAN='<', VISIBLE=False),
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
    SInt16('permutation index'),
    SIZE=32,
    )


mod2_body = Struct('tagdata',
    Bool32('flags',
        'blend shared normals',
        'parts have local nodes',
        'ignore skinning'
        ),
    SInt32('node list checksum'),

    Float('superhigh lod cutoff', SIDETIP="pixels"),
    Float('high lod cutoff', SIDETIP="pixels"),
    Float('medium lod cutoff', SIDETIP="pixels"),
    Float('low lod cutoff', SIDETIP="pixels"),
    Float('superlow lod cutoff', SIDETIP="pixels"),

    SInt16('superhigh lod nodes', SIDETIP="nodes"),
    SInt16('high lod nodes', SIDETIP="nodes"),
    SInt16('medium lod nodes', SIDETIP="nodes"),
    SInt16('low lod nodes', SIDETIP="nodes"),
    SInt16('superlow lod nodes', SIDETIP="nodes"),

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
