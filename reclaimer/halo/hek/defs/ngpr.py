from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

ngpr_body = Struct("Data",
    #I didnt feel like adding offsets since
    #there is only padding in one spot
    StrLatin1("name", SIZE=32),
    Struct("primary color",   INCLUDE=R_G_B_Float),
    Struct("secondary color", INCLUDE=R_G_B_Float),

    TagIndexRef("pattern", INCLUDE=Tag_Index_Ref_Struct),
    BSInt16("pattern bitmap index"),
    Pad(2),
    TagIndexRef("decal",  INCLUDE=Tag_Index_Ref_Struct),
    BSInt16("decal bitmap index"),
    SIZE=896
    )


def get():
    return ngpr_def

ngpr_def = TagDef(
    blam_header('ngpr', 2),
    ngpr_body,
    
    NAME="preferences_network_game",
    
    ext=".preferences_network_game", def_id="ngpr", endian=">"
    )
