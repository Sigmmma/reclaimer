from ...common_descs import *
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
    BFloat("radius"),
    QStruct("radius modifier", INCLUDE=from_to),
    BFloat("falloff angle"),  # measured in radians
    BFloat("cutoff angle"),  # measured in radians
    BFloat("lens flare only radius"),
    Pad(24),

    #Color
    BBool32("interpolation flags", *blend_flags),
    QStruct("color lower bound", INCLUDE=argb_float),
    QStruct("color upper bound", INCLUDE=argb_float),
    Pad(12),

    #Gel
    Struct("gel map",
        dependency("primary cube map", valid_bitmaps),
        Pad(2),
        BSEnum16("texture animation function", *animation_functions),
        BFloat("texture animation period"),

        dependency("secondary cube map", valid_bitmaps),
        Pad(2),
        BSEnum16("yaw animation function", *animation_functions),
        BFloat("yaw animation period"),
        Pad(2),
        BSEnum16("roll animation function", *animation_functions),
        BFloat("roll animation period"),
        Pad(2),
        BSEnum16("pitch animation function", *animation_functions),
        BFloat("pitch animation period"),
        Pad(8)
        ),

    #Lens flare
    dependency("lens flare", valid_lens_flares),
    Pad(24),

    #Radiosity
    BFloat("intensity"),
    QStruct("color", INCLUDE=rgb_float),
    Pad(16),

    #Effect parameters
    BFloat("duration"),
    Pad(2),
    BSEnum16("falloff function", *fade_functions),

    SIZE=352,
    )

    
def get():
    return ligh_def

ligh_def = TagDef("ligh",
    blam_header("ligh", 3),
    ligh_body,

    ext=".light", endian=">",
    )
