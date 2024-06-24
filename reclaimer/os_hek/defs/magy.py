#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .objs.magy import MagyTag
from .antr import *

magy_body = desc_variant(antr_body,
    ("pad_13", dependency_os("stock_animation", valid_model_animations_yelo)),
    SIZE=300, verify=False
    )


def get():
    return magy_def

magy_def = TagDef("magy",
    blam_header_os('magy', 0),
    magy_body,

    ext=".model_animations_yelo", endian=">", tag_cls=MagyTag
    )
