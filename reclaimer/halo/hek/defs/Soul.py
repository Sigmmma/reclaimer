from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

soul_body = Struct("Data",
    Reflexive("ui widget definitions",
        INCLUDE=Reflexive_Struct,

        CHILD=Array("ui widget definitions array",
            SIZE=".Count", MAX=32,
            SUB_STRUCT=TagIndexRef("ui widget definition",
                INCLUDE=Tag_Index_Ref_Struct,
                )
            )
        ),
    SIZE=12,
    )


def get():
    return soul_def

soul_def = TagDef(
    com( {1:{DEFAULT:"Soul" }}, Tag_Header),
    soul_body,#lol Megaman X4
    
    NAME="ui_widget_collection",
    
    ext=".ui_widget_collection", def_id="Soul", endian=">"
    )
