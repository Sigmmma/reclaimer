from .shdr import *
from supyr_struct.defs.tag_def import TagDef
from .objs.schi import SchiTag

chicago_4_stage_maps = Struct("four stage map",
    BBool16("flags" ,
        "unfiltered",
        "alpha replicate",
        "u-clamped",
        "v-clamped",
        ),

    Pad(42),
    BSEnum16("color function", *blend_functions),
    BSEnum16("alpha function", *blend_functions),

    Pad(36),
    #shader transformations
    BFloat("map u-scale"),
    BFloat("map v-scale"),
    BFloat("map u-offset"),
    BFloat("map v-offset"),
    BFloat("map rotation"),#degrees
    BFloat("map bias"),#[0,1]
    dependency("bitmap", "bitm"),

    #shader animations
    Pad(40),
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),

    QStruct("rotation center", INCLUDE=xy_float),
    SIZE=220,
    )

schi_attrs = Struct("schi attrs",
    # Shader Properties
    UInt8("numeric counter limit"),#[0,255]

    Bool8("chicago shader flags", *trans_shdr_properties),
    BSEnum16("first map type", *trans_shdr_first_map_type),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *render_fade_mode),
    BSEnum16("framebuffer fade source", *function_outputs),

    Pad(2),
    #Lens Flare
    BFloat("lens flare spacing"),#world units
    dependency("lens flare", "lens"),
    reflexive("extra layers", extra_layers_block, 4),
    reflexive("maps", chicago_4_stage_maps, 4),
    BBool32("extra flags",
        "dont fade active camouflage",
        "numeric countdown timer"
        ),
    SIZE=68
    )

schi_body = Struct("tagdata",
    shdr_attrs,
    schi_attrs,
    SIZE=108
    )

    
def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header('schi'),
    schi_body,

    ext=".shader_transparent_chicago",
    endian=">", tag_cls=SchiTag
    )
