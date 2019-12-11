import sys

try:
    from reclaimer.sounds.ext import ogg_ext
    OGG_VORBIS_AVAILABLE = True
except ImportError:
    OGG_VORBIS_AVAILABLE = False

try:
    from reclaimer.sounds.ext import wma_ext
    WMA_AVAILABLE = True
except ImportError:
    WMA_AVAILABLE = False
    

DEFAULT_PITCH_RANGE_NAME = "default"
DEFAULT_PERMUTATION_NAME = "unnamed"

SOUND_COMPILE_MODE_NEW = 0
SOUND_COMPILE_MODE_PRESERVE = 1
SOUND_COMPILE_MODE_ADDITIVE = 2


COMPRESSION_UNKNOWN = -1
# NOTE: the ordering of these constants is such that their endianess
# can be swapped by flipping the first bit. This is used in util.py
COMPRESSION_PCM_16_LE = 0  # 16bit signed pcm
COMPRESSION_PCM_16_BE = COMPRESSION_PCM_16_LE + 1
COMPRESSION_PCM_24_LE = 2  # 24bit signed pcm
COMPRESSION_PCM_24_BE = COMPRESSION_PCM_24_LE + 1
COMPRESSION_PCM_32_LE = 4  # 32bit signed pcm
COMPRESSION_PCM_32_BE = COMPRESSION_PCM_32_LE + 1

COMPRESSION_PCM_8_SIGNED   = 6
COMPRESSION_PCM_8_UNSIGNED = 7

COMPRESSION_ADPCM = 16
COMPRESSION_OGG   = 17  # halo pc only
COMPRESSION_WMA   = 18  # halo 2 only

# these encoding constants mirror halo 1/2 enum values.
ENCODING_UNKNOWN = -1
ENCODING_MONO   = 0
ENCODING_STEREO = 1
ENCODING_CODEC  = 2

SAMPLE_RATE_22K = 22050
SAMPLE_RATE_32K = 32000
SAMPLE_RATE_44K = 44100

SAMPLE_RATE_VOICE = 7350  # Chosen as it should filter out high frequency
#                           signals while being high enough fidelity to
#                           capture the human voice frequency range.
#                           Also chosen rather than 8000 as it divides
#                           22050 and 44100 into whole integers.

SAMPLE_RATE_MOUTH_DATA = 30

MAX_SAMPLE_CHUNK_SIZE   = 0x400000
MAX_MOUTH_DATA          = 0x2000
MAX_OGG_DECOMP_BUFFER_SIZE = 0xE3800

ADPCM_SAMPLE_CHUNK_SIZE = 0x10000

ADPCM_COMPRESSED_BLOCKSIZE   = 36
ADPCM_DECOMPRESSED_BLOCKSIZE = 128

WAV_FORMAT_PCM = 0x0001
WAV_FORMAT_IMA_ADPCM = 0x0011
WAV_FORMAT_XBOX_ADPCM = 0x0069

ALLOWED_WAV_FORMATS = set((
    WAV_FORMAT_PCM,
    WAV_FORMAT_IMA_ADPCM,
    WAV_FORMAT_XBOX_ADPCM
    ))

# Endianness interop constants
if sys.byteorder == "little":
    ADPCM_DECOMPRESSED_FORMAT = COMPRESSION_PCM_16_LE
    DEFAULT_UNCOMPRESSED_FORMAT = COMPRESSION_PCM_16_LE
    HIGHEST_FIDELITY_FORMAT = COMPRESSION_PCM_32_LE
    NATIVE_ENDIANNESS_FORMATS = {
        COMPRESSION_PCM_16_LE, COMPRESSION_PCM_24_LE,
        COMPRESSION_PCM_32_LE,
        COMPRESSION_PCM_8_SIGNED, COMPRESSION_PCM_8_UNSIGNED
        }
else:
    ADPCM_DECOMPRESSED_FORMAT = COMPRESSION_PCM_16_BE
    DEFAULT_UNCOMPRESSED_FORMAT = COMPRESSION_PCM_16_BE
    HIGHEST_FIDELITY_FORMAT = COMPRESSION_PCM_32_BE
    NATIVE_ENDIANNESS_FORMATS = {
        COMPRESSION_PCM_16_BE, COMPRESSION_PCM_24_BE,
        COMPRESSION_PCM_32_BE,
        COMPRESSION_PCM_8_SIGNED, COMPRESSION_PCM_8_UNSIGNED
        }

PCM_FORMATS = {
    COMPRESSION_PCM_16_LE, COMPRESSION_PCM_16_BE,
    COMPRESSION_PCM_24_LE, COMPRESSION_PCM_24_BE,
    COMPRESSION_PCM_32_LE, COMPRESSION_PCM_32_BE,
    COMPRESSION_PCM_8_SIGNED, COMPRESSION_PCM_8_UNSIGNED
    }

channel_counts = {
    ENCODING_UNKNOWN: 1,
    ENCODING_MONO:    1,
    ENCODING_STEREO:  2,
    ENCODING_CODEC:   6,
    }

sample_widths = {
    COMPRESSION_PCM_8_SIGNED: 1,
    COMPRESSION_PCM_8_UNSIGNED: 1,
    COMPRESSION_PCM_16_LE: 2,
    COMPRESSION_PCM_16_BE: 2,
    COMPRESSION_PCM_24_LE: 3,
    COMPRESSION_PCM_24_BE: 3,
    COMPRESSION_PCM_32_LE: 4,
    COMPRESSION_PCM_32_BE: 4,
    }

# maps wave format enum options and sample widths to our compression constants
wav_format_mapping = {
    (WAV_FORMAT_PCM, 1): COMPRESSION_PCM_8_UNSIGNED,
    (WAV_FORMAT_PCM, 2): COMPRESSION_PCM_16_LE,
    (WAV_FORMAT_PCM, 3): COMPRESSION_PCM_24_LE,
    (WAV_FORMAT_PCM, 4): COMPRESSION_PCM_32_LE,
    (WAV_FORMAT_IMA_ADPCM, None): COMPRESSION_ADPCM,
    (WAV_FORMAT_XBOX_ADPCM, None): COMPRESSION_ADPCM,
    }

# these mappings key halo 1 compression enums
# to the compression/sample rate constants
halo_1_compressions = {
    0: COMPRESSION_PCM_16_LE,
    1: COMPRESSION_ADPCM,
    2: COMPRESSION_ADPCM,
    3: COMPRESSION_OGG,
    }
halo_1_sample_rates = {
    0: SAMPLE_RATE_22K,
    1: SAMPLE_RATE_44K,
    }

# these mappings key halo 2 compression enums
# to the compression/sample rate constants
halo_2_compressions = {
    0: COMPRESSION_PCM_16_BE,
    1: COMPRESSION_ADPCM,
    2: COMPRESSION_ADPCM,
    3: COMPRESSION_PCM_16_LE,
    4: COMPRESSION_WMA,
    }
halo_2_sample_rates = {
    0: SAMPLE_RATE_22K,
    1: SAMPLE_RATE_44K,
    2: SAMPLE_RATE_32K,
    }

# unneeded for export
del sys
