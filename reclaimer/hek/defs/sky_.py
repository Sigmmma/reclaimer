#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shader_function = Struct('shader_function',
    Pad(4),
    ascii_str32("global_function_name"),
    SIZE=36
    )

animation = Struct('animation',
    SInt16('animation_index'),
    Pad(2),
    float_sec("period"),
    SIZE=36
    )

light = Struct('light',
    dependency("lens_flare", "lens"),
    ascii_str32("global_function_name"),
    Pad(28),
    Bool32('flags',
        'affects_exteriors',
        'affects_interiors',
        ),
    QStruct("color", INCLUDE=rgb_float),
    Float("power"),
    Float("test_distance"),
    Pad(4),
    yp_float_rad("direction"),  # radians
    float_rad("diameter"),  # radians (yeah, it sounds weird, but this
    #                         value is stored as a radian coefficient)
    SIZE=116
    )


sky__body = Struct("tagdata",
    dependency("model", valid_models),
    dependency("animation_graph", "antr"),
    Pad(24),

    QStruct("indoor_ambient_radiosity_color", INCLUDE=rgb_float),
    Float("indoor_ambient_radiosity_power"),

    QStruct("outdoor_ambient_radiosity_color", INCLUDE=rgb_float),
    Float("outdoor_ambient_radiosity_power"),

    QStruct("outdoor_fog_color", INCLUDE=rgb_float),
    Pad(8),
    float_zero_to_one("outdoor_fog_maximum_density"),
    float_wu("outdoor_fog_start_distance"),
    float_wu("outdoor_fog_opaque_distance"),

    QStruct("indoor_fog_color", INCLUDE=rgb_float),
    Pad(8),
    float_zero_to_one("indoor_fog_maximum_density"),
    float_wu("indoor_fog_start_distance"),
    float_wu("indoor_fog_opaque_distance"),

    dependency("indoor_fog_screen", "fog "),
    Pad(4),
    reflexive("shader_functions", shader_function, 8,
        DYN_NAME_PATH='.global_function_name'),
    reflexive("animations", animation, 8),
    reflexive("lights", light, 8,
        DYN_NAME_PATH='.lens_flare.filepath'),

    SIZE=208,
    )


def get():
    return sky__def

sky__def = TagDef("sky ",
    blam_header('sky '),
    sky__body,

    ext=".sky", endian=">", tag_cls=HekTag,
    )
