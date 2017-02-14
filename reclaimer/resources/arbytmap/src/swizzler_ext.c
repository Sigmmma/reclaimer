#include <stdio.h>
#include "Python.h"
#include "abstract.h"
#include "longobject.h"
#include "modsupport.h"
#include "object.h"

static void swizzle_char_array(
    Py_ssize_t c_size, char *c_offs_chars,
    Py_ssize_t x_size, char *x_offs_chars,
    Py_ssize_t y_size, char *y_offs_chars,
    Py_ssize_t z_size, char *z_offs_chars,
    Py_ssize_t swizz_size,   char *swizz_arr_chars,
    Py_ssize_t unswizz_size, char *unswizz_arr_chars,
    Py_ssize_t stride, char swizz)
{
    int i=0, zi=0, yi=0, xi=0, ci=0;
    unsigned long z=0, y=0, x=0, c=0, yz=0, xyz=0, cxyz=0;
    unsigned long max_i=0;
    unsigned long (*c_offs)[] = (unsigned long(*)[])c_offs_chars;
    unsigned long (*x_offs)[] = (unsigned long(*)[])x_offs_chars;
    unsigned long (*y_offs)[] = (unsigned long(*)[])y_offs_chars;
    unsigned long (*z_offs)[] = (unsigned long(*)[])z_offs_chars;
    unsigned char (*swizz_arr)[] = (unsigned char(*)[])swizz_arr_chars;
    unsigned char (*unswizz_arr)[] = (unsigned char(*)[])unswizz_arr_chars;
    c_size /= 4; x_size /= 4; y_size /= 4; z_size /= 4;
    swizz_size /= stride; unswizz_size /= stride;
    max_i = c_size * x_size * y_size * z_size;

    if ((max_i != swizz_size) || (max_i != unswizz_size)) {
        // raise an error because the arrays aren't the right size
        // how do i do that exactly? idk.... gotta look that up
        return;
        }

    if (swizz) {
        if (stride == 8) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<3;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++;
                        }
                    }
                }
            }
        } else if (stride == 4) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<2;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++;
                        }
                    }
                }
            }
        } else if (stride == 2) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<1;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++; cxyz++;
                            (*swizz_arr)[cxyz] = (*unswizz_arr)[i]; i++;
                        }
                    }
                }
            }
        } else {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            (*swizz_arr)[xyz + (*c_offs)[ci]] = (*unswizz_arr)[i];
                            i++;
                        }
                    }
                }
            }
        }
    } else {
        if (stride == 8) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<3;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++;
                        }
                    }
                }
            }
        } else if (stride == 4) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<2;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++;
                        }
                    }
                }
            }
        } else if (stride == 2) {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            cxyz = (xyz + (*c_offs)[ci])<<1;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++; cxyz++;
                            (*swizz_arr)[i] = (*unswizz_arr)[cxyz]; i++;
                        }
                    }
                }
            }
        } else {
            for (zi=0; zi < z_size; zi++) {
                z = (*z_offs)[zi];
                for (yi=0; yi < y_size; yi++) {
                    yz = z + (*y_offs)[yi];
                    for (xi=0; xi < x_size; xi++) {
                        xyz = yz + (*x_offs)[xi];
                        for (ci=0; ci < c_size; ci++) {
                            (*swizz_arr)[i] = (*unswizz_arr)[xyz + (*c_offs)[ci]];
                            i++;
                        }
                    }
                }
            }
        }
    }
}


static PyObject *py_swizzle_array(PyObject *self, PyObject *args) {
    Py_buffer bufs[6];

    // Get the pointers to each of the array objects
    if (!PyArg_ParseTuple(args, "w*w*w*w*w*w*:swizzle_array",
        &bufs[0], &bufs[1], &bufs[2], &bufs[3], &bufs[4], &bufs[5]))
        return Py_None;

    swizzle_char_array(
        bufs[0].len, bufs[0].buf, bufs[1].len, bufs[1].buf,
        bufs[2].len, bufs[2].buf, bufs[3].len, bufs[3].buf,
        bufs[4].len, bufs[4].buf, bufs[5].len, bufs[5].buf,
        bufs[5].itemsize, 1);

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]);
    PyBuffer_Release(&bufs[3]);
    PyBuffer_Release(&bufs[4]);
    PyBuffer_Release(&bufs[5]);

    return Py_None;
}

static PyObject *py_unswizzle_array(PyObject *self, PyObject *args) {
    Py_buffer bufs[6];

    // Get the pointers to each of the array objects
    if (!PyArg_ParseTuple(args, "w*w*w*w*w*w*:swizzle_array",
        &bufs[0], &bufs[1], &bufs[2], &bufs[3], &bufs[4], &bufs[5]))
        return Py_None;

    swizzle_char_array(
        bufs[0].len, bufs[0].buf, bufs[1].len, bufs[1].buf,
        bufs[2].len, bufs[2].buf, bufs[3].len, bufs[3].buf,
        bufs[4].len, bufs[4].buf, bufs[5].len, bufs[5].buf,
        bufs[5].itemsize, 0);

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]);
    PyBuffer_Release(&bufs[3]);
    PyBuffer_Release(&bufs[4]);
    PyBuffer_Release(&bufs[5]);

    return Py_None;
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef swizzler_ext_methods[] = {
    {"swizzle_array", py_swizzle_array, METH_VARARGS, ""},
    {"unswizzle_array", py_unswizzle_array, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef swizzler_ext_module = {
    PyModuleDef_HEAD_INIT,
    "swizzler_ext",
    "A set of C functions to replace certain speed intensive swizzler functions",
    -1,
    swizzler_ext_methods,
};

PyMODINIT_FUNC PyInit_swizzler_ext(void) {
    return PyModule_Create(&swizzler_ext_module);
}
