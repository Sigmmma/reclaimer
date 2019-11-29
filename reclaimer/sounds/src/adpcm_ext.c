#include "shared.h"


static PyObject *py_decode_adpcm_samples(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    uint8 channel_count;
    int big_endian, i;

    if (!PyArg_ParseTuple(args, "w*w*bp:decode_adpcm_samples",
        &bufs[0], &bufs[1], &channel_count, &big_endian)) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

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
