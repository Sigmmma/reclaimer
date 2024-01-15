#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.lens import *
from supyr_struct.util import desc_variant

bitmaps = Struct("bitmaps",
    dependency("bitmap", "bitm"),
    Bool16("flags",
        "sun",
        "no_occlusion_test",
        "only_render_in_first_person",
        "only_render_in_third_person",
        "fade_in_more_quickly",
        "fade_out_more_quickly",
        "scale_by_marker",
        ),
    Pad(78),
    )

lens_body = desc_variant(lens_body,
    ("bitmaps", bitmaps),
    )

def get():
    return lens_def

lens_def = TagDef("lens",
    blam_header("lens", 2),
    lens_body,

    ext=".lens_flare", endian=">", tag_cls=LensTag,
    )
