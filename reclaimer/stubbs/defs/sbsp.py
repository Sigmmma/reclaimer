#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.sbsp import *
from ..common_descs import *


cluster = Struct("cluster",
    SInt16('sky'),
    SInt16('fog'),
    dyn_senum16('background_sound',
        DYN_NAME_PATH="tagdata.background_sounds_palette.STEPTREE[DYN_I].name"),
    dyn_senum16('sound_environment',
        DYN_NAME_PATH="tagdata.sound_environments_palette." +
        "STEPTREE[DYN_I].name"),
    dyn_senum16('weather',
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),

    UInt16("transition_structure_bsp", VISIBLE=False),
    UInt16("first_decal_index", VISIBLE=False),
    UInt16("decal_count", VISIBLE=False),
    QStruct("unknown0",
        Float('float_0'),
        Float('float_1'),
        Float('float_2'),
        Float('float_3'),
        Float('float_4'),
        Float('float_5'),
        SIZE=24
        ),

    reflexive("predicted_resources", predicted_resource, 1024),
    reflexive("subclusters", subcluster, 4096),
    SInt16("first_lens_flare_marker_index"),
    SInt16("lens_flare_marker_count"),

    # stubbs seems to have different data here than surface indices
    Pad(12),
    reflexive("mirrors", mirror, 16, DYN_NAME_PATH=".shader.filepath"),
    reflexive("portals", portal, 128),
    SIZE=104
    )


sbsp_body = dict(sbsp_body)
sbsp_body[28] = reflexive("clusters", cluster, 8192)

fast_sbsp_body = dict(fast_sbsp_body)
fast_sbsp_body[28] = reflexive("clusters", cluster, 8192)


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header_stubbs("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )

fast_sbsp_def = TagDef("sbsp",
    blam_header_stubbs("sbsp", 5),
    fast_sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )
