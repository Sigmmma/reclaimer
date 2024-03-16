import ctypes
import io
import itertools
import pathlib
import random
import threading

import reclaimer
from reclaimer.sounds import constants, util

try:
    import pyogg
    from pyogg import vorbis as pyogg_vorbis, ogg as pyogg_ogg
except ImportError:
    pyogg = pyogg_vorbis = pyogg_ogg = None


class VorbisEncoderSetupError(Exception):
    pass

class VorbisAnalysisError(Exception):
    pass


# ogg does analysis and compression on 1024 float samples at a time
OGG_ANALYSIS_BUFFER_SIZE = 1024


def pyogg_audiofile_from_filepath(filepath, ext=None, streaming=False):
    cls = _get_pyogg_class(filepath, ext, streaming)
    return cls(str(filepath))


def pyogg_audiofile_from_data_stream(data_stream, ext, streaming=False):
    # look, it's WAY easier to just dump the file to a temp folder and
    # have VorbisFile decode the entire thing than to try and hook into
    # calling the ogg parsing and vorbis decoder functions on a stream.
    # TODO: linux supports memory-only files, so look into doing that
    #       so we don't have to dump to a temp directory on linux.
    filepath = constants.TEMP_ROOT.joinpath(
        constants.OGGVORBIS_TMPNAME_FORMAT % (
            threading.get_native_id(), ext
            )
        )
    cls = _get_pyogg_class(filepath, ext, streaming)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(data_stream)

    return cls(str(filepath))


def get_ogg_pcm_sample_count(data_stream):
    vorbis_file = pyogg_audiofile_from_data_stream(
        data_stream, constants.CONTAINER_EXT_OGG, streaming=True
        )
    return pyogg_vorbis.libvorbisfile.ov_pcm_total(
        ctypes.byref(vorbis_file.vf), 0
        )


def decode_oggvorbis(data_stream):
    vorbis_file = pyogg_audiofile_from_data_stream(
        data_stream, constants.CONTAINER_EXT_OGG, streaming=False
        )
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
        sample_data, sample_rate, sample_width, channels, is_big_endian=False,
        bitrate_lower=-1, bitrate_nominal=-1, bitrate_upper=-1,
        quality_setting=1.0, use_quality_value=True, bitrate_managed=True
        ):
    if not (pyogg and constants.OGGVORBIS_ENCODING_AVAILABLE): 
        raise NotImplementedError(
            "OggVorbis encoder not available. Cannot compress."
            )
    elif channels not in (1, 2):
        raise NotImplementedError(
            "Cannot encode %s channel audio to OggVorbis." % channels
            )
    elif sample_width not in (1, 2, 4):
        raise NotImplementedError(
            "Cannot encode %s-byte width samples to OggVorbis." % width
            )

    # one Ogg bitstream page. Vorbis packets inside
    opg   = pyogg_ogg.ogg_page()
    opg_p = ctypes.pointer(opg)

    # one raw packet of data for decode
    opk_p = ctypes.pointer(pyogg_ogg.ogg_packet())
    # takes pages, weld into a logical packet stream
    oss_p = ctypes.pointer(pyogg_ogg.ogg_stream_state())

    # local working space for packet->PCM decode
    vbl_p = ctypes.pointer(pyogg_vorbis.vorbis_block())
    # struct that stores all user comments
    vco_p = ctypes.pointer(pyogg_vorbis.vorbis_comment())
    # central working state for packet->PCM decoder
    vds_p = ctypes.pointer(pyogg_vorbis.vorbis_dsp_state())
    # struct storing all static vorbis bitstream settings
    vin_p = ctypes.pointer(pyogg_vorbis.vorbis_info())

    pyogg_vorbis.vorbis_info_init(vin_p)

    if use_quality_value:
        err = pyogg_vorbis.vorbis_encode_init_vbr(vin_p,
            ctypes.c_int(channels),
            ctypes.c_int(sample_rate),
            ctypes.c_float(quality_setting)
            )
    else:
        err = pyogg_vorbis.vorbis_encode_init(vin_p,
            ctypes.c_int(channels),
            ctypes.c_int(sample_rate),
            ctypes.c_int(bitrate_upper), 
            ctypes.c_int(bitrate_nominal), 
            ctypes.c_int(bitrate_lower)
            )

    if err:
        raise VorbisEncoderSetupError(
            "Vorbis encoder returned error code during setup. "
            "Encoder settings are likely incorrect."
            )

    # create an output buffer
    ogg_data = io.BytesIO()

    # add comments
    pyogg_vorbis.vorbis_comment_init(vco_p)
    for string in (
            str.encode("RECLAIMERVER=%s.%s.%s" % reclaimer.__version__),
            str.encode("PYOGGVER=%s" % pyogg.__version__),
            ):
        pyogg_vorbis.vorbis_comment_add(vco_p,
            ctypes.create_string_buffer(string)
            )

    # set up the analysis state and auxiliary encoding storage
    pyogg_vorbis.vorbis_analysis_init(vds_p, vin_p)
    pyogg_vorbis.vorbis_block_init(vds_p, vbl_p)

    # initialise stream state
    # pick a random serial number; that way we can more
    # likely build chained streams just by concatenation
    pyogg_ogg.ogg_stream_init(oss_p, _get_random_serial_no())

    # Vorbis streams begin with three headers; the initial header
    # (with most of the codec setup parameters) which is mandated
    # by the Ogg bitstream spec. The second header holds any comment
    # fields. The third header holds the bitstream codebook. 
    # We merely need to make the headers and pass them to libvorbis one
    # by one; libvorbis handles the additional Ogg bitstream constraints
    ovh_p      = ctypes.pointer(pyogg_ogg.ogg_packet())
    ovh_comm_p = ctypes.pointer(pyogg_ogg.ogg_packet())
    ovh_code_p = ctypes.pointer(pyogg_ogg.ogg_packet())

    pyogg_vorbis.vorbis_analysis_headerout(
        vds_p, vco_p, ovh_p, ovh_comm_p, ovh_code_p
        )
    pyogg_ogg.ogg_stream_packetin(oss_p, ovh_p)
    pyogg_ogg.ogg_stream_packetin(oss_p, ovh_comm_p)
    pyogg_ogg.ogg_stream_packetin(oss_p, ovh_code_p)

    # per spec, ensure vorbis audio data starts on a new page, so
    # we need to flush the current page and start a new one
    while pyogg_ogg.ogg_stream_flush(oss_p, opg_p):
        _write_ogg_page(ogg_data, opg)

    # deinterleave the audio if it's stereo, and convert it to float
    inp_buffers = [
        util.convert_pcm_int_to_pcm_float32(buffer, sample_width, True)
        for buffer in (
            util.deinterleave_stereo(sample_data, sample_width, True)
            if channels == 2 else [sample_data]
            )
        ]

    i, sample_count   = 0, min(len(b) for b in inp_buffers)
    samples_per_chunk = OGG_ANALYSIS_BUFFER_SIZE // channels
    vorbis_buf_size   = ctypes.c_int(OGG_ANALYSIS_BUFFER_SIZE)

    # if using bitrate managed encoding, vorbis coded block is not
    # dumped directly to a packet. instead, it must be flushed using
    # vorbis_bitrate_flushpacket after calling vorbis_bitrate_addblock.
    # when not using bitrate managed encoding, we pass the pointer to
    # the packet the vorbis analysis should dump its results directly to.
    vorbis_out_opk_p  = None if bitrate_managed else opk_p

    # encode the pcm data to vorbis and dump it to the ogg_data buffer
    while i <= sample_count:
        # figure out how much data to pass to the analysis buffer
        read = min(sample_count - i, samples_per_chunk)

        # transfer sample data to analysis buffer(if any)
        if read:
            vorbis_buffers = pyogg_vorbis.vorbis_analysis_buffer(
                vds_p, vorbis_buf_size
                )
            for c in range(channels):
                tuple(
                    itertools.starmap(
                    vorbis_buffers[c].__setitem__,
                    enumerate(inp_buffers[c][i: i+read])
                    ))

            i += read

        # tell the vorbis encoder how many samples to analyze
        pyogg_vorbis.vorbis_analysis_wrote(vds_p, ctypes.c_int(read))

        # get a single block for encoding
        while pyogg_vorbis.vorbis_analysis_blockout(vds_p, vbl_p) == 1:
            # do analysis
            res = pyogg_vorbis.vorbis_analysis(vbl_p, vorbis_out_opk_p)
            if res:
                raise VorbisAnalysisError("Vorbis analysis returned error: %d" % res)

            # NOTE: we're ALWAYS going to use the bitrate management
            #       system, as there are no downsides, but i am keeping
            #       this code here as an example of how to not use it.
            # see here for why:  
            #   https://xiph.org/vorbis/doc/libvorbis/overview.html
            #
            if not bitrate_managed:
                pyogg_ogg.ogg_stream_packetin(oss_p, opk_p)
                while pyogg_ogg.ogg_stream_pageout(oss_p, opg_p):
                    _write_ogg_page(ogg_data, opg)

                continue

            pyogg_vorbis.vorbis_bitrate_addblock(vbl_p)

            # while there are packets to flush, weld them into 
            # the bitstream and write out any resulting pages.
            while pyogg_vorbis.vorbis_bitrate_flushpacket(vds_p, opk_p) == 1:
                pyogg_ogg.ogg_stream_packetin(oss_p, opk_p)
                while pyogg_ogg.ogg_stream_pageout(oss_p, opg_p):
                    _write_ogg_page(ogg_data, opg)

        if pyogg_ogg.ogg_page_eos(opg_p):
            i = sample_count + 1
            break

    # ensure everything is flushed
    while pyogg_ogg.ogg_stream_flush(oss_p, opg_p):
        _write_ogg_page(ogg_data, opg)

    # finish up by clearing everything
    pyogg_ogg.ogg_stream_clear(oss_p)
    pyogg_vorbis.vorbis_block_clear(vbl_p)
    pyogg_vorbis.vorbis_comment_clear(vco_p)
    pyogg_vorbis.vorbis_dsp_clear(vds_p)
    pyogg_vorbis.vorbis_info_clear(vin_p)

    ogg_bitstream_bytes = ogg_data.getbuffer().tobytes()
    return ogg_bitstream_bytes


def _get_random_serial_no(bit_count=(ctypes.sizeof(ctypes.c_int)*8)):
    return ctypes.c_int(random.randint(
        -(1<<(bit_count - 1)),
        (1<<(bit_count - 1))-1
        ))


def _c_pointer_to_buffer(pointer, buf_len, buf_typ=ctypes.c_ubyte):
    BufferPtr = ctypes.POINTER(buf_typ * buf_len)
    return BufferPtr(pointer)[0]


def _write_ogg_page(buffer, ogg_page):
    buffer.write(_c_pointer_to_buffer(
        ogg_page.header.contents, ogg_page.header_len
        ))
    buffer.write(_c_pointer_to_buffer(
        ogg_page.body.contents, ogg_page.body_len
        ))


def _get_pyogg_class(filepath=None, ext=None, streaming=False):
    if filepath and ext is None:
        ext = pathlib.Path(filepath).suffix

    if not pyogg: 
        raise NotImplementedError("PyOgg not available. Cannot open files.")
    elif ext not in constants.PYOGG_CONTAINER_EXTS:
        raise ValueError("Unknown PyOgg extension '%s'" % ext)
    elif ((ext == constants.CONTAINER_EXT_OPUS and not constants.OPUS_AVAILABLE) or
          (ext == constants.CONTAINER_EXT_FLAC and not constants.FLAC_AVAILABLE) or
          (ext == constants.CONTAINER_EXT_OGG  and not constants.OGGVORBIS_AVAILABLE)
          ):
        raise NotImplementedError(
            "PyOgg was improperly initialized. Cannot open '%s' files" % ext
            )

    return (
        (pyogg.OpusFileStream if streaming else pyogg.OpusFile)
        if ext == constants.CONTAINER_EXT_OPUS else
        (pyogg.FlacFileStream if streaming else pyogg.FlacFile)
        if ext == constants.CONTAINER_EXT_FLAC else
        (pyogg.VorbisFileStream if streaming else pyogg.VorbisFile)
        # NOTE: not checking for ogg ext cause it was done above
        )