import ctypes
import pathlib
import tempfile
import threading
import uuid

from reclaimer.sounds import constants, util

try:
    import pyogg
    from pyogg import vorbis as pyogg_vorbis
except ImportError:
    pyogg = pyogg_vorbis = None

TEMP_ROOT   = pathlib.Path(tempfile.gettempdir(), "reclaimer_tmp")
NAME_FORMAT = "ogg_tmpfile_%s.ogg"


def vorbis_file_from_data_stream(data_stream, streaming=False):
    if not (pyogg and constants.OGGVORBIS_AVAILABLE): 
        raise NotImplementedError(
        "OggVorbis decoder not available. Cannot decompress."
        )
    
    # look, it's WAY easier to just dump the file to a temp folder and
    # have VorbisFile decode the entire thing than to try and hook into
    # calling the ogg parsing and vorbis decoder functions on a stream.
    filepath = TEMP_ROOT.joinpath(NAME_FORMAT % threading.get_native_id())
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(data_stream)

    return (
        pyogg.VorbisFileStream if streaming else 
        pyogg.VorbisFile
        )(str(filepath))


def decode_oggvorbis(data_stream):
    vorbis_file = vorbis_file_from_data_stream(data_stream)
    sample_data = vorbis_file.buffer
    sample_rate = vorbis_file.frequency
    compression = constants.OGG_DECOMPRESSED_FORMAT
    encoding    = (
        constants.ENCODING_STEREO if vorbis_file.channels == 2 else
        constants.ENCODING_MONO   if vorbis_file.channels == 1 else
        constants.ENCODING_UNKNOWN
        )

    return sample_data, compression, encoding, sample_rate


def encode_oggvorbis(
        sample_data, channel_count, sample_rate, 
        is_big_endian=False, **kwargs
        ):
    if not (pyogg and constants.OGGVORBIS_ENCODING_AVAILABLE): 
        raise NotImplementedError(
            "OggVorbis encoder not available. Cannot compress."
            )
    data_stream = b''

    return data_stream


def get_pcm_sample_count(data_stream):
    vorbis_file = vorbis_file_from_data_stream(data_stream, streaming=True)
    return pyogg_vorbis.libvorbisfile.ov_pcm_total(
        ctypes.byref(vorbis_file.vf), 0
        )