#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

message_index_comment = """MESSAGE INDEX
This sets which string from tags\\ui\\hud\\hud_item_messages.unicode_string_list to display."""

item_attrs = Struct('item_attrs',
    Bool32("flags",
        "always_maintains_z_up",
        "destroyed_by_explosions",
        "unaffected_by_gravity",
        ),
    SInt16("message_index", COMMENT=message_index_comment),
    SInt16("sort_order"),
    Float("scale"),
    SInt16("hud_message_value_scale"),

    Pad(18),

    SEnum16("A_in", *device_functions),
    SEnum16("B_in", *device_functions),
    SEnum16("C_in", *device_functions),
    SEnum16("D_in", *device_functions),

    Pad(164),

    dependency("material_effects", "foot"),
    dependency("collision_sound", "snd!"),

    Pad(120),

    from_to_sec("detonation_delay"),
    dependency("detonating_effect", "effe"),
    dependency("detonation_effect", "effe"),
    SIZE=396,
    )

item_body = Struct('tagdata',
    item_attrs,
    SIZE=396
    )

def get():
    return item_def

item_def = TagDef("item",
    blam_header('item', 2),
    item_body,

    ext=".item", endian=">", tag_cls=HekTag
    )
