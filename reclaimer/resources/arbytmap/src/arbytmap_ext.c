#include <stdio.h>
#include "Python.h"
#include "abstract.h"
#include "longobject.h"
#include "modsupport.h"
#include "object.h"


static void depalettize_bitmap_8(
    Py_buffer *unpacked_pix_buf, Py_buffer *unpacked_idx_buf,
    Py_buffer *unpacked_pal_buf, char channel_count)
{
    unsigned long long i=0, j=0, max_i=0;
    unsigned char (*unpacked_pix)[];
    unsigned char (*unpacked_pal)[];
    unsigned char (*unpacked_idx)[];

    unpacked_pix = (unsigned char(*)[])unpacked_pix_buf->buf;
    unpacked_pal = (unsigned char(*)[])unpacked_pal_buf->buf;
    unpacked_idx = (unsigned char(*)[])unpacked_idx_buf->buf;
    max_i = unpacked_pix_buf->len;

    if (channel_count == 4) {
        for (i=0; i < max_i; i += 4) {
            j = (*unpacked_idx)[i>>2]<<2;
            (*unpacked_pix)[i]   = (*unpacked_pal)[j];
            (*unpacked_pix)[i+1] = (*unpacked_pal)[j+1];
            (*unpacked_pix)[i+2] = (*unpacked_pal)[j+2];
            (*unpacked_pix)[i+3] = (*unpacked_pal)[j+3];
        }
    } else if (channel_count == 2) {
        for (i=0; i < max_i; i += 2) {
            j = (*unpacked_idx)[i>>1]<<1;
            (*unpacked_pix)[i]   = (*unpacked_pal)[j];
            (*unpacked_pix)[i+1] = (*unpacked_pal)[j+1];
        }
    } else {
        for (i=0; i < max_i; i++) {
            (*unpacked_pix)[i] = (*unpacked_pal)[(*unpacked_idx)[i]];
        }
    }
}

static void downsample_bitmap_8(
    Py_buffer *downsamp_pix_buf, Py_buffer *swizzled_pix_buf,
    unsigned long merge_count, char channel_count)
{
    unsigned long long i=0, j=0, max_i=0, swizz_i=0;
    unsigned long long merge_val=0;
    unsigned char (*downsamp_pix)[];
    unsigned char (*swizzled_pix)[];

    downsamp_pix = (unsigned char(*)[])downsamp_pix_buf->buf;
    swizzled_pix = (unsigned char(*)[])swizzled_pix_buf->buf;
    max_i = downsamp_pix_buf->len;

    for (i=0; i < max_i; i++) {
        merge_val = 0;
        for (j=0; j < merge_count; j++) {
            merge_val += (*swizzled_pix)[swizz_i];
            swizz_i++;
        }
        (*downsamp_pix)[i] = (merge_val/merge_count)&0xFF;
    }
}

/*
    Deep color versions of the above functions
*/

static void depalettize_bitmap_16(
    Py_buffer *unpacked_pix_buf, Py_buffer *unpacked_idx_buf,
    Py_buffer *unpacked_pal_buf, char channel_count)
{
    unsigned long long i=0, j=0, max_i=0;
    unsigned short (*unpacked_pix)[];
    unsigned short (*unpacked_pal)[];
    unsigned char (*unpacked_idx)[];

    unpacked_pix = (unsigned short(*)[])unpacked_pix_buf->buf;
    unpacked_pal = (unsigned short(*)[])unpacked_pal_buf->buf;
    unpacked_idx = (unsigned char(*)[])unpacked_idx_buf->buf;
    max_i = unpacked_pix_buf->len;

    if (channel_count == 4) {
        for (i=0; i < max_i; i += 4) {
            j = (*unpacked_idx)[i>>2]<<2;
            (*unpacked_pix)[i]   = (*unpacked_pal)[j];
            (*unpacked_pix)[i+1] = (*unpacked_pal)[j+1];
            (*unpacked_pix)[i+2] = (*unpacked_pal)[j+2];
            (*unpacked_pix)[i+3] = (*unpacked_pal)[j+3];
        }
    } else if (channel_count == 2) {
        for (i=0; i < max_i; i += 2) {
            j = (*unpacked_idx)[i>>1]<<1;
            (*unpacked_pix)[i]   = (*unpacked_pal)[j];
            (*unpacked_pix)[i+1] = (*unpacked_pal)[j+1];
        }
    } else {
        for (i=0; i < max_i; i++) {
            (*unpacked_pix)[i] = (*unpacked_pal)[(*unpacked_idx)[i]];
        }
    }
}

static void downsample_bitmap_16(
    Py_buffer *downsamp_pix_buf, Py_buffer *swizzled_pix_buf,
    unsigned long merge_count, char channel_count)
{
    unsigned long long i=0, j=0, max_i=0, swizz_i=0;
    unsigned long long merge_val=0;
    unsigned short (*downsamp_pix)[];
    unsigned short (*swizzled_pix)[];

    downsamp_pix = (unsigned short(*)[])downsamp_pix_buf->buf;
    swizzled_pix = (unsigned short(*)[])swizzled_pix_buf->buf;
    max_i = downsamp_pix_buf->len;

    for (i=0; i < max_i; i++) {
        merge_val = 0;
        for (j=0; j < merge_count; j++) {
            merge_val += (*swizzled_pix)[swizz_i];
            swizz_i++;
        }
        (*downsamp_pix)[i] = (merge_val/merge_count)&0xFF;
    }
}


static PyObject *py_depalettize_bitmap(PyObject *self, PyObject *args) {
    Py_buffer bufs[3];
    char channel_count;

    // Get the pointers to each of the array objects and channel count
    if (!PyArg_ParseTuple(args, "w*w*w*b:depalettize_bitmap",
        &bufs[0], &bufs[1], &bufs[2], &channel_count))
        return Py_None;

    if (bufs[0].itemsize == 2) {
        depalettize_bitmap_16(&bufs[0], &bufs[1], &bufs[2], channel_count);
    } else {
        depalettize_bitmap_8(&bufs[0], &bufs[1], &bufs[2], channel_count);
    }

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]);

    return Py_None;
}

static PyObject *py_downsample_bitmap(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    unsigned long merge_count;
    char channel_count;

    // Get the pointers to each of the array objects and channel count
    if (!PyArg_ParseTuple(args, "w*w*kb:downsample_bitmap",
        &bufs[0], &bufs[1], &merge_count, &channel_count))
        return Py_None;

    if (bufs[0].itemsize == 2) {
        downsample_bitmap_16(&bufs[0], &bufs[1], merge_count, channel_count);
    } else {
        downsample_bitmap_8(&bufs[0], &bufs[1], merge_count, channel_count);
    }

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);

    return Py_None;
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef arbytmap_ext_methods[] = {
    {"depalettize_bitmap", py_depalettize_bitmap, METH_VARARGS, ""},
    {"downsample_bitmap", py_downsample_bitmap, METH_VARARGS, ""},
    //{"downsample_bitmap_gamma", py_downsample_bitmap_gamma, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef arbytmap_ext_module = {
    PyModuleDef_HEAD_INIT,
    "arbytmap_ext",
    "A set of C functions to replace certain speed intensive Arbytmap functions",
    -1,
    arbytmap_ext_methods,
};

PyMODINIT_FUNC PyInit_arbytmap_ext(void) {
    return PyModule_Create(&arbytmap_ext_module);
}
