#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.snd_ import Snd_Tag
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

sound_classes = (
    ("projectile_impact", 0),
    ("projectile_detonation", 1),

    ("weapon_fire", 4),
    ("weapon_ready", 5),
    ("weapon_reload", 6),
    ("weapon_empty", 7),
    ("weapon_charge", 8),
    ("weapon_overheat", 9),
    ("weapon_idle", 10),

    ("object_impacts", 13),
    ("particle_impacts", 14),
    ("slow_particle_impacts", 15),

    ("unit_footsteps", 18),
    ("unit_dialog", 19),

    ("vehicle_collision", 22),
    ("vehicle_engine", 23),

    ("device_door", 26),
    ("device_force_field", 27),
    ("device_machinery", 28),
    ("device_nature", 29),
    ("device_computers", 30),

    ("music", 32),
    ("ambient_nature", 33),
    ("ambient_machinery", 34),
    ("ambient_computers", 35),

    ("first_person_damage", 39),

    ("scripted_dialog_player", 44),
    ("scripted_effect", 45),
    ("scripted_dialog_other", 46),
    ("scripted_dialog_force_unspatialized", 47),

    ("game_event", 50),
    )

compression = SEnum16("compression",
    'none',
    'xbox_adpcm',
    'ima_adpcm',
    'ogg',
    TOOLTIP="""
IMA ADPCM is unsupported on pc, and is actually treated as
MS ADPCM, with an additional header on the data stream.
For all intents and purposes, "ima adpcm" is useless.
"""
    )

permutation = Struct('permutation',
    ascii_str32("name"),
    Float("skip_fraction"),
    Float("gain", DEFAULT=1.0),
    compression,
    SInt16("next_permutation_index", DEFAULT=-1),
    UInt32("sample_data_pointer", VISIBLE=False),
    UInt32("unknown", VISIBLE=False),  # always zero?
    UInt32("parent_tag_id", VISIBLE=False),
    # for ogg vorbis, this is the required length of the
    # decompression buffer. For "none" compression, this
    # mirrors samples.size
    FlUInt32("buffer_size", EDITABLE=False),
    UInt32("parent_tag_id2", VISIBLE=False),
    rawdata_ref("samples", max_size=4194304, widget=SoundSampleFrame),
    rawdata_ref("mouth_data", max_size=8192),
    rawdata_ref("subtitle_data", max_size=512),
    SIZE=124
    )

pitch_range = Struct('pitch_range',
    ascii_str32("name"),

    Float("natural_pitch"),
    QStruct("bend_bounds", INCLUDE=from_to),
    SInt16("actual_permutation_count"),
    Pad(2),
    Float("playback_rate", VISIBLE=False),
    SInt32("unknown1", VISIBLE=False, DEFAULT=-1),
    SInt32("unknown2", VISIBLE=False, DEFAULT=-1),

    reflexive("permutations", permutation, 256,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    SIZE=72,
    )


snd__body = Struct("tagdata",
    Bool32("flags",
        "fit_to_adpcm_blocksize",
        "split_long_sound_into_permutations"
        ),
    SEnum16("sound_class", *sound_classes),
    SEnum16("sample_rate",
        {NAME: "khz_22", GUI_NAME: "22kHz"},
        {NAME: "khz_44", GUI_NAME: "44kHz"},
        ),
    float_wu("minimum_distance"),
    float_wu("maximum_distance"),
    float_zero_to_one("skip_fraction"),

    #Randomization
    QStruct("random_pitch_bounds", INCLUDE=from_to),
    float_rad("inner_cone_angle"),  # radians
    float_rad("outer_cone_angle"),  # radians
    float_zero_to_one("outer_cone_gain"),
    Float("gain_modifier"),
    Float("maximum_bend_per_second"),
    Pad(12),

    QStruct("modifiers_when_scale_is_zero",
        Float("skip_fraction"),
        Float("gain"),
        Float("pitch"),
        ),
    Pad(12),

    QStruct("modifiers_when_scale_is_one",
        Float("skip_fraction"),
        Float("gain"),
        Float("pitch"),
        ),
    Pad(12),

    SEnum16("encoding",
        'mono',
        'stereo'
        ),
    compression,
    dependency("promotion_sound", "snd!"),
    SInt16("promotion_count"),
    Pad(2),
    FlUInt32("max_play_length", VISIBLE=False),
    Pad(8),
    FlUInt32("unknown1", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    FlUInt32("unknown2", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    reflexive("pitch_ranges", pitch_range, 8,
        DYN_NAME_PATH='.name'),

    SIZE=164,
    )


def get():
    return snd__def

snd__def = TagDef("snd!",
    blam_header('snd!', 4),
    snd__body,

    ext=".sound", endian=">", tag_cls=Snd_Tag,
    )

snd__meta_stub = desc_variant(
    snd__body, ("pitch_ranges", reflexive_struct)
    )
snd__meta_stub_blockdef = BlockDef(snd__meta_stub)
