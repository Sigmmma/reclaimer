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

light_volume_comment = """LIGHT VOLUME
Draws a sequence of glow bitmaps along a line. Can be used for contrail-type effects
as well as volumetric lights."""

brightness_scale_comment = """BRIGHTNESS SCALE
Fades the effect in and out with distance, viewer angle and external source."""

bitmaps_comment = """BITMAPS
Bitmap tag used to draw the light volume, repeated <count> times. Default is
'tags\\rasterizer_textures\\glow'.
Note: Sprite plates are not valid for light volumes."""

frame_animation_comment = """FRAME ANIMATION
Frames are descriptions of the light volume at a particular point in time,
interpolated by an external source. For example: A bolt of energy can be made
to stretch out and grow thinner as it is fired from a weapon."""

frame = Struct("frame",
    Pad(16),
    float_wu("offset_from_marker"),
    Float("offset_exponent"),
    float_wu("length"),

    Pad(32),
    float_wu("radius_hither"),
    float_wu("radius_yon"),
    Float("radius_exponent"),

    Pad(32),
    QStruct("tint_color_hither", INCLUDE=argb_float),
    QStruct("tint_color_yon", INCLUDE=argb_float),
    Float("tint_color_exponent"),
    Float("brightness_exponent"),
    SIZE=176
    )

mgs2_body = Struct("tagdata",
    #Light volume
    ascii_str32("attachment_marker", COMMENT=light_volume_comment),
    Bool32("flags", *blend_flags),
    Pad(16),

    #Brightness scale
    float_wu("near_fade_distance", COMMENT=brightness_scale_comment),
    float_wu("far_fade_distance"),
    float_zero_to_one("perpendicular_brightness_scale"),
    float_zero_to_one("parallel_brightness_scale"),
    SEnum16("brightness_scale_source", *function_outputs),
    Pad(22),

    #Bitmaps
    dependency("map", "bitm", COMMENT=bitmaps_comment),
    SInt16("map_sequence_index"),
    SInt16("map_count"),
    Pad(72),

    #Frame animation
    SEnum16("frame_animation_source", *function_outputs, COMMENT=frame_animation_comment),
    Pad(102),

    reflexive("frames", frame, 2),

    SIZE=332,
    )


def get():
    return mgs2_def

mgs2_def = TagDef("mgs2",
    blam_header("mgs2"),
    mgs2_body,

    ext=".light_volume", endian=">", tag_cls=HekTag,
    )
