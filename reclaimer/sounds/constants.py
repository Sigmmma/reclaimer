#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import sys

PLAYBACK_AVAILABLE  = False
OGGVORBIS_AVAILABLE = False
FLAC_AVAILABLE      = False
OPUS_AVAILABLE      = False
WMA_AVAILABLE       = False

OGGVORBIS_ENCODING_AVAILABLE = False

try:
    import pyogg
    OGGVORBIS_AVAILABLE = (
        pyogg.PYOGG_OGG_AVAIL and
        pyogg.PYOGG_VORBIS_AVAIL and 
        pyogg.PYOGG_VORBIS_FILE_AVAIL
        )
    FLAC_AVAILABLE = pyogg.PYOGG_FLAC_AVAIL
    OPUS_AVAILABLE = (
        pyogg.PYOGG_OPUS_AVAIL and
        pyogg.PYOGG_OPUS_FILE_AVAIL
        )
    # encoding isn't available in all releases
    OGGVORBIS_ENCODING_AVAILABLE = OGGVORBIS_AVAILABLE and getattr(
        pyogg, "PYOGG_VORBIS_ENC_AVAIL", False
        )

    # NOTE: for right now these won't be available.
    #       still need to implement them.
    OGGVORBIS_ENCODING_AVAILABLE = False
    OPUS_AVAILABLE = FLAC_AVAILABLE = False
except ImportError:
    pass

try:
    import simpleaudio
    del simpleaudio
    PLAYBACK_AVAILABLE = True
except ImportError:
    pass


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

COMPRESSION_XBOX_ADPCM = 16
COMPRESSION_IMA_ADPCM  = 17
COMPRESSION_OGG   = 18  # halo pc only
COMPRESSION_WMA   = 19  # halo 2 only

# picking much higher enum values that will never actually be used
COMPRESSION_OPUS  = 1024
COMPRESSION_FLAC  = 1025

# these encoding constants mirror halo 1/2 enum values.
ENCODING_UNKNOWN = -1
ENCODING_MONO   = 0
ENCODING_STEREO = 1
ENCODING_CODEC  = 2

SAMPLE_RATE_22K = 22050
SAMPLE_RATE_32K = 32000
SAMPLE_RATE_44K = 44100

# Halo constants
DEFAULT_PITCH_RANGE_NAME = "default"

SAMPLE_RATE_MOUTH_DATA = 30

MAX_SAMPLE_CHUNK_SIZE = 0x400000
MAX_MOUTH_DATA        = 0x2000
DEF_SAMPLE_CHUNK_SIZE = 0x38E00  # the number of bytes of pcm data
#                                  to split input samples into when
#                                  splitting into smaller chunks

MAX_HALO_SAMPLE_RATE = 48000

XBOX_ADPCM_COMPRESSED_BLOCKSIZE   = 36
XBOX_ADPCM_DECOMPRESSED_BLOCKSIZE = 128
IMA_ADPCM_COMPRESSED_BLOCKSIZE   = 36   # not correct
IMA_ADPCM_DECOMPRESSED_BLOCKSIZE = 128  # not correct

# Wave file format constants
WAV_FORMAT_PCM        = 0x0001
WAV_FORMAT_PCM_FLOAT  = 0x0003
WAV_FORMAT_IMA_ADPCM  = 0x0011
WAV_FORMAT_XBOX_ADPCM = 0x0069

ALLOWED_WAV_FORMATS = set((
    WAV_FORMAT_PCM,
    WAV_FORMAT_PCM_FLOAT,
    WAV_FORMAT_IMA_ADPCM,
    WAV_FORMAT_XBOX_ADPCM
    ))
PYOGG_CONTAINER_FORMATS = set((
    COMPRESSION_OGG,
    COMPRESSION_OPUS,
    COMPRESSION_FLAC,
    ))

CONTAINER_EXT_WAV  = ".wav"
CONTAINER_EXT_OGG  = ".ogg"
CONTAINER_EXT_OPUS = ".opus"
CONTAINER_EXT_FLAC = ".flac"
PYOGG_CONTAINER_EXTS = frozenset((
    CONTAINER_EXT_OGG, 
    CONTAINER_EXT_OPUS, 
    CONTAINER_EXT_FLAC
    ))
SUPPORTED_CONTAINER_EXTS = frozenset((
    CONTAINER_EXT_WAV,
    *([CONTAINER_EXT_OGG]  if OGGVORBIS_AVAILABLE else []),
    *([CONTAINER_EXT_OPUS] if OPUS_AVAILABLE      else []),
    *([CONTAINER_EXT_FLAC] if FLAC_AVAILABLE      else []),
    ))

# for all our purposes we only care about 
# decoding ogg to little-endian 16bit pcm
OGG_DECOMPRESSED_FORMAT = COMPRESSION_PCM_16_LE

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
    (WAV_FORMAT_IMA_ADPCM, None): COMPRESSION_IMA_ADPCM,
    (WAV_FORMAT_XBOX_ADPCM, None): COMPRESSION_XBOX_ADPCM,
    }

# these mappings key halo 1 compression enums
# to the compression/sample rate constants
halo_1_compressions = {
    0: COMPRESSION_PCM_16_LE,
    1: COMPRESSION_XBOX_ADPCM,
    2: COMPRESSION_IMA_ADPCM,
    3: COMPRESSION_OGG,
    }
halo_1_sample_rates = {
    0: SAMPLE_RATE_22K,
    1: SAMPLE_RATE_44K,
    }
halo_1_encodings = {
    0: ENCODING_MONO,
    1: ENCODING_STEREO,
    }

# these mappings key halo 2 compression enums
# to the compression/sample rate constants
halo_2_compressions = {
    0: COMPRESSION_PCM_16_BE,
    1: COMPRESSION_XBOX_ADPCM,
    2: COMPRESSION_IMA_ADPCM,
    3: COMPRESSION_PCM_16_LE,
    4: COMPRESSION_WMA,
    }
halo_2_sample_rates = {
    0: SAMPLE_RATE_22K,
    1: SAMPLE_RATE_44K,
    2: SAMPLE_RATE_32K,
    }
halo_2_encodings = {
    0: ENCODING_MONO,
    1: ENCODING_STEREO,
    2: ENCODING_CODEC,
    }

# unneeded for export
del sys
