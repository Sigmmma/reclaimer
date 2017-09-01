from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

detail_sound = Struct("detail sound",
    dependency("sound", "snd!"),
    from_to_sec('random period bounds'),
    Float("gain"),
    Bool32("flags",
        "dont play with alternate",
        "dont play without alternate",
        ),

    Pad(48),
    from_to_rad('yaw bounds'),  # radians
    from_to_rad('pitch bounds'),  # radians
    from_to_wu('distance bounds'),  # world units

    SIZE=104
    )

track = Struct("track",
    Bool32("flags",
        "fade in at start",
        "fade out at stop",
        "fade in alternate",
        ),
    Float("gain"),
    float_sec("fade in duration"),
    float_sec("fade out duration"),

    Pad(32),
    dependency("start", "snd!"),
    dependency("loop", "snd!"),
    dependency("end", "snd!"),

    Pad(32),
    dependency("alternate loop", "snd!"),
    dependency("alternate end", "snd!"),
    SIZE=160
    )


lsnd_body = Struct("tagdata",
    Bool32("flags",
        "deafening to ai",
        "not a loop",
        "stops music",
        ),
    Float("detail sound period at zero"),
    FlFloat("unknown0", DEFAULT=1.0, VISIBLE=False),
    FlFloat("unknown1", DEFAULT=1.0, VISIBLE=False),
    Float("detail sound period at one"),
    FlFloat("unknown2", DEFAULT=1.0, VISIBLE=False),
    FlFloat("unknown3", DEFAULT=1.0, VISIBLE=False),
    FlSInt16("unknown4", DEFAULT=-1, VISIBLE=False),
    FlSInt16("unknown5", DEFAULT=-1, VISIBLE=False),
    FlFloat("unknown6", DEFAULT=1.0, VISIBLE=False),
    Pad(8),
    dependency("continuous damage effect", "cdmg"),

    reflexive("tracks", track, 4),
    reflexive("detail sounds", detail_sound, 32,
        DYN_NAME_PATH='.sound.filepath'),

    SIZE=84,
    )

    
def get():
    return lsnd_def

lsnd_def = TagDef("lsnd",
    blam_header("lsnd", 3),
    lsnd_body,

    ext=".sound_looping", endian=">", tag_cls=HekTag,
    )
