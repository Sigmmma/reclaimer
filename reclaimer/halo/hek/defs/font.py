from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return font_def


character_table = QuickStruct("character table",
    BSInt16("character index"),
    SIZE=2
    )

character_tables = Struct("character tables",
    reflexive("character table", character_table, 256),
    SIZE=12
    )

character = QuickStruct("character",
    BSInt16("character"),
    BSInt16("character width"),
    BSInt16("bitmap width"),
    BSInt16("bitmap height"),
    BSInt16("bitmap origin x"),
    BSInt16("bitmap origin y"),
    BSInt16("hardware character index"),
    Pad(2),
    BSInt32("pixels offset"),
    SIZE=20
    )

font_body = Struct("tagdata",
    BSInt32("flags"),
    BSInt16("ascending height"),
    BSInt16("decending height"),
    BSInt16("leading height"),
    BSInt16("leading width"),
    Pad(36),

    reflexive("character tables", character_tables, 256),
    dependency("bold", valid_fonts),
    dependency("italic", valid_fonts),
    dependency("condense", valid_fonts),
    dependency("underline", valid_fonts),
    reflexive("characters", character),
    rawdata_ref("pixels"),
    SIZE=156,
    )

font_def = TagDef("font",
    blam_header('font'),
    font_body,

    ext=".font", endian=">"
    )
