from os.path import splitext
from math import sqrt, acos, sin
from array import array
from struct import pack_into

from .tag import *
from supyr_struct.field_types import *
from supyr_struct.field_type_methods import byteorder_char
from supyr_struct.defs.block_def import BlockDef


frame_header = BlockDef("frame_header",
    BitUInt("frames_count", SIZE=12),
    BitUInt("frames_offset", SIZE=20),
    SIZE=4, TYPE=BitStruct
    )

# Translation is not compressed, and is still an xyz float.
# Scale is also not compressed, and is a single float.
compressed_rotation = BlockDef("compressed_rotation",
    BSInt16("i"),
    BitStruct("compressed components",
        BitUInt("w", SIZE=11),
        Bit1SInt("k", SIZE=11),
        Bit1SInt("j", SIZE=10)
        ),
    SIZE=6
    )
# need to swap first 2 bytes with last 2 bytes like so:
# data = data[2:] + data[:2]
# after decompressing, the components need to be normalized


def stream_size(node=None, parent=None, attr_index=None,
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

    # looking for the NEXT offset
    attr_index += 1

    if attr_index <= 3:
        end = comp_frame[transform_index][attr_index]
    elif transform_index == 2:
        end = len(rawdata)
    else:
        end = comp_frame[transform_index + 1][0]

    return end - offset


# frame_head:
# Contains the frame count for each frame as well as an
# unknown increasing 16 or 24 bit number(buffer end?).

# frame_nums:
# An array of arrays of UInt16s that specify the frames
# that are actually stored in the frame_data for each node.

# begin_frame:
# The initial rotation/translation/scale for each of
# the nodes, even ones that arent being animatied.

# frame_data:
# Contains the data for each node for each frame. The data is
# different depending on if it is rotation, translation, or scale.
# Frame data is NOT guaranteed to contain the final keyframe.

compressed_frames = BlockDef("compressed frames",
    Struct("rotation_offsets",
        # frame_info offset for rotation is directly
        # after the header, so it is ALWAYS 44
        Void("frame_head"),
        SInt32("frame_nums"),
        SInt32("begin_frame"),
        SInt32("frame_data"),
        ),
    QStruct("translation_offsets",
        SInt32("frame_head"),
        SInt32("frame_nums"),
        SInt32("begin_frame"),
        SInt32("frame_data"),
        ),
    QStruct("scale_offsets",
        SInt32("frame_head"),
        SInt32("frame_nums"),
        SInt32("begin_frame"),
        SInt32("frame_data"),
        ),

    Container("rotation",
        UInt32Array("frame_head", SIZE=stream_size),
        SInt16Array("frame_nums", SIZE=stream_size),
        SInt16Array("begin_frame", SIZE=stream_size),
        SInt16Array("frame_data", SIZE=stream_size),
        ),
    Container("translation",
        UInt32Array("frame_head", SIZE=stream_size),
        SInt16Array("frame_nums", SIZE=stream_size),
        FloatArray("begin_frame", SIZE=stream_size, ENDIAN='>'),
        FloatArray("frame_data", SIZE=stream_size, ENDIAN='>'),
        ),
    Container("scale",
        UInt32Array("frame_head", SIZE=stream_size),
        SInt16Array("frame_nums", SIZE=stream_size),
        FloatArray("begin_frame", SIZE=stream_size, ENDIAN='>'),
        FloatArray("frame_data", SIZE=stream_size, ENDIAN='>'),
        ),
    endian='<'
    )

class AntrTag(HekTag):

    def decompress_all_anims(self):
        decompressed_indices = []

        for i in range(self.data.tagdata.animations.size):
            if self.decompress_anim(i):
                compressed_indices.append(i)

        return decompressed_indices

    def decompress_anim(self, i):
        anim = self.data.tagdata.animations.STEPTREE[i]

        if not anim.flags.compressed_data:
            return False
        elif anim.frame_count == 0:
            # no animation to decompress
            return False

        frame_count = anim.frame_count
        node_count = anim.node_count
        trans_flags = anim.trans_flags0 + (anim.trans_flags1 << 32)
        rot_flags = anim.rot_flags0 + (anim.rot_flags1 << 32)
        scale_flags = anim.scale_flags0 + (anim.scale_flags1 << 32)

        offset = anim.offset_to_compressed_data
        comp_data = anim.frame_data.STEPTREE
        if offset > 0:
            comp_data = comp_data[offset:]

        try:
            comp_data = compressed_frames.build(rawdata=comp_data)
        except Exception:
            print(format_exc())
            return False

        # make a nested list to store all transforms
        node_frames = []
        rot_count = trans_count = scale_count = 0
        for i in range(node_count):
            bit = 1<<i
            has_rot = bool(rot_flags&bit)
            has_trans = bool(trans_flags&bit)
            has_scale = bool(scale_flags&bit)
            rot_count += has_rot
            trans_count += has_trans
            scale_count += has_scale

            # the node stores rotation, translation, and scale
            frames = [ [[None, None, None, None],
                        [None, None, None], None]
                       for j in range(frame_count) ]

            node_frames.append(frames)

        # decompress the headers for each of the frame_nums
        rot,   rot_head   = comp_data.rotation,    []
        trans, trans_head = comp_data.translation, []
        scale, scale_head = comp_data.scale,       []

        # get the frame_nums counts and frame_nums offsets
        # Right shift by 13 rather than 12 because we're also dividing by 2
        # to count for the fact that the offsets are in bytes, not entries.
        for info in rot.frame_head:   rot_head.append((info&4095, info>>13))
        for info in trans.frame_head: trans_head.append((info&4095, info>>13))
        for info in scale.frame_head: scale_head.append((info&4095, info>>13))

        # get the data to decompress
        rot_nums  = rot.frame_nums
        rot_begin = rot.begin_frame
        rot_data  = rot.frame_data
        trans_nums  = trans.frame_nums
        trans_begin = trans.begin_frame
        trans_data  = trans.frame_data
        scale_nums  = scale.frame_nums
        scale_begin = scale.begin_frame
        scale_data  = scale.frame_data

        # decompress the first frames data
        i = 0
        sq = sqrt  # local reference
        for node in node_frames:
            frame0 = node[0]
            rot = frame0[0]
            trans = frame0[1]

            # rotation
            comp_rot = (rot_begin[i*3 + 1] << 16) + rot_begin[i*3 + 2]
            rot[0] = rot_begin[i*3]/32767
            rot[1] = ((comp_rot>>22)&511)/511
            rot[2] = ((comp_rot>>11)&1023)/1023
            rot[3] = (comp_rot&2047)/2047
            length = sq(rot[0]**2+rot[1]**2+rot[2]**2+rot[3]**2)
            if sum(rot):
                if comp_rot&0x80000000: rot[1] = rot[1]-1
                if comp_rot&0x00200000: rot[2] = rot[2]-1
                length = sq(rot[0]**2+rot[1]**2+rot[2]**2+rot[3]**2)
                rot[0] /= length
                rot[1] /= length
                rot[2] /= length
                rot[3] /= length
            else:
                # avoid division by zero
                rot[3] = 1

            # translation
            trans[0] = trans_begin[i*3]
            trans[1] = trans_begin[i*3+1]
            trans[2] = trans_begin[i*3+2]

            # scale
            if scale_flags&(1<<i):
                frame0[2] = scale_begin[i]

            i += 1

        # decompress the transforms
        ri = ti = si = 0
        node_rot_nums = [()]*node_count
        node_trans_nums = [()]*node_count
        node_scale_nums = [()]*node_count
        for n in range(node_count):
            rot_frames = trans_frames = scale_frames = ()

            # get the frames that this node is animated on
            if rot_flags&(1<<n):
                rot_frame_ct, rot_off = rot_head.pop(0)
                rot_frames = rot_nums[rot_off:rot_off+rot_frame_ct]
                node_rot_nums[n] = rot_frames
            if trans_flags&(1<<n):
                trans_frame_ct, trans_off = trans_head.pop(0)
                trans_frames = trans_nums[trans_off:trans_off+trans_frame_ct]
                node_trans_nums[n] = trans_frames
            if scale_flags&(1<<n):
                scale_frame_ct, scale_off = scale_head.pop(0)
                scale_frames = scale_nums[scale_off:scale_off+scale_frame_ct]
                node_scale_nums[n] = scale_frames

            # rotation
            for f in rot_frames:
                rot = node_frames[n][f][0]
                comp_rot = rot_data[ri+2] + (rot_data[ri+1] << 16)
                rot[0] = rot_data[ri]/32767
                rot[1] = ((comp_rot>>22)&511)/511
                rot[2] = ((comp_rot>>11)&1023)/1023
                rot[3] = (comp_rot&2047)/2047
                if sum(rot):
                    if comp_rot&0x80000000: rot[1] = rot[1]-1
                    if comp_rot&0x00200000: rot[2] = rot[2]-1
                    length = sq(rot[0]**2+rot[1]**2+rot[2]**2+rot[3]**2)
                    rot[0] /= length
                    rot[1] /= length
                    rot[2] /= length
                    rot[3] /= length
                else:
                    # avoid division by zero
                    rot[3] = 1

                ri += 3

            # translation
            for f in trans_frames:
                node_frames[n][f][1][:] = trans_data[ti:ti+3]
                ti += 3

            # scale
            for f in scale_frames:
                node_frames[n][f][2] = scale_data[si]
                si += 1

        # interpolate over the given frames to fill in the missing ones
        for n in range(node_count):
            node = node_frames[n]
            f0 = node[0][0]
            i0 = f0[0]
            j0 = f0[1]
            k0 = f0[2]
            w0 = f0[3]
            last_num = 0

            # interpolate the rotations
            for next_num in node_rot_nums[n]:
                f1 = node[next_num][0]
                i1 = f1[0]
                j1 = f1[1]
                k1 = f1[2]
                w1 = f1[3]
                num_dist = next_num - last_num

                cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
                if abs(cos_half_theta) >= 1.0:
                    half_theta = 0.0
                else:
                    half_theta = acos(cos_half_theta)
                sin_half_theta = sqrt(max(1 - cos_half_theta**2, 0))

                # angle is not well defined in floating point when this small
                if sin_half_theta <= 0.000001:
                    r0 = r1 = 0.5
                for i in range(1, num_dist):
                    f = node[last_num+i][0]
                    i = i/num_dist

                    if sin_half_theta > 0.000001:
                        r0 = sin((1 - i)*half_theta) / sin_half_theta
                        r1 = sin(i*half_theta) / sin_half_theta
                    f[0] = i0*r0 + i1*r1
                    f[1] = j0*r0 + j1*r1
                    f[2] = k0*r0 + k1*r1
                    f[3] = w0*r0 + w1*r1

                f0 = f1
                i0 = i1
                j0 = j1
                k0 = k1
                w0 = w1
                last_num = next_num

            # repeat the last frame to the end
            for i in range(last_num, frame_count):
                node[i][0] = f0

            f0 = node[0][1]
            x0 = f0[0]
            y0 = f0[1]
            z0 = f0[2]
            last_num = 0
            # interpolate the translations
            for next_num in node_trans_nums[n]:
                f1 = node[next_num][1]
                x1 = f1[0]
                y1 = f1[1]
                z1 = f1[2]
                num_dist = next_num - last_num
                for i in range(1, num_dist):
                    f = node[last_num+i][1]
                    f[0] = (x0*(num_dist-i) + x1*i) / num_dist
                    f[1] = (y0*(num_dist-i) + y1*i) / num_dist
                    f[2] = (z0*(num_dist-i) + z1*i) / num_dist

                x0 = x1
                y0 = y1
                z0 = z1
                last_num = next_num

            # repeat the last frame to the end
            for i in range(last_num, frame_count):
                node[i][1] = f0

            f0 = node[0][2]
            last_num = 0
            # interpolate the scales
            for next_num in node_scale_nums[n]:
                f1 = node[next_num][2]
                num_dist = next_num - last_num
                for i in range(1, num_dist):
                    node[last_num+i][2] = (f0*(num_dist-i) + f1*i) / num_dist

                f0 = f1
                last_num = next_num

            # repeat the last frame to the end
            for i in range(last_num, frame_count):
                node[i][2] = f0


        # make sure the frame_size is accurate and uncheck the compressed flag
        anim.frame_size = rot_count*8 + trans_count*12 + scale_count*4
        anim.flags.compressed_data = False

        # write the rotations, translations, and scales to the new_frame_data
        new_frame_data = bytearray(b'\x00'*anim.frame_size*frame_count)
        i = 0
        node_range = range(node_count)
        for f in range(frame_count):
            for n in node_range:
                node = node_frames[n][f]
                if node is None:
                    continue
                if rot_flags&(1<<n):
                    rot = node[0]
                    pack_into('>hhhh', new_frame_data, i,
                              int(rot[0]*32767), int(rot[1]*32767),
                              int(rot[2]*32767), int(rot[3]*32767))
                    i += 8
                if trans_flags&(1<<n):
                    pack_into('>fff', new_frame_data, i, *node[1])
                    i += 12
                if scale_flags&(1<<n):
                    pack_into('>f', new_frame_data, i, node[2])
                    i += 4

        anim.frame_data.STEPTREE = new_frame_data

        return True
