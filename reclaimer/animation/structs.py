#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from supyr_struct.defs.block_def import BlockDef
from supyr_struct.field_types import QStruct, Struct, Container, Void,\
     UBitInt, BitStruct, Float, UInt16, UInt32,\
     UInt32Array, UInt16Array, FloatArray
# these structure definitions aren't really used in any code, but
# are a good way to illustrate the structure of the compressed data.
# for uncompressed animations, the data is stored as:
#     rotation first, then translation, and finally scale

keyframe_header_def = BlockDef("keyframe_header",
    UBitInt("keyframe_count", SIZE=12),
    UBitInt("keyframe_data_offset", SIZE=20),
    SIZE=4, TYPE=BitStruct
    )

# compressed quaternion rotation
# Bits AND bytes are ordered left to right as most significant to least
#   bbbbbbbb aaaaaaaa   dddddddd cccccccc   ffffffff eeeeeeee
#   iiiiiiii iiiijjjj   jjjjjjjj kkkkkkkk   kkkkwwww wwwwwwww
quaternion48_def = BlockDef("quaternion48",
    # you'll need to read the 6 bytes as 3 little endian ints, then bit shift
    # them together like so:    compressed_quat = w2 + (w1<<16) + (w0<<32)
    UInt16("w0"),
    UInt16("w1"),
    UInt16("w2"),
    SIZE=6, TYPE=QStruct
    )

# Translation is not compressed, and is still an xyz float triple.
translation_def = BlockDef("translation",
    Float("x"),
    Float("y"),
    Float("z"),
    )


def compressed_stream_size(node=None, parent=None, attr_index=None,
                           rawdata=None, new_value=None, *args, **kwargs):
    if attr_index is None:
        raise IndexError
    elif new_value is not None:
        return
    elif parent is None:
        raise TypeError
    elif node is None:
        node = parent[attr_index]

    if node is not None:
        return len(node) * node.itemsize
    elif rawdata is None:
        return 0

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
    # in it is given by either quaternion48_def or a translation_def.
    # Scale is ONLY stored here if the nodes scale is animated.
    # Assume a scale of 1.0 otherwise.

    # keyframe_data:
    # Contains the data for each node for each stored keyframe.
    # The data is different depending on the transformation type.
    #     (follows the same rules as default_data)

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
