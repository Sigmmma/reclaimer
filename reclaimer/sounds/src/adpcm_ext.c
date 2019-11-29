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
const static int XBOX_ADPCM_DIFF_SAMPLE_COUNT = 64;


// Description of ADPCM stream block
//   first 2 bytes are the initial 16bit pcm sample
//   next 2 bytes are the initial step table index(do a CLAMP(0, 88))
//   each byte afterward is a pair of adpcm codes encoded in each nibble

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
    return 2 * (coded_sample_count + 1);
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
    if (state.code < 0)
        state.code = 0;
    else if (state.code > 88)
        state.code = 88;

    return state;
}


static void decode_adpcm_stream(
    Py_buffer *adpcm_stream_buf, Py_buffer *pcm_stream_buf,
    uint8 channel_count, int is_big_endian, int coded_sample_count) {

    AdpcmState adpcm_state[MAX_AUDIO_CHANNEL_COUNT];
}


static PyObject *py_decode_adpcm_samples(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    uint8 channel_count;
    int is_big_endian, i, coded_sample_count, block_count;

    if (!PyArg_ParseTuple(args, "w*w*bpi:decode_adpcm_samples",
        &bufs[0], &bufs[1], &channel_count, &is_big_endian, &coded_sample_count)) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    if (coded_sample_count <= 0)
        coded_sample_count = XBOX_ADPCM_DIFF_SAMPLE_COUNT;

    block_count = bufs[0].len / get_adpcm_encoded_blocksize(coded_sample_count);

    // handle invalid data sizes and such
    if (bufs[0].len % get_adpcm_encoded_blocksize(coded_sample_count)) {
        RELEASE_PY_BUFFER_ARRAY(bufs, i)
        PySys_FormatStdout("Provided adpcm buffer is not a multiple of block size.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    } else if (bufs[1].len < block_count * get_adpcm_decoded_blocksize(coded_sample_count)) {
        RELEASE_PY_BUFFER_ARRAY(bufs, i)
            PySys_FormatStdout("Provided pcm buffer is not large enough to hold decoded data.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    } else if (channel_count > MAX_AUDIO_CHANNEL_COUNT) {
        RELEASE_PY_BUFFER_ARRAY(bufs, i)
            PySys_FormatStdout("Too many channels to decode in adpcm stream.\n");
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    // do the decoding!
    decode_adpcm_stream(&bufs[0], &bufs[1], channel_count, is_big_endian, coded_sample_count);

    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs, i)

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
