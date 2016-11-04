from .efpp import *

shader = Struct("shader",
    dependency("shader", valid_shader_postprocess_generic),
    SIZE=16
    )

shader_index = Struct("shader index",
    BSInt32("shader"),
    SIZE=4
    )

exposed_parameter = Struct("exposed parameter",
    ascii_str32("exposed name"),
    ascii_str32("parameter name"),
    BSInt32("shader index"),
    SIZE=80
    )

efpg_body = Struct("tagdata",
    efpp_attrs,
    reflexive("shaders", shader, 12),
    reflexive("shaders indices", shader_index, 12),
    reflexive("exposed parameters", exposed_parameter, 32),
    SIZE=96
    )

def get():
    return efpg_def

efpg_def = TagDef("efpg",
    blam_header_os('efpg'),
    efpg_body,

    ext=".effect_postprocess_generic", endian=">"
    )
