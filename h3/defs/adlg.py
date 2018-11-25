from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

adlg_vocalization_perception_type = (
    "none",
    "speaker",
    "listener",
    )


adlg_vocalization_response = Struct("responses",
    string_id_meta("vocalization_name"),
    Bool16("flags",
        ),
    SInt16("vocalization_index"),
    SInt16("response_type"),
    SInt16("import_dialogue_index"),
    ENDIAN=">", SIZE=12
    )


adlg_vocalization = Struct("vocalizations",
    string_id_meta("vocalization"),
    SInt16("parent_index"),
    SInt16("priority"),
    Bool32("flags",
        ),
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
    string_id_meta("sample_line"),
    reflexive("responses", adlg_vocalization_response),
    ENDIAN=">", SIZE=92
    )


adlg_pattern = Struct("patterns",
    SInt16("dialogue_type"),
    SInt16("vocalizations_index"),
    string_id_meta("vocalization_name"),
    SInt16("speaker_type"),
    Bool16("flags",
        ),
    SInt16("hostility"),
    Bool16("unknown",
        ),
    SInt16("unknown_1"),
    SInt16("cause_type"),
    string_id_meta("cause_ai_type_name"),
    Pad(4),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("attitude"),
    SInt16("unknown_5"),
    Bool32("conditions",
        ),
    SInt16("spacial_relationship"),
    SInt16("damage_type"),
    SInt16("unknown_6"),
    SInt16("subject_type"),
    string_id_meta("subject_ai_type_name"),
    ENDIAN=">", SIZE=52
    )


adlg_dialog_data = Struct("dialog_data",
    SInt16("start_index"),
    SInt16("length"),
    ENDIAN=">", SIZE=4
    )


adlg_involuntary_data = Struct("involuntary_data",
    SInt16("involuntary_vocalization_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=4
    )


adlg_meta_def = BlockDef("adlg",
    Pad(16),
    reflexive("vocalizations", adlg_vocalization),
    reflexive("patterns", adlg_pattern),
    Pad(12),
    reflexive("dialog_data", adlg_dialog_data),
    reflexive("involuntary_data", adlg_involuntary_data),
    TYPE=Struct, ENDIAN=">", SIZE=76
    )