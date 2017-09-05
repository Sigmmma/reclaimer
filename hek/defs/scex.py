from .schi import *
from supyr_struct.defs.tag_def import TagDef
from .objs.scex import ScexTag

chicago_2_stage_maps = Struct("two stage map", INCLUDE=chicago_4_stage_maps)

scex_attrs = Struct("scex attrs",
    # Shader Properties
    Struct("chicago shader extended",
        UInt8("numeric counter limit",
            MIN=0, MAX=255, SIDETIP="[0,255]"),  # [0,255]

        Bool8("chicago shader flags", *trans_shdr_properties),
        SEnum16("first map type", *trans_shdr_first_map_type),
        SEnum16("framebuffer blend function", *framebuffer_blend_functions),
        SEnum16("framebuffer fade mode", *render_fade_mode),
        SEnum16("framebuffer fade source", *function_outputs),
        Pad(2),
        ),

    #Lens Flare
    float_wu("lens flare spacing"),  # world units
    dependency("lens flare", "lens"),
    reflexive("extra layers", extra_layers_block, 4,
        DYN_NAME_PATH='.filepath'),
    reflexive("four stage maps", chicago_4_stage_maps, 4,
        DYN_NAME_PATH='.bitmap.filepath'),
    reflexive("two stage maps", chicago_2_stage_maps, 2,
        DYN_NAME_PATH='.bitmap.filepath'),
    Bool32("extra flags",
        "dont fade active camouflage",
        "numeric countdown timer"
        ),
    SIZE=80
    )

scex_body = Struct("tagdata",
    shdr_attrs,
    scex_attrs,
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
