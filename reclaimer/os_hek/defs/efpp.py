#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

efpp_attrs = Struct("efpp_attrs",
    Pad(12),
    QStruct("quad_tesselation",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    from_to_zero_to_one("x_screen_bounds"),
    from_to_zero_to_one("y_screen_bounds"),
    SIZE=60
    )


efpp_body = Struct("tagdata", efpp_attrs)

def get():
    return efpp_def

efpp_def = TagDef("efpp",
    blam_header_os('efpp'),
    efpp_body,

    ext=".effect_postprocess", endian=">", tag_cls=HekTag
    )
