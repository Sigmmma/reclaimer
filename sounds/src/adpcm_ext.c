#include "shared.h"


const static int ADPCM_STEP_TABLE[89] = {
    7, 8, 9, 10, 11, 12, 13, 14, 16, 17,
    19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
    50, 55, 60, 66, 73, 80, 88, 97, 107, 118,
    130, 143, 157, 173, 190, 209, 230, 253, 279, 307,
    337, 371, 408, 449, 494, 544, 598, 658, 724, 796,
    876, 963, 1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066,
    2272, 2499, 2749, 3024, 3327, 3660, 4026, 4428, 4871, 5358,
    5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487, 12635, 13899,
    15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
    };
const static int ADPCM_INDEX_TABLE[16] = {
    -1, -1, -1, -1, 2, 4, 6, 8,
    -1, -1, -1, -1, 2, 4, 6, 8
    };
const static int ADPCM_STEP_TABLE_MAX_INDEX = sizeof(ADPCM_STEP_TABLE) / sizeof(ADPCM_STEP_TABLE[0]) - 1;
const static int XBOX_ADPCM_DIFF_SAMPLE_COUNT = 64;


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
    sint8 index;  /* An index into ADPCM_STEP_TABLE.
    **               Used for calculating the current differential step.
    **               Contains the next step index when the function returns.*/
    uint8 code;  /* An index into ADPCM_INDEX_TABLE.
    **              The 4bit adpcm code for calculating the next differential index.
    **              Update this before calling decode_adpcm_sample.*/
} AdpcmState;


static int get_adpcm_encoded_blocksize(int coded_sample_count) {
    return 4 + ((coded_sample_count + 1) / 2);
}
static int get_adpcm_decoded_blocksize(int coded_sample_count) {
    return 2 * coded_sample_count;
}


/* This function will decode the next adpcm sample given as an AdpcmState struct.
This function accepts and returns the whole struct since it can easily fit in a
single 32bit register, and should be more efficient than passing a pointer to a struct.
*/
static AdpcmState decode_adpcm_sample(AdpcmState state) {
    int delta, step_size = ADPCM_STEP_TABLE[state.index];
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

    state.index += ADPCM_INDEX_TABLE[state.code];
    if (state.index < 0)
        state.index = 0;
    else if (state.index > ADPCM_STEP_TABLE_MAX_INDEX)
        state.index = ADPCM_STEP_TABLE_MAX_INDEX;

    return state;
}


static void decode_adpcm_stream(
    Py_buffer *adpcm_stream_buf, Py_buffer *pcm_stream_buf,
    uint8 channel_count, int code_chunks_count) {

    AdpcmState adpcm_states[MAX_AUDIO_CHANNEL_COUNT];
    int block_count = (int)(
        adpcm_stream_buf->len / 
        (channel_count * get_adpcm_encoded_blocksize(code_chunks_count * 8)));
    uint8 *adpcm_stream = adpcm_stream_buf->buf;
    sint16 *pcm_stream = pcm_stream_buf->buf;
    uint32 codes;

    for (int b = 0; b < block_count; b++) {
        // initialize the adpcm state structs
        for (int c = 0; c < channel_count; c++) {
            adpcm_states[c].pcm_sample = adpcm_stream[0] | (adpcm_stream[1] << 8);
            adpcm_states[c].index = adpcm_stream[2];
            adpcm_stream += 4;

            if (adpcm_states[c].index < 0)
                adpcm_states[c].index = 0;
            else if (adpcm_states[c].index > ADPCM_STEP_TABLE_MAX_INDEX)
                adpcm_states[c].index = ADPCM_STEP_TABLE_MAX_INDEX;
        }

        // loop over each code chunk(8 codes in 4 bytes per chunk)
        for (int h = 0; h < code_chunks_count; h++) {
            // loop over each channel in each chunk
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
                for (int i = c; i < 8 * channel_count; i += channel_count) {
                    adpcm_states[c].code = codes & 0xF;
                    codes >>= 4;
                    adpcm_states[c] = decode_adpcm_sample(adpcm_states[c]);
                    pcm_stream[i] = adpcm_states[c].pcm_sample;
                }
            }
            // skip over the chunk of 8 samples per channel we just decoded
            pcm_stream += channel_count * 8;
        }
    }
}


static PyObject *py_decode_adpcm_samples(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    uint8 channel_count;
    int coded_sample_count, block_count;

    if (!PyArg_ParseTuple(args, "y*w*bi:decode_adpcm_samples",
        &bufs[0], &bufs[1], &channel_count, &coded_sample_count)) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    if (coded_sample_count <= 0)
        coded_sample_count = XBOX_ADPCM_DIFF_SAMPLE_COUNT;

    block_count = (int)(bufs[0].len / (channel_count * get_adpcm_encoded_blocksize(coded_sample_count)));

    // handle invalid data sizes and such
    if (bufs[0].len % get_adpcm_encoded_blocksize(coded_sample_count)) {
        RELEASE_PY_BUFFER_ARRAY(bufs)
        PySys_FormatStdout("Provided adpcm buffer is not a multiple of block size.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    } else if (bufs[1].len < block_count * get_adpcm_decoded_blocksize(coded_sample_count)) {
        RELEASE_PY_BUFFER_ARRAY(bufs)
        PySys_FormatStdout("Provided pcm buffer is not large enough to hold decoded data.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    } else if (channel_count > MAX_AUDIO_CHANNEL_COUNT) {
        RELEASE_PY_BUFFER_ARRAY(bufs)
        PySys_FormatStdout("Too many channels to decode in adpcm stream.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    } else if (coded_sample_count % 8) {
        RELEASE_PY_BUFFER_ARRAY(bufs)
        PySys_FormatStdout("coded_sample_count must be a multiple of 8.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    // do the decoding!
    decode_adpcm_stream(&bufs[0], &bufs[1], channel_count, coded_sample_count / 8);

    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs)

    return Py_BuildValue("");  // return Py_None while incrementing it
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef adpcm_ext_methods[] = {
    {"decode_adpcm_samples", py_decode_adpcm_samples, METH_VARARGS, ""},
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
