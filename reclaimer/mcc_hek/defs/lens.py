#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.lens import LensTag
from supyr_struct.defs.tag_def import TagDef

occlusion_comment = """Occlusion factor affects overall lens flare brightness and can also affect scale.
Occlusion never affects rotation."""

corona_rotation_comment = """Controls how corona rotation is affected by the viewer and light angles."""

reflection = Struct("reflection",
    Bool16("flags",
        "align_rotation_with_screen_center",
        "radius_not_scaled_by_distance",
        "radius_scaled_by_occlusion_factor",
        "occluded_by_solid_objects",
        ),
    Pad(2),
    SInt16("bitmap_index"),
    Pad(22),
    Float("position", SIDETIP="along flare axis"), # along flare axis
    float_deg("rotation_offset"), # degrees
    Pad(4),
    from_to_wu("radius"),  # world units
    SEnum16("radius_scaled_by",
        "none",
        "rotation",
        "rotation_and_strafing",
        "distance_from_center",
        ),
    Pad(2),
    from_to_zero_to_one("brightness"),  # [0,1]
    SEnum16("brightness_scaled_by",
        "none",
        "rotation",
        "rotation_and_strafing",
        "distance_from_center",
        ),
    Pad(2),

    #Tint color
    QStruct("tint_color", INCLUDE=argb_float),

    #Animation
    Struct("animation",
        QStruct("color_lower_bound", INCLUDE=argb_float),
        QStruct("color_upper_bound", INCLUDE=argb_float),
        Bool16("flags", *blend_flags),
        SEnum16("function", *animation_functions),
        float_sec("period"),  # seconds
        float_sec("phase"),  # seconds
        ),

    SIZE=128
    )


lens_body = Struct("tagdata",
    float_rad("falloff_angle"),  # radians
    float_rad("cutoff_angle"),  # radians
    FlFloat("cosine_falloff_angle", VISIBLE=False),
    FlFloat("cosine_cutoff_angle", VISIBLE=False),
    Struct("occlusion",
        float_wu("radius"),
        SEnum16("offset_direction",
            "toward_viewer",
            "marker_forward",
            "none",
            ),
        Pad(2),
        float_wu("near_fade_distance"),
        float_wu("far_fade_distance"),
	    COMMENT=occlusion_comment
        ),

    Struct("bitmaps",
        dependency("bitmap", "bitm"),
        Bool16("flags",
            "sun",
            ),
        Pad(78),
        ),

    Struct("corona_rotation",
        SEnum16("function",
            "none",
            "rotation_a",
            "rotation_b",
            "rotation_translation",
            "translation",
            ),
        Pad(2),
        float_rad("function_scale"),  # radians
		COMMENT=corona_rotation_comment
        ),

    Struct("corona_radius_scale",
        Pad(24),
        Float("horizontal_scale"),
        Float("vertical_scale"),
        ),

    Pad(28),

    reflexive("reflections", reflection, 32),

    SIZE=240,
    )


def get():
    return lens_def

lens_def = TagDef("lens",
    blam_header("lens", 2),
    lens_body,

    ext=".lens_flare", endian=">", tag_cls=LensTag,
    )
