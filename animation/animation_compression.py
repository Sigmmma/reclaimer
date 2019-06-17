import traceback

from reclaimer.vector_util import decompress_quaternion48
from supyr_struct.field_types import *
from supyr_struct.defs.block_def import BlockDef

# for uncompressed animations, the data is stored as:
#     rotation first, then translation, and finally scale

# these structure definitions aren't really used in the code below, but
# are a good way to illustrate the structure of the compressed data.
keyframe_header = BlockDef("keyframe_header",
    UBitInt("keyframe_count", SIZE=12),
    UBitInt("keyframe_offset", SIZE=20),
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
# Contains information on which keyframes are stored for each
# node and where to jump to in the keyframes array to read them.
# Look at the above keyframe_header struct for exact specifications.

# keyframes:
# An array of arrays of UInt16s. The outer array stores one array
# of UInt16s for each node being rotated, translated, or scaled.
# Each of these UInt16 arrays stores the keyframe numbers of which
# frames have been stored in keyframe_data

# default_data:
# An array of transformation data(rotation, translation, or scale) for
# each nodes initial state(Maybe use this to remake the default_data).
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
        SInt16Array("keyframes", SIZE=compressed_stream_size),
        SInt16Array("default_data", SIZE=compressed_stream_size),
        SInt16Array("keyframe_data", SIZE=compressed_stream_size),
        ),
    Container("translation",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        SInt16Array("keyframes", SIZE=compressed_stream_size),
        FloatArray("default_data", SIZE=compressed_stream_size),
        FloatArray("keyframe_data", SIZE=compressed_stream_size),
        ),
    Container("scale",
        UInt32Array("keyframe_head", SIZE=compressed_stream_size),
        SInt16Array("keyframes", SIZE=compressed_stream_size),
        FloatArray("default_data", SIZE=compressed_stream_size),
        FloatArray("keyframe_data", SIZE=compressed_stream_size),
        ),
    endian='<'
    )


def get_keyframe_index_of_frame(frame, keyframes):
    keyframe_count = len(keyframes)

    lower_keyframe_bound = 0
    upper_keyframe_bound = keyframe_count - 1
    keyframe_index = 0

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
    return keyframe_index


def decompress_animation(anim, jma_nodes=None):
    if jma_nodes is None:
        jma_nodes = [jma.JmaNode() for n in range(anim.node_count)]

    jma_anim = jma.JmaAnimation(
        anim.name, anim.node_list_checksum, anim.type.enum_name,
        anim.frame_info_type.enum_name, anim.flags.world_relative, jma_nodes
        )

    jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    comp_data = anim.frame_data.STEPTREE
    if anim.offset_to_compressed_data > 0:
        comp_data = comp_data[anim.offset_to_compressed_data: ]

    try:
        comp_anim = compressed_frames_def.build(rawdata=comp_data)
    except Exception:
        print(traceback.format_exc())
        return None

    # decompress the headers for each of the keyframes
    rot   = comp_data.rotation
    trans = comp_data.translation
    scale = comp_data.scale

    # get the keyframe counts and keyframe offsets
    # Right shift by 13 rather than 12 because we're also dividing by 2
    # to account for the fact that the offsets are in bytes, not entries.
    rot_head   = [(v & 4095, v >> 13) for v in rot.keyframe_head]
    trans_head = [(v & 4095, v >> 13) for v in trans.keyframe_head]
    scale_head = [(v & 4095, v >> 13) for v in scale.keyframe_head]

    return jma_anim
