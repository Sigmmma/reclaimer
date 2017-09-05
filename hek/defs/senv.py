from .shdr import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

environment_shader = Struct("environment shader",
    Bool16("environment shader flags",
        "alpha tested",
        "bump-map is specular mask",
        "true atmospheric fog",
        ),
    SEnum16("environment shader type",
        "normal",
        "blended",
        "blended base specular",
        ),
    )

diffuse = Struct("diffuse",
    Bool16("diffuse flags",
        "rescale detail maps",
        "rescale bump maps",
        ),
    Pad(26),
    dependency("base map", "bitm"),
                   
    Pad(24),
    SEnum16("detail map function", *detail_map_functions),
    Pad(2),

    Float("primary detail map scale"),
    dependency("primary detail map", "bitm"),
    Float("secondary detail map scale"),
    dependency("secondary detail map", "bitm"),

    Pad(24),
    SEnum16("micro detail map function", *detail_map_functions),

    Pad(2),
    Float("micro detail map scale"),
    dependency("micro detail map", "bitm"),
    QStruct("material color", INCLUDE=rgb_float),
    )

bump_properties = Struct("bump properties",
    Float("map scale"),
    dependency("map", "bitm"),
    FlFloat("map scale x"),
    FlFloat("map scale y"),
    )

self_illumination = Struct("self illumination",
    QStruct("primary on-color",  INCLUDE=rgb_float),
    QStruct("primary off-color", INCLUDE=rgb_float),
    Struct("primary animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    QStruct("secondary on-color",  INCLUDE=rgb_float),
    QStruct("secondary off-color", INCLUDE=rgb_float),
    Struct("secondary animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    QStruct("plasma on-color",  INCLUDE=rgb_float),
    QStruct("plasma off-color", INCLUDE=rgb_float),
    Struct("plasma animation", INCLUDE=anim_func_per_pha),

    Pad(24),
    Float("map scale"),
    dependency("map", "bitm"),
    )

specular = Struct("specular",
    Bool16("specular flags",
        "overbright",
        "extra-shiny",
        "lightmap is specular"
        ),
    Pad(18),
    float_zero_to_one("brightness"),  # [0,1]

    Pad(20),
    QStruct("perpendicular color", INCLUDE=rgb_float),
    QStruct("parallel color",      INCLUDE=rgb_float),
    )

reflection = Struct("reflection",
    Bool16("reflection flags",
        "dynamic mirror",
         ),
    SEnum16("reflection type",
        "bumped cubemap",
        "flat cubemap",
        "bumped radiosity",
        ),

    float_zero_to_one("lightmap brightness scale"),  # [0,1]
    Pad(28),
    float_zero_to_one("perpendicular brightness"),  # [0,1]
    float_zero_to_one("parallel brightness"),  # [0,1]

    Pad(40),
    dependency("cube map", "bitm"),
    )

senv_attrs = Struct("senv attrs",
    #Environment Shader Properties
    environment_shader,

    #Lens Flare
    float_wu("lens flare spacing"),  # world units
    dependency("lens flare", "lens"),

    # this padding is the reflexive for the OS shader environment extension
    Pad(12),

    Pad(32),
    #Diffuse Properties
    diffuse,

    Pad(12),
    #Bump Properties
    bump_properties,

    Pad(16),
    #Texture Animation
    Struct("u-scrolling animation", INCLUDE=anim_func_per_sca),
    Struct("v-scrolling animation", INCLUDE=anim_func_per_sca),

    Pad(52),
    #Self Illumination
    self_illumination,

    Pad(24),
    #Specular Properties
    specular,

    Pad(16),
    #Reflection Properties
    reflection,
    SIZE=796
    )

senv_body = Struct("tagdata",
    shdr_attrs,
    senv_attrs,
    SIZE=836,
    )


def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=HekTag
    )
