############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: -DeToX-
# 	Mapped plugin structure a new.
# revision: 2		author: Lord Zedd
# 	thx h2
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


mdlg_line_variant = Struct("variant", 
    h3_string_id("variant_designation"),
    h3_dependency("sound"),
    h3_string_id("sound_effect"),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


mdlg_line = Struct("line", 
    h3_string_id("name"),
    h3_reflexive("variants", mdlg_line_variant),
    h3_string_id("default_sound_effect"),
    ENDIAN=">", SIZE=20
    )


mdlg_meta_def = BlockDef("mdlg", 
    h3_reflexive("lines", mdlg_line),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )