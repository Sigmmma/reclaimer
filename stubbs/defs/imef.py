from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from ..common_descs import *

unknown_float_struct = Struct("unknown float struct",
    # f0 and f1 sum to 1.0
    Struct("floats", Float("f0"), Float("f1"), ORIENT='h'),
    Struct("color", INCLUDE=rgb_float),
    )

stage = Struct("stage",
    Pad(32),
    SInt32("unknown0"),
    Struct("unknown-animation", INCLUDE=anim_src_func_per_pha_sca),

    Struct("unknown1", Float("f0"), Float("f1"), ORIENT='h'),
    dependency_stubbs("bitmap", "bitm"),

    Pad(32),
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
    SIZE=164
    )

floats_9 = tuple(Float("unknown" + str(i)) for i in range(9))
floats_7 = tuple(Float("unknown" + str(i)) for i in range(7))

imef_body = Struct("tagdata",
    Struct("unknown floats0", *floats_9),
    Struct("color0", INCLUDE=rgb_float),
    Struct("color1", INCLUDE=rgb_float),
    Struct("unknown-animation0", INCLUDE=anim_src_func_per_pha_sca),
    Pad(4),
    Struct("unknown struct1", INCLUDE=unknown_float_struct),
    Struct("unknown floats1", *floats_9),
    Struct("color2", INCLUDE=rgb_float),
    Struct("unknown struct2", INCLUDE=unknown_float_struct),
    Struct("unknown floats2", *floats_7),
    SInt16("unknown0"),
    Struct("unknown-animation1", INCLUDE=anim_src_func_per_pha_sca),
    Struct("unknown floats3", *floats_7),

    Pad(156),
    reflexive("stages", stage, OFFSET=416),
    SIZE=428
    )

def get():
    return imef_def

imef_def = TagDef("imef",
    blam_header_os('imef', 1),
    imef_body,

    ext=".image_effect", endian=">"
    )
