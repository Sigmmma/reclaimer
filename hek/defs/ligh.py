from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

gel_comment = """The map tints the light per-pixel of cubemap."""

lens_flare_comment = """LENS FLARE
Optional lens flare associated with this light."""

radiosity_comment = """Controls how the light affects the lightmaps (ignored for dynamic lights)."""

effect_parameters_comment = """If the light is created by an effect, it will animate itself as follows."""

ligh_body = Struct("tagdata",
    Bool32("flags",
        "dynamic",
        "no specular",
        "dont light own object",
        "supersize in first person",
        "first person flashlight",
        "dont fade active camouflage",
        ),

    #Shape
    Struct("shape",
        Float("radius"),
        QStruct("radius modifier", INCLUDE=from_to),
        float_rad("falloff angle"),  # radians
        float_rad("cutoff angle"),  # radians
        Float("lens flare only radius"),
        Pad(24),
        ),

    #Color
    Struct("color",
        Bool32("interpolation flags", *blend_flags),
        QStruct("color lower bound", INCLUDE=argb_float),
        QStruct("color upper bound", INCLUDE=argb_float),
        Pad(12),
        ),

    #Gel
    Struct("gel map",
        dependency("primary cube map", "bitm"),
        Pad(2),
        SEnum16("texture animation function", *animation_functions),
        float_sec("texture animation period"),

        dependency("secondary cube map", "bitm"),
        Pad(2),
        SEnum16("yaw animation function", *animation_functions),
        float_sec("yaw animation period"),
        Pad(2),
        SEnum16("roll animation function", *animation_functions),
        float_sec("roll animation period"),
        Pad(2),
        SEnum16("pitch animation function", *animation_functions),
        float_sec("pitch animation period"),
        Pad(8),
        COMMENT=gel_comment
        ),

    #Lens flare
    dependency("lens flare", "lens", COMMENT=lens_flare_comment),
    Pad(24),

    #Radiosity
    Struct("radiosity",
        Float("intensity"),
        QStruct("color", INCLUDE=rgb_float),
        Pad(16),
        COMMENT=radiosity_comment
        ),

    #Effect parameters
    Struct("effect parameters",
        float_sec("duration"),
        Pad(2),
        SEnum16("falloff function", *fade_functions),
        COMMENT=effect_parameters_comment
        ),

    SIZE=352,
    )

    
def get():
    return ligh_def

ligh_def = TagDef("ligh",
    blam_header("ligh", 3),
    ligh_body,

    ext=".light", endian=">", tag_cls=HekTag,
    )
