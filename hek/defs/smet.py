from .shdr import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

smet_attrs = Struct("smet attrs",
    #Meter Shader Properties
    Struct("meter shader",
        Bool16("meter shader flags",
            "decal",
            "two-sided",
            "flash color is negative",
            "tint mode-2",
            "unfiltered"
            ),
        Pad(34),
        dependency("map", "bitm"),
        Pad(32),
        ),

    #Colors
    Struct("colors",
        Struct("gadient min", INCLUDE=rgb_float),
        Struct("gadient max", INCLUDE=rgb_float),
        Struct("background", INCLUDE=rgb_float),
        Struct("flash", INCLUDE=rgb_float),
        Struct("tint", INCLUDE=rgb_float),
        float_zero_to_one("meter transparency"),
        float_zero_to_one("background transparency"),
        ),

    Pad(24),
    #External Function Sources
    Struct("external function sources",
        SEnum16("meter brightness", *function_outputs),
        SEnum16("flash brightness", *function_outputs),
        SEnum16("value",            *function_outputs),
        SEnum16("gradient",         *function_outputs),
        SEnum16("flash-extension",  *function_outputs),
        ),
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

    ext=".shader_transparent_meter", endian=">", tag_cls=HekTag
    )
