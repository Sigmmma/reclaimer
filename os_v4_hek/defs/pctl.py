from ...hek.defs.pctl import *

particle_state = dict(particle_state)
particle_type  = dict(particle_type)
pctl_body      = dict(pctl_body)

particle_state[19] = reflexive(
    "shader extensions",
    Struct("shader extension", INCLUDE=os_shader_extension),
    1)
particle_type[12] = reflexive(
    "particle states", particle_state, 8, DYN_NAME_PATH='.name')
pctl_body[5] = reflexive(
    "particle types", particle_type, 4, DYN_NAME_PATH='.name')

    
def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
