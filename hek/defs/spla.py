from .shdr import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

noise_map = Struct("noise_map",
    FlUInt16("unknown0", VISIBLE=False),
    FlUInt16("unknown1", VISIBLE=False),
    float_sec("animation period"),
    QStruct("animation direction", INCLUDE=ijk_float),
    Float("noise map scale"),
    dependency("noise map", "bitm"),
    Pad(32),
    )

spla_attrs = Struct("spla attrs",
    Pad(4),
    #Intensity
    Struct("intensity",
        SEnum16("source", *function_outputs),
        Pad(2),
        Float("exponent"),
        ),

    #Offset
    Struct("offset",
        SEnum16("source", *function_outputs),
        Pad(2),
        float_wu("amount"),
        Float("exponent"),
        ),

    Pad(32),

    #Color
    Struct("color",
        float_zero_to_one("perpendicular brightness"),
        QStruct("perpendicular tint color", INCLUDE=rgb_float),
        float_zero_to_one("parallel brightness"),
        QStruct("parallel tint color", INCLUDE=rgb_float),
        SEnum16("tint color source", *function_names),
        ),

    Pad(58),
    #Primary Noise Map
    Struct("primary noise map", INCLUDE=noise_map),

    #Secondary Noise Map
    Struct("secondary noise map", INCLUDE=noise_map),
    SIZE=292
    )

spla_body = Struct("tagdata",
    shdr_attrs,
    spla_attrs,
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef("spla",
    blam_header('spla'),
    spla_body,

    ext=".shader_transparent_plasma", endian=">", tag_cls=HekTag
    )
