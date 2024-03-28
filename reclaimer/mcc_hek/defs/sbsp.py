#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.sbsp import *

sbsp_meta_header_def = BlockDef("sbsp_meta_header",
    # to convert the meta pointer to offsets, do:  pointer - bsp_magic
    UInt32("meta_pointer"),
    # the rest of these are literal pointers in the map
    UInt32("uncompressed_render_vertices_size"),
    UInt32("uncompressed_render_vertices_pointer"),
    UInt32("compressed_render_vertices_size"),  # name is a guess
    UInt32("compressed_render_vertices_pointer"),  # name is a guess
    UInt32("sig", DEFAULT="sbsp"),
    SIZE=24, TYPE=QStruct
    )