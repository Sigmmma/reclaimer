import math
import traceback

from supyr_struct.field_types import *
from supyr_struct.defs.block_def import BlockDef

from reclaimer.animation.jma import JmaAnimation
from reclaimer.util import compression
from reclaimer.animation import serialization

__all__ = ("compress_animation", "decompress_animation", )

# these structure definitions aren't really used in the code below, but
# are a good way to illustrate the structure of the compressed data.
# for uncompressed animations, the data is stored as:
#     rotation first, then translation, and finally scale

keyframe_header = BlockDef("keyframe_header",
    UBitInt("keyframe_count", SIZE=12),
    UBitInt("keyframe_data_offset", SIZE=20),
    SIZE=4, TYPE=BitStruct
    )

# compressed quaternion rotation
# Bits AND bytes are ordered left to right as most significant to least
#   bbbbbbbb aaaaaaaa   dddddddd cccccccc   ffffffff eeeeeeee
#   iiiiiiii iiiijjjj   jjjjjjjj kkkkkkkk   kkkkwwww wwwwwwww
rot_def = BlockDef("comp_rotation",
    # you'll need to read the 6 bytes as 3 little endian ints, then bit shift
    # them together like so:    compressed_quat = q2 + (q1<<16) + (q0<<32)
    UInt16("q0"),
    UInt16("q1"),
    UInt16("q2"),
    SIZE=6, TYPE=QStruct
    )

# Translation is not compressed, and is still an xyz float triple.
trans_def = BlockDef("translation",
    Float("x"),
    Float("y"),
    Float("z"),
    )


def compressed_stream_size(node=None, parent=None, attr_index=None,
                rawdata=None, new_value=None, *args, **kwargs):
    if attr_index is None:
        raise IndexError
    elif new_value is not None:
        raise NotImplementedError
    elif parent is None:
        raise TypeError
    elif node is None:
        node = parent[attr_index]

    if node is not None:
        return len(node)
    elif rawdata is None:
        raise TypeError

    comp_frame = parent.parent
    transform_index = comp_frame.index_by_id(parent) - 3

    offset = 44
    if transform_index != 0 or attr_index != 0:
        offset = comp_frame[transform_index][attr_index]

    # looking for the NEXT streams offset
    attr_index += 1

    if attr_index <= 3:
        end = comp_frame[transform_index][attr_index]
    elif transform_index == 2:
        end = len(rawdata)
    else:
        end = comp_frame[transform_index + 1][0]

    return end - offset


# keyframe_head:
# Contains information on which keyframes are stored for each node
# and where in the keyframes array to read the keyframe index from.
# Look at the above keyframe_header struct for exact specifications.

# keyframes:
# An array of arrays of UInt16s. The outer array stores one array
# of UInt16s for each node being rotated, translated, or scaled.
# Each of these UInt16 arrays stores the keyframe numbers of which
# frames have been stored in keyframe_data

# default_data:
# An array of default rotation and translation data for each node.
# The array has one entry for each node in the animation, and the data
# in it is given by either rot_def(rotation), trans_def(translation),
# or is a single float(scale).  Scale is NOT stored here if a nodes
# scale isnt animated. Assume a scale of 1.0 in that case.

# keyframe_data:
# Contains the data for each node for each stored keyframe.
# The data is different depending on the transformation
# type(follows the same rules as default_data) and should NOT
# be expected to contain the final frame in the animation.

compressed_frames_def = BlockDef("compressed frames",
    Struct("rotation_offsets",
        # keyframe_head offset for rotation is directly
        # after the header, so it is ALWAYS 44
        Void("keyframe_head"),
        SInt32("keyframes"),
        SInt32("default_data"),
        SInt32("keyframe_data"),
        SIZE=12
        ),
    QStruct("translation_offsets",
        SInt32("keyframe_head"),
        SInt32("keyframes"),
        SInt32("default_data"),
        SInt32("keyframe_data"),
        SIZE=16
        ),
    QStruct("scale_offsets",
        SInt32("keyframe_head"),
        SInt32("keyframes"),
        SInt32("default_data"),
        SInt32("keyframe_data"),
        SIZE=16
        ),

    Container("rotation",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        UInt16Array("keyframes", SIZE=compressed_stream_size),
        UInt16Array("default_data", SIZE=compressed_stream_size),
        SInt16Array("keyframe_data", SIZE=compressed_stream_size),
        ),
    Container("translation",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        UInt16Array("keyframes", SIZE=compressed_stream_size),
        FloatArray("default_data", SIZE=compressed_stream_size),
        FloatArray("keyframe_data", SIZE=compressed_stream_size),
        ),
    Container("scale",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        UInt16Array("keyframes", SIZE=compressed_stream_size),
        FloatArray("default_data", SIZE=compressed_stream_size),
        FloatArray("keyframe_data", SIZE=compressed_stream_size),
        ),
    endian='<'
    )


def get_keyframe_index_of_frame(frame, keyframes,
                                offset=0, keyframe_count=None):
    if keyframe_count is None:
        keyframe_count = len(keyframes)

    lower_keyframe_bound = offset
    upper_keyframe_bound = offset + keyframe_count - 1
    keyframe_index = offset

    if min(keyframes) > frame:
        raise ValueError("No keyframes at or below frame %s" % frame)

    # binary search through the keyframe indices to
    # find the keyframe_index of the frame we want.
    while True:
        # find the proper lower bound for the keyframe bounds window
        while True:
            # set the keyframe_index to the middle of the bounds of our sliding window
            keyframe_index = (lower_keyframe_bound + upper_keyframe_bound) // 2

            # if the keyframe_index is the very last keyframe, or the
            # frame number of the NEXT keyframe is past the frame we're
            # looking for, we break here. if we dont we'll go too far and
            # the lower bound will be past the frame we're requesting.
            if (keyframe_index + 1 >= keyframe_count or
                keyframes[keyframe_index + 1] > frame):
                break

            # otherwise shrink the windows lower bound
            lower_keyframe_bound = keyframe_index

        # if the frame number of this keyframe is below or equal to the frame
        # we're requesting, we'll have found the keyframe to use. break here.
        if keyframes[keyframe_index] <= frame:
            break

        # otherwise shrink the windows upper bound
        upper_keyframe_bound = keyframe_index

    # so at this point, we've found a keyframe_index where this is true:
    #   keyframes[keyframe_index]  <=  frame  <  keyframes[keyframe_index + 1]
    return keyframe_index - offset


def decompress_animation(anim, keep_compressed=True):
    temp_jma = JmaAnimation()
    temp_jma.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    temp_jma.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    temp_jma.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    # make some fake nodes
    temp_jma.nodes  = [None] * anim.node_count
    # make a bunch of frames we can fill in below
    temp_jma.append_frames([()] * anim.frame_count)

    anim.frame_size = temp_jma.frame_data_frame_size

    trans_flags = temp_jma.trans_flags
    rot_flags   = temp_jma.rot_flags
    scale_flags = temp_jma.scale_flags

    comp_data = anim.frame_data.STEPTREE
    if anim.offset_to_compressed_data > 0:
        comp_data = comp_data[anim.offset_to_compressed_data: ]

    try:
        comp_anim = compressed_frames_def.build(rawdata=comp_data)
    except Exception:
        print(traceback.format_exc())
        return False

    # decompress the headers for each of the keyframes
    rot   = comp_anim.rotation
    trans = comp_anim.translation
    scale = comp_anim.scale

    # get the keyframe counts and keyframe offsets
    rot_keyframe_offsets   = [v >> 12 for v in rot.keyframe_head]
    trans_keyframe_offsets = [v >> 12 for v in trans.keyframe_head]
    scale_keyframe_offsets = [v >> 12 for v in scale.keyframe_head]

    rot_keyframe_counts   = [v & 4095 for v in rot.keyframe_head]
    trans_keyframe_counts = [v & 4095 for v in trans.keyframe_head]
    scale_keyframe_counts = [v & 4095 for v in scale.keyframe_head]

    rot_keyframes   = rot.keyframes
    trans_keyframes = trans.keyframes
    scale_keyframes = scale.keyframes

    rot_default_data   = rot.default_data
    trans_default_data = trans.default_data
    scale_default_data = scale.default_data

    rot_keyframe_data   = rot.keyframe_data
    trans_keyframe_data = trans.keyframe_data
    scale_keyframe_data = scale.keyframe_data
    '''
    print("HEADERS")
    for v in rot.keyframe_head:
        print("    %s" % v)
    print("COUNTS")
    for v in rot_keyframe_counts:
        print("    %s" % v)
    print("OFFSETS")
    for v in rot_keyframe_offsets:
        print("    %s" % v)
    print("KEYFRAMES:", len(rot_keyframes))
    for v in rot_keyframes:
        print("    %s" % v)
    print("DEFAULT_DATA:", len(rot_default_data))
    print("KEYFRAME_DATA:", len(rot_keyframe_data))'''

    # make the uncompressed default and decomp data
    default_data = bytearray(temp_jma.default_data_size)
    decomp_data  = bytearray(anim.frame_size * anim.frame_count)
    anim.offset_to_compressed_data = len(decomp_data)

    if keep_compressed:
        decomp_data += comp_data

    anim.default_data.STEPTREE = default_data
    anim.frame_data.STEPTREE = decomp_data

    decomp_quat = compression.decompress_quaternion48
    blend_quats = compression.nlerp_blend_quaternions
    blend_trans = compression.lerp_blend_vectors

    sqrt = math.sqrt
    rot_i = trans_i = scale_i = 0
    for ni in range(temp_jma.node_count):
        rot_kf_ct = trans_kf_ct = scale_kf_ct = 0

        if rot_flags[ni]:
            rot_kf_ct  = rot_keyframe_counts[rot_i]
            rot_kf_off = rot_keyframe_offsets[rot_i]
            rot_i += 1

        if trans_flags[ni]:
            trans_kf_ct  = trans_keyframe_counts[trans_i]
            trans_kf_off = trans_keyframe_offsets[trans_i]
            trans_i += 1

        if scale_flags[ni]:
            scale_kf_ct = scale_keyframe_counts[scale_i]
            scale_kf_off = scale_keyframe_offsets[scale_i]
            scale_i += 1

        rot_def = decomp_quat(*rot_default_data[
            3 * ni: 3 * (ni + 1)])
        trans_def = trans_default_data[
            3 * ni: 3 * (ni + 1)]
        scale_def = 1.0

        if rot_kf_ct:
            rot_first_keyframe = rot_keyframes[rot_kf_off]
            rot_last_keyframe  = rot_keyframes[
                rot_kf_off + rot_kf_ct - 1]
            rot_first = decomp_quat(*rot_keyframe_data[
                3 * rot_kf_off:
                3 * (rot_kf_off + 1)])
            rot_last = decomp_quat(*rot_keyframe_data[
                3 * (rot_kf_off + rot_kf_ct - 1):
                3 * (rot_kf_off + rot_kf_ct)])

        if trans_kf_ct:
            trans_first_keyframe = trans_keyframes[trans_kf_off]
            trans_last_keyframe  = trans_keyframes[
                trans_kf_off + trans_kf_ct - 1]
            trans_first = trans_keyframe_data[
                3 * trans_kf_off:
                3 * (trans_kf_off + 1)]
            trans_last = trans_keyframe_data[
                3 * (trans_kf_off + trans_kf_ct - 1):
                3 * (trans_kf_off + trans_kf_ct)]

        if scale_kf_ct:
            scale_first_keyframe = scale_keyframes[scale_kf_off]
            scale_last_keyframe  = scale_keyframes[
                scale_kf_off + scale_kf_ct - 1]
            scale_first = trans_keyframe_data[
                scale_kf_off]
            scale_last = trans_keyframe_data[
                scale_kf_off + scale_kf_ct - 1]

        for fi in range(temp_jma.frame_count):
            node_frame = temp_jma.frames[fi][ni]

            if not rot_kf_ct:
                # only stores default data for this node
                i, j, k, w = rot_def
            elif fi == rot_last_keyframe:
                # frame is the last keyframe. repeat it to the end
                i, j, k, w = rot_last
            else:
                if fi < rot_first_keyframe:
                    # frame is before the first stored keyframe.
                    # blend from default data to first keyframe.
                    ratio = fi / rot_first_keyframe
                    q0 = rot_def
                    q1 = rot_first
                else:
                    # frame is at/past the first stored keyframe.
                    # don't need to use default data at all.
                    kfi = get_keyframe_index_of_frame(
                        fi, rot_keyframes, rot_kf_off, rot_kf_ct)
                    ratio = ((fi - rot_keyframes[kfi]) /
                             (rot_keyframes[kfi + 1] -
                              rot_keyframes[kfi]))

                    kfi *= 3
                    q0 = decomp_quat(*rot_keyframe_data[kfi    : kfi + 3])
                    q1 = decomp_quat(*rot_keyframe_data[kfi + 3: kfi + 6])

                if ratio == 0:
                    i, j, k, w = q0
                else:
                    i, j, k, w = blend_quats(q0, q1, ratio)


            if not trans_kf_ct:
                # only stores default data for this node
                x, y, z = trans_def
            elif fi == trans_last_keyframe:
                # frame is the last keyframe. repeat it to the end
                x, y, z = trans_last
            else:
                if fi < trans_first_keyframe:
                    # frame is before the first stored keyframe.
                    # blend from default data to first keyframe.
                    ratio = fi / trans_first_keyframe
                    p0 = trans_def
                    p1 = trans_first
                else:
                    # frame is at/past the first stored keyframe.
                    # don't need to use default data at all.
                    kfi = get_keyframe_index_of_frame(
                        fi, trans_keyframes, trans_kf_off, trans_kf_ct)
                    ratio = ((fi - trans_keyframes[kfi]) /
                             (trans_keyframes[kfi + 1] -
                              trans_keyframes[kfi]))

                    kfi *= 3
                    p0 = trans_keyframe_data[kfi    : kfi + 3]
                    p1 = trans_keyframe_data[kfi + 3: kfi + 6]

                if ratio == 0:
                    x, y, z = p0
                else:
                    x, y, z = blend_trans(p0, p1, ratio)


            if not scale_kf_ct:
                # only stores default data for this node
                scale = scale_def
            elif fi == scale_last_keyframe:
                # frame is the last keyframe. repeat it to the end
                scale = scale_last
            else:
                if fi < scale_first_keyframe:
                    # frame is before the first stored keyframe.
                    # blend from default data to first keyframe.
                    ratio = fi / scale_first_keyframe
                    s0 = scale_def
                    s1 = scale_first
                else:
                    # frame is at/past the first stored keyframe.
                    # don't need to use default data at all.
                    kfi = get_keyframe_index_of_frame(
                        fi, scale_keyframes, scale_kf_off, scale_kf_ct)
                    ratio = ((fi - scale_keyframes[kfi]) /
                             (scale_keyframes[kfi + 1] -
                              scale_keyframes[kfi]))
                    s0 = scale_keyframe_data[kfi]
                    s1 = scale_keyframe_data[kfi + 1]

                if ratio == 0:
                    scale = s0
                else:
                    scale = s0 * (1 - ratio) + s1 * ratio


            nmag = i**2 + j**2 + k**2 + w**2
            if nmag:
                nmag = sqrt(nmag)
                node_frame.rot_i = i / nmag
                node_frame.rot_j = j / nmag
                node_frame.rot_k = k / nmag
                node_frame.rot_w = w / nmag

            node_frame.pos_x = x * 100
            node_frame.pos_y = y * 100
            node_frame.pos_z = z * 100

            node_frame.scale = scale

    # compile the animation data into the tag
    serialization.serialize_uncompressed_frame_data(anim, temp_jma)

    return True


def compress_animation(anim, keep_uncompressed=True):
    pass
