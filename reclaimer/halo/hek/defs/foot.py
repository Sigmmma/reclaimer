from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

material = Struct("material",
    dependency("effect"),
    dependency("sound", valid_sounds),
    SIZE=48,
    )
                         
effect = Struct("effect",
    reflexive("materials", material, 33),
    SIZE=28,
    )

foot_body = Struct("tagdata",
    reflexive("effects", effect, 13),
    SIZE=140,
    )



def get():
    return foot_def

foot_def = TagDef("foot",
    blam_header('foot'),
    foot_body,
    
    ext=".material_effects", endian=">"
    )
