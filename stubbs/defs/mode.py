from ...hek.defs.mode import *

def get():
    return mode_def

# my guess at what the struct might be like
unknown_struct = Struct("unknown",
    ascii_str32("name"),
    LFloat('unknown1', ENDIAN='<', DEFAULT=1.0),
    LFloat('unknown2', ENDIAN='<', DEFAULT=1.0),
    BytesRaw("unknown data", SIZE=64-32-4*2),
    SIZE=64
    )

#unknown_struct = Struct("unknown",
#    BytesRaw("unknown data", SIZE=64),
#    SIZE=64
#    )

pc_part = Struct('part',
    BBool32('flags',
        'stripped',
        'ZONER',
        ),
    dyn_senum16('shader index',
        DYN_NAME_PATH="tagdata.shaders.shaders_array[DYN_I].shader.filepath"),
    SInt8('previous part index'),
    SInt8('next part index'),

    BSInt16('centroid primary node'),
    BSInt16('centroid secondary node'),
    BFloat('centroid primary weight'),
    BFloat('centroid secondary weight'),

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
        # THESE VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("indices magic offset"),
        UInt32("indices offset"),

        UEnum32("vertex type",  # name is a guess
            ("uncompressed", 4),
            ("compressed",   5),
            ),
        UInt32("vertex count"),
        Pad(4),  # always 0?
        # THESE VALUES ARE DIFFERENT THAN ON XBOX IT SEEMS
        UInt32("vertices magic offset"),
        UInt32("vertices offset"),
        VISIBLE=False, SIZE=36
        ),

    SIZE=104
    )

fast_part = dict(part)
fast_part[9]  = raw_reflexive("uncompressed vertices", fast_uncompressed_vertex)
fast_part[10] = raw_reflexive("compressed vertices", fast_compressed_vertex)
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
    BBool32('flags',
        'blend shared normals',
        'parts have local nodes',
        'ignore skinning'
        ),
    BSInt32('node list checksum'),

    BFloat('superhigh lod cutoff', SIDETIP="pixels"),
    BFloat('high lod cutoff', SIDETIP="pixels"),
    BFloat('medium lod cutoff', SIDETIP="pixels"),
    BFloat('low lod cutoff', SIDETIP="pixels"),
    BFloat('superlow lod cutoff', SIDETIP="pixels"),

    BSInt16('superhigh lod nodes', SIDETIP="nodes"),
    BSInt16('high lod nodes', SIDETIP="nodes"),
    BSInt16('medium lod nodes', SIDETIP="nodes"),
    BSInt16('low lod nodes', SIDETIP="nodes"),
    BSInt16('superlow lod nodes', SIDETIP="nodes"),

    Pad(10),

    BFloat('base map u scale'),
    BFloat('base map v scale'),

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
    blam_header('mode', 6),  # increment to differentiate it from mode and mod2
    mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )

fast_mode_def = TagDef("mode",
    blam_header('mode', 6),  # increment to differentiate it from mode and mod2
    fast_mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )

pc_mode_def = TagDef("mode",
    blam_header('mode', 6),  # increment to differentiate it from mode and mod2
    pc_mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )
