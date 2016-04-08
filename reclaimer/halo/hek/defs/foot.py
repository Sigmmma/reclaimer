from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

material = Struct("material",
    TagIndexRef("effect", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("sound",  INCLUDE=Tag_Index_Ref_Struct),
    SIZE=48,
    )
                         
effect = Struct("effect",
    Reflexive("materials",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("materials array", MAX=33,
            SIZE=".Count", SUB_STRUCT=material)
        ),
    SIZE=28,
    )

foot_body = Struct("Data",
    Reflexive("effects",
        INCLUDE=Reflexive_Struct,

        CHILD=Array("effects array", MAX=13,
            SIZE=".Count", SUB_STRUCT=effect )
        ),
    SIZE=140,
    )



def get():
    return foot_def

foot_def = TagDef(
    com( {1:{DEFAULT:"foot" }}, Tag_Header),
    foot_body,
    
    NAME="material_effects",
    
    ext=".material_effects", def_id="foot", endian=">"
    )
