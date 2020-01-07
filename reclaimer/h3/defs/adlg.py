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
# revision: 2		author: DeadCanadian
# 	naming stuff
# revision: 3		author: OrangeMohawk
# 	Responses/Indexes
# revision: 4		author: Lord Zedd
# 	Updates and corrections
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

adlg_vocalization_perception_type = (
    "none",
    "speaker",
    "listener",
    )


adlg_vocalization_response = Struct("response",
    h3_string_id("vocalization_name"),
    Bool16("flags", *unknown_flags_16),
    SInt16("vocalization_index"),
    SInt16("response_type"),
    SInt16("import_dialogue_index"),
    ENDIAN=">", SIZE=12
    )


adlg_vocalization = Struct("vocalization",
    h3_string_id("vocalization"),
    SInt16("parent_index"),
    SInt16("priority"),
    Bool32("flags", *unknown_flags_32),
    SInt16("glance_behavior"),
    SInt16("glance_recipient"),
    SEnum16("perception_type", *adlg_vocalization_perception_type),
    SInt16("max_combat_status"),
    SInt16("animation_impulse"),
    SInt16("overlap_priority"),
    Float("sound_repetition_delay"),
    Float("allowable_queue_delay"),
    Float("pre_vocalization_delay"),
    Float("notification_delay"),
    Float("post_vocalization_delay"),
    Float("repeat_delay"),
    Float("weight"),
    Float("speaker_freeze_time"),
    Float("listener_freeze_time"),
    SInt16("speaker_emotion"),
    SInt16("listener_emotion"),
    Float("skip_fraction1"),
    Float("skip_fraction2"),
    Float("skip_fraction3"),
    h3_string_id("sample_line"),
    h3_reflexive("responses", adlg_vocalization_response),
    ENDIAN=">", SIZE=92
    )


adlg_pattern = Struct("pattern",
    SInt16("dialogue_type"),
    SInt16("vocalizations_index"),
    h3_string_id("vocalization_name"),
    SInt16("speaker_type"),
    Bool16("flags", *unknown_flags_16),
    SInt16("hostility"),
    Bool16("unknown_0", *unknown_flags_16),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("cause_type"),
    h3_string_id("cause_ai_type_name"),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("attitude"),
    SInt16("unknown_5", VISIBLE=False),
    Bool32("conditions", *unknown_flags_32),
    SInt16("spacial_relationship"),
    SInt16("damage_type"),
    SInt16("unknown_6", VISIBLE=False),
    SInt16("subject_type"),
    h3_string_id("subject_ai_type_name"),
    ENDIAN=">", SIZE=52
    )


adlg_dialog_data = Struct("dialog_data",
    SInt16("start_index"),
    SInt16("length"),
    ENDIAN=">", SIZE=4
    )


adlg_involuntary_data = Struct("involuntary_data",
    SInt16("involuntary_vocalization_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


adlg_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=16, VISIBLE=False),
    h3_reflexive("vocalizations", adlg_vocalization),
    h3_reflexive("patterns", adlg_pattern),
    BytesRaw("unknown_1", SIZE=12, VISIBLE=False),
    h3_reflexive("dialog_data", adlg_dialog_data),
    h3_reflexive("involuntary_data", adlg_involuntary_data),
    ENDIAN=">", SIZE=76
    )


def get():
    return adlg_def

adlg_def = TagDef("adlg",
    h3_blam_header('adlg'),
    adlg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["adlg"], endian=">", tag_cls=H3Tag
    )
