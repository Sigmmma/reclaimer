#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.antr import *
from supyr_struct.util import desc_variant

unit_weapon_desc = desc_variant(unit_weapon_desc,
    ("ik_points", reflexive("ik_points", ik_point_desc, 8, DYN_NAME_PATH=".marker")),
    ("weapon_types", reflexive("weapon_types", weapon_types_desc, 8, DYN_NAME_PATH=".label")),
    )
unit_desc = desc_variant(unit_desc,
    ("ik_points", reflexive("ik_points", ik_point_desc, 8, DYN_NAME_PATH=".marker")),
    ("weapons", reflexive("weapons", unit_weapon_desc, 64, DYN_NAME_PATH=".name")),
    )
vehicle_desc = desc_variant(vehicle_desc,
    ("suspension_animations", reflexive("suspension_animations", suspension_desc, 32)),
    )
fp_animation_desc = desc_variant(fp_animation_desc,
    ("animations", reflexive("animations", anim_enum_desc, 30, *fp_animation_names_mcc)),
    )
animation_desc = desc_variant(animation_desc,
    ("frame_data", rawdata_ref("frame_data", max_size=4194304)),
    )

antr_body = desc_variant(antr_body,
    ("units", reflexive("units", unit_desc, 2048, DYN_NAME_PATH=".label")),
    ("vehicles", reflexive("vehicles", vehicle_desc, 1)),
    ("fp_animations", reflexive("fp_animations", fp_animation_desc, 1)),
    ("sound_references", reflexive("sound_references", sound_reference_desc, 512, DYN_NAME_PATH=".sound.filepath")),
    ("animations", reflexive("animations", animation_desc, 2048, DYN_NAME_PATH=".name")),
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
