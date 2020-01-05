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
# revision: 2		author: Lord Zedd
# 	Copypasta H2.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

sncl_sound_classe_cache_miss_mode = (
    "discard",
    "postpone",
    )

sncl_sound_classe_stereo_playback_type = (
    "first_person",
    "ambient",
    )


sncl_sound_classe = Struct("sound_classe",
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
        "dont_strip_from_mainmenu",
        "ignore_stereo_headroom",
        ),
    SInt16("priority"),
    SEnum16("cache_miss_mode", *sncl_sound_classe_cache_miss_mode),
    Float("reverb_gain"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=8, VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    Float("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    QStruct("distance_bounds", INCLUDE=from_to),
    QStruct("gain_bounds", INCLUDE=from_to),
    Float("cutscene_ducking"),
    Float("cutscene_ducking_fade_in_time"),
    Float("cutscene_ducking_sustain"),
    Float("cutscene_ducking_fade_out_time"),
    Float("scripted_dialog_ducking"),
    Float("scripted_dialog_ducking_fade_in"),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    Float("unknown_8", VISIBLE=False),
    Float("unknown_9", VISIBLE=False),
    Float("unknown_10", VISIBLE=False),
    BytesRaw("unknown_11", SIZE=4, VISIBLE=False),
    Float("unknown_12", VISIBLE=False),
    Float("unknown_13", VISIBLE=False),
    Float("doppler_factor"),
    SEnum8("stereo_playback_type", *sncl_sound_classe_stereo_playback_type),
    SInt8("unknown_14", VISIBLE=False),
    SInt8("unknown_15", VISIBLE=False),
    SInt8("unknown_16", VISIBLE=False),
    Float("transmission_multiplier"),
    Float("obstruction_max_bend"),
    Float("occlusion_max_bend"),
    SInt32("unknown_17", VISIBLE=False),
    ENDIAN=">", SIZE=152
    )


sncl_body = Struct("tagdata",
    h3_reflexive("sound_classes", sncl_sound_classe),
    ENDIAN=">", SIZE=12
    )


def get():
    return sncl_def

sncl_def = TagDef("sncl",
    h3_blam_header('sncl'),
    sncl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sncl"], endian=">", tag_cls=H3Tag
    )
