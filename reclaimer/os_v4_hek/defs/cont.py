#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.cont import *

cont_body = dict(cont_body)
cont_body[4] = reflexive(
    "shader_extensions",
    Struct("shader_extension", INCLUDE=os_shader_extension),
    1)


def get():
    return cont_def

cont_def = TagDef("cont",
    blam_header("cont", 3),
    cont_body,

    ext=".contrail", endian=">", tag_cls=HekTag,
    )
