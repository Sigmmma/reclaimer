#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.common_descs import *
from .objs.fmod import FModSoundBankTag,\
    FMOD_BANK_HEADER_SIZE, FMOD_SAMPLE_CHUNK_SIZE
from supyr_struct.defs.tag_def import TagDef


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


def sample_data_size(
        parent=None, node=None, attr_index=None, 
        new_val=None, root_offset=0, offset=0, rawdata=None,
        **kwargs
        ):
    if new_val is not None:
        # can't set size here
        return
    elif parent is not None and attr_index is not None:
        node = parent[attr_index]

    if node is not None:
        return len(node)

    sample_array = getattr(parent, "parent", None)
    if not sample_array or not rawdata:
        # NOTE: checking if rawdata is passed to indicate that
        #       we're actually trying to parse from something.
        #       if it's not, we've appended an empty block.
        return 0

    next_sample_index = sample_array.index_by_id(parent) + 1
    if next_sample_index >= len(sample_array):
        start  = parent.header.data_qword_offset * FMOD_SAMPLE_CHUNK_SIZE
        end    = sample_array.parent.header.sample_data_size
    else:
        start  = sample_data_pointer(parent=parent)
        end    = sample_data_pointer(parent=sample_array[next_sample_index])

    return max(0, end - start)


def sample_data_pointer(parent=None, root_offset=0, offset=0, **kwargs):
    sample_header = parent.header
    bank_header = _get_fmod_bank(sample_header).header
    return (
        root_offset + offset + FMOD_BANK_HEADER_SIZE +
        bank_header.sample_headers_size +
        bank_header.sample_names_size +
        sample_header.data_qword_offset * FMOD_SAMPLE_CHUNK_SIZE
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
    UInt32('sample_index'),
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
        "invalid",
        "channels",
        "frequency",
        "loop",
        "unknown4",
        "unknown5",
        "xma_seek",
        "dsp_coeff",
        "unknown8",
        "unknown9",
        "xwma_data",
        "vorbis_data",
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
    StrHex('hash', SIZE=8),
    StrHex('guid', SIZE=16),
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
    ext='.fsb', endian='<', tag_cls=FModSoundBankTag
    )
