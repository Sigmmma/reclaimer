from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


play_compression_codec = Struct("compression_codecs",
    BytesRaw("guid", SIZE=16),
    ENDIAN=">", SIZE=16
    )


play_external_cache_reference = Struct("external_cache_references",
    StrLatin1("map_path", SIZE=256),
    SInt16("unknown"),
    SInt16("unknown_1"),
    Pad(4),
    ENDIAN=">", SIZE=264
    )


play_raw_page = Struct("raw_pages",
    SInt16("salt"),
    SInt8("flags"),
    SInt8("compression_codec_index"),
    SInt16("shared_cache_index"),
    SInt16("unknown"),
    UInt32("block_offset"),
    UInt32("compressed_block_size"),
    UInt32("uncompressed_block_size"),
    SInt32("crc_checksum"),
    BytesRaw("entire_buffer_hash", SIZE=20),
    BytesRaw("first_chunk_hash", SIZE=20),
    BytesRaw("last_chunk_hash", SIZE=20),
    SInt16("block_asset_count"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=88
    )


play_size_part = Struct("parts",
    SInt32("unknown"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


play_size = Struct("sizes",
    SInt32("overall_size"),
    reflexive("parts", play_size_part),
    ENDIAN=">", SIZE=16
    )


play_segment = Struct("segments",
    SInt16("primary_page_index"),
    SInt16("secondary_page_index"),
    SInt32("primary_segment_offset"),
    SInt32("secondary_segment_offset"),
    SInt16("primary_size_index"),
    SInt16("secondary_size_index"),
    ENDIAN=">", SIZE=16
    )


play_meta_def = BlockDef("play",
    reflexive("compression_codecs", play_compression_codec),
    reflexive("external_cache_references", play_external_cache_reference),
    reflexive("raw_pages", play_raw_page),
    reflexive("sizes", play_size),
    reflexive("segments", play_segment),
    TYPE=Struct, ENDIAN=">", SIZE=60
    )