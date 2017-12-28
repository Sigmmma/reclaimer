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
    float_wu("offset from marker"),
    Float("offset exponent"),
    float_wu("length"),

    Pad(32),
    float_wu("radius hither"),
    float_wu("radius yon"),
    Float("radius exponent"),

    Pad(32),
    QStruct("tint color hither", INCLUDE=argb_float),
    QStruct("tint color yon", INCLUDE=argb_float),
    Float("tint color exponent"),
    Float("brightness exponent"),
    SIZE=176
    )

mgs2_body = Struct("tagdata",
    #Light volume
    ascii_str32("attachment marker", COMMENT=light_volume_comment),
    Bool32("flags", *blend_flags),
    Pad(16),

    #Brightness scale
    float_wu("near fade distance", COMMENT=brightness_scale_comment),
    float_wu("far fade distance"),
    float_zero_to_one("perpendicular brightness scale"),
    float_zero_to_one("parallel brightness scale"),
    SEnum16("brightness scale source", *function_outputs),
    Pad(22),

    #Bitmaps
    dependency("map", "bitm", COMMENT=bitmaps_comment),
    SInt16("sequence index"),
    SInt16("count"),
    Pad(72),

    #Frame animation
    SEnum16("frame animation source", *function_outputs, COMMENT=frame_animation_comment),
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
