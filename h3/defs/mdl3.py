############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	Mapped out value types
# revision: 3		author: Lord Zedd
# 	Updated and copypasted.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


mdl3_camera_refinement_zoom_data_1 = Struct("zoom_data_1", 
    h3_rawdata_ref("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


mdl3_camera_refinement_zoom_data_2 = Struct("zoom_data_2", 
    h3_rawdata_ref("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


mdl3_camera_refinement = Struct("camera_refinement", 
    h3_string_id("biped", VISIBLE=False),
    Array("unknown_array", SIZE=8, SUB_STRUCT=Float("unknown"), VISIBLE=False),
    h3_reflexive("zoom_data_1", mdl3_camera_refinement_zoom_data_1),
    h3_reflexive("zoom_data_2", mdl3_camera_refinement_zoom_data_2),
    VISIBLE=False,
    ENDIAN=">", SIZE=60
    )


mdl3_meta_def = BlockDef("mdl3", 
    Bool32("flags", *unknown_flags_32),
    h3_string_id("name"),
    SInt16("unknown", VISIBLE=False),
    SInt16("layer"),
    SInt16("widescreen_y_bounds_min"),
    SInt16("widescreen_x_bounds_min"),
    SInt16("widescreen_y_bounds_max"),
    SInt16("widescreen_x_bounds_max"),
    SInt16("standard_y_bounds_min"),
    SInt16("standard_x_bounds_min"),
    SInt16("standard_y_bounds_max"),
    SInt16("standard_x_bounds_max"),
    h3_dependency("animation"),
    h3_reflexive("camera_refinement", mdl3_camera_refinement),
    TYPE=Struct, ENDIAN=">", SIZE=56
    )