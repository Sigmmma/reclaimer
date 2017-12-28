from .shpp import *
from ...hek.defs.objs.tag import HekTag

def merged_value_case(parent=None, **kwargs):
    if parent is None:
        raise ValueError()

    case  = parent.value_type.enum_name
    count = parent.value_count
    if count > 1:
        case += str(count)
    return case


value_name  = ascii_str32("value name")
boolean_flags = Bool16("flags",
    "invert",
    )
runtime_value = SEnum16("runtime value",
    "none",
    )
animation_flags1 = Bool8("animation flags",
    "invert"
    )
animation_flags2 = Bool8("animation flags",
    "invert",
    "multichannel noise",
    )
animation_flags3 = Bool8("animation flags",
    "invert",
    "multichannel noise",
    "ignore alpha",
    )
animation_function = SEnum16("animation function", *animation_functions)

merged_value = Struct("merged value",
    value_name,
    UEnum16("value type",
        "boolean",
        "integer",
        "float",
        "color",
        "unused",
        "bitmap",
        ),
    UInt16("value count", DEFAULT=1),
    Pad(4),
    Union("values",
        CASE=merged_value_case,
        CASES={
            "boolean": QStruct("value",
                UInt8("value", MIN=0, MAX=1, SIDETIP="[0 or 1]"),
                Pad(31)
                ),
            "integer": QStruct("value",
                SInt32("value lower bound"),
                SInt32("value upper bound"),
                Pad(24)
                ),
            "float": QStruct("value",
                Float("value lower bound"),
                Pad(12),
                Float("value upper bound"),
                Pad(12)
                ),
            "float2": Struct("value",
                QStruct("value lower bound", INCLUDE=ij_float),
                Pad(8),
                QStruct("value upper bound", INCLUDE=ij_float),
                Pad(8)
                ),
            "float3": Struct("value",
                QStruct("value lower bound", INCLUDE=ijk_float),
                Pad(4),
                QStruct("value upper bound", INCLUDE=ijk_float),
                Pad(4)
                ),
            "float4": Struct("value",
                QStruct("value lower bound", INCLUDE=ijkw_float),
                QStruct("value upper bound", INCLUDE=ijkw_float),
                ),
            "color": Struct("value",
                QStruct("value lower bound", INCLUDE=argb_float),
                QStruct("value upper bound", INCLUDE=argb_float),
                ),
            "bitmap": QStruct("value",
                SInt16("bitmap index"),
                Pad(30),
                )
            },
        SIZE=32,
        ),

    # Runtime value override
    runtime_value,
    boolean_flags,

    # Animation
    animation_function,
    animation_flags3,
    Pad(1),

    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),

    dependency_os("bitmap", "bitm"),
    Pad(12),
    SIZE=116
    )

bitmap = Struct("bitmap",
    value_name,
    Pad(8),
    SInt16("bitmap index"),
    Pad(30),

    Pad(28),
    dependency_os("bitmap", "bitm"),
    SIZE=116
    )

boolean = Struct("boolean",
    value_name,
    Pad(8),
    UInt8("value", MIN=0, MAX=1, SIDETIP="[0 or 1]"),
    Pad(31),

    runtime_value,
    boolean_flags,

    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

integer = Struct("integer",
    value_name,
    Pad(8),
    SInt32("value lower bound"),
    SInt32("value upper bound"),
    Pad(24),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_1d = Struct("float 1d",
    value_name,
    Pad(8),
    Float("value lower bound"),
    Pad(12),
    Float("value upper bound"),
    Pad(12),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_2d = Struct("float 2d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ij_float),
    Pad(8),
    QStruct("value upper bound", INCLUDE=ij_float),
    Pad(8),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_3d = Struct("float 3d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ijk_float),
    Pad(4),
    QStruct("value upper bound", INCLUDE=ijk_float),
    Pad(4),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_4d = Struct("float 4d",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=ijkw_float),
    QStruct("value upper bound", INCLUDE=ijkw_float),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

color = Struct("color",
    value_name,
    Pad(8),
    QStruct("value lower bound", INCLUDE=argb_float),
    QStruct("value upper bound", INCLUDE=argb_float),

    # Runtime value override
    SEnum16("runtime value",
        "none",
        "player team color",
        ),
    Pad(2),

    # Animation
    animation_function,
    animation_flags3,
    Pad(1),
    float_sec("animation duration"),
    Float("animation rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

shpg_attrs = Struct("shpg attrs",
    Pad(4),
    dependency_os("base shader", "shpg"),

    # when compiled into a map, all values are merged into this array
    reflexive("merged values", merged_value, 0,
              DYN_NAME_PATH='.value_name', VISIBLE=False),
    reflexive("bitmaps",   bitmap,   16, DYN_NAME_PATH='.value_name'),
    reflexive("booleans",  boolean,  16, DYN_NAME_PATH='.value_name'),
    reflexive("integers",  integer,  16, DYN_NAME_PATH='.value_name'),
    reflexive("floats 1d", float_1d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats 2d", float_2d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats 3d", float_3d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats 4d", float_4d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("colors",    color,    16, DYN_NAME_PATH='.value_name'),
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
