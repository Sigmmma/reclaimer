from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

material = Struct("material",
    TagIndexRef("effect", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("sound",  INCLUDE=Tag_Index_Ref_Struct),
    SIZE=48,
    )
                         
effect = Struct("effect",
    reflexive("materials", material, 33),
    SIZE=28,
    )

foot_body = Struct("Data",
    reflexive("effects", effect, 13),
    SIZE=140,
    )



def get():
    return foot_def

foot_def = TagDef(
    blam_header('foot'),
    foot_body,
    
    NAME="material_effects",
    
    ext=".material_effects", def_id="foot", endian=">"
    )
