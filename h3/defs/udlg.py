from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


udlg_vocalization = Struct("vocalizations",
    Bool16("flags",
        "new_vocalization",
        ),
    SInt16("unknown"),
    string_id_meta("vocalization"),
    dependency("sound"),
    ENDIAN=">", SIZE=24
    )


udlg_meta_def = BlockDef("udlg",
    dependency("global_dialogue_info"),
    Bool32("flags",
        "female",
        ),
    reflexive("vocalizations", udlg_vocalization),
    string_id_meta("mission_dialogue_designator"),
    TYPE=Struct, ENDIAN=">", SIZE=36
    )