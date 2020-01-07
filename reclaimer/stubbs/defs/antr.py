#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.antr import *
from ..common_descs import *

# As meta, it seems MOST arrays of anim_enum_desc have an extra extra on the end

animations_extended_desc = Struct("weapon_types",
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=28,
    )

unit_weapon_desc = Struct("weapon",
    ascii_str32("name"),
    ascii_str32("grip_marker"),
    ascii_str32("hand_marker"),
    #Aiming screen bounds

    Pad(32),
    #pitch and yaw are saved in radians.
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    reflexive("animations_extended", animations_extended_desc),
    reflexive("ik_points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon_types", weapon_types_desc, DYN_NAME_PATH=".label"),
    SIZE=188,
    )

label_desc = Struct("label",
    ascii_str32("label"),
    SIZE=32
    )

unknown_unit_desc = Struct("unknown_unit_desc",
    SInt32("unknown0"),
    SInt32("unknown1"),
    ascii_str32("label"),
    reflexive("labels", label_desc),
    reflexive("animations", anim_enum_desc),
    SIZE=64
    )

unit_desc = Struct("unit",
    ascii_str32("label"),
    #pitch and yaw are saved in radians.

    #Looking screen bounds
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    Pad(8),
    reflexive("animations", anim_enum_desc),
    reflexive("ik_points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapons", unit_weapon_desc, DYN_NAME_PATH=".name"),
    reflexive("unknown", unknown_unit_desc),
    SIZE=128,
    )

seat_desc = Struct("seat",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=60
    )

vehicle_desc = Struct("vehicle",
    #pitch and yaw are saved in radians.

    #Steering screen bounds
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    Pad(56),
    reflexive("seats", seat_desc),
    reflexive("animations", anim_enum_desc, 8,
        'steering','roll','throttle','velocity',
        'braking','ground-speed','occupied','unoccupied'),
    reflexive("suspension_animations", suspension_desc, 8),
    SIZE=116,
    )

effect_reference_desc = Struct("effect_reference",
    dependency_stubbs('effect', ("snd!", "effe")),
    SIZE=20,
    )

animation_desc = Struct("animation",
    ascii_str32("name"),
    SEnum16("type", *anim_types),
    SInt16("frame_count"),
    SInt16("frame_size"),
    SEnum16("frame_info_type", *anim_frame_info_types),
    SInt32("node_list_checksum"),
    SInt16("node_count"),
    SInt16("loop_frame_index"),

    Float("weight"),
    SInt16("key_frame_index"),
    SInt16("second_key_frame_index"),
    Pad(8),

    dyn_senum16("next_animation", DYN_NAME_PATH="..[DYN_I].name"),
    Bool16("flags",
        "compressed_data",
        "world_relative",
        {NAME:"pal", GUI_NAME:"25Hz(PAL)"},
        ),
    dyn_senum16("sound",
        DYN_NAME_PATH="tagdata.effect_references." +
        "effect_references_array[DYN_I].effect.filepath"),
    SInt16("sound_frame_index"),
    SInt8("left_foot_frame_index"),
    SInt8("right_foot_frame_index"),
    FlSInt16("first_permutation_index", VISIBLE=False,
        TOOLTIP="The index of the first animation in the permutation chain."),
    FlFloat("chance_to_play", VISIBLE=False,
        MIN=0.0, MAX=1.0, SIDETIP="[0,1]",
        TOOLTIP=("Seems to be the chance range to select this permutation.\n"
                 "Random number in the range [0,1] is rolled. The permutation\n"
                 "chain is looped until the number is higher than or equal\n"
                 "to that permutations chance to play. This chance to play\n"
                 "is likely influenced by the animations 'weight' field.\n"
                 "All permutation chains should have the last one end with\n"
                 "a chance to play of 1.0")),

    rawdata_ref("frame_info", max_size=32768),
    UInt32("trans_flags0", EDITABLE=False),
    UInt32("trans_flags1", EDITABLE=False),
    Pad(8),
    UInt32("rot_flags0", EDITABLE=False),
    UInt32("rot_flags1", EDITABLE=False),
    Pad(8),
    UInt32("scale_flags0", EDITABLE=False),
    UInt32("scale_flags1", EDITABLE=False),
    Pad(4),
    SInt32("offset_to_compressed_data", EDITABLE=False),
    rawdata_ref("default_data", max_size=16384),
    rawdata_ref("frame_data", max_size=1048576),
    SIZE=188,
    )

antr_body = Struct("tagdata",
    reflexive("objects",  object_desc),
    reflexive("units",    unit_desc, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapon_desc),
    reflexive("vehicles", vehicle_desc),
    reflexive("devices",  device_desc),
    reflexive("unit_damages", anim_enum_desc),
    reflexive("fp_animations", fp_animation_desc),

    reflexive("effect_references", effect_reference_desc,
        DYN_NAME_PATH=".effect.filepath"),
    Float("limp_body_node_radius"),
    Bool16("flags",
        "compress_all_animations",
        "force_idle_compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, DYN_NAME_PATH=".name"),
    SIZE=128,
    )


def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header_stubbs('antr', 5),  # increment to differentiate it from halo antr
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
