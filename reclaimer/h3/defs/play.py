#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: -DeToX-
# 	Created layout of plugin
# revision: 2		author: -DeToX-
# 	Labelled some reflexives related to raw.
# revision: 3		author: -DeToX-
# 	Labelled raw size for sounds.
# revision: 4		author: Lord Zedd
# 	Copypasta
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


play_compression_codec = Struct("compression_codec",
    BytesRaw("guid", SIZE=16, EDITABLE=False),
    ENDIAN=">", SIZE=16
    )


play_external_cache_reference = Struct("external_cache_reference",
    StrLatin1("map_path", SIZE=256),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    UInt32("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=264
    )


play_raw_page = Struct("raw_page",
    SInt16("salt"),
    SInt8("flags"),
    SEnum8("compression_codec", *play_raw_page_compression_codec),
    dyn_senum16("shared_cache_index",
        DYN_NAME_PATH=".....external_cache_references.STEPTREE[DYN_I].map_path",
        WIDGET_WIDTH=32
        ),
    SInt16("unknown_page_index", SIDETIP="(Seems to be either the pages index, or -1)"),
    UInt32("block_offset"),
    UInt32("compressed_block_size"),
    UInt32("uncompressed_block_size"),
    UInt32("crc_checksum"),
    BytesRaw("entire_buffer_hash", SIZE=20, EDITABLE=False),
    BytesRaw("first_chunk_hash", SIZE=20, EDITABLE=False),
    BytesRaw("last_chunk_hash", SIZE=20, EDITABLE=False),
    SInt16("block_asset_count"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=88
    )


play_raw_size_chunk = QStruct("chunk",
    # figure out what the crap this actually is
    SInt32("offset"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


play_raw_size = Struct("raw_size",
    SInt32("total_size"),
    h3_reflexive("chunks", play_raw_size_chunk),
    ENDIAN=">", SIZE=16
    )


play_segment = Struct("segment",
    # doing these as arrays to allow iterating over them easily in later halo's
    Array("page_indices",     SUB_STRUCT=SInt16("idx"),    SIZE=2, MIN=2, MAX=2),
    Array("segment_offsets",  SUB_STRUCT=SInt32("offset"), SIZE=2, MIN=2, MAX=2),
    Array("raw_size_indices", SUB_STRUCT=SInt16("size"),   SIZE=2, MIN=2, MAX=2),
    ENDIAN=">", SIZE=16
    )


play_body = Struct("tagdata",
    h3_reflexive("compression_codecs", play_compression_codec),
    h3_reflexive("external_cache_references", play_external_cache_reference),
    h3_reflexive("raw_pages", play_raw_page),
    h3_reflexive("raw_sizes", play_raw_size),
    h3_reflexive("segments", play_segment),
    ENDIAN=">", SIZE=60
    )


def get():
    return play_def

play_def = TagDef("play",
    h3_blam_header('play'),
    play_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["play"], endian=">", tag_cls=H3Tag
    )
