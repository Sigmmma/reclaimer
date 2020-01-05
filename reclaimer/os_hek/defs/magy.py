#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .objs.magy import MagyTag
from ...hek.defs.antr import *

magy_body = Struct("tagdata",
    reflexive("objects",  object_desc, 4),
    reflexive("units",    unit_desc, 32, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapon_desc, 1),
    reflexive("vehicles", vehicle_desc, 1),
    reflexive("devices",  device_desc, 1),
    reflexive("unit_damages", anim_enum_desc, 176,
        *unit_damage_animation_names
        ),
    reflexive("fp_animations", fp_animation_desc, 1),
    #i have no idea why they decided to cap it at 257 instead of 256....
    reflexive("sound_references", sound_reference_desc, 257,
        DYN_NAME_PATH=".sound.filepath"),
    Float("limp_body_node_radius"),
    Bool16("flags",
        "compress_all_animations",
        "force_idle_compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, 64, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, 2048, DYN_NAME_PATH=".name"),
    dependency_os("stock_animation", valid_model_animations_yelo),
    SIZE=300,
    )


def get():
    return magy_def

magy_def = TagDef("magy",
    blam_header_os('magy', 0),
    magy_body,

    ext=".model_animations_yelo", endian=">", tag_cls=MagyTag
    )
