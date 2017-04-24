from .efpp import *
from ...hek.defs.objs.tag import HekTag

shader = Struct("shader",
    dependency_os("shader", 'shpg'),
    SIZE=16
    )

shader_index = Struct("shader index",
    dyn_senum32("shader",
        DYN_NAME_PATH="tagdata.shaders.STEPTREE[DYN_I].shader.filepath"),
    SIZE=4
    )

exposed_parameter = Struct("exposed parameter",
    ascii_str32("exposed name"),
    ascii_str32("parameter name"),
    dyn_senum32("shader index",
        DYN_NAME_PATH="tagdata.shader_indices.STEPTREE[DYN_I].NAME"),
    SIZE=80
    )

efpg_body = Struct("tagdata",
    efpp_attrs,
    reflexive("shaders", shader, 12,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("shader indices", shader_index, 12),
    reflexive("exposed parameters", exposed_parameter, 32,
        DYN_NAME_PATH='.exposed_name'),
    SIZE=96
    )

def get():
    return efpg_def

efpg_def = TagDef("efpg",
    blam_header_os('efpg'),
    efpg_body,

    ext=".effect_postprocess_generic", endian=">", tag_cls=HekTag
    )
