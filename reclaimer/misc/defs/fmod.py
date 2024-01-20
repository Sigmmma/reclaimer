#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

FMOD_BANK_HEADER_SIZE = 60


def get():
    return fmod_bank_def, fmod_list_def
    

def _get_fmod_bank(block):
    while block and getattr(block, "NAME", "") != "fmod_bank":
        block = block.parent
    return block


def has_next_chunk(parent=None, **kwargs):
    if parent is None:
        return False
    return (parent[-1] if parent else parent.parent).header.has_next_chunk


def sample_data_size(parent=None, root_offset=0, offset=0, **kwargs):
    sample_array = getattr(parent, "parent", None)
    if not sample_array:
        return 0

    next_sample_index = sample_array.index_by_id(parent) + 1
    start = sample_data_pointer(parent=parent, root_offset=root_offset, offset=offset)
    if next_sample_index >= len(sample_array):
        fsb_header = getattr(getattr(sample_array, "parent", None), "header", None)
        data_size  = getattr(fsb_header, "sample_data_size", 0) - start
    else:
        end = sample_data_pointer(parent=sample_array[next_sample_index])
        data_size = end - start

    return max(0, data_size)


def sample_data_pointer(parent=None, root_offset=0, offset=0, **kwargs):
    sample_header = parent.header
    bank_header = _get_fmod_bank(sample_header).header
    return (
        root_offset + offset + FMOD_BANK_HEADER_SIZE +
        bank_header.sample_headers_size +
        bank_header.sample_names_size +
        sample_header.data_qword_offset * 16
        )


def sample_name_offsets_pointer(parent=None, root_offset=0, offset=0, **kwargs):
    return (
        root_offset + offset + FMOD_BANK_HEADER_SIZE +
        _get_fmod_bank(parent).header.sample_headers_size
        )


def sample_name_pointer(parent=None, root_offset=0, offset=0, **kwargs):
    return sample_name_offsets_pointer(
        parent, root_offset, offset
        ) + parent.offset


sound_list_header = Container("sound_list_header",
    UInt32('string_len'),
    StrUtf8('sound_name',
        SIZE='.string_len', 
        WIDGET_WIDTH=100
        ),
    UInt32('sample_id'),
    UInt32('sample_count'),
    )

fmod_list_header = Struct("header",
    UInt32("version", DEFAULT=1),
    UInt32("sound_count"),
    SIZE=8
    )

fmod_list_def = TagDef('fmod_list',
    fmod_list_header,
    Array("sample_headers",
        SUB_STRUCT=sound_list_header, SIZE=".header.sound_count",
        DYN_NAME_PATH=".sound_name", WIDGET=DynamicArrayFrame
        ),
    ext='.bin', endian='<'
    )

chunk_header = BitStruct("header",
    Bit("has_next_chunk"),
    UBitInt("size", SIZE=24),
    UBitEnum("type",
        ("channels", 1),
        ("frequency", 2),
        ("loop", 3),
        ("xma_seek", 6),
        ("dsp_coeff", 7),
        ("xwma_data", 10),
        ("vorbis_data", 11),
        SIZE=4,
        ),
    Pad(3),
    SIZE=4
    )

chunk = Container("chunk",
    chunk_header,
    BytesRaw("data", SIZE=".header.size"),
    )

sample_header = BitStruct("header",
    Bit("has_next_chunk"),
    UBitEnum("frequency", 
        "invalid",
        "hz_8000",
        "hz_11000",
        "hz_11025",
        "hz_16000",
        "hz_22050",
        "hz_24000",
        "hz_32000",
        "hz_44100",
        "hz_48000",
        SIZE=4
        ),
    Bit("channel_count"),  # add 1 cause at least 1 is assumed
    UBitInt("data_qword_offset", SIZE=28),
    UBitInt("sample_count", SIZE=30),
    SIZE=8,
    )

sample = Container("sample",
    sample_header,
    WhileArray("chunks",
        CASE=has_next_chunk, SUB_STRUCT=chunk
        ),
    STEPTREE=BytesRaw("sample_data",
        SIZE=sample_data_size, POINTER=sample_data_pointer
        )
    )

sample_name = QStruct("sample_name",
    UInt32("offset"),
    STEPTREE=CStrUtf8("name", 
        POINTER=sample_name_pointer, 
        WIDGET_WIDTH=100
        ),
    SIZE=4, 
    )

fmod_bank_header = Struct("header",
    UInt32('sig', DEFAULT=893539142),  # 'FSB5' bytes as little-endian uint32
    UInt32("version", DEFAULT=1),
    UInt32("sample_count"),
    UInt32("sample_headers_size"),
    UInt32("sample_names_size"),
    UInt32("sample_data_size"),
    UEnum32("mode",
        "none",
        "pcm8",
        "pcm16",
        "pcm24",
        "pcm32",
        "pcm_float",
        "gcadpcm",
        "imaadpcm",
        "vag",
        "hevag",
        "xma",
        "mpeg",
        "celt",
        "at9",
        "xwma",
        "vorbis",
        ),
    Pad(8),
    StrHex('hash', SIZE=16),
    StrHex('dummy', SIZE=8),
    SIZE=FMOD_BANK_HEADER_SIZE
    )

fmod_bank_def = TagDef('fmod_bank',
    fmod_bank_header,
    Array("samples", 
        SUB_STRUCT=sample,
        SIZE=".header.sample_count"
        ),
    Array("names", 
        SUB_STRUCT=sample_name, SIZE=".header.sample_count",
        POINTER=sample_name_offsets_pointer,
        DYN_NAME_PATH=".name", WIDGET=DynamicArrayFrame,
        ),
    ext='.fsb', endian='<'
    )
