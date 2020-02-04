#pragma once
#include <stdio.h>
#include <stdint.h>
#include <Python.h>
#include <abstract.h>    // contains PyBuffer_Release
#include <modsupport.h>  // contains PyArg_ParseTuple
#include <object.h>      // contains Py_buffer

typedef int8_t   sint8;
typedef int16_t  sint16;
typedef int32_t  sint32;
typedef int64_t  sint64;
typedef uint8_t  uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;
typedef uint64_t uint64;

#define RELEASE_PY_BUFFER_ARRAY(bufs)\
    for (int py_buffer_release_index = 0; py_buffer_release_index < (sizeof(bufs) / sizeof(bufs[0])); py_buffer_release_index++) {\
        PyBuffer_Release(&bufs[py_buffer_release_index]);\
    }\

