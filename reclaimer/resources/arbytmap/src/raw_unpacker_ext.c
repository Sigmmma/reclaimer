#include <stdio.h>
#include "Python.h"
#include "abstract.h"
#include "longobject.h"
#include "modsupport.h"
#include "object.h"

//short-hand macros for unpacker routines
#define UNPACK_ARGB(pixel_array)\
    for (i=0; i < max_i; i++) {\
        pixel = (*pixel_array)[i];\
        j = i<<2;\
        (*unpacked_pix)[j] = (*a_scale)[(pixel&a_mask)>>a_shift]; j++;\
        (*unpacked_pix)[j] = (*r_scale)[(pixel&r_mask)>>r_shift]; j++;\
        (*unpacked_pix)[j] = (*g_scale)[(pixel&g_mask)>>g_shift]; j++;\
        (*unpacked_pix)[j] = (*b_scale)[(pixel&b_mask)>>b_shift];\
    }

#define UNPACK_AI(pixel_array)\
    for (i=0; i < max_i; i++) {\
        pixel = (*pixel_array)[i];\
        j = i<<1;\
        (*unpacked_pix)[j] = (*a_scale)[(pixel&a_mask)>>a_shift]; j++;\
        (*unpacked_pix)[j] = (*i_scale)[(pixel&i_mask)>>i_shift];\
    }

#define UNPACK_A(pixel_array)\
    for (i=0; i < max_i; i++) {\
        (*unpacked_pix)[i] = (*scale)[(((*pixel_array)[i])&mask)>>shift];\
    }

static void unpack_raw_4_channel_8bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *a_scale_buf, Py_buffer *r_scale_buf,
    Py_buffer *g_scale_buf, Py_buffer *b_scale_buf,
    unsigned long long a_mask, unsigned long long r_mask,
    unsigned long long g_mask, unsigned long long b_mask,
    char a_shift,  char r_shift,  char g_shift,  char b_shift)
{
    Py_ssize_t packed_pix_size;
    unsigned char (*unpacked_pix)[];
    unsigned char (*a_scale)[], (*r_scale)[], (*g_scale)[], (*b_scale)[];
    unsigned long long i=0, j=0, max_i=0, pixel=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long  (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[]) packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[])packed_pix_buf->buf;

    unpacked_pix = (unsigned char(*)[])unpacked_pix_buf->buf;
    a_scale = (unsigned char(*)[])a_scale_buf->buf;
    r_scale = (unsigned char(*)[])r_scale_buf->buf;
    g_scale = (unsigned char(*)[])g_scale_buf->buf;
    b_scale = (unsigned char(*)[])b_scale_buf->buf;

    max_i = (unpacked_pix_buf->len)/4;

    if (packed_pix_size == 8) {
        UNPACK_ARGB(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_ARGB(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_ARGB(packed_pix_16)
    } else {
        UNPACK_ARGB(packed_pix_8)
    }
}

static void unpack_raw_2_channel_8bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *a_scale_buf, Py_buffer *i_scale_buf,
    unsigned long long a_mask, unsigned long long i_mask,
    char a_shift,  char i_shift)
{
    Py_ssize_t packed_pix_size;
    unsigned char (*unpacked_pix)[];
    unsigned char (*a_scale)[], (*i_scale)[];
    unsigned long long i=0, j=0, max_i=0, pixel=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long  (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[]) packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[]) packed_pix_buf->buf;

    unpacked_pix = (unsigned char(*)[])unpacked_pix_buf->buf;
    a_scale = (unsigned char(*)[])a_scale_buf->buf;
    i_scale = (unsigned char(*)[])i_scale_buf->buf;

    max_i = (unpacked_pix_buf->len)/2;

    if (packed_pix_size == 8) {
        UNPACK_AI(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_AI(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_AI(packed_pix_16)
    } else {
        UNPACK_AI(packed_pix_8)
    }
}

static void unpack_raw_1_channel_8bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *scale_buf, unsigned long long mask,  char shift)
{
    Py_ssize_t packed_pix_size;
    unsigned char (*unpacked_pix)[];
    unsigned char (*scale)[];
    unsigned long long i=0, max_i=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];
    // THESE ALL NEED TO BE CHANGED TO ACCEPT UP TO packed_pix_64

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[])packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[])packed_pix_buf->buf;

    unpacked_pix = (unsigned char(*)[])unpacked_pix_buf->buf;
    scale = (unsigned char(*)[])scale_buf->buf;

    max_i = unpacked_pix_buf->len;

    if (packed_pix_size == 8) {
        UNPACK_A(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_A(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_A(packed_pix_16)
    } else {
        UNPACK_A(packed_pix_8)
    }
}

/*
    Deep color versions of the above functions
*/


static void unpack_raw_4_channel_16bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *a_scale_buf, Py_buffer *r_scale_buf,
    Py_buffer *g_scale_buf, Py_buffer *b_scale_buf,
    unsigned long long a_mask, unsigned long long r_mask,
    unsigned long long g_mask, unsigned long long b_mask,
    char a_shift,  char r_shift,  char g_shift,  char b_shift)
{
    Py_ssize_t packed_pix_size;
    unsigned short (*unpacked_pix)[];
    unsigned short (*a_scale)[], (*r_scale)[], (*g_scale)[], (*b_scale)[];
    unsigned long long i=0, j=0, max_i=0, pixel=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long  (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[]) packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[])packed_pix_buf->buf;

    unpacked_pix = (unsigned short(*)[])unpacked_pix_buf->buf;
    a_scale = (unsigned short(*)[])a_scale_buf->buf;
    r_scale = (unsigned short(*)[])r_scale_buf->buf;
    g_scale = (unsigned short(*)[])g_scale_buf->buf;
    b_scale = (unsigned short(*)[])b_scale_buf->buf;

    max_i = (unpacked_pix_buf->len)/8;

    if (packed_pix_size == 8) {
        UNPACK_ARGB(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_ARGB(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_ARGB(packed_pix_16)
    } else {
        UNPACK_ARGB(packed_pix_8)
    }
}

static void unpack_raw_2_channel_16bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *a_scale_buf, Py_buffer *i_scale_buf,
    unsigned long long a_mask, unsigned long long i_mask,
    char a_shift,  char i_shift)
{
    Py_ssize_t packed_pix_size;
    unsigned short (*unpacked_pix)[];
    unsigned short (*a_scale)[], (*i_scale)[];
    unsigned long long i=0, j=0, max_i=0, pixel=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long  (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[]) packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[]) packed_pix_buf->buf;

    unpacked_pix = (unsigned short(*)[])unpacked_pix_buf->buf;
    a_scale = (unsigned short(*)[])a_scale_buf->buf;
    i_scale = (unsigned short(*)[])i_scale_buf->buf;

    max_i = (unpacked_pix_buf->len)/4;

    if (packed_pix_size == 8) {
        UNPACK_AI(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_AI(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_AI(packed_pix_16)
    } else {
        UNPACK_AI(packed_pix_8)
    }
}

static void unpack_raw_1_channel_16bpp(
    Py_buffer *unpacked_pix_buf, Py_buffer *packed_pix_buf,
    Py_buffer *scale_buf, unsigned long long mask,  char shift)
{
    Py_ssize_t packed_pix_size;
    unsigned short (*unpacked_pix)[];
    unsigned short (*scale)[];
    unsigned long long i=0, max_i=0;

    unsigned char  (*packed_pix_8)[];
    unsigned short (*packed_pix_16)[];
    unsigned long (*packed_pix_32)[];
    unsigned long long (*packed_pix_64)[];

    packed_pix_size = packed_pix_buf->itemsize;

    packed_pix_8  = (unsigned char(*)[]) packed_pix_buf->buf;
    packed_pix_16 = (unsigned short(*)[])packed_pix_buf->buf;
    packed_pix_32 = (unsigned long(*)[])packed_pix_buf->buf;
    packed_pix_64 = (unsigned long long(*)[])packed_pix_buf->buf;

    unpacked_pix = (unsigned short(*)[])unpacked_pix_buf->buf;
    scale = (unsigned short(*)[])scale_buf->buf;

    max_i = (unpacked_pix_buf->len)/2;

    if (packed_pix_size == 8) {
        UNPACK_A(packed_pix_64)
    } else if (packed_pix_size == 4) {
        UNPACK_A(packed_pix_32)
    } else if (packed_pix_size == 2) {
        UNPACK_A(packed_pix_16)
    } else {
        UNPACK_A(packed_pix_8)
    }
}


static void unpack_indexing(
    Py_buffer *unpacked_indexing_buf, Py_buffer *packed_indexing_buf,
    char indexing_size)
{
    //THIS FUNCTION IS CURRENTLY UNTESTED.
    unsigned char (*packed_indexing)[];
    unsigned char (*unpacked_indexing)[];
    unsigned char index_chunk;
    unsigned long long i=0, max_i=0;

    packed_indexing = (unsigned char(*)[]) packed_indexing_buf->buf;
    unpacked_indexing = (unsigned char(*)[]) unpacked_indexing_buf->buf;

    max_i = unpacked_indexing_buf->len;

    if (indexing_size == 4) {
        for (i=0; i < max_i; i++) {
            index_chunk = (*packed_indexing)[i];
            (*unpacked_indexing)[i] = index_chunk&15; i++;
            (*unpacked_indexing)[i] = (index_chunk>>4)&15;
        }
    } else if (indexing_size == 2) {
        for (i=0; i < max_i; i++) {
            index_chunk = (*packed_indexing)[i];
            (*unpacked_indexing)[i] = index_chunk&3; i++;
            (*unpacked_indexing)[i] = (index_chunk>>2)&3; i++;
            (*unpacked_indexing)[i] = (index_chunk>>4)&3; i++;
            (*unpacked_indexing)[i] = (index_chunk>>6)&3; i++;
        }
    } else {
        for (i=0; i < max_i; i++) {
            index_chunk = (*packed_indexing)[i];
            (*unpacked_indexing)[i] = index_chunk&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>1)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>2)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>3)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>4)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>5)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>6)&1; i++;
            (*unpacked_indexing)[i] = (index_chunk>>7)&1; i++;
        }
    }
}


static PyObject *py_unpack_raw_4_channel(PyObject *self, PyObject *args) {
    Py_buffer bufs[6];
    unsigned long long masks[4];
    char shifts[4];

    // Get the pointers to each of the arrays, masks, and shifts
    if (!PyArg_ParseTuple(args, "w*w*w*w*w*w*KKKKbbbb:unpack_raw_4_channel",
        &bufs[0], &bufs[1], &bufs[2], &bufs[3], &bufs[4], &bufs[5],
        &masks[0], &masks[1], &masks[2], &masks[3],
        &shifts[0], &shifts[1], &shifts[2], &shifts[3]))
        return Py_None;

    if (bufs[0].itemsize == 2) {
        unpack_raw_4_channel_16bpp(
            &bufs[0], &bufs[1], &bufs[2], &bufs[3], &bufs[4], &bufs[5],
            masks[0], masks[1], masks[2], masks[3],
            shifts[0], shifts[1], shifts[2], shifts[3]);
    } else {
        unpack_raw_4_channel_8bpp(
            &bufs[0], &bufs[1], &bufs[2], &bufs[3], &bufs[4], &bufs[5],
            masks[0], masks[1], masks[2], masks[3],
            shifts[0], shifts[1], shifts[2], shifts[3]);
    }

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]); PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]); PyBuffer_Release(&bufs[3]);
    PyBuffer_Release(&bufs[4]); PyBuffer_Release(&bufs[5]);

    return Py_None;
}

static PyObject *py_unpack_raw_2_channel(PyObject *self, PyObject *args) {
    Py_buffer bufs[4];
    unsigned long long masks[2];
    char shifts[2];

    // Get the pointers to each of the arrays, masks, and shifts
    if (!PyArg_ParseTuple(args, "w*w*w*w*KKbb:unpack_raw_2_channel",
        &bufs[0], &bufs[1], &bufs[2], &bufs[3],
        &masks[0], &masks[1], &shifts[0], &shifts[1]))
        return Py_None;

    if (bufs[0].itemsize == 2) {
        unpack_raw_2_channel_16bpp(
            &bufs[0], &bufs[1], &bufs[2], &bufs[3],
            masks[0], masks[1], shifts[0], shifts[1]);
    } else {
        unpack_raw_2_channel_8bpp(
            &bufs[0], &bufs[1], &bufs[2], &bufs[3],
            masks[0], masks[1], shifts[0], shifts[1]);
    }

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]); PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]); PyBuffer_Release(&bufs[3]);

    return Py_None;
}

static PyObject *py_unpack_raw_1_channel(PyObject *self, PyObject *args) {
    Py_buffer bufs[3];
    unsigned long long mask;
    char shift;

    // Get the pointers to each of the arrays, mask, and shift
    if (!PyArg_ParseTuple(args, "w*w*w*Kb:unpack_raw_1_channel",
        &bufs[0], &bufs[1], &bufs[2], &mask, &shift))
        return Py_None;

    if (bufs[0].itemsize == 2) {
        unpack_raw_1_channel_16bpp(&bufs[0], &bufs[1], &bufs[2], mask, shift);
    } else {
        unpack_raw_1_channel_8bpp(&bufs[0], &bufs[1], &bufs[2], mask, shift);
    }

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);
    PyBuffer_Release(&bufs[2]);

    return Py_None;
}

static PyObject *py_unpack_indexing(PyObject *self, PyObject *args) {
    Py_buffer bufs[2];
    char indexing_size;

    // Get the pointers to each of the arrays and indexing size
    if (!PyArg_ParseTuple(args, "w*w*b:unpack_indexing",
        &bufs[0], &bufs[1], &indexing_size))
        return Py_None;

    unpack_indexing(&bufs[0], &bufs[1], indexing_size);

    // Release the buffer objects
    PyBuffer_Release(&bufs[0]);
    PyBuffer_Release(&bufs[1]);

    return Py_None;
}

/* A list of all the methods defined by this module.
"METH_VARGS" tells Python how to call the handler.
The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef raw_unpacker_ext_methods[] = {
    {"unpack_raw_4_channel", py_unpack_raw_4_channel, METH_VARARGS, ""},
    {"unpack_raw_2_channel", py_unpack_raw_2_channel, METH_VARARGS, ""},
    {"unpack_raw_1_channel", py_unpack_raw_1_channel, METH_VARARGS, ""},
    {"unpack_indexing", py_unpack_indexing, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}      /* sentinel */
};

/* When Python imports a C module named 'X' it loads the
module then looks for a method named "init"+X and calls it.*/
static struct PyModuleDef raw_unpacker_ext_module = {
    PyModuleDef_HEAD_INIT,
    "raw_unpacker_ext",
    "A set of C functions to replace certain speed intensive pixel unpacker functions",
    -1,
    raw_unpacker_ext_methods,
};

PyMODINIT_FUNC PyInit_raw_unpacker_ext(void) {
    return PyModule_Create(&raw_unpacker_ext_module);
}
