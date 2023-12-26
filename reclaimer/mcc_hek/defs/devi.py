#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.devi import DeviTag
from supyr_struct.defs.tag_def import TagDef

devi_attrs = Struct("devi_attrs",
    Bool32("flags",
        "position_loops",
        "position_not_interpolated",
        ),

    float_sec("power_transition_time"),
    float_sec("power_acceleration_time"),
    float_sec("position_transition_time"),
    float_sec("position_acceleration_time"),
    float_sec("depowered_position_transition_time"),
    float_sec("depowered_position_acceleration_time"),

    SEnum16("A_in", *device_functions),
    SEnum16("B_in", *device_functions),
    SEnum16("C_in", *device_functions),
    SEnum16("D_in", *device_functions),

    dependency("open", valid_event_effects),
    dependency("close", valid_event_effects),
    dependency("opened", valid_event_effects),
    dependency("closed", valid_event_effects),
    dependency("depowered", valid_event_effects),
    dependency("repowered", valid_event_effects),

    float_sec("delay_time"),
    Pad(8),
    dependency("delay_effect", valid_event_effects),
    float_wu("automatic_activation_radius"),

    Pad(84),
    FlFloat("inv_power_acceleration_time"),
    FlFloat("inv_power_transition_time"),
    FlFloat("inv_depowered_acceleration_time"),
    FlFloat("inv_depowered_transition_time"),
    FlFloat("inv_position_acceleration_time"),
    FlFloat("inv_position_transition_time"),
    Pad(4),

    SIZE=276,
    )

devi_body = Struct('tagdata',
    devi_attrs,
    SIZE=276
    )

def get():
    return devi_def

devi_def = TagDef("devi",
    blam_header('devi'),
    devi_body,

    ext=".device", endian=">", tag_cls=DeviTag
    )
