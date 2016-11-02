from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

detail_sound = Struct("detail sound",
    dependency("sound", valid_sounds),
    QStruct('random period bounds', INCLUDE=from_to),
    BFloat("gain"),
    BBool32("flags",
        "dont play with alternate",
        "dont play without alternate",
        ),

    Pad(48),
    QStruct('yaw bounds', INCLUDE=from_to),  # radians
    QStruct('pitch bounds', INCLUDE=from_to),  # radians
    QStruct('distance bounds', INCLUDE=from_to),

    SIZE=104
    )

track = Struct("track",
    BBool32("flags",
        "fade in at start",
        "fade out at stop",
        "fade in alternate",
        ),
    BFloat("gain"),
    BFloat("fade in duration"),
    BFloat("fade out duration"),

    Pad(32),
    dependency("start", valid_sounds),
    dependency("loop", valid_sounds),
    dependency("end", valid_sounds),

    Pad(32),
    dependency("alternate loop", valid_sounds),
    dependency("alternate end", valid_sounds),
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
    dependency("continuous damage effect", valid_continuous_damages),

    reflexive("tracks", track, 4),
    reflexive("detail sounds", detail_sound, 32),

    SIZE=84,
    )

    
def get():
    return sndl_def

sndl_def = TagDef("sndl",
    blam_header("sndl", 3),
    sndl_body,

    ext=".sound_looping", endian=">",
    )
