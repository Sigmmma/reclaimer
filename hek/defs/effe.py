from ...common_descs import *
from .objs.tag import HekTag
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
    dyn_senum16("location",
        DYN_NAME_PATH="........locations.locations_array[DYN_I].marker_name"),
    BBool16("flags",
        {NAME:"face_down", GUI_NAME:"face down regardless of location(decals)"}
        ),
    Pad(12),

    BUEnum32("effect class", INCLUDE=valid_tags_os, VISIBLE=False),
    dependency("type", valid_effect_events),
    Pad(24),

    from_to_wu_sec("velocity bounds"),  # world units/sec
    float_rad("velocity cone angle"),  # radians
    from_to_rad_sec("angular velocity bounds"),  # radians/sec
    QStruct("radius modifier bounds"),

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
    dyn_senum16("location",
        DYN_NAME_PATH="........locations.locations_array[DYN_I].marker_name"),
    Pad(2),

    yp_float_rad("relative direction"),  # radians
    QStruct("relative offset", INCLUDE=ijk_float),
    Pad(52),

    dependency("particle type", "part"),
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

    QStruct("count",
        BSInt16("from", GUI_NAME=""),
        BSInt16("to"), ORIENT='h'
        ),
    from_to_wu("distribution radius"),
    Pad(12),

    from_to_wu_sec("velocity"),
    float_rad("velocity cone angle"),  # radians
    from_to_rad_sec("angular velocity"),  # radians
    Pad(8),

    from_to_wu("radius"),
    Pad(8),

    QStruct("tint lower bound", INCLUDE=argb_float),
    QStruct("tint upper bound", INCLUDE=argb_float),
    Pad(16),

    BBool32("A scales values", *particle_scale_modifiers),
    BBool32("B scales values", *particle_scale_modifiers),
    SIZE=232
    )


location = Struct("location",
    ascii_str32("marker name"),
    )

event = Struct("event",
    Pad(4),
    BFloat("skip fraction"),
    from_to_sec("delay bounds"),
    from_to_sec("duration bounds"),

    Pad(20),
    reflexive("parts", part, 32, DYN_NAME_PATH='.type.filepath'),
    reflexive("particles", particle, 32, DYN_NAME_PATH='.particle_type.filepath'),
    SIZE=68
    )


effe_body = Struct("tagdata",
    BBool32("flags",
        {NAME: "deleted when inactive", GUI_NAME: "deleted when attachment deactivates"},
        {NAME: "required", GUI_NAME: "required for gameplay(cannot optimize)"},
        #'unknown'  # found only in map meta data
        ),
    dyn_senum16("loop start event",
        DYN_NAME_PATH=".events.events_array[DYN_I].NAME"),
    dyn_senum16("loop stop event",
        DYN_NAME_PATH=".events.events_array[DYN_I].NAME"),

    Pad(32),
    reflexive("locations", location, 32, DYN_NAME_PATH='.marker_name'),
    reflexive("events", event, 32),

    SIZE=64,
    )

    
def get():
    return effe_def

effe_def = TagDef("effe",
    blam_header("effe", 4),
    effe_body,

    ext=".effect", endian=">", tag_cls=HekTag,
    )
