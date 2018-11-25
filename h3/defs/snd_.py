from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

snd_sound_class = (
    "projectile_impact",
    "projectile_detonation",
    "projectile_flyby",
    "projectile_detonation_lod",
    "weapon_fire",
    "weapon_ready",
    "weapon_reload",
    "weapon_empty",
    "weapon_charge",
    "weapon_overheat",
    "weapon_idle",
    "weapon_melee",
    "weapon_animation",
    "object_impacts",
    "particle_impacts",
    "weapon_fire_lod",
    "unused1_impacts",
    "unused2_impacts",
    "unit_footsteps",
    "unit_dialog",
    "unit_animation",
    "unit_unused",
    "vehicle_collision",
    "vehicle_engine",
    "vehicle_animation",
    "vehicle_engine_lod",
    "device_door",
    "device_unused0",
    "device_machinery",
    "device_stationary",
    "device_unused1",
    "device_unused2",
    "music",
    "ambient_nature",
    "ambient_machinery",
    "ambient_stationary",
    "huge_ass",
    "object_looping",
    "cinematic_music",
    "unknown_unused0",
    "unknown_unused1",
    "ambient_flock",
    "no_pad",
    "no_pad_stationary",
    "mission_unused0",
    "cortana_mission",
    "cortana_gravemind_channel",
    "mission_dialog",
    "cinematic_dialog",
    "scripted_cinematic_foley",
    "game_event",
    "ui",
    "test",
    "multilingual_test",
    )


snd__meta_def = BlockDef("snd!",
    Bool16("flags",
        "fit_to_adpcm_blocksize",
        "split_long_sound_into_permutations",
        ),
    SEnum8("sound_class", *snd_sound_class),
    SInt8("unknown"),
    SInt16("ugh_platform_codec_index"),
    SInt16("ugh_pitch_range_index"),
    SInt16("ugh_language_b_index"),
    SInt16("unknown_1"),
    SInt16("ugh_playback_parameter_index"),
    SInt16("ugh_scale_index"),
    SInt8("ugh_promotion_index"),
    SInt8("ugh_custom_playback_index"),
    SInt16("ugh_extra_info_index"),
    SInt32("unknown_2"),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding"),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )