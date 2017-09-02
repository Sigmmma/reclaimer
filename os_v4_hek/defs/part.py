from ...hek.defs.part import *

part_body = dict(part_body)
part_body[11] = reflexive(
    "particle shader extensions",
    Struct("particle shader extension", INCLUDE=os_shader_extension),
    1)

    
def get():
    return part_def

part_def = TagDef("part",
    blam_header("part", 2),
    part_body,

    ext=".particle", endian=">", tag_cls=HekTag,
    )
