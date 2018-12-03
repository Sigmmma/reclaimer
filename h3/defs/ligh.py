############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Standardizing
# revision: 3		author: Lehvak
# 	Mapped Bit 7
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


ligh_body = Struct("tagdata", 
    Bool32("flags", 
        ("no_shadow", 1 << 1),
        "only_render_in_first_person",
        "only_render_in_third_person",
        ("snap_to_first_person_camera_req_only_first_person", 1 << 7),
        ),
    SEnum16("type", *scnr_light_volume_type_1),
    SInt16("unknown_0", VISIBLE=False),
    Float("light_range"),
    Float("near_width"),
    Float("height_stretch"),
    float_rad("field_of_view"),
    h3_string_id("function_name_0"),
    h3_string_id("function_name_1"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_rawdata_ref("function_0"),
    h3_string_id("function_name_2"),
    h3_string_id("function_name_3"),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("unknown_5", VISIBLE=False),
    BytesRaw("unknown_6", SIZE=4, VISIBLE=False),
    h3_rawdata_ref("function_1"),
    h3_dependency("gel_map"),
    Array("unknown_array_0", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    Array("unknown_array_1", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_dependency("lens_flare"),
    ENDIAN=">", SIZE=148
    )


def get():
    return ligh_def

ligh_def = TagDef("ligh",
    h3_blam_header('ligh'),
    ligh_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["ligh"], endian=">", tag_cls=H3Tag
    )