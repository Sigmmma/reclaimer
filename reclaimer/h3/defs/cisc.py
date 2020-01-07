#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

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


cisc_puppet_unknown_2 = Struct("unknown_2",
    BytesRaw("unknown_0", SIZE=40, VISIBLE=False),
    h3_dependency("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=56
    )


cisc_puppet = Struct("puppet",
    ascii_str32("import_name"),
    h3_string_id("name"),
    h3_string_id("variant"),
    h3_dependency("puppet_animation"),
    h3_dependency("puppet_object"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    h3_rawdata_ref("import_script"),
    h3_reflexive("unknown_2", cisc_puppet_unknown_2),
    ENDIAN=">", SIZE=116
    )


cisc_shot_lighting = Struct("lighting",
    h3_dependency("cinematic_light"),
    SInt32("owner_puppet_index"),
    h3_string_id("marker"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_unknown_3_unknown_1 = Struct("unknown_1",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


cisc_shot_unknown_3 = Struct("unknown_3",
    BytesRaw("unknown_0", SIZE=32, VISIBLE=False),
    h3_reflexive("unknown_1", cisc_shot_unknown_3_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=44
    )


cisc_shot_sound = Struct("sound",
    h3_dependency("sound"),
    SInt32("frame"),
    Float("unknown_0", VISIBLE=False),
    h3_string_id("unknown_1"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    h3_string_id("unknown_3"),
    ENDIAN=">", SIZE=36
    )


cisc_shot_background_sound = Struct("background_sound",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    h3_dependency("sound"),
    SInt32("frame"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_effect = Struct("effect",
    h3_dependency("effect"),
    SInt32("frame"),
    h3_string_id("marker"),
    SInt32("owner_puppet_index"),
    ENDIAN=">", SIZE=28
    )


cisc_shot_function_value = Struct("value",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


cisc_shot_function = Struct("function",
    SInt32("owner_puppet_index"),
    h3_string_id("target_function_name"),
    h3_reflexive("values", cisc_shot_function_value),
    ENDIAN=">", SIZE=20
    )


cisc_shot_cortana_effect = Struct("cortana_effect",
    h3_dependency("effect"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


cisc_shot_import_script = Struct("import_script",
    SInt32("frame"),
    h3_rawdata_ref("import_script"),
    ENDIAN=">", SIZE=24
    )


cisc_shot_frame = Struct("frame",
    QStruct("position", INCLUDE=xyz_float),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Float("fov"),
    Bool32("flags",
        "enable_depth_of_field",
        ),
    Float("near_plane"),
    Float("far_plane"),
    Float("focal_depth"),
    Float("blur_amount"),
    ENDIAN=">", SIZE=68
    )


cisc_shot = Struct("shot",
    h3_rawdata_ref("opening_import_script"),
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    h3_reflexive("lighting", cisc_shot_lighting),
    h3_reflexive("unknown_3", cisc_shot_unknown_3),
    h3_reflexive("sounds", cisc_shot_sound),
    h3_reflexive("background_sounds", cisc_shot_background_sound),
    h3_reflexive("effects", cisc_shot_effect),
    h3_reflexive("functions", cisc_shot_function),
    h3_reflexive("cortana_effects", cisc_shot_cortana_effect),
    h3_reflexive("import_scripts", cisc_shot_import_script),
    h3_rawdata_ref("import_script"),
    SInt32("loaded_frame_count"),
    h3_reflexive("frames", cisc_shot_frame),
    ENDIAN=">", SIZE=164
    )


cisc_texture_camera_shot_frame = Struct("frame",
    SInt32("unknown", VISIBLE=False),
    QStruct("position", INCLUDE=xyz_float),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=8, VISIBLE=False),
    Float("fov"),
    Bool32("flags",
        "enable_depth_of_field",
        ),
    Float("near_plane"),
    Float("far_plane"),
    Float("focal_depth"),
    Float("blur_amount"),
    ENDIAN=">", SIZE=72
    )


cisc_texture_camera_shot = Struct("shot",
    h3_reflexive("frames", cisc_texture_camera_shot_frame),
    ENDIAN=">", SIZE=12
    )


cisc_texture_camera = Struct("texture_camera",
    h3_string_id("name"),
    h3_string_id("unknown"),
    h3_reflexive("shots", cisc_texture_camera_shot),
    ENDIAN=">", SIZE=20
    )


cisc_body = Struct("tagdata",
    h3_string_id("name"),
    ascii_str32("anchor_name"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_rawdata_ref("import_script_0"),
    h3_reflexive("puppets", cisc_puppet),
    h3_reflexive("shots", cisc_shot),
    h3_reflexive("texture_cameras", cisc_texture_camera),
    h3_rawdata_ref("import_script_1"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


def get():
    return cisc_def

cisc_def = TagDef("cisc",
    h3_blam_header('cisc'),
    cisc_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["cisc"], endian=">", tag_cls=H3Tag
    )
