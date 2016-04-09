from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef


scenario_description = Struct("scenario description",
    TagIndexRef("descriptive bitmap", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("displayed map name", INCLUDE=Tag_Index_Ref_Struct),
    StrLatin1("scenario tag directory path", SIZE=32),
    SIZE=68
    )

mply_body = Struct("Data",
    Reflexive("multiplayer scenario descriptions",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("scenario descriptions array", MAX=32,
            SIZE=".Count", SUB_STRUCT=scenario_description ),
        ),
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
