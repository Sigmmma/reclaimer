#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.ligh import LighTag
from supyr_struct.defs.tag_def import TagDef

gel_comment = """The map tints the light per-pixel of cubemap."""

lens_flare_comment = """LENS FLARE
Optional lens flare associated with this light."""

radiosity_comment = """Controls how the light affects the lightmaps (ignored for dynamic lights)."""

effect_parameters_comment = """If the light is created by an effect, it will animate itself as follows."""

ligh_body = Struct("tagdata",
    Bool32("flags",
        "dynamic",
        "no_specular",
        "dont_light_own_object",
        "supersize_in_first_person",
        "first_person_flashlight",
        "dont_fade_active_camouflage",
        ),

    #Shape
    Struct("shape",
        Float("radius"),
        QStruct("radius_modifier", INCLUDE=from_to),
        float_rad("falloff_angle"),  # radians
        float_rad("cutoff_angle"),  # radians
        Float("lens_flare_only_radius"),
        Float("cosine_falloff_angle", VISIBLE=False),
        Float("cosine_cutoff_angle", VISIBLE=False),
        Float("unknown", VISIBLE=False),
        Float("sine_cutoff_angle", VISIBLE=False),
        Pad(8),
        ),

    #Color
    Struct("color",
        Bool32("interpolation_flags", *blend_flags),
        QStruct("color_lower_bound", INCLUDE=argb_float),
        QStruct("color_upper_bound", INCLUDE=argb_float),
        Pad(12),
        ),

    #Gel
    Struct("gel_map",
        dependency("primary_cube_map", "bitm"),
        Pad(2),
        SEnum16("texture_animation_function", *animation_functions),
        float_sec("texture_animation_period"),

        dependency("secondary_cube_map", "bitm"),
        Pad(2),
        SEnum16("yaw_animation_function", *animation_functions),
        float_sec("yaw_animation_period"),
        Pad(2),
        SEnum16("roll_animation_function", *animation_functions),
        float_sec("roll_animation_period"),
        Pad(2),
        SEnum16("pitch_animation_function", *animation_functions),
        float_sec("pitch_animation_period"),
        Pad(8),
        COMMENT=gel_comment
        ),

    #Lens flare
    dependency("lens_flare", "lens", COMMENT=lens_flare_comment),
    Pad(24),

    #Radiosity
    Struct("radiosity",
        Float("intensity"),
        QStruct("color", INCLUDE=rgb_float),
        Pad(16),
        COMMENT=radiosity_comment
        ),

    #Effect parameters
    Struct("effect_parameters",
        float_sec("duration"),
        Pad(2),
        SEnum16("falloff_function", *fade_functions),
        COMMENT=effect_parameters_comment
        ),

    SIZE=352,
    )


def get():
    return ligh_def

ligh_def = TagDef("ligh",
    blam_header("ligh", 3),
    ligh_body,

    ext=".light", endian=">", tag_cls=LighTag,
    )
