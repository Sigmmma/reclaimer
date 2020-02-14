#include "../../src/shared.h"
#include "adpcm-xq/adpcm-lib.h"

const static int ADPCM_STEP_TABLE_MAX_INDEX = sizeof(step_table) / sizeof(step_table[0]) - 1;
const static int XBOX_ADPCM_ENCODED_BLOCKSIZE = 36;
const static int XBOX_ADPCM_DECODED_BLOCKSIZE = 128;


// Description of ADPCM stream block:
//   The stream starts with a 4 byte chunk for each audio channel:
//     bytes 0-2: the initial 16bit pcm sample(little endian sint16)
//     byte 2:    the initial step table index
//       NOTE: do a CLAMP(0, ADPCM_STEP_TABLE_SIZE))
//     byte 3: reserved(usually left at 0)
//
//   The rest of the stream is alternating chunks of adpcm codes for each channel.
//   Each chunk is 4 bytes, and contains 8 codes. The code bytes are sequential, 
//   and the first nibble of each byte is the first code. So the stream will look
//   like this:
//     channel 0: (left)   b0   b1   b2   b3
//     channel 1: (right)  b4   b5   b6   b7
//     channel 0: (left)   b8   b9   b10  b11
//     channel 1: (right)  b12  b13  b14  b15
//     cont...

typedef struct {
    sint16 pcm_sample;  /* the current decoded adpcm sample. When calling
    **                     decode_adpcm_sample this is supposed to be the
    **                     predictor for decoding the next sample. Contains
    **                     the decoded sample when the function returns.*/
    sint8 index;  /* An index into step_table.
    **               Used for calculating the current differential step.
    **               Contains the next step index when the function returns.*/
    uint8 code;  /* An index into index_table.
    **              The 4bit adpcm code for calculating the next differential index.
    **              Update this before calling decode_adpcm_sample.*/
} AdpcmState;


/* This function will decode the next adpcm sample given as an AdpcmState struct.
This function accepts and returns the whole struct since it can easily fit in a
single 32bit register, and should be more efficient than passing a pointer to a struct.
*/
static AdpcmState decode_adpcm_sample(AdpcmState state) {
    int delta, step_size = step_table[state.index];
    int result = state.pcm_sample;  /* pcm_sample could over/underflow in the code below,
    **                                 so we keep the result as an int for clamping.*/

    delta = step_size >> 3;
    if (state.code & 4) delta += step_size;
    if (state.code & 2) delta += step_size >> 1;
    if (state.code & 1) delta += step_size >> 2;
    if (state.code & 8) delta = -delta;

    result += delta;

    if (result >= 32767)
        state.pcm_sample = 32767;
    else if (result <= -32768)
        state.pcm_sample = -32768;
    else
        state.pcm_sample = (sint16)result;

    state.index += index_table[state.code];
    if (state.index < 0)
        state.index = 0;
    else if (state.index > ADPCM_STEP_TABLE_MAX_INDEX)
        state.index = ADPCM_STEP_TABLE_MAX_INDEX;

    return state;
}


static void decode_xbadpcm_stream(
    Py_buffer *adpcm_stream_buf, Py_buffer *pcm_stream_buf,
    uint8 channel_count, uint32 code_chunks_count) {

    AdpcmState adpcm_states[MAX_AUDIO_CHANNEL_COUNT];
    int block_count = (int)(
        adpcm_stream_buf->len / 
        (channel_count * (4 + 4 * code_chunks_count)));
    uint8 *adpcm_stream = adpcm_stream_buf->buf;
    sint16 *pcm_stream = pcm_stream_buf->buf;
    uint32 codes;
    uint32 samples_per_chunk = 8 * channel_count;
    uint32 samples_this_chunk = 0, samples_remaining_this_block = 0;
    uint32 samples_per_block = samples_per_chunk * code_chunks_count;
    uint32 samples_decoded = 0;

    if (channel_count < 0)
        return;

    for (int b = 0; b < block_count; b++) {
        samples_remaining_this_block = samples_per_block;
        // initialize the adpcm state structs
        for (int c = 0; c < channel_count; c++) {
            adpcm_states[c].pcm_sample = adpcm_stream[0] | (adpcm_stream[1] << 8);
            adpcm_states[c].index = adpcm_stream[2];
            adpcm_stream += 4;

            pcm_stream[0] = adpcm_states[c].pcm_sample;
            pcm_stream++;
            samples_remaining_this_block--;

            if (adpcm_states[c].index < 0)
                adpcm_states[c].index = 0;
            else if (adpcm_states[c].index > ADPCM_STEP_TABLE_MAX_INDEX)
                adpcm_states[c].index = ADPCM_STEP_TABLE_MAX_INDEX;
        }

        while (samples_remaining_this_block) {
            // loop over each channel in each chunk
            if (samples_remaining_this_block < samples_per_chunk)
                samples_this_chunk = samples_remaining_this_block;
            else
                samples_this_chunk = samples_per_chunk;

            for (int c = 0; c < channel_count; c++) {
                // OR the codes together for easy access
                codes = (
                     adpcm_stream[0] | 
                    (adpcm_stream[1] << 8) |
                    (adpcm_stream[2] << 16) |
                    (adpcm_stream[3] << 24));
                adpcm_stream += 4;

                // loop over the 8 codes in this channels chunk.
                // loop is structured like this to properly interleave the pcm data.
                // otherwise we would have to store the decoded samples to several temp
                // buffers and then interleave those temp buffers into the pcm stream.
                for (int i = c; i < samples_this_chunk; i += channel_count) {
                    adpcm_states[c].code = codes & 0xF;
                    codes >>= 4;
                    adpcm_states[c] = decode_adpcm_sample(adpcm_states[c]);
                    pcm_stream[i] = adpcm_states[c].pcm_sample;
                }
            }
            // skip over the chunk of samples we just decoded
            pcm_stream += samples_this_chunk;
            samples_remaining_this_block -= samples_this_chunk;
        }
    }
}


static void encode_xbadpcm_stream(
    Py_buffer *pcm_stream_buf, Py_buffer *adpcm_stream_buf,
    uint8 channel_count, uint32 code_chunks_count, uint16 lookahead, uint8 noise_shaping) {

    sint16 *pcm_stream = pcm_stream_buf->buf;
    uint8 *adpcm_stream = adpcm_stream_buf->buf;

    uint32 sample_count = pcm_stream_buf->len / (channel_count * sizeof(sint16));
    uint32 samples_per_block = code_chunks_count * 8;
    uint32 block_count = sample_count / samples_per_block;
    size_t num_bytes_decoded = 0;

    uint32 pcm_block_size   = samples_per_block * channel_count;  // number of pcm sint16 per block
    uint32 adpcm_block_size = (code_chunks_count * 4 + 4) * channel_count;  // number of adpcm bytes per block

    sint32 average_deltas[MAX_AUDIO_CHANNEL_COUNT];
    void *adpcm_context = NULL;

    // calculate initial adpcm predictors using decaying average
    for (int c = 0; c < channel_count; c++) {
        average_deltas[c] = 0;
        for (int i = c + pcm_block_size - channel_count; i >= channel_count; i -= channel_count) {
            average_deltas[c] = (average_deltas[c] / 8) + abs(
                (sint32)pcm_stream[i] - pcm_stream[i - channel_count]);
        }
        average_deltas[c] /= 8;
    }

    adpcm_context = adpcm_create_context(channel_count, lookahead, noise_shaping, average_deltas);
    for (int b = 0; b < block_count; b++) {
        adpcm_encode_block(adpcm_context, adpcm_stream, &num_bytes_decoded, pcm_stream, samples_per_block);
        adpcm_stream += adpcm_block_size;
        pcm_stream += pcm_block_size;
    }
    adpcm_free_context(adpcm_context);
}


static PyObject *py_decode_xbadpcm_samples(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    uint8 channel_count;
    int block_count;

    if (!PyArg_ParseTuple(args, "y*w*b:decode_xbadpcm_samples",
        &bufs[0], &bufs[1], &channel_count)) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    block_count = (int)(bufs[0].len / (channel_count * XBOX_ADPCM_ENCODED_BLOCKSIZE));

    // handle invalid data sizes and such
    if (bufs[0].len % XBOX_ADPCM_ENCODED_BLOCKSIZE)
        PySys_FormatStdout("Provided xbadpcm buffer is not a multiple of block size.\n");
    else if (bufs[1].len < block_count * XBOX_ADPCM_DECODED_BLOCKSIZE)
        PySys_FormatStdout("Provided pcm buffer is not large enough to hold decoded data.\n");
    else if (channel_count > MAX_AUDIO_CHANNEL_COUNT)
        PySys_FormatStdout("Too many channels to decode in xbadpcm stream.\n");
    else {
        // do the decoding!
        decode_xbadpcm_stream(&bufs[0], &bufs[1], channel_count, 8);
    }

    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs)

    return Py_BuildValue("");  // return Py_None while incrementing it
}


static PyObject *py_encode_xbadpcm_samples(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    uint8 channel_count, noise_shaping = NOISE_SHAPING_OFF, lookahead = 3;
    int block_count;

    if (!PyArg_ParseTuple(args, "y*w*b|BB:encode_xbadpcm_samples",
        &bufs[0], &bufs[1], &channel_count, &noise_shaping, &lookahead)) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    block_count = (int)(bufs[0].len / (channel_count * XBOX_ADPCM_DECODED_BLOCKSIZE));

    // handle invalid data sizes and such
    if (bufs[0].len % XBOX_ADPCM_DECODED_BLOCKSIZE)
        PySys_FormatStdout("Provided pcm buffer is not a multiple of block size.\n");
    else if (bufs[1].len < block_count * XBOX_ADPCM_ENCODED_BLOCKSIZE)
        PySys_FormatStdout("Provided xbadpcm buffer is not large enough to hold encoded data.\n");
    else if (channel_count > MAX_AUDIO_CHANNEL_COUNT)
        PySys_FormatStdout("Too many channels to encode to adpcm.\n");
    else if (noise_shaping != NOISE_SHAPING_OFF &&
             noise_shaping != NOISE_SHAPING_STATIC &&
             noise_shaping != NOISE_SHAPING_DYNAMIC)
        PySys_FormatStdout("Invalid value for noise_shaping parameter.\n");
    else if (lookahead > 5)
        PySys_FormatStdout("Invalid value for lookahead parameter. Must be in the range [0, 5]\n");
    else {
        // do the encoding!
        encode_xbadpcm_stream(&bufs[0], &bufs[1], channel_count, 8, lookahead, noise_shaping);
    }

    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs)

    return Py_BuildValue("");  // return Py_None while incrementing it
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef adpcm_ext_methods[] = {
    {"decode_xbadpcm_samples", py_decode_xbadpcm_samples, METH_VARARGS, ""},
    {"encode_xbadpcm_samples", py_encode_xbadpcm_samples, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef adpcm_ext_module = {
    PyModuleDef_HEAD_INIT,
    "adpcm_ext",
    "A set of C functions to replace certain speed intensive ADPCM functions",
    -1,
    adpcm_ext_methods,
};

PyMODINIT_FUNC PyInit_adpcm_ext(void) {
    return PyModule_Create(&adpcm_ext_module);
}
