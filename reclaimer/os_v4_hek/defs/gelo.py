#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.gelo import *

gelo_body = desc_variant(gelo_body,
    # was removed
    ("chokin_victim_globals", Pad(16)),
    )

def get():
    return gelo_def

gelo_def = TagDef("gelo",
    blam_header_os('gelo', 2),
    gelo_body,

    ext=".project_yellow_globals", endian=">", tag_cls=HekTag
    )
