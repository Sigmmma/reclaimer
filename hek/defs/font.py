from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return font_def


character_table = QStruct("character table",
    SInt16("character index"),
    SIZE=2
    )

character_tables = Struct("character tables",
    reflexive("character table", character_table, 256),
    SIZE=12
    )

character = QStruct("character",
    UInt16("character"),
    SInt16("character width"),
    SInt16("bitmap width", EDITABLE=False),
    SInt16("bitmap height", EDITABLE=False),
    SInt16("bitmap origin x"),
    SInt16("bitmap origin y"),
    SInt16("hardware character index"),
    Pad(2),
    SInt32("pixels offset", EDITABLE=False),
    SIZE=20, WIDGET=FontCharacterFrame
    )

font_body = Struct("tagdata",
    SInt32("flags"),
    SInt16("ascending height"),
    SInt16("decending height"),
    SInt16("leading height"),
    SInt16("leading width"),
    Pad(36),

    reflexive("character tables", character_tables, 256),
    dependency("bold", "font"),
    dependency("italic", "font"),
    dependency("condense", "font"),
    dependency("underline", "font"),
    reflexive("characters", character),
    rawdata_ref("pixels", max_size=8388608),
    SIZE=156,
    )

font_def = TagDef("font",
    blam_header('font'),
    font_body,

    ext=".font", endian=">", tag_cls=HekTag
    )
