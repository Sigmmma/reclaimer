#include "../../../src/shared.h"


static inline void byteswap_eight_byte_array(
    char *orig, char *swap, uint64 start, uint64 end, uint64 struct_size,
    int *offs, int off_count)
{
    for (int i = 0; i < off_count; i++) {
        for (int off = start + offs[i]; off + 8 <= end; off += struct_size) {
            swap[off]     = orig[off + 7];
            swap[off + 1] = orig[off + 6];
            swap[off + 2] = orig[off + 5];
            swap[off + 3] = orig[off + 4];
            swap[off + 4] = orig[off + 3];
            swap[off + 5] = orig[off + 2];
            swap[off + 6] = orig[off + 1];
            swap[off + 7] = orig[off];
        }
    }
}


static inline void byteswap_four_byte_array(
    char *orig, char *swap, uint64 start, uint64 end, uint64 struct_size,
    int *offs, int off_count)
{
    for (int i = 0; i < off_count; i++) {
        for (int off = start + offs[i]; off + 4 <= end; off += struct_size) {
            swap[off]     = orig[off + 3];
            swap[off + 1] = orig[off + 2];
            swap[off + 2] = orig[off + 1];
            swap[off + 3] = orig[off];
        }
    }
}


static inline void byteswap_two_byte_array(
    char *orig, char *swap, uint64 start, uint64 end, uint64 struct_size,
    int *offs, int off_count)
{
    for (int i = 0; i < off_count; i++) {
        for (int off = start + offs[i]; off + 2 <= end; off += struct_size) {
            swap[off]     = orig[off + 1];
            swap[off + 1] = orig[off];
        }
    }
}


static PyObject *py_byteswap_struct_array(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    Py_buffer field_offset_bufs[3];
    int field_offset_sizes[3] = { 2, 4, 8 };
    uint64 start, end, struct_size;

    if (!PyArg_ParseTuple(args, "y*w*KKK|y*y*y*:byteswap_struct_array",
        &bufs[0], &bufs[1], &start, &end, &struct_size,
        &field_offset_bufs[0], &field_offset_bufs[1], &field_offset_bufs[2])) {
        return Py_BuildValue("");  // return Py_None while incrementing it
    }

    // handle invalid data sizes and such
    if (field_offset_bufs[0].itemsize != 4) {
        PySys_FormatStdout("two_byte_offs array format must be 'I'.\n");
    } else if (field_offset_bufs[1].itemsize != 4) {
        PySys_FormatStdout("four_byte_offs array format must be 'I'.\n");
    } else if (field_offset_bufs[2].itemsize != 4) {
        PySys_FormatStdout("eight_byte_offs array format must be 'I'.\n");
    } else if (end > bufs[0].len) {
        PySys_FormatStdout("end must within bounds of input buffer.\n");
    } else if (end > bufs[1].len) {
        PySys_FormatStdout("end must within bounds of output buffer.\n");
    } else if (bufs[0].buf == bufs[1].buf) {
        PySys_FormatStdout("src and dst cannot be the same.\n");
    } else if (struct_size == 0) {
        PySys_FormatStdout("struct size must be greater than zero.\n");
    } else if (start > end) {
        PySys_FormatStdout("start must be less than end.\n");
    } else {
        int item_count;
        for (int i = 0; i < 3; i++) {
            if (field_offset_bufs[i].buf == NULL)
                continue;

            item_count = field_offset_bufs[i].len / field_offset_bufs[i].itemsize;
            for (int j = 0; j < item_count; j++) {
                if (((int *)field_offset_bufs[i].buf)[j] + field_offset_sizes[i] > struct_size) {
                    PySys_FormatStdout("offsets must be within the struct size.\n");
                    goto exit;
                }
            }
        }
        // everything looks good. lets process!
        item_count = field_offset_bufs[0].len / field_offset_bufs[0].itemsize;
        if (field_offset_bufs[0].buf && item_count > 0)
            byteswap_two_byte_array(
                bufs[0].buf, bufs[1].buf, start, end, struct_size,
                field_offset_bufs[0].buf, item_count
            );

        item_count = field_offset_bufs[1].len / field_offset_bufs[1].itemsize;
        if (field_offset_bufs[1].buf && item_count > 0)
            byteswap_four_byte_array(
                bufs[0].buf, bufs[1].buf, start, end, struct_size,
                field_offset_bufs[1].buf, item_count
            );

        item_count = field_offset_bufs[2].len / field_offset_bufs[2].itemsize;
        if (field_offset_bufs[2].buf && item_count > 0)
            byteswap_eight_byte_array(
                bufs[0].buf, bufs[1].buf, start, end, struct_size,
                field_offset_bufs[2].buf, item_count
            );
    }

    exit:
    // Release the buffer objects
    RELEASE_PY_BUFFER_ARRAY(bufs)
    RELEASE_PY_BUFFER_ARRAY(field_offset_bufs)

    return Py_BuildValue("");  // return Py_None while incrementing it
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef byteswapping_ext_methods[] = {
    {"byteswap_struct_array", py_byteswap_struct_array, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef byteswapping_ext_module = {
    PyModuleDef_HEAD_INIT,
    "byteswapping_ext",
    "A set of C functions to replace certain speed intensive byteswapping functions",
    -1,
    byteswapping_ext_methods,
};

PyMODINIT_FUNC PyInit_byteswapping_ext(void) {
    return PyModule_Create(&byteswapping_ext_module);
}
