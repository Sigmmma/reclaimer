from .shdr import *
from supyr_struct.defs.tag_def import TagDef
from .objs.schi import SchiTag

chicago_4_stage_maps = Struct("four stage map",
    Bool16("flags" ,
        "unfiltered",
        "alpha replicate",
        "u-clamped",
        "v-clamped",
        ),

    Pad(42),
    SEnum16("color function", *blend_functions),
    SEnum16("alpha function", *blend_functions),

    Pad(36),
    #shader transformations
    Float("map u-scale"),
    Float("map v-scale"),
    Float("map u-offset"),
    Float("map v-offset"),
    float_deg("map rotation"),  # degrees
    float_zero_to_one("map bias"),  # [0,1]
    dependency("bitmap", "bitm"),

    #shader animations
    Pad(40),
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),

    QStruct("rotation center", INCLUDE=xy_float),
    SIZE=220,
    )

schi_attrs = Struct("schi attrs",
    # Shader Properties
    Struct("chicago shader",
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
    reflexive("maps", chicago_4_stage_maps, 4,
        DYN_NAME_PATH='.bitmap.filepath'),
    Bool32("extra flags",
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
