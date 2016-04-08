from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

tagc_body = Struct("Data",
    Reflexive("tag references",
        INCLUDE=Reflexive_Struct,

        CHILD=Array("tag references array",
            SIZE=".Count", MAX=200,
            SUB_STRUCT=TagIndexRef("tag",
                SIZE=16, INCLUDE=Tag_Index_Ref_Struct)
            ),
        ),
    SIZE=12,
    )


def get():
    return tagc_def

tagc_def = TagDef(
    com( {1:{DEFAULT:"tagc" }}, Tag_Header),
    tagc_body,
    
    NAME="tag_collection",
    
    ext=".tag_collection", def_id="tagc", endian=">"
    )
