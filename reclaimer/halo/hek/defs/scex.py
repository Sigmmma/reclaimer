from .schi import *
from supyr_struct.defs.tag_def import TagDef
from .objs.scex import ScexTag

chicago_2_stage_maps = Struct("two stage map", INCLUDE=chicago_4_stage_maps)

scex_body = Struct("tagdata",
    shader_attrs,

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
    dependency("lens flare"),
    reflexive("extra layers", extra_layers_block, 4),
    reflexive("four stage maps", chicago_4_stage_maps, 4),
    reflexive("two stage maps", chicago_2_stage_maps, 2),
    BBool32("extra flags",
        "dont fade active camouflage",
        "numeric countdown timer"
        ),
    SIZE=120
    )


def get():
    return scex_def

scex_def = TagDef("scex",
    blam_header('scex'),
    scex_body,

    ext=".shader_transparent_chicago_extended", 
    endian=">", tag_cls=ScexTag
    )
