from .shpp import *
from ...hek.defs.objs.tag import HekTag

value_name = ascii_str32("value name")
runtime_value = BSEnum16("runtime value",
    "none",
    )
animation_flags1 = Bool8("animation flags",
    "invert"
    )
animation_flags2 = Bool8("animation flags",
    "invert",
    "multichannel noise",
    )
animation_function = BSEnum16("animation function", *animation_functions)

bitmap = Struct("bitmap",
    value_name,

    Pad(8),
    BSInt16("bitmap index"),

    Pad(58),
    dependency_os("bitmap", "bitm"),
    SIZE=116
    )

boolean = Struct("boolean",
    value_name,
    Pad(8),
    UInt8("value", MIN=0, MAX=1, SIDETIP="[0 or 1]"),

    Pad(31),
    # Runtime value override
    Pad(2),  # runtime_value,
    BBool16("flags", "invert"),
    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

integer = Struct("integer",
    value_name,
    Pad(8),
    BSInt32("value lower bound"),
    BSInt32("value upper bound"),

    Pad(24),
    # Runtime value override
    Pad(2),  # runtime_value,

    Pad(2),
    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_1d = Struct("float 1d",
    value_name,
    Pad(8),
    BFloat("value lower bound"),
    Pad(12),
    BFloat("value upper bound"),

    Pad(12),
    # Runtime value override
    Pad(2),  # runtime_value,

    Pad(2),
    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_2d = Struct("float 2d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ij_float),
    Pad(8),
    QStruct("value upper bound", INCLUDE=ij_float),

    Pad(8),
    # Runtime value override
    Pad(2),  # runtime_value,

    Pad(2),
    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_3d = Struct("float 3d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ijk_float),
    Pad(4),
    QStruct("value upper bound", INCLUDE=ijk_float),

    Pad(4),
    # Runtime value override
    Pad(2),  # runtime_value,

    Pad(2),
    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_4d = Struct("float 4d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ijkw_float),
    QStruct("value upper bound", INCLUDE=ijkw_float),

    # Runtime value override
    Pad(2),  # runtime_value,

    Pad(2),
    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

color = Struct("color",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=argb_float),
    QStruct("value upper bound", INCLUDE=argb_float),

    # Runtime value override
    BSEnum16("runtime value",
        "none",
        "player team color",
        ),

    Pad(2),
    # Animation
    animation_function,
    Bool8("animation flags",
        "invert",
        "multichannel noise",
        "ignore alpha",
        ),
    Pad(1),
    float_sec("animation duration"),
    BFloat("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

shpg_attrs = Struct("shpg attrs",
    Pad(4),
    dependency_os("base shader", "shpg"),

    # whatever this is, each is 116 bytes
    Pad(12),#reflexive("unknown", void_desc),
    reflexive("bitmaps", bitmap, 16,    DYN_NAME_PATH='.value_name'),
    reflexive("booleans", boolean, 16,  DYN_NAME_PATH='.value_name'),
    reflexive("integers", integer, 16,  DYN_NAME_PATH='.value_name'),
    reflexive("float 1d", float_1d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("float 2d", float_2d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("float 3d", float_3d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("float 4d", float_4d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("colors", color, 16,      DYN_NAME_PATH='.value_name'),
    SIZE=164
    )

shpg_body = Struct("tagdata",
    shpp_attrs,
    shpg_attrs,
    SIZE=328
    )

def get():
    return shpg_def

shpg_def = TagDef("shpg",
    blam_header_os('shpg'),
    shpg_body,

    ext=".shader_postprocess_generic", endian=">", tag_cls=HekTag
    )
