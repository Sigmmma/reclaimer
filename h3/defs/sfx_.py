from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


sfx_sound_effect_filter = Struct("filter",
    SInt32("filter_type"),
    SInt32("filter_width"),
    Pad(64),
    ENDIAN=">", SIZE=72
    )


sfx_sound_effect_pitch_lfo = Struct("pitch_lfo",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


sfx_sound_effect_filter_lfo = Struct("filter_lfo",
    Pad(64),
    ENDIAN=">", SIZE=48
    )


sfx_sound_effect_sound_effect_component = Struct("components",
    dependency("sound"),
    Pad(4),
    SInt32("flags"),
    ENDIAN=">", SIZE=24
    )


sfx_sound_effect_sound_effect_template_collection_parameter = Struct("parameters",
    string_id_meta("name"),
    Pad(20),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=44
    )


sfx_sound_effect_sound_effect_template_collection = Struct("template_collection",
    string_id_meta("dsp_effect"),
    reflexive("parameters", sfx_sound_effect_sound_effect_template_collection_parameter),
    ENDIAN=">", SIZE=16
    )


sfx_sound_effect_sound_effect = Struct("sound_effect",
    dependency("unknown"),
    reflexive("components", sfx_sound_effect_sound_effect_component),
    reflexive("template_collection", sfx_sound_effect_sound_effect_template_collection),
    Pad(32),
    ENDIAN=">", SIZE=72
    )


sfx_sound_effect = Struct("sound_effects",
    string_id_meta("name"),
    Pad(12),
    Bool32("flags",
        "use_3d_radio_hack",
        ),
    Pad(8),
    reflexive("filter", sfx_sound_effect_filter),
    reflexive("pitch_lfo", sfx_sound_effect_pitch_lfo),
    reflexive("filter_lfo", sfx_sound_effect_filter_lfo),
    reflexive("sound_effect", sfx_sound_effect_sound_effect),
    ENDIAN=">", SIZE=76
    )


sfx__meta_def = BlockDef("sfx+",
    reflexive("sound_effects", sfx_sound_effect),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )
