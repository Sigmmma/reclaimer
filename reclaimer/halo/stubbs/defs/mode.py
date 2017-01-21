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

    Pad(104),
    reflexive("unknown", unknown_struct, DYN_NAME_PATH=".name"),

    reflexive("markers", marker, 256, DYN_NAME_PATH=".name"),
    reflexive("nodes", node, 64, DYN_NAME_PATH=".name"),
    reflexive("regions", region, 32, DYN_NAME_PATH=".name"),
    reflexive("geometries", geometry, 256),
    reflexive("shaders", shader, 256, DYN_NAME_PATH=".shader.filepath"),

    SIZE=232
    )

mode_def = TagDef("mode",
    blam_header('mode', 4),
    mode_body,

    ext=".model", endian=">", tag_cls=ModeTag
    )
