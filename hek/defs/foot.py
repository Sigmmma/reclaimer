from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

material = Struct("material",
    dependency("effect", "effe"),
    dependency("sound", "snd!"),
    SIZE=48,
    )
                         
effect = Struct("effect",
    reflexive("materials", material, len(materials_list), *materials_list),
    SIZE=28,
    )

foot_body = Struct("tagdata",
    reflexive("effects", effect, 13,
        "walk", "run", "sliding", "shuffle", "jump", "jump land",
        "biped unused1", "biped unused2",
        "impact", "vehicle tire slip", "vehicle chassis slip",
        "vehicle unused1", "vehicle unused2"),
    SIZE=140,
    )



def get():
    return foot_def

foot_def = TagDef("foot",
    blam_header('foot'),
    foot_body,
    
    ext=".material_effects", endian=">", tag_cls=HekTag
    )
