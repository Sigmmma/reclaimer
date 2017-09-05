from .objs.magy import MagyTag
from ...hek.defs.antr import *

magy_body = Struct("tagdata",
    reflexive("objects",  object_desc, 4),
    reflexive("units",    unit_desc, 32, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapons_desc, 1),
    reflexive("vehicles", vehicle_desc, 1),
    reflexive("devices",  device_desc, 1),
    reflexive("unit damage", anim_enum_desc, 176),
    reflexive("fp animations", fp_animation_desc, 1),
    #i have no idea why they decided to cap it at 257 instead of 256....
    reflexive("sound references", sound_reference_desc, 257,
        DYN_NAME_PATH=".sound.filepath"),
    Float("limp body node radius"),
    Bool16("flags",
        "compress all animations",
        "force idle compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, 64, 256, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, 2048, 256, DYN_NAME_PATH=".name"),
    dependency_os("stock animation", valid_model_animations_yelo),
    SIZE=300,
    )


def get():
    return magy_def

magy_def = TagDef("magy",
    blam_header_os('magy', 0),
    magy_body,

    ext=".model_animations_yelo", endian=">", tag_cls=MagyTag
    )
