#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.common_descs import *

from supyr_struct.defs.bitmaps.dds import pixelformat_typecodes
from supyr_struct.defs.block_def import BlockDef


d3d_texture = Struct("d3d_texture",
    UInt16("width"),
    UInt16("height"),
    UInt8("depth"),
    UInt8("texture_count"), # mipmap_count + 1
    UEnum8("type",
        "texture_2d",
        "texture_3d",
        "cubemap",
        "lightmap",
        ),
    UInt8("tex_page_index"),  # page the fullsize image is stored in.
    #                           mipmaps are always stored in primary.
    UEnum32("format", *pixelformat_typecodes)
    )


s_tag_d3d_texture = Struct("s_tag_d3d_texture",
    Struct("primary_page_data", INCLUDE=rawdata_ref_struct),
    Struct("secondary_page_data", INCLUDE=rawdata_ref_struct),
    Struct("texture", INCLUDE=d3d_texture)
    )


s_tag_d3d_texture_interleaved = Struct("s_tag_d3d_texture_interleaved",
    Struct("primary_page_data", INCLUDE=rawdata_ref_struct),
    Struct("secondary_page_data", INCLUDE=rawdata_ref_struct),
    Struct("texture0", INCLUDE=d3d_texture),
    Struct("texture1", INCLUDE=d3d_texture),
    )

s_tag_d3d_texture_def = BlockDef(
    s_tag_d3d_texture,
    endian=">"
    )
s_tag_d3d_texture_interleaved_def = BlockDef(
    s_tag_d3d_texture_interleaved,
    endian=">"
    )
