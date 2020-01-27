#include "..\..\..\src\shared.h"


static PyObject *py_byteswap_struct_array(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    int block_count;

    if (!PyArg_ParseTuple(args, "y*w*b|BB:byteswap_struct_array",
        &bufs[0], &bufs[1])) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    // handle invalid data sizes and such
    if (bufs[0].len % struct_size)
        PySys_FormatStdout("Provided pcm buffer is not a multiple of block size.\n");

    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs)

    return Py_BuildValue("");  // return Py_None while incrementing it
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef byteswapping_ext_methods[] = {
    {"decode_xbadpcm_samples", py_byteswap_struct_array, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef byteswapping_ext_module = {
    PyModuleDef_HEAD_INIT,
    "adpcm_ext",
    "A set of C functions to replace certain speed intensive byteswapping functions",
    -1,
    byteswapping_ext_methods,
};

PyMODINIT_FUNC PyInit_byteswapping_ext(void) {
    return PyModule_Create(&byteswapping_ext_module);
}
