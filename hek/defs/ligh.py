from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

ligh_body = Struct("tagdata",
    BBool32("flags",
        "dynamic",
        "no specular",
        "dont light own object",
        "supersize in first person",
        "first person flashlight",
        "dont fade active camouflage",
        ),

    #Shape
    Struct("shape",
        BFloat("radius"),
        QStruct("radius modifier", INCLUDE=from_to),
        float_rad("falloff angle"),  # radians
        float_rad("cutoff angle"),  # radians
        BFloat("lens flare only radius"),
        Pad(24),
        ),

    #Color
    Struct("color",
        BBool32("interpolation flags", *blend_flags),
        QStruct("color lower bound", INCLUDE=argb_float),
        QStruct("color upper bound", INCLUDE=argb_float),
        Pad(12),
        ),

    #Gel
    Struct("gel map",
        dependency("primary cube map", "bitm"),
        Pad(2),
        BSEnum16("texture animation function", *animation_functions),
        float_sec("texture animation period"),

        dependency("secondary cube map", "bitm"),
        Pad(2),
        BSEnum16("yaw animation function", *animation_functions),
        float_sec("yaw animation period"),
        Pad(2),
        BSEnum16("roll animation function", *animation_functions),
        float_sec("roll animation period"),
        Pad(2),
        BSEnum16("pitch animation function", *animation_functions),
        float_sec("pitch animation period"),
        Pad(8)
        ),

    #Lens flare
    dependency("lens flare", "lens"),
    Pad(24),

    #Radiosity
    Struct("radiosity",
        BFloat("intensity"),
        QStruct("color", INCLUDE=rgb_float),
        Pad(16),
        ),

    #Effect parameters
    Struct("effect parameters",
        float_sec("duration"),
        Pad(2),
        BSEnum16("falloff function", *fade_functions),
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
