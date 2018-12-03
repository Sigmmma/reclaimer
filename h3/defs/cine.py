############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


cine_scene_unknown = Struct("scene_unknown", 
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


cine_cinematic_scene = Struct("cinematic_scene", 
    h3_dependency("scene"),
    ENDIAN=">", SIZE=16
    )


cine_body = Struct("tagdata", 
    SInt32("unknown_0"),
    h3_reflexive("scene_unknown", cine_scene_unknown),
    h3_dependency("import_scenario"),
    SInt32("unknown_1"),
    h3_string_id("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt32("unknown_5"),
    Pad(20),
    SInt32("unknown_7"),
    Pad(12),
    SInt32("unknown_9"),
    h3_dependency("unknown_10"),
    h3_rawdata_ref("import_script_0"),
    h3_reflexive("cinematic_scenes", cine_cinematic_scene),
    h3_rawdata_ref("import_script_1"),
    h3_rawdata_ref("import_script_2"),
    ENDIAN=">", SIZE=176
    )


def get():
    return cine_def

cine_def = TagDef("cine",
    h3_blam_header('cine'),
    cine_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["cine"], endian=">", tag_cls=H3Tag
    )