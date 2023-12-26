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

def get(): return font_def


character_table = QStruct("character_table",
    SInt16("character_index"),
    SIZE=2
    )

character_tables = Struct("character_tables",
    reflexive("character_table", character_table, 256),
    SIZE=12
    )

character = QStruct("character",
    UInt16("character"),
    SInt16("character_width"),
    SInt16("bitmap_width", EDITABLE=False),
    SInt16("bitmap_height", EDITABLE=False),
    SInt16("bitmap_origin_x"),
    SInt16("bitmap_origin_y"),
    SInt16("hardware_character_index"),
    Pad(2),
    SInt32("pixels_offset", EDITABLE=False),
    SIZE=20, WIDGET=FontCharacterFrame
    )

font_body = Struct("tagdata",
    SInt32("flags"),
    SInt16("ascending_height"),
    SInt16("decending_height"),
    SInt16("leading_height"),
    SInt16("leading_width"),
    Pad(36),

    reflexive("character_tables", character_tables, 256),
    dependency("bold", "font"),
    dependency("italic", "font"),
    dependency("condense", "font"),
    dependency("underline", "font"),
    reflexive("characters", character, 65535),
    rawdata_ref("pixels", max_size=8388608),
    SIZE=156,
    )

font_def = TagDef("font",
    blam_header('font'),
    font_body,

    ext=".font", endian=">", tag_cls=HekTag
    )
