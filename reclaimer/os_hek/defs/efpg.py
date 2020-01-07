#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .efpp import *
from ...hek.defs.objs.tag import HekTag

shader = Struct("shader",
    dependency_os("shader", 'shpg'),
    SIZE=16
    )

shader_index = Struct("shader_index",
    dyn_senum32("shader",
        DYN_NAME_PATH="tagdata.efpg_attrs.shaders.STEPTREE[DYN_I].shader.filepath"),
    SIZE=4
    )

exposed_parameter = Struct("exposed_parameter",
    ascii_str32("exposed_name"),
    ascii_str32("parameter_name"),
    dyn_senum32("shader_index",
        DYN_NAME_PATH="tagdata.efpg_attrs.shader_indices.STEPTREE[DYN_I].NAME"),
    SIZE=80
    )

efpg_attrs = Struct("efpg_attrs",
    reflexive("shaders", shader, 12,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("shader_indices", shader_index, 12),
    reflexive("exposed_parameters", exposed_parameter, 32,
        DYN_NAME_PATH='.exposed_name'),
    SIZE=36
    )

efpg_body = Struct("tagdata",
    efpp_attrs,
    efpg_attrs,
    SIZE=96
    )

def get():
    return efpg_def

efpg_def = TagDef("efpg",
    blam_header_os('efpg'),
    efpg_body,

    ext=".effect_postprocess_generic", endian=">", tag_cls=HekTag
    )
