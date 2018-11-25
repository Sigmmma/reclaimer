from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

sncl_sound_classe_cache_miss_mode = (
    "discard",
    "postpone",
    )

sncl_sound_classe_stereo_playback_type = (
    "first_person",
    "ambient",
    )


sncl_sound_classe = Struct("sound_classes",
    SInt16("max_sounds_per_tag"),
    SInt16("max_sounds_per_object"),
    SInt32("preemption_time"),
    Bool16("internal_flags",
        "valid",
        "is_speech",
        "scripted",
        "stops_with_object",
        ("multilingual", 1 << 7),
        ),
    Bool16("flags",
        "plays_during_pause",
        "dry_stereo_mix",
        "no_object_obstruction",
        "use_center_speaker_unspatialized",
        "send_mono_to_lfe",
        "deterministic",
        "use_huge_transmission",
        "always_use_speakers",
        "don_t_strip_from_mainmenu",
        "ignore_stereo_headroom",
        ),
    SInt16("priority"),
    SEnum16("cache_miss_mode", *sncl_sound_classe_cache_miss_mode),
    Float("reverb_gain"),
    Pad(12),
    Float("unknown_1"),
    Float("unknown_2"),
    Pad(8),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("distance_bounds_min"),
    Float("distance_bounds_max"),
    Float("gain_bounds_min"),
    Float("gain_bounds_max"),
    Float("cutscene_ducking"),
    Float("cutscene_ducking_fade_in_time"),
    Float("cutscene_ducking_sustain"),
    Float("cutscene_ducking_fade_out_time"),
    Float("scripted_dialog_ducking"),
    Float("scripted_dialog_ducking_fade_in"),
    Pad(4),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Pad(4),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("doppler_factor"),
    SEnum8("stereo_playback_type", *sncl_sound_classe_stereo_playback_type),
    SInt8("unknown_14"),
    SInt8("unknown_15"),
    SInt8("unknown_16"),
    Float("transmission_multiplier"),
    Float("obstruction_max_bend"),
    Float("occlusion_max_bend"),
    SInt32("unknown_17"),
    ENDIAN=">", SIZE=152
    )


sncl_meta_def = BlockDef("sncl",
    reflexive("sound_classes", sncl_sound_classe),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )