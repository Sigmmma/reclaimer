#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.scnr import *

lightmap_set = Struct("lightmap_set",
    ascii_str32("name"),
    Pad(4),
    dependency_os("std_lightmap", "bitm"),
    dependency_os("dir_lightmap_1", "bitm"),
    dependency_os("dir_lightmap_2", "bitm"),
    dependency_os("dir_lightmap_3", "bitm"),
    SIZE=124
    )


sky_set_sky = Struct("sky",
    Pad(2),
    dyn_senum16("sky_index",
        DYN_NAME_PATH="...........skies.STEPTREE[DYN_I].sky.filepath"),
    dependency_os("sky", "sky "),
    SIZE=20
    )


sky_set = Struct("sky_set",
    ascii_str32("name"),
    reflexive("skies", sky_set_sky, 8),
    SIZE=44
    )


bsp_modifier = Struct("bsp_modifier",
    Pad(2),
    dyn_senum16("bsp_index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    reflexive("lightmap_sets", lightmap_set, 64),
    reflexive("sky_sets", sky_set, 64),
    SIZE=64
    )


scnr_body = dict(scnr_body)
scnr_body[64] = reflexive("bsp_modifiers", bsp_modifier, 32)

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )
