'''
This module provides a pure-python replacement for MOST of the audioop functions
that Reclaimer relies on for audio conversion. This module exists because audioop
is being deprecated in python 3.11, and will be removed in 3.13. Some of this
functionality isn't necessary for audio compiling, and those methods that arent
have not been reimplemented.

A better solution would be to use a pypi library replacement, however the
pure-python versions out there are extremely slow. Example:
    https://github.com/jiaaro/pydub/blob/master/pydub/pyaudioop.py

To learn about the deprecation, see here:
    https://peps.python.org/pep-0594/#audioop
'''
from types import MethodType
import array
import itertools

try:
    import audioop
except ModuleNotFoundError:
    # THEY TOOK MY FUCKING BATTERIES!!!!!
    audioop = None

SAMPLE_WIDTH_BOUNDS = (
    (      -0x80,        0x7F),
    (    -0x8000,      0x7Fff),
    (  -0x800000,    0x7FffFF),
    (-0x80000000,  0x7FffFFff),
    )

SAMPLE_TYPECODES = (
    "b",
    "h",
    "t", # NOTE: not a real typecode
    "i"
    )

def adpcm2lin(fragment, width, state):
    # TODO: replace with python fallback
    raise NotImplementedError(
        "No accelerators found, and audioop is removed in this "
        "version of Python. Cannot decode ADPCM audio samples."
        )


def bias(fragment, width, bias):
    if width not in (1, 2, 4):
        raise NotImplementedError("Cannot bias sample data of width %s." % width)

    # ensure fragment is the correct data type
    if width > 1 and not(isinstance(fragment, array.array) and
                         fragment.itemsize == 1):
        fragment = array.array("I" if width == 4 else "H", fragment)

    modulous = 1 << (8*width)
    mapper = map(
        modulous.__rmod__, 
        map(int(bias).__add__, fragment)
        )

    if width == 1:
        fragment = bytes(mapper)
    elif width in (2, 4):
        fragment = array.array("I" if width == 4 else "H", mapper).tobytes()

    return fragment


def byteswap(fragment, width):
    if width not in (1, 2, 3, 4):
        raise NotImplementedError(
            "Cannot byteswap sample data of width %s." % width
            )

    orig_fragment = (
        fragment           if isinstance(fragment, (bytes, bytearray)) else
        fragment.tobytes() if isinstance(fragment, array.array) else
        bytes(fragment)
        )
    if width == 3:
        # for 24bit we gotta do some clever shit to do this reasonable fast.
        # sample data must be bytes or bytearray if we want to use slices
        fragment = bytearray(orig_fragment)
        # use slices to move byte 0 of each original word into byte 2
        # of the byteswapped word, and vice versa for the other bytes
        fragment[::3]  = orig_fragment[2::3]
        fragment[2::3] = orig_fragment[::3]
        fragment = bytes(fragment)
    elif width == 2 or width == 4:
        # we can use array.array to byteswap 16/32 bit pcm
        fragment = array.array("i" if width == 4 else "h", fragment)
        fragment.byteswap()
        fragment = fragment.tobytes()
    else:
        fragment = orig_fragment

    return fragment


def lin2lin(fragment, width, newwidth):
    if width not in (1, 2, 4):
        raise NotImplementedError("Cannot convert from sample width %s." % width)
    elif newwidth not in (1, 2, 4):
        raise NotImplementedError("Cannot convert to sample width %s." % newwidth)

    typecode     = SAMPLE_TYPECODES[width-1]
    new_typecode = SAMPLE_TYPECODES[newwidth-1]
    if not(isinstance(fragment, array.array) and
           fragment.typecode == typecode):
        fragment = array.array(typecode, fragment)

    if width == newwidth:
        # same width? why? whatever....
        new_fragment = fragment
    else:
        shift_diff = abs(width - newwidth) * 8
        shift_func = (
            shift_diff.__rrshift__      # shift samples right(divide)
            if width > newwidth else
            shift_diff.__rlshift__      # shift samples left(multiply)
            )

        min_val_clip = MethodType(max, SAMPLE_WIDTH_BOUNDS[newwidth-1][0])
        max_val_clip = MethodType(min, SAMPLE_WIDTH_BOUNDS[newwidth-1][1])
        new_fragment = array.array(new_typecode,
            map(max_val_clip,
            map(min_val_clip,
            map(round,
            map(shift_func, fragment
            )))))

    return new_fragment.tobytes()


def ratecv(fragment, width, nchannels, inrate, outrate, state, weightA=1, weightB=0):
    # TODO: replace with python fallback
    raise NotImplementedError(
        "audioop is removed in this version of Python. "
        "Cannot convert sample rate to target."
        )


def tomono(fragment, width, lfactor, rfactor):
    if width not in (1, 2, 4):
        raise NotImplementedError(
            "Cannot convert %s width samples to mono." % width
            )

    typecode = SAMPLE_TYPECODES[width-1]
    if not(isinstance(fragment, array.array) and
           fragment.typecode == typecode):
        fragment = array.array(typecode, fragment)

    min_val_clip = MethodType(max, SAMPLE_WIDTH_BOUNDS[width-1][0])
    max_val_clip = MethodType(min, SAMPLE_WIDTH_BOUNDS[width-1][1])

    # these are some pretty simple map chains that just grab odd/even
    # audio channel values and multiply them by their channel factor
    left_channel_data  = map(lfactor.__mul__, fragment[0::2])
    right_channel_data = map(rfactor.__mul__, fragment[1::2])

    # WARNING: MAP FROM HELL
    # now that we have our audio channels separated into maps,
    # we can zip them together, pass that zip into a mapped sum
    # to add the left/right channels, pass the result into a
    # min/max clip map, and finally fast everything to integers.
    new_fragment = array.array(typecode,
        map(max_val_clip,
        map(min_val_clip,
        map(round,
        map(sum,
        zip(left_channel_data, right_channel_data)
        )))))

    return new_fragment.tobytes()


def tostereo(fragment, width, lfactor, rfactor):
    if width not in (1, 2, 4):
        raise NotImplementedError(
            "Cannot convert %s width samples to stereo." % width
            )

    typecode = SAMPLE_TYPECODES[width-1]
    if not(isinstance(fragment, array.array) and
           fragment.typecode == typecode):
        fragment = array.array(typecode, fragment)

    min_val_clip = MethodType(max, SAMPLE_WIDTH_BOUNDS[width-1][0])
    max_val_clip = MethodType(min, SAMPLE_WIDTH_BOUNDS[width-1][1])

    # WARNING: MAPS FROM HELL
    # essentially we're doing the opposite of the tomono maps above.
    # we're multiplying the input samples by the left/right factors,
    # rounding to integers, and then clipping to out min/max values.
    interleaved_fragment = array.array(
        typecode, b'\x00'*(len(fragment)*width*2)
        )
    interleaved_fragment[0::2] = fragment
    interleaved_fragment[1::2] = fragment

    new_fragment = array.array(typecode,
        map(max_val_clip,
        map(min_val_clip,
        map(round,
        itertools.starmap(float.__mul__,
        zip(
            itertools.cycle((lfactor, rfactor)),
            interleaved_fragment,
        ))))))
    return new_fragment.tobytes()


# TESTS
# these tests show that behavior is unchanged between the audioop
# implementation and the pure python version we've developed
def _run_tests():

    for test_vals in [
            # NOTE: we use steps here to ensure we generate enough data
            #       for the test, but not TOO MUCH data(i.e. multiple MB)
            (      -0x80,       0x7F,     0x01, 1, 2, "b",       0x80),
            (      -0x80,       0x7F,     0x01, 1, 4, "b",       0x80),
            (       0x00,       0xFF,     0x01, 1, 2, "B",       0x80),
            (       0x00,       0xFF,     0x01, 1, 4, "B",       0x80),
            (    -0x8000,     0x7Fff,     0x01, 2, 1, "h",     0x8000),
            (    -0x8000,     0x7Fff,     0x01, 2, 4, "h",     0x8000),
            (       0x00,     0xFFff,     0x01, 2, 1, "H",     0x8000),
            (       0x00,     0xFFff,     0x01, 2, 4, "H",     0x8000),
            (  -0x800000,   0x7FffFF,     0x80, 3, 1, "i",   0x800000),
            (  -0x800000,   0x7FffFF,     0x80, 3, 4, "i",   0x800000),
            (       0x00,   0xFFffFF,     0x80, 3, 1, "I",   0x800000),
            (       0x00,   0xFFffFF,     0x80, 3, 4, "I",   0x800000),
            (-0x80000000, 0x7FffFFff,   0x8000, 4, 1, "i", 0x7FffFFff),
            (-0x80000000, 0x7FffFFff,   0x8000, 4, 2, "i", 0x7FffFFff),
            (       0x00, 0xFFffFFff,   0x8000, 4, 1, "I", 0x7FffFFff),
            (       0x00, 0xFFffFFff,   0x8000, 4, 2, "I", 0x7FffFFff),
            #(-0x80000000, 0x7FffFFff,   0x100, 4, 1, "i", 0x7FffFFff),
            #(-0x80000000, 0x7FffFFff,   0x100, 4, 2, "i", 0x7FffFFff),
            #(       0x00, 0xFFffFFff,   0x100, 4, 1, "I", 0x7FffFFff),
            #(       0x00, 0xFFffFFff,   0x100, 4, 2, "I", 0x7FffFFff),
            ]:
        get_delta = lambda: list(
                itertools.starmap(int.__sub__,
                zip(
                    array.array(typecode, audioop_data),
                    array.array(typecode, reclaimer_data)
                ))
            )

        min_val, max_val, step_val, width, new_width, typecode, bias_val = test_vals
        test_vals_str = ", ".join(str(v) for v in test_vals)

        test_data = array.array(typecode, range(min_val, max_val+1, step_val))
        # ensure test data is multiple of sample width
        # also ensure audio data is a multiple of 2 for stereo/mono tests
        test_data = test_data.tobytes()[:width*2*(len(test_data)//(width*2))]

        # test 1: audioop.byteswap vs byteswap
        audioop_data    = audioop.byteswap(test_data, width)
        reclaimer_data  = byteswap(test_data, width)

        if width == 3:
            # NOTE: can't do much ATM with 24bit samples cause of how awkward they are
            continue

        delta           = get_delta()
        if max(map(abs, delta)) > 1:
            print(delta)
            print("Test failure: Inconsistency in byteswap(%s)" % test_vals_str)

        # test 2: audioop.bias vs bias
        audioop_data    = audioop.bias(test_data, width, bias_val)
        reclaimer_data  = bias(test_data, width, bias_val)
        delta           = get_delta()
        if max(map(abs, delta)) > 1:
            print(delta)
            print("Test failure: Inconsistency in bias(%s)" % test_vals_str)


        # test 3: audioop.tomono vs tomono
        audioop_data    = audioop.tomono(test_data, width, 0.5, 0.5)
        reclaimer_data  = tomono(test_data, width, 0.5, 0.5)
        delta           = get_delta()
        if max(map(abs, delta)) > 1:
            print(delta)
            print("Test failure: Inconsistency in tomono(%s)" % test_vals_str)


        # test 4: audioop.tostereo vs tostereo
        audioop_data    = audioop.tostereo(test_data, width, 1.0, 1.0)
        reclaimer_data  = tostereo(test_data, width, 1.0, 1.0)
        delta           = get_delta()
        if max(map(abs, delta)) > 1:
            print(delta)
            print("Test failure: Inconsistency in tostereo(%s)" % test_vals_str)
            input()

        # test 5: audioop.lin2lin vs lin2lin
        audioop_data    = audioop.lin2lin(test_data, width, new_width)
        reclaimer_data  = lin2lin(test_data, width, new_width)
        delta           = get_delta()
        if max(map(abs, delta)) > 1:
            print(delta)
            print("Test failure: Inconsistency in lin2lin(%s)" % test_vals_str)
            input()


if __name__ == "__main__" and audioop is not None:
    _run_tests()
    #import cProfile
    #cProfile.runctx("_run_tests()", locals(), globals())


if audioop is not None:
    # if audioop is loaded, use its methods
    from audioop import *
