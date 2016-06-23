from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


spla_body = Struct("tagdata",
    #Radiosity Properties
    radiosity_settings,

    #Shader Type
    material_type,
    FlSEnum16("numeric shader id", DEFAULT=11,
              INCLUDE=shader_id_num),

    Pad(6),
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
    Struct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color", INCLUDE=rgb_float),
    BSEnum16("tint color source", *function_names),

    Pad(62),
    #Primary Noise Map
    BFloat("primary animation period"),
    Struct("primary animation direction", INCLUDE=ijk_float),
    BFloat("primary noise map scale"),
    dependency("primary noise map", valid_bitmaps),

    Pad(36),
    #Secondary Noise Map
    BFloat("secondary animation period"),
    Struct("secondary animation direction", INCLUDE=ijk_float),
    BFloat("secondary noise map scale"),
    dependency("secondary noise map", valid_bitmaps),
    SIZE=332,
    )


def get():
    return spla_def

spla_def = TagDef(
    blam_header('spla'),
    spla_body,
    
    NAME="shader_transparent_plasma",
    
    ext=".shader_transparent_plasma", def_id="spla", endian=">"
    )
