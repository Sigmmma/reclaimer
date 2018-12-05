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
        DYN_NAME_PATH=".....external_cache_references.STEPTREE[DYN_I].map_path"
        ),
    SInt16("unknown_0"),
    UInt32("block_offset"),
    UInt32("compressed_block_size"),
    UInt32("uncompressed_block_size"),
    UInt32("crc_checksum"),
    BytesRaw("entire_buffer_hash", SIZE=20, EDITABLE=False),
    BytesRaw("first_chunk_hash", SIZE=20, EDITABLE=False),
    BytesRaw("last_chunk_hash", SIZE=20, EDITABLE=False),
    SInt16("block_asset_count"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=88
    )


play_size_part = Struct("part", 
    SInt32("unknown"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


play_size = Struct("size", 
    SInt32("overall_size"),
    h3_reflexive("parts", play_size_part),
    ENDIAN=">", SIZE=16
    )


play_segment = Struct("segment", 
    SInt16("primary_page_index"),
    SInt16("secondary_page_index"),
    SInt32("primary_segment_offset"),
    SInt32("secondary_segment_offset"),
    SInt16("primary_size_index"),
    SInt16("secondary_size_index"),
    ENDIAN=">", SIZE=16
    )


play_body = Struct("tagdata", 
    h3_reflexive("compression_codecs", play_compression_codec),
    h3_reflexive("external_cache_references", play_external_cache_reference),
    h3_reflexive("raw_pages", play_raw_page),
    h3_reflexive("sizes", play_size),
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
