#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.bitm import *

def get(): return bitm_def

# replace the model animations dependency with an open sauce one
bitm_body = dict(bitm_body)
bitm_body[3] = Bool16("flags",
    "enable_diffusion_dithering",
    "disable_height_map_compression",
    "uniform_sprite_sequences",
    "sprite_bug_fix",
    ("never_share_resources", 1<<13)
    )

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=BitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
