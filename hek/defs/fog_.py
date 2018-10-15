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
        "is water",
        "atmospheric dominant",
        "fog screen only",
        COMMENT=fog_comment
        ),

    Pad(84),
    #Density
    float_zero_to_one("maximum density"),
    Pad(4),
    float_wu("opaque distance"),
    Pad(4),
    float_wu("opaque depth"),
    Pad(8),
    float_wu("distance to water plane"),

    #Color
    QStruct("fog color", INCLUDE=rgb_float),

    #Screen Layers
    Struct("screen layers",
        Bool16("flags",
            "no environment multipass",
            "no model multipass",
            "no texture-based falloff",
            ),
        UInt16("layer count", SIDETIP="[0,4]", MIN=0, MAX=4),

        from_to_wu("distance gradient"),
        from_to_zero_to_one("density gradient"),

        float_wu("start distance from fog plane"),
        Pad(4),

        #QStruct("color", INCLUDE=xrgb_byte),
        UInt32("color", INCLUDE=xrgb_uint32),
        float_zero_to_one("rotation multiplier"),
        float_zero_to_one("strafing multiplier"),
        float_zero_to_one("zoom multiplier"),
        Pad(8),
        Float("map scale"),
        dependency("fog map", "bitm")
        ),

    #Screen Layer Animation
    Struct("screen layer animation",
        float_sec("animation period"),
        Pad(4),
        from_to_wu_sec("wind velocity"),
        from_to_sec("wind period"),
        float_zero_to_one("wind acceleration weight"),
        float_zero_to_one("wind perpendicular weight")
        ),

    Pad(8),
    #Sound
    dependency("background sound", "lsnd"),
    dependency("sound environment", "snde"),
    SIZE=396,
    )

def get():
    return fog__def

fog__def = TagDef("fog ",
    blam_header('fog '),
    fog__body,

    ext=".fog", endian=">", tag_cls=HekTag
    )
