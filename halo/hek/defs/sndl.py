from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

detail_sound = Struct("detail sound",
    dependency("sound", "snd!"),
    from_to_sec('random period bounds'),
    BFloat("gain"),
    BBool32("flags",
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
    BBool32("flags",
        "fade in at start",
        "fade out at stop",
        "fade in alternate",
        ),
    BFloat("gain"),
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


sndl_body = Struct("tagdata",
    BBool32("flags",
        "deafening to ai",
        "not a loop",
        "stops music",
        ),
    BFloat("detail sound period at zero"),
    Pad(8),
    BFloat("detail sound period at one"),
    Pad(24),
    dependency("continuous damage effect", "cdmg"),

    reflexive("tracks", track, 4),
    reflexive("detail sounds", detail_sound, 32,
        DYN_NAME_PATH='.sound.filepath'),

    SIZE=84,
    )

    
def get():
    return sndl_def

sndl_def = TagDef("sndl",
    blam_header("sndl", 3),
    sndl_body,

    ext=".sound_looping", endian=">",
    )
