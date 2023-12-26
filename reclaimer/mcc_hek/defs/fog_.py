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

fog_comment = """FLAGS
Setting <atmosphere dominant> prevents polygon popping when the atmospheric fog maximum
density (in the sky tag) is 1 and the atmospheric fog opaque distance is less than the
diameter of the map. However, this flag will cause artifacts when the camera goes below
the fog plane - so it should only be used when the fog plane is close to the ground."""

fog__body = Struct("tagdata",
    #fog flags
    Bool32("flags",
        "is_water",
        "atmospheric_dominant",
        "fog_screen_only",
        COMMENT=fog_comment
        ),

    Pad(84),
    #Density
    float_zero_to_one("maximum_density"),
    Pad(4),
    float_wu("opaque_distance"),
    Pad(4),
    float_wu("opaque_depth"),
    Pad(8),
    float_wu("distance_to_water_plane"),

    #Color
    QStruct("fog_color", INCLUDE=rgb_float),

    #Screen Layers
    Struct("screen_layers",
        Bool16("flags",
            "no_environment_multipass",
            "no_model_multipass",
            "no_texture_based_falloff",
            ),
        UInt16("layer_count", SIDETIP="[0,4]", MIN=0, MAX=4),

        from_to_wu("distance_gradient"),
        from_to_zero_to_one("density_gradient"),

        float_wu("start_distance_from_fog_plane"),
        Pad(4),

        #QStruct("color", INCLUDE=xrgb_byte),
        UInt32("color", INCLUDE=xrgb_uint32),
        float_zero_to_one("rotation_multiplier"),
        float_zero_to_one("strafing_multiplier"),
        float_zero_to_one("zoom_multiplier"),
        Pad(8),
        Float("map_scale"),
        dependency("fog_map", "bitm")
        ),

    #Screen Layer Animation
    Struct("screen_layer_animation",
        float_sec("animation_period"),
        Pad(4),
        from_to_wu_sec("wind_velocity"),
        from_to_sec("wind_period"),
        float_zero_to_one("wind_acceleration_weight"),
        float_zero_to_one("wind_perpendicular_weight")
        ),

    Pad(8),
    #Sound
    dependency("background_sound", "lsnd"),
    dependency("sound_environment", "snde"),
    SIZE=396,
    )

def get():
    return fog__def

fog__def = TagDef("fog ",
    blam_header('fog '),
    fog__body,

    ext=".fog", endian=">", tag_cls=HekTag
    )
