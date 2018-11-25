from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


mdlg_line_variant = Struct("variants",
    string_id_meta("variant_designation"),
    dependency("sound"),
    string_id_meta("sound_effect"),
    ENDIAN=">", SIZE=24
    )


mdlg_line = Struct("lines",
    string_id_meta("name"),
    reflexive("variants", mdlg_line_variant),
    string_id_meta("default_sound_effect"),
    ENDIAN=">", SIZE=20
    )


mdlg_meta_def = BlockDef("mdlg",
    reflexive("lines", mdlg_line),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )