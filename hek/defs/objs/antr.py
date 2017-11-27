from os.path import splitext, dirname
from math import sqrt, acos, sin
from array import array
from tkinter.filedialog import askopenfilename
from struct import pack_into, unpack

from .tag import *
from ..mod2 import mod2_def
from supyr_struct.field_types import *
from supyr_struct.field_type_methods import byteorder_char
from supyr_struct.defs.block_def import BlockDef


# for uncompressed animations, the data is stored as:
#     rotation first, then translation, and finally scale

# these structure definitions aren't really used in the code below, but
# are a good way to illustrate the structure of the compressed data.
frame_header = BlockDef("frame_header",
    UBitInt("frames_count", SIZE=12),
    UBitInt("frames_offset", SIZE=20),
    SIZE=4, TYPE=BitStruct
    )

# compressed quaternion rotation
# Bits AND bytes are ordered left to right as most significant to least
#   bbbbbbbb aaaaaaaa   dddddddd cccccccc   ffffffff eeeeeeee
#   iiiiiiii iiiijjjj   jjjjjjjj kkkkkkkk   kkkkwwww wwwwwwww
rot_def = BlockDef("comp_rotation",
    UInt16("q0"),
    UInt16("q1"),
    UInt16("q2"),
    SIZE=6, TYPE=QStruct
    )
# you'll need to read the 6 bytes as 3 little endian ints, then bit shift
# them together like so:    compressed_quat = q2 + (q1<<16) + (q0<<32)

# Translation is not compressed, and is still an xyz float triple.
trans_def = BlockDef("translation",
    Float("x"),
    Float("y"),
    Float("z"),
    )

# Scale is also not compressed, and is a single float.


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

    # looking for the NEXT streams offset
    attr_index += 1

    if attr_index <= 3:
        end = comp_frame[transform_index][attr_index]
    elif transform_index == 2:
        end = len(rawdata)
    else:
        end = comp_frame[transform_index + 1][0]

    return end - offset


# frame_head:
# Contains information on which frames are stored for each
# node and where to jump to in the frame_nums to read them.
# Look at the above frame_header struct for exact specifications.

# frame_nums:
# An array of arrays of UInt16s. The outer array stores one array
# of UInt16s for each node being rotated, translated, or scaled.
# Each of these UInt16 arrays stores the frame numbers that specify
# which frames have been stored in frame_data(the missing frames
# will need to be recreated by interpolating between stored frames).

# begin_frame:
# An array of transformation data(rotation, translation, or scale) for
# each nodes initial state(Maybe use this to remake the default_data).
# The array has one entry for each node in the animation, and the data
# in it is given by either rot_def(rotation), trans_def(translation),
# or is a single float(scale).  Scale doesnt seem to be stored here if
# a nodes scale isnt animated, so assume the scale is 1.0 for those.

# frame_data:
# Contains the data for each node for each stored frame.
# The data is different depending on the transformation
# type(follows the same rules as begin_frame) and should NOT
# be expected to contain the final frame in the animation.

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
        FloatArray("begin_frame", SIZE=stream_size),
        FloatArray("frame_data", SIZE=stream_size),
        ),
    Container("scale",
        UInt32Array("frame_head", SIZE=stream_size),
        SInt16Array("frame_nums", SIZE=stream_size),
        FloatArray("begin_frame", SIZE=stream_size),
        FloatArray("frame_data", SIZE=stream_size),
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

    def decompress_anim(self, anim_index):
        anim = self.data.tagdata.animations.STEPTREE[anim_index]

        if not anim.flags.compressed_data:
            return False
        elif anim.frame_count == 0:
            # no animation to decompress
            return False

        frame_count = anim.frame_count
        node_count = anim.node_count
        trans_flags = anim.trans_flags0 + (anim.trans_flags1 << 32)
        rot_flags   = anim.rot_flags0   + (anim.rot_flags1 << 32)
        scale_flags = anim.scale_flags0 + (anim.scale_flags1 << 32)

        offset = anim.offset_to_compressed_data
        comp_data = anim.frame_data.STEPTREE
        def_data = anim.default_data.STEPTREE
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
            frames = [ [[0.0, 0.0, 0.0, 1.0],
                        [0.0, 0.0, 0.0], 1.0]
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
        n = si = 0
        sq = sqrt  # local reference
        for node in node_frames:
            frame0 = node[0]
            rot = frame0[0]
            trans = frame0[1]

            # rotation
            comp_rot = rot_begin[n*3+2]+(rot_begin[n*3+1]<<16)+(rot_begin[n*3]<<32)
            rot[3] = comp_rot&2047
            rot[2] = (comp_rot>>12)&2047
            rot[1] = (comp_rot>>24)&2047
            rot[0] = (comp_rot>>36)&2047
            if sum(rot):
                if comp_rot&0x800:          rot[3] = rot[3]-2047
                if comp_rot&0x800000:       rot[2] = rot[2]-2047
                if comp_rot&0x800000000:    rot[1] = rot[1]-2047
                if comp_rot&0x800000000000: rot[0] = rot[0]-2047
                length = sq(rot[0]**2+rot[1]**2+
                            rot[2]**2+rot[3]**2)
                rot[0] /= length
                rot[1] /= length
                rot[2] /= length
                rot[3] /= length
            else:
                # avoid division by zero
                rot[3] = 1

            # translation
            trans[0] = trans_begin[n]
            trans[1] = trans_begin[n+1]
            trans[2] = trans_begin[n+2]

            # scale
            if scale_flags&(1<<n):
                frame0[2] = scale_begin[si]
                si += 1  # for scale, only nodes with keyframes are
                #          stored in the first frame, not every node

            n += 1


        # if the default data is all empty, try to extract
        # it from the gbxmodel that this animation goes to.
        if not sum(def_data):
            def_data = bytearray()
            try:
                # try to get a cached default_data from
                # a previous animation looking for it.
                mod2_nodes = self.gbxmodel_nodes
            except AttributeError:
                mod2_nodes = None

            if mod2_nodes is None:
                print("    This animation is missing its default_data, " +
                      "which will prevent it from being imported properly.\n" +
                      "    Select the gbxmodel that it animates to extract it.")
                print("    WARNING!: If multiple model are animated by this " +
                      "animation(such as with first person weapon anims) " +
                      "then this will not work.\n    I think you can export " +
                      "a gbxmodel with all the pieces to animate parented " +
                      "together in their default positions and use that.\n" +
                      "    That might work, but honestly I don't know...")
                mod2_tag = None
                while mod2_tag is None or len(mod2_nodes) != node_count:
                    if mod2_tag is not None:
                        print("Gbxmodel node count did not match " +
                              "the node count in this animation.")
                    mod2_path = askopenfilename(
                        initialdir=dirname(self.filepath), filetypes=(
                            ('Gbxmodel', '*.gbxmodel'), ('All', '*')),
                        title="Select a Gbxmodel tag")
                    try:
                        mod2_tag = mod2_def.build(filepath=mod2_path)
                        mod2_nodes = mod2_tag.data.tagdata.nodes.STEPTREE
                    except Exception:
                        print(format_exc())
                        mod2_tag = None

            # cache the default data in case another animation needs it
            self.gbxmodel_nodes = mod2_nodes

            i = 0
            for n in range(node_count):
                rot   = mod2_nodes[n].rotation
                trans = mod2_nodes[n].translation
                if not (rot_flags&(1<<n)):
                    def_data += b'\x00'*8
                    pack_into('>hhhh', def_data, i,
                              int(rot[0]*32767), int(rot[1]*32767),
                              int(rot[2]*32767), int(rot[3]*32767))
                    i += 8
                if not (trans_flags&(1<<n)):
                    def_data += b'\x00'*12
                    pack_into('>fff', def_data, i, *trans)
                    i += 12
                if not (scale_flags&(1<<n)):
                    def_data += b'\x00'*4
                    pack_into('>f', def_data, i, 1.0)
                    i += 4

        # decompress the transforms
        ri = ti = si = 0
        node_rot_nums = [()]*node_count
        node_trans_nums = [()]*node_count
        node_scale_nums = [()]*node_count
        for n in range(node_count):
            rot_frames = trans_frames = scale_frames = ()
            nf = node_frames[n]

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
                rot = nf[f][0]
                comp_rot = rot_data[ri+2]+(rot_data[ri+1]<<16)+(rot_data[ri]<<32)
                rot[3] = comp_rot&2047
                rot[2] = (comp_rot>>12)&2047
                rot[1] = (comp_rot>>24)&2047
                rot[0] = (comp_rot>>36)&2047
                if sum(rot):
                    if comp_rot&0x800:          rot[3] = rot[3]-2047
                    if comp_rot&0x800000:       rot[2] = rot[2]-2047
                    if comp_rot&0x800000000:    rot[1] = rot[1]-2047
                    if comp_rot&0x800000000000: rot[0] = rot[0]-2047
                    length = sq(rot[0]**2+rot[1]**2+
                                rot[2]**2+rot[3]**2)
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
                nf[f][1][:] = trans_data[ti:ti+3]
                ti += 3

            # scale
            for f in scale_frames:
                nf[f][2] = scale_data[si]
                si += 1


        # interpolate over the given frames to fill in the missing ones
        for n in range(node_count):
            node = node_frames[n]

            f0 = node[0][0]
            # copy the first frames to frame[0]
            if node_rot_nums[n]:
                node[0][0] = node[node_rot_nums[n][0]][0]
            if node_trans_nums[n]:
                node[0][1] = node[node_trans_nums[n][0]][1]
            if node_scale_nums[n]:
                node[0][2] = node[node_scale_nums[n][0]][2]

            i0 = f0[0]
            j0 = f0[1]
            k0 = f0[2]
            w0 = f0[3]
            last_num = 0
            reverse_orient = False
            #if n == 1 and anim_index == 1:
            #    print(node_rot_nums[n])
            #    print(0, f0)

            # interpolate the rotations
            for next_num in node_rot_nums[n]:
                f1 = node[next_num][0]
                ######################################################
                #
                #    NOTE: Some of the frame numbers are out of order.
                #    This might be what I'm missing, and might help me
                #    finally be able to fully decode these animations.
                #
                ######################################################
                i1 = f1[0]
                j1 = f1[1]
                k1 = f1[2]
                w1 = f1[3]
                num_dist = next_num - last_num

                cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
                #if (cos_half_theta < 0) != reverse_orient:
                #    reverse_orient = not reverse_orient
                #    cos_half_theta *= -1

                #if reverse_orient:
                #    # need to change the vector rotations to be 2pi - rot
                #    f1[0] = i1 = -i1
                #    f1[1] = j1 = -j1
                #    f1[2] = k1 = -k1
                #    f1[3] = w1 = -w1

                #if n == 1 and anim_index == 1:
                #    print(next_num, reverse_orient, cos_half_theta, f1)

                # slerp interpolation code
                '''
                if abs(cos_half_theta) >= 1.0:
                    half_theta = 0.0
                else:
                    half_theta = acos(cos_half_theta)
                    
                sin_half_theta = sqrt(max(1 - cos_half_theta**2, 0))

                for i in range(1, num_dist):
                    f = node[last_num+i][0]
                    i = i/num_dist

                    # angle is not well defined in floating point at this point
                    if sin_half_theta <= 0.000001:
                        r0 = 1 - i
                        r1 = i
                    else:
                        r0 = sin((1 - i)*half_theta) / sin_half_theta
                        r1 = sin(i*half_theta) / sin_half_theta

                    f[0] = i0*r0 + i1*r1
                    f[1] = j0*r0 + j1*r1
                    f[2] = k0*r0 + k1*r1
                    f[3] = w0*r0 + w1*r1
                '''
                if num_dist:
                    # nlerp interpolation code
                    di = (i1 - i0) / num_dist
                    dj = (j1 - j0) / num_dist
                    dk = (k1 - k0) / num_dist
                    dw = (w1 - w0) / num_dist
                    for i in range(1, num_dist):
                        f = node[last_num+i][0]

                        f[0] = i0 + di*i
                        f[1] = j0 + dj*i
                        f[2] = k0 + dk*i
                        f[3] = w0 + dw*i
                        length = sqrt(f[0]**2 + f[1]**2 + f[2]**2 + f[3]**2)
                        f[0] /= length
                        f[1] /= length
                        f[2] /= length
                        f[3] /= length

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

                f0 = f1
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
        anim.default_data.STEPTREE = def_data
        anim.frame_data.STEPTREE = new_frame_data = bytearray(
            b'\x00'*anim.frame_size*frame_count)
        anim.offset_to_compressed_data = 0
        anim.flags.compressed_data = False

        # write the rotations, translations, and scales to the new_frame_data
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

        return True
