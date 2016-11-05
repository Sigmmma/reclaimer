from .shdr import *
from supyr_struct.defs.tag_def import TagDef

smet_attrs = Struct("smet attrs",
    #Meter Shader Properties
    BBool16("meter shader flags",
        "decal",
        "two-sided",
        "flash color is negative",
        "tint mode-2",
        "unfiltered"
        ),
    Pad(34),
    dependency("meter map", "bitm"),
    Pad(32),

    #Colors
    Struct("gadient min color", INCLUDE=rgb_float),
    Struct("gadient max color", INCLUDE=rgb_float),
    Struct("background color", INCLUDE=rgb_float),
    Struct("flash color", INCLUDE=rgb_float),
    Struct("tint color", INCLUDE=rgb_float),
    BFloat("meter transparency"),
    BFloat("background transparency"),
    Pad(24),

    #External Function Sources
    BSEnum16("meter brightness source", *function_outputs),
    BSEnum16("flash brightness source", *function_outputs),
    BSEnum16("value source",            *function_outputs),
    BSEnum16("gradient source",         *function_outputs),
    BSEnum16("flash-extension source",  *function_outputs),
    SIZE=220,
    )

smet_body = Struct("tagdata",
    shdr_attrs,
    smet_attrs,
    SIZE=260,
    )



def get():
    return smet_def

smet_def = TagDef("smet",
    blam_header('smet'),
    smet_body,

    ext=".shader_meter", endian=">"
    )
