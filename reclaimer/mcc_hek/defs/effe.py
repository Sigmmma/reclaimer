#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.effe import EffeTag
from supyr_struct.defs.tag_def import TagDef

part_scale_modifiers = (
    "velocity",
    "velocity_delta",
    "velocity_cone_angle",
    "angular_velocity",
    "angular_velocity_delta",
    "type_specific_scale"
    )

particle_scale_modifiers = (
    "velocity",
    "velocity_delta",
    "velocity_cone_angle",
    "angular_velocity",
    "angular_velocity_delta",
    "count",
    "count_delta",
    "distribution_radius",
    "distribution_radius_delta",
    "particle_radius",
    "particle_radius_delta",
    "tint"
    )

create_in_env = SEnum16("create_in_env",
    "any_environment",
    "air_only",
    "water_only",
    "space_only",
    )

create_in_mode = SEnum16("create_in_mode",
    "either_mode",
    "violent_mode_only",
    "nonviolent_mode_only",
    )

part = Struct("part",
    create_in_env,
    create_in_mode,
    dyn_senum16("location",
        DYN_NAME_PATH="........locations.locations_array[DYN_I].marker_name"),
    Bool16("flags",
        {NAME:"face_down", GUI_NAME:"face down regardless of location(decals)"}
        ),
    Pad(12),

    UEnum32("effect_class", INCLUDE=valid_tags_os, VISIBLE=False),
    dependency("type", valid_effect_events),
    Pad(24),

    from_to_wu_sec("velocity_bounds"),  # world units/sec
    float_rad("velocity_cone_angle"),  # radians
    from_to_rad_sec("angular_velocity_bounds"),  # radians/sec
    QStruct("radius_modifier_bounds"),

    Bool32("A_scales_values", *part_scale_modifiers),
    Bool32("B_scales_values", *part_scale_modifiers),
    SIZE=104,
    )

particle = Struct("particle",
    create_in_env,
    create_in_mode,
    SEnum16("create_in_camera",
        "either",
        "first_person_only",
        "third_person_only",
        "first_person_if_possible",
        ),
    FlSInt16("unknown0", VISIBLE=False),
    dyn_senum16("location",
        DYN_NAME_PATH="........locations.locations_array[DYN_I].marker_name"),
    FlSInt16("unknown1", VISIBLE=False),

    yp_float_rad("relative_direction"),  # radians
    QStruct("relative_offset", INCLUDE=ijk_float),
    QStruct("relative_direction_vector", INCLUDE=xyz_float, VISIBLE=False),
    Pad(40),

    dependency("particle_type", "part"),
    Bool32("flags",
        "stay_attached_to_marker",
        "random_initial_angle",
        "tint_from_object_color",
        {NAME: "tint_as_hsv", GUI_NAME: "interpolate tint as hsv"},
        {NAME: "use_long_hue_path", GUI_NAME: "...across the long hue path"},
        ),
    SEnum16("distribution_function",
        "start",
        "end",
        "constant",
        "buildup",
        "falloff",
        "buildup_and_falloff",
        ),
    Pad(2),

    QStruct("created_count",
        SInt16("from", GUI_NAME=""),
        SInt16("to"), ORIENT='h'
        ),
    from_to_wu("distribution_radius"),
    Pad(12),

    from_to_wu_sec("velocity"),
    float_rad("velocity_cone_angle"),  # radians
    from_to_rad_sec("angular_velocity"),  # radians
    Pad(8),

    from_to_wu("radius"),
    Pad(8),

    QStruct("tint_lower_bound", INCLUDE=argb_float),
    QStruct("tint_upper_bound", INCLUDE=argb_float),
    Pad(16),

    Bool32("A_scales_values", *particle_scale_modifiers),
    Bool32("B_scales_values", *particle_scale_modifiers),
    SIZE=232
    )


location = Struct("location",
    ascii_str32("marker_name"),
    )

event = Struct("event",
    Pad(4),
    Float("skip_fraction"),
    from_to_sec("delay_bounds"),
    from_to_sec("duration_bounds"),

    Pad(20),
    reflexive("parts", part, 32, DYN_NAME_PATH='.type.filepath'),
    reflexive("particles", particle, 32, DYN_NAME_PATH='.particle_type.filepath'),
    SIZE=68
    )


effe_body = Struct("tagdata",
    Bool32("flags",
        {NAME: "deleted_when_inactive", GUI_NAME: "deleted when attachment deactivates"},
        {NAME: "required", GUI_NAME: "required for gameplay (cannot optimize out)"},
        {NAME: "never_cull", VISIBLE: VISIBILITY_HIDDEN}
        ),
    dyn_senum16("loop_start_event",
        DYN_NAME_PATH=".events.events_array[DYN_I].NAME"),
    dyn_senum16("loop_stop_event",
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

    ext=".effect", endian=">", tag_cls=EffeTag,
    )
