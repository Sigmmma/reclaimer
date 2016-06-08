from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


scenario_description = Struct("scenario description",
    dependency("descriptive bitmap", valid_bitmaps),
    dependency("displayed map name", valid_strings),
    StrLatin1("scenario tag directory path", SIZE=32),
    SIZE=68
    )

mply_body = Struct("tagdata",
    reflexive("multiplayer scenario descriptions",
              scenario_description, 32),
    SIZE=12,
    )


def get():
    return mply_def

mply_def = TagDef(
    blam_header('mply'),
    mply_body,
    
    NAME="multiplayer_scenario_description",
    
    ext=".multiplayer_scenario_description", def_id="mply", endian=">"
    )
