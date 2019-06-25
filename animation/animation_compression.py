import math
import traceback

from supyr_struct.field_types import *
from supyr_struct.defs.block_def import BlockDef

from reclaimer.animation import serialization
from reclaimer.animation import jma
from reclaimer.util import compression
from reclaimer.util import matrices

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
        UInt32("keyframes"),
        UInt32("default_data"),
        UInt32("keyframe_data"),
        SIZE=12
        ),
    QStruct("translation_offsets",
        UInt32("keyframe_head"),
        UInt32("keyframes"),
        UInt32("default_data"),
        UInt32("keyframe_data"),
        SIZE=16
        ),
    QStruct("scale_offsets",
        UInt32("keyframe_head"),
        UInt32("keyframes"),
        UInt32("default_data"),
        UInt32("keyframe_data"),
        SIZE=16
        ),

    Container("rotation",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        UInt16Array("keyframes", SIZE=compressed_stream_size),
        UInt16Array("default_data", SIZE=compressed_stream_size),
        UInt16Array("keyframe_data", SIZE=compressed_stream_size),
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
                                keyframe_count=None, offset=0):
    if keyframe_count is None:
        keyframe_count = len(keyframes) - offset

    # TODO: make this more efficent using a binary search
    for i in range(offset, offset + keyframe_count - 1):
        if keyframes[i] <= frame and keyframes[i + 1] > frame:
            return i

    raise ValueError(
        "No keyframes pairs containing frame %s" % frame)



def decompress_animation(anim, keep_compressed=True):
    if not anim.flags.compressed_data:
        return True

    temp_jma = jma.JmaAnimation()
    temp_jma.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    temp_jma.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    temp_jma.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    # make some fake nodes
    temp_jma.nodes  = [None] * anim.node_count
    # make a bunch of frames we can fill in below
    temp_jma.append_frames([()] * (anim.frame_count + 1))

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

    # make the uncompressed default and decomp data
    default_data = bytearray(temp_jma.default_data_size)
    decomp_data  = bytearray(anim.frame_size * anim.frame_count)
    anim.offset_to_compressed_data = len(decomp_data)

    if keep_compressed:
        decomp_data += comp_data

    anim.default_data.STEPTREE = default_data
    anim.frame_data.STEPTREE = decomp_data

    decomp_quat = compression.decompress_quaternion48
    blend_quats = matrices.nlerp_blend_quaternions
    blend_trans = matrices.lerp_blend_vectors

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
            scale_kf_ct  = scale_keyframe_counts[scale_i]
            scale_kf_off = scale_keyframe_offsets[scale_i]
            scale_i += 1

        rot_def = decomp_quat(*rot_default_data[
            3 * ni: 3 * (ni + 1)])
        trans_def = trans_default_data[
            3 * ni: 3 * (ni + 1)]
        scale_def = 1.0

        if rot_kf_ct:
            rot_first_kf = rot_keyframes[rot_kf_off]
            rot_last_kf  = rot_keyframes[rot_kf_off + rot_kf_ct - 1]
            rot_first = decomp_quat(*rot_keyframe_data[
                3 * rot_kf_off:
                3 * (rot_kf_off + 1)])
            rot_last = decomp_quat(*rot_keyframe_data[
                3 * (rot_kf_off + rot_kf_ct - 1):
                3 * (rot_kf_off + rot_kf_ct)])

        if trans_kf_ct:
            trans_first_kf = trans_keyframes[trans_kf_off]
            trans_last_kf  = trans_keyframes[trans_kf_off + trans_kf_ct - 1]
            trans_first = trans_keyframe_data[
                3 * trans_kf_off:
                3 * (trans_kf_off + 1)]
            trans_last = trans_keyframe_data[
                3 * (trans_kf_off + trans_kf_ct - 1):
                3 * (trans_kf_off + trans_kf_ct)]

        if scale_kf_ct:
            scale_first_kf = scale_keyframes[scale_kf_off]
            scale_last_kf  = scale_keyframes[scale_kf_off + scale_kf_ct - 1]
            scale_first = trans_keyframe_data[
                scale_kf_off]
            scale_last = trans_keyframe_data[
                scale_kf_off + scale_kf_ct - 1]

        for fi in range(anim.frame_count):
            node_frame = temp_jma.frames[fi][ni]

            if not rot_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                i, j, k, w = rot_def
            elif fi == rot_last_kf:
                # frame is the last keyframe. repeat it to the end
                i, j, k, w = rot_last
            elif fi < rot_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                i, j, k, w = blend_quats(
                    rot_def, rot_first, fi / rot_first_kf)
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, rot_keyframes, rot_kf_ct, rot_kf_off)
                kf0 = rot_keyframes[kf_i]
                q0 = decomp_quat(
                    *rot_keyframe_data[kf_i * 3: (kf_i + 1) * 3])
                
                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    i, j, k, w = q0
                else:
                    kf1 = rot_keyframes[kf_i + 1]
                    ratio = (fi - kf0) / (kf1 - kf0)
                    kf_i += 1
                    q1 = decomp_quat(
                        *rot_keyframe_data[kf_i * 3: (kf_i + 1) * 3])
                    i, j, k, w = blend_quats(q0, q1, ratio)


            if not trans_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                x, y, z = trans_def
            elif fi == trans_last_kf:
                # frame is the last keyframe. repeat it to the end
                x, y, z = trans_last
            elif fi < trans_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                x, y, z = blend_trans(
                    trans_def, trans_first, fi / trans_first_kf)
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, trans_keyframes, trans_kf_ct, trans_kf_off)
                kf0 = trans_keyframes[kf_i]
                p0 = trans_keyframe_data[kf_i * 3: (kf_i + 1) * 3]
                
                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    x, y, z = p0
                else:
                    kf1 = trans_keyframes[kf_i + 1]
                    ratio = (fi - kf0) / (kf1 - kf0)

                    kf_i += 1
                    p1 = trans_keyframe_data[kf_i * 3: (kf_i + 1) * 3]
                    x, y, z = blend_trans(p0, p1, ratio)


            if not scale_kf_ct or fi == 0:
                # first frame OR only default data stored for this node
                scale = scale_def
            elif fi == scale_last_kf:
                # frame is the last keyframe. repeat it to the end
                scale = scale_last
            elif fi < scale_first_kf:
                # frame is before the first stored keyframe.
                # blend from default data to first keyframe.
                ratio = fi / scale_first_kf
                scale = scale_def * (1 - ratio) + scale_first * ratio
            else:
                # frame is at/past the first stored keyframe.
                # don't need to use default data at all.
                kf_i = get_keyframe_index_of_frame(
                    fi, scale_keyframes, scale_kf_ct, scale_kf_off)

                if fi == kf0:
                    # this keyframe is the frame we want.
                    # no blending required
                    scale = s0
                else:
                    ratio = ((fi - scale_keyframes[kf_i]) /
                             (scale_keyframes[kf_i + 1] -
                              scale_keyframes[kf_i]))
                    scale = (
                        scale_keyframe_data[kf_i] * (1 - ratio) +
                        scale_keyframe_data[kf_i + 1] * ratio)


            nmag = i**2 + j**2 + k**2 + w**2
            if nmag:
                nmag = 1 / sqrt(nmag)
                if w < 0:
                    i = -i
                    j = -j
                    k = -k
                    w = -w
                node_frame.rot_i = i * nmag
                node_frame.rot_j = j * nmag
                node_frame.rot_k = k * nmag
                node_frame.rot_w = w * nmag

            node_frame.pos_x = x * 100
            node_frame.pos_y = y * 100
            node_frame.pos_z = z * 100

            node_frame.scale = scale

    # compile the animation data into the tag
    serialization.serialize_uncompressed_frame_data(anim, temp_jma)

    return True


def compress_animation(anim, keep_uncompressed=True):
    pass
