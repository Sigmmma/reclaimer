#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

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


value_name  = ascii_str32("value_name")
boolean_flags = Bool16("flags",
    "invert",
    )
runtime_value = SEnum16("runtime_value",
    "none",
    )
animation_flags1 = Bool8("animation_flags",
    "invert"
    )
animation_flags2 = Bool8("animation_flags",
    "invert",
    "multichannel_noise",
    )
animation_flags3 = Bool8("animation_flags",
    "invert",
    "multichannel_noise",
    "ignore_alpha",
    )
animation_function = SEnum16("animation_function", *animation_functions)

merged_value = Struct("merged_value",
    value_name,
    UEnum16("value_type",
        "boolean",
        "integer",
        "float",
        "color",
        "unused",
        "bitmap",
        ),
    UInt16("value_count", DEFAULT=1),
    Pad(4),
    Union("values",
        CASE=merged_value_case,
        CASES={
            "boolean": QStruct("value",
                UInt8("value", MIN=0, MAX=1, SIDETIP="[0 or 1]"),
                Pad(31)
                ),
            "integer": QStruct("value",
                SInt32("value_lower_bound"),
                SInt32("value_upper_bound"),
                Pad(24)
                ),
            "float": QStruct("value",
                Float("value_lower_bound"),
                Pad(12),
                Float("value_upper_bound"),
                Pad(12)
                ),
            "float2": Struct("value",
                QStruct("value_lower_bound", INCLUDE=ij_float),
                Pad(8),
                QStruct("value_upper_bound", INCLUDE=ij_float),
                Pad(8)
                ),
            "float3": Struct("value",
                QStruct("value_lower_bound", INCLUDE=ijk_float),
                Pad(4),
                QStruct("value_upper_bound", INCLUDE=ijk_float),
                Pad(4)
                ),
            "float4": Struct("value",
                QStruct("value_lower_bound", INCLUDE=ijkw_float),
                QStruct("value_upper_bound", INCLUDE=ijkw_float),
                ),
            "color": Struct("value",
                QStruct("value_lower_bound", INCLUDE=argb_float),
                QStruct("value_upper_bound", INCLUDE=argb_float),
                ),
            "bitmap": QStruct("value",
                SInt16("bitmap_index"),
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

    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),

    dependency_os("bitmap", "bitm"),
    Pad(12),
    SIZE=116
    )

bitmap = Struct("bitmap",
    value_name,
    Pad(8),
    SInt16("bitmap_index"),
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
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

integer = Struct("integer",
    value_name,
    Pad(8),
    SInt32("value_lower_bound"),
    SInt32("value_upper_bound"),
    Pad(24),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_1d = Struct("float_1d",
    value_name,
    Pad(8),
    Float("value_lower_bound"),
    Pad(12),
    Float("value_upper_bound"),
    Pad(12),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags1,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_2d = Struct("float_2d",
    value_name,
    Pad(8),
    QStruct("value_lower_bound", INCLUDE=ij_float),
    Pad(8),
    QStruct("value_upper_bound", INCLUDE=ij_float),
    Pad(8),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_3d = Struct("float_3d",
    value_name,
    Pad(8),
    QStruct("value_lower_bound", INCLUDE=ijk_float),
    Pad(4),
    QStruct("value_upper_bound", INCLUDE=ijk_float),
    Pad(4),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

float_4d = Struct("float_4d",
    value_name,
    Pad(8),
    QStruct("value_lower_bound", INCLUDE=ijkw_float),
    QStruct("value_upper_bound", INCLUDE=ijkw_float),

    runtime_value,
    Pad(2),

    # Animation
    animation_function,
    animation_flags2,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

color = Struct("color",
    value_name,
    Pad(8),
    QStruct("value_lower_bound", INCLUDE=argb_float),
    QStruct("value_upper_bound", INCLUDE=argb_float),

    # Runtime value override
    SEnum16("runtime_value",
        "none",
        "player_team_color",
        ),
    Pad(2),

    # Animation
    animation_function,
    animation_flags3,
    Pad(1),
    float_sec("animation_duration"),
    Float("animation_rate", UNIT_SCALE=per_sec_unit_scale),
    SIZE=88
    )

shpg_attrs = Struct("shpg_attrs",
    Pad(4),
    dependency_os("base_shader", "shpg"),

    # when compiled into a map, all values are merged into this array
    reflexive("merged_values", merged_value, 16*8,
              DYN_NAME_PATH='.value_name', VISIBLE=False),
    reflexive("bitmaps",   bitmap,   16, DYN_NAME_PATH='.value_name'),
    reflexive("booleans",  boolean,  16, DYN_NAME_PATH='.value_name'),
    reflexive("integers",  integer,  16, DYN_NAME_PATH='.value_name'),
    reflexive("floats_1d", float_1d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats_2d", float_2d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats_3d", float_3d, 16, DYN_NAME_PATH='.value_name'),
    reflexive("floats_4d", float_4d, 16, DYN_NAME_PATH='.value_name'),
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
