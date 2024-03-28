#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.antr import *

unit_weapon_desc = desc_variant(unit_weapon_desc,
    reflexive("ik_points", ik_point_desc, 8, DYN_NAME_PATH=".marker"),
    reflexive("weapon_types", weapon_types_desc, 64, DYN_NAME_PATH=".label"),
    )
unit_desc = desc_variant(unit_desc,
    reflexive("ik_points", ik_point_desc, 8, DYN_NAME_PATH=".marker"),
    reflexive("weapons", unit_weapon_desc, 64, DYN_NAME_PATH=".name"),
    )
vehicle_desc = desc_variant(vehicle_desc,
    reflexive("suspension_animations", suspension_desc, 32),
    )
fp_animation_desc = desc_variant(fp_animation_desc,
    reflexive("animations", anim_enum_desc, 30, *fp_animation_names_mcc),
    )
animation_desc = desc_variant(animation_desc,
    rawdata_ref("frame_data", max_size=4194304),
    )

antr_body = desc_variant(antr_body,
    reflexive("units", unit_desc, 2048, DYN_NAME_PATH=".label"),
    reflexive("vehicles", vehicle_desc, 1),
    reflexive("fp_animations", fp_animation_desc, 1),
    reflexive("sound_references", sound_reference_desc, 512, DYN_NAME_PATH=".sound.filepath"),
    reflexive("animations", animation_desc, 2048, DYN_NAME_PATH=".name"),
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
