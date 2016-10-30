from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

part_scale_modifiers = (
    "velocity",
    "velocity delta",
    "velocity cone angle",
    "angular velocity",
    "angular velocity delta",
    "type-specific scale"
    )

particle_scale_modifiers = (
    "velocity",
    "velocity delta",
    "velocity cone angle",
    "angular velocity",
    "angular velocity delta",
    "count",
    "count delta",
    "distribution radius",
    "distribution radius delta",
    "particle radius",
    "particle radius delta",
    "tint"
    )

create_in_env = BSEnum16("create in env",
    "any environment",
    "air only",
    "water only",
    "space only",
    )

create_in_mode = BSEnum16("create in mode",
    "either mode",
    "violent mode only",
    "nonviolent mode only",
    )

part = Struct("part",
    create_in_env,
    create_in_mode,
    BSInt16("location"),
    BBool16("flags",
        {NAME:"face_down", GUI_NAME:"face down regardless of location(decals)"}
        ),
    Pad(16),

    dependency("type", valid_effect_events),
    Pad(24),

    QStruct("velocity bounds", INCLUDE=from_to),
    BFloat("velocity cone angle"),  # radians
    QStruct("angular velocity bounds", INCLUDE=from_to),  # radians
    QStruct("radius modifier bounds", INCLUDE=from_to),

    BBool32("A scales values", *part_scale_modifiers),
    BBool32("B scales values", *part_scale_modifiers),
    SIZE=104,
    )

particle = Struct("particle",
    create_in_env,
    create_in_mode,
    BSEnum16("create in camera",
        "either",
        "first person only",
        "third person only",
        "first person if possible",
        ),
    Pad(2),
    BSInt16("location"),
    Pad(2),

    QStruct("relative direction", INCLUDE=yp_float),  # measured in radians
    QStruct("relative offset", INCLUDE=ijk_float),
    Pad(52),

    dependency("particle type", valid_particles),
    BBool32("flags",
        "stay attached to marker",
        "random initial angle",
        "tint from object color",
        {NAME: "tint_as_hsv", GUI_NAME: "interpolate tint as hsv"},
        {NAME: "use_long_hue_path", GUI_NAME: "...across the long hue path"},
        ),
    BSEnum16("distribution function",
        "start",
        "end",
        "constant",
        "buildup",
        "falloff",
        "buildup and falloff",
        ),
    Pad(2),

    QStruct("count", INCLUDE=from_to),
    QStruct("distribution radius", INCLUDE=from_to),
    Pad(12),

    QStruct("velocity", INCLUDE=from_to),
    BFloat("velocity cone angle"),  # measured in radians
    QStruct("angular velocity", INCLUDE=from_to),  # measured in radians
    Pad(8),

    QStruct("radius", INCLUDE=from_to),
    Pad(8),

    QStruct("tint lower bound", INCLUDE=argb_float),
    QStruct("tint upper bound", INCLUDE=argb_float),
    Pad(16),

    BBool32("A scales values", *particle_scale_modifiers),
    BBool32("B scales values", *particle_scale_modifiers),
    SIZE=232
    )


location = Struct("location",
    StrLatin1("marker name", SIZE=32),
    )

event = Struct("event",
    Pad(4),
    BFloat("skip fraction"),
    QStruct("delay bounds", INCLUDE=from_to),
    QStruct("duration bounds", INCLUDE=from_to),

    Pad(20),
    reflexive("parts", part, 32),
    reflexive("particles", particle, 32),
    SIZE=68
    )


effe_body = Struct("tagdata",
    BBool32("flags",
        {NAME: "deleted when inactive", GUI_NAME: "deleted when attachment deactivates"},
        {NAME: "required", GUI_NAME: "required for gameplay(cannot optimize)"},
        #'unknown'  # found only in map meta data
        ),
    BSInt16("loop start event"),
    BSInt16("loop stop event"),

    Pad(32),
    reflexive("locations", location, 32),
    reflexive("events", event, 32),

    SIZE=64,
    )

    
def get():
    return effe_def

effe_def = TagDef("effe",
    blam_header("effe", 4),
    effe_body,

    ext=".effect", endian=">",
    )
