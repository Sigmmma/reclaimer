#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.mode import *
from ..common_descs import *

def get():
    return mode_def

# my guess at what the struct might be like
unknown_struct = Struct("unknown",
    ascii_str32("name"),
    Float('unknown1', DEFAULT=1.0),
    Float('unknown2', DEFAULT=1.0),
    BytesRaw("unknown_data", SIZE=64-32-4*2),
    SIZE=64
    )

#unknown_struct = Struct("unknown",
#    BytesRaw("unknown_data", SIZE=64),
#    SIZE=64
#    )

pc_part   = desc_variant(part, model_meta_info)
fast_part = desc_variant(part,
    raw_reflexive("uncompressed_vertices", fast_uncompressed_vertex, SINT16_MAX),
    raw_reflexive("compressed_vertices", fast_compressed_vertex, SINT16_MAX),
    raw_reflexive("triangles", triangle, SINT16_MAX),
    )
fast_pc_part = desc_variant(fast_part, model_meta_info)

pc_geometry      = desc_variant(geometry, reflexive("parts", pc_part, 32, EXT_MAX=SINT16_MAX))
fast_geometry    = desc_variant(geometry, reflexive("parts", fast_part, 32, EXT_MAX=SINT16_MAX))
fast_pc_geometry = desc_variant(geometry, reflexive("parts", fast_pc_part, 32, EXT_MAX=SINT16_MAX))

mode_body = desc_variant(mode_body,
    ("pad_16", reflexive("unknown", unknown_struct, DYN_NAME_PATH=".name")),
    )
pc_mode_body      = desc_variant(mode_body, reflexive("geometries", pc_geometry, 256, EXT_MAX=SINT16_MAX))
fast_mode_body    = desc_variant(mode_body, reflexive("geometries", fast_geometry, 256, EXT_MAX=SINT16_MAX))
fast_pc_mode_body = desc_variant(mode_body, reflexive("geometries", fast_pc_geometry, 256, EXT_MAX=SINT16_MAX))

# increment version to differentiate from halo models
stubbs_mode_header = blam_header_stubbs('mode', 6)
stubbs_mode_kwargs = dict(ext=".model", endian=">", tag_cls=ModeTag)

mode_def = TagDef("mode",
    stubbs_mode_header,
    mode_body, 
    **stubbs_mode_kwargs
    )

fast_mode_def = TagDef("mode",
    stubbs_mode_header,
    fast_mode_body, 
    **stubbs_mode_kwargs
    )

pc_mode_def = TagDef("mode",
    stubbs_mode_header,
    pc_mode_body,
    **stubbs_mode_kwargs
    )

fast_pc_mode_def = TagDef("mode",
    stubbs_mode_header,
    fast_pc_mode_body,
    **stubbs_mode_kwargs
    )
