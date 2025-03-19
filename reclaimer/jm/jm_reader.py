import io
import itertools
import mmap
import re

from types import MethodType

# Test showing off the regex can be seen here:
# https://regex101.com/r/7PKpWi/2
JM_V1_REGEX = re.compile(br'([^\s][^\t\r\n]*)')
# https://regex101.com/r/ySgI1Z/2
JM_V2_REGEX = re.compile(br'(?:\n+|\t+|^)([^;\t\r\n]+)')

# Test showing off the regex can be seen here:
# https://regex101.com/r/Fpd23n/1
JM_INT_PARSE_REGEX = re.compile(r'^\s*([-+]?\d+)')
# https://regex101.com/r/rKvo0t/2
# TODO: Should this match numbers that start with a . and are just commas?
# Check atof description.
JM_FLOAT_PARSE_REGEX = re.compile(r'^\s*([-+]?(?:\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?)')


class JMReader:
    _data    = b''
    comments = False
    def __init__(self, jm_stream_or_string, comments=False):
        self.comments = comments
        self.data     = jm_stream_or_string

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, stream_or_string):
        # to unify everything, we'll work in bytes
        jm_data = (
            stream_or_string.encode("utf-8")
            if isinstance(stream_or_string, str) else
            stream_or_string
            )

        if isinstance(jm_data, (bytes, bytearray)):
            self._data = jm_data.lstrip("\ufeff".encode())
        elif isinstance(jm_data, io.IOBase):
            self._data = mmap.mmap(jm_data.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            raise ValueError("Unsupported stream type %s" % type(jm_data))

        self.reset_stream()

    def reset_stream(self):
        'Resets reading the JM data stream to the beginning.'
        regex = JM_V2_REGEX if self.comments else JM_V1_REGEX
        stream = (
            map(bytes.decode,
            map(re.Match.group, regex.finditer(self._data), itertools.repeat(0)
            )))
        self._next = MethodType(next, stream)

    def _next(self):
        raise NotImplementedError()

    @property
    def next(self):
        '''
        Get the next string from the jm data.
        '''
        return self._next()

    @property
    def next_int(self):
        '''
        Get the next integer from the jm data as a proper integer.
        Based on description of C atoi spec.
        Returns 0 when it can't find anything or is interupted.
        '''
        result = JM_INT_PARSE_REGEX.search(self._next())
        return (result and int(result.group())) or 0

    @property
    def next_float(self):
        '''
        Get the next float from the jm data as a proper float.
        Based on description of C atof spec.
        Returns 0.0 for NaN or when it can't find anything or is interupted.
        '''
        result = JM_FLOAT_PARSE_REGEX.search(self._next())
        return (result and float(result.group())) or 0
