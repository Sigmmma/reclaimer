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

# As meta, it seems MOST arrays of anim_enum_desc have an extra enum on the end

animations_extended_desc = Struct("weapon_types",
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=28,
    )

# NOTE: this requires further investigation. It doesn't seem like
#       they actually moved the padding to before the yaw_per_frame.
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

unit_desc = desc_variant(unit_desc,
    ("pad_13", reflexive("unknown", unknown_unit_desc)),
    SIZE=128,
    verify=False
    )

seat_desc = Struct("seat",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=60
    )

vehicle_desc = desc_variant(vehicle_desc,
    ("pad_9", reflexive("seats", seat_desc)),
    )

effect_reference_desc = Struct("effect_reference",
    dependency_stubbs('effect', ("snd!", "effe")),
    SIZE=20,
    )

animation_desc = desc_variant(animation_desc,
    ("pad_11", Pad(8)),
    ("sound", dyn_senum16("effect",
        DYN_NAME_PATH="tagdata.effect_references." +
        "effect_references_array[DYN_I].effect.filepath"
        )),
    SIZE=188,
    verify=False
    )

antr_body = desc_variant(antr_body,
    reflexive("units",    unit_desc, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapon_desc),
    reflexive("vehicles", vehicle_desc),
    reflexive("unit_damages", anim_enum_desc),
    ("sound_references",  reflexive("effect_references",
        effect_reference_desc, DYN_NAME_PATH=".effect.filepath")
        ),
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
