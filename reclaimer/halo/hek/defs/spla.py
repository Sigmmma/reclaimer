from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef


spla_body = Struct("tagdata",
    radiosity_settings,
    shader_physics,

    Pad(4),
    #Intensity
    BSEnum16("intensity source", *function_outputs),
    Pad(2),
    BFloat("intensity exponent"),

    #Offset
    BSEnum16("offset source", *function_outputs),
    Pad(2),
    BFloat("offset amount"),
    BFloat("offset exponent"),

    Pad(32),

    #Color
    BFloat("perpendicular brightness"),#[0,1]
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    QStruct("parallel tint color", INCLUDE=rgb_float),
    BSEnum16("tint color source", *function_names),

    Pad(62),
    #Primary Noise Map
    BFloat("primary animation period"),
    QStruct("primary animation direction", INCLUDE=ijk_float),
    BFloat("primary noise map scale"),
    dependency("primary noise map", valid_bitmaps),

    Pad(36),
    #Secondary Noise Map
    BFloat("secondary animation period"),
    QStruct("secondary animation direction", INCLUDE=ijk_float),
    BFloat("secondary noise map scale"),
    dependency("secondary noise map", valid_bitmaps),
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef("spla",
    blam_header('spla'),
    spla_body,

    ext=".shader_transparent_plasma", endian=">"
    )
