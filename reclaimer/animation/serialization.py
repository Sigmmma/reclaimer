#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import math

from array import array
from copy import deepcopy
from struct import pack_into, unpack_from
from types import MethodType

from reclaimer.animation.jma import JmaRootNodeState, JmaNodeState
from reclaimer.animation.structs import compressed_frames_def
from reclaimer.util import compression
from reclaimer.util import matrices

__all__ = ("serialize_frame_info", "deserialize_frame_info",
           "serialize_default_data", "deserialize_default_data",
           "serialize_frame_data", "deserialize_frame_data",
           "deserialize_compressed_frame_data",
           "serialize_compressed_frame_data",
           "get_anim_flags", "get_keyframe_index_of_frame",)


def serialize_frame_info(jma_anim, endian=">"):
    frame_ct = jma_anim.frame_count - 1
    data = bytearray(jma_anim.root_node_info_frame_size * frame_ct)

    pack_2_float_into = MethodType(pack_into, endian + "2f")
    pack_3_float_into = MethodType(pack_into, endian + "3f")
    pack_4_float_into = MethodType(pack_into, endian + "4f")
    frame_info_node_size = jma_anim.root_node_info_frame_size

    i = 0
    # write to the data
    if jma_anim.has_dz:
        for info in jma_anim.root_node_info[: frame_ct]:
            pack_4_float_into(
                data, i, info.dx / 100, info.dy / 100, info.dz / 100, info.dyaw)
            i += frame_info_node_size

    elif jma_anim.has_dyaw:
        for info in jma_anim.root_node_info[: frame_ct]:
            pack_3_float_into(
                data, i, info.dx / 100, info.dy / 100, info.dyaw)
            i += frame_info_node_size

    elif jma_anim.has_dxdy:
        for info in jma_anim.root_node_info[: frame_ct]:
            pack_2_float_into(
                data, i, info.dx / 100, info.dy / 100)
            i += frame_info_node_size

    return data


def deserialize_frame_info(anim, include_extra_base_frame=False, endian=">"):
    i = 0
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = [JmaRootNodeState() for i in range(anim.frame_count)]
    frame_info = anim.frame_info.data

    # write to the data
    if "dz" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "4f")
        for f in range(anim.frame_count):
            dx, dy, dz, dyaw = unpack(frame_info, i)
            dx *= 100; dy *= 100; dz *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dz = dz; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.z  = z;  info.yaw  = yaw

            x += dx; y += dy; z += dz; yaw += dyaw
            i += 16

    elif "dyaw" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "3f")
        for f in range(anim.frame_count):
            dx, dy, dyaw = unpack(frame_info, i)
            dx *= 100; dy *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.yaw  = yaw

            x += dx; y += dy; yaw += dyaw
            i += 12

    elif "dx" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "2f")
        for f in range(anim.frame_count):
            dx, dy = unpack(frame_info, i)
            dx *= 100; dy *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy
            info.x  = x;  info.y  = y

            x += dx; y += dy
            i += 8

    if include_extra_base_frame and root_node_info:
        # duplicate the last frame and apply the change
        # that frame to the total change at that frame.
        last_root_node_info = deepcopy(root_node_info[-1])
        last_root_node_info.x += last_root_node_info.dx
        last_root_node_info.y += last_root_node_info.dy
        last_root_node_info.z += last_root_node_info.dz
        last_root_node_info.yaw += last_root_node_info.dyaw

        # no delta on last frame. zero it out
        last_root_node_info.dx = 0.0
        last_root_node_info.dy = 0.0
        last_root_node_info.dz = 0.0
        last_root_node_info.dyaw = 0.0

        root_node_info.append(last_root_node_info)

    return root_node_info


def serialize_default_data(jma_anim, endian=">"):
    data = bytearray(jma_anim.default_data_size)

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    pack_1_float_into = MethodType(pack_into, endian +  "f")
    pack_3_float_into = MethodType(pack_into, endian + "3f")
    pack_4_int16_into = MethodType(pack_into, endian + "4h")

    sqrt = math.sqrt

    i = 0
    # write to the data
    def_frames = jma_anim.frames[0]
    for n in range(jma_anim.node_count):
        node_state = def_frames[n]
        if not rot_flags[n]:
            # components are ones-signed
            qi = node_state.rot_i
            qj = node_state.rot_j
            qk = node_state.rot_k
            qw = node_state.rot_w
            nmag = qi**2 + qj**2 + qk**2 + qw**2
            if nmag:
                nmag = 32767.5 / sqrt(nmag)
                qi = int(qi*nmag)
                qj = int(qj*nmag)
                qk = int(qk*nmag)
                qw = int(qw*nmag)
            else:
                qi = qj = qk = 0
                qw = 32767

            pack_4_int16_into(data, i, qi, qj, qk, qw)
            i += 8

        if not trans_flags[n]:
            pack_3_float_into(data, i,
                node_state.pos_x / 100,
                node_state.pos_y / 100,
                node_state.pos_z / 100)
            i += 12

        if not scale_flags[n]:
            pack_1_float_into(data, i, node_state.scale)
            i += 4

    return data


def deserialize_default_data(anim, endian=">"):
    return _deserialize_frame_data(anim, True, (), endian)[0]


def serialize_frame_data(jma_anim, endian=">"):
    data = bytearray(jma_anim.frame_data_frame_size *
                     (jma_anim.frame_count - 1))

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    pack_1_float_into = MethodType(pack_into, endian +  "f")
    pack_3_float_into = MethodType(pack_into, endian + "3f")
    pack_4_int16_into = MethodType(pack_into, endian + "4h")

    is_overlay = jma_anim.anim_type == "overlay"

    sqrt = math.sqrt

    i = 0
    for f in range(jma_anim.frame_count):
        if not is_overlay and f + 1 == jma_anim.frame_count:
            # skip the last frame for non-overlays
            break
        elif f == 0 and is_overlay:
            # skip the first frame for overlays
            continue

        # write to the data
        for n in range(jma_anim.node_count):
            node_state = jma_anim.frames[f][n]

            if rot_flags[n]:
                # components are ones-signed
                qi = node_state.rot_i
                qj = node_state.rot_j
                qk = node_state.rot_k
                qw = node_state.rot_w
                nmag = qi**2 + qj**2 + qk**2 + qw**2
                if nmag:
                    nmag = 32767.5 / sqrt(nmag)
                    qi = int(qi*nmag)
                    qj = int(qj*nmag)
                    qk = int(qk*nmag)
                    qw = int(qw*nmag)
                else:
                    qi = qj = qk = 0
                    qw = 32767

                pack_4_int16_into(data, i, qi, qj, qk, qw)
                i += 8

            if trans_flags[n]:
                pack_3_float_into(data, i,
                    node_state.pos_x / 100,
                    node_state.pos_y / 100,
                    node_state.pos_z / 100)
                i += 12

            if scale_flags[n]:
                pack_1_float_into(data, i, node_state.scale)
                i += 4

    return data


def deserialize_frame_data(anim, def_node_states=None,
                           include_extra_base_frame=False, endian=">"):
    if def_node_states is None:
        def_node_states = deserialize_default_data(anim, endian)

    frame_data = _deserialize_frame_data(anim, False, def_node_states, endian)

    if not include_extra_base_frame:
        pass
    if anim.type.enum_name != "overlay":
        # duplicate the first frame to the last frame for non-overlays
        frame_data.append(deepcopy(frame_data[0]))
    else:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        frame_data.insert(0, def_node_states)

    return frame_data


def _deserialize_frame_data(anim, get_default_data, def_node_states, endian):
    unpack_trans = MethodType(unpack_from, endian + "3f")
    unpack_ijkw  = MethodType(unpack_from, endian + "4h")
    unpack_float = MethodType(unpack_from, endian +  "f")
    sqrt = math.sqrt

    rot_flags, trans_flags, scale_flags = get_anim_flags(anim)

    if get_default_data:
        store = False
        stored_frame_count = 1
        data = anim.default_data.data
    else:
        store = True
        stored_frame_count = anim.frame_count
        data = anim.frame_data.data

    all_node_states = [[JmaNodeState() for n in range(anim.node_count)]
                       for f in range(stored_frame_count)]

    if get_default_data:
        def_node_states = all_node_states[0]

    assert len(def_node_states) == anim.node_count

    i = 0
    for f in range(stored_frame_count):
        node_states = all_node_states[f]

        for n in range(anim.node_count):
            def_node_state = def_node_states[n]
            state = node_states[n]

            qi = qj = qk = x = y = z = 0.0
            qw = scale = 1.0
            if rot_flags[n] == store:
                qi, qj, qk, qw = unpack_ijkw(data, i)
                i += 8

                rot_len = qi**2 + qj**2 + qk**2 + qw**2
                if rot_len:
                    rot_len = 1 / sqrt(rot_len)
                    qi *= rot_len
                    qj *= rot_len
                    qk *= rot_len
                    qw *= rot_len
                else:
                    qi = qj = qk = 0.0
                    qw = 1.0
            else:
                qi = def_node_state.rot_i
                qj = def_node_state.rot_j
                qk = def_node_state.rot_k
                qw = def_node_state.rot_w

            if trans_flags[n] == store:
                x, y, z = unpack_trans(data, i)
                i += 12

                x *= 100
                y *= 100
                z *= 100
            else:
                x = def_node_state.pos_x
                y = def_node_state.pos_y
                z = def_node_state.pos_z

            if scale_flags[n] == store:
                scale = unpack_float(data, i)[0]
                i += 4
            else:
                scale = def_node_state.scale

            state.pos_x = x; state.pos_y = y; state.pos_z = z
            state.rot_i = qi; state.rot_j = qj
            state.rot_k = qk; state.rot_w = qw
            state.scale = scale

    return all_node_states


def serialize_compressed_frame_data(jma_anim):
    # make a compressed block to store the data for serialization
    comp_anim_block = compressed_frames_def.build()

    # local references for all these things to make access faster
    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    rot_keyframes   = comp_anim_block.rotation.keyframes
    trans_keyframes = comp_anim_block.translation.keyframes
    scale_keyframes = comp_anim_block.scale.keyframes

    rot_def_data   = comp_anim_block.rotation.default_data
    trans_def_data = comp_anim_block.translation.default_data
    scale_def_data = comp_anim_block.scale.default_data

    rot_keyframe_data   = comp_anim_block.rotation.keyframe_data
    trans_keyframe_data = comp_anim_block.translation.keyframe_data
    scale_keyframe_data = comp_anim_block.scale.keyframe_data

    rot_keyframes_by_nodes   = [[] for i in range(jma_anim.node_count)]
    trans_keyframes_by_nodes = [[] for i in range(jma_anim.node_count)]
    scale_keyframes_by_nodes = [[] for i in range(jma_anim.node_count)]

    # skip the first frame for overlays, otherwise the last frame
    last_keyframe = jma_anim.frame_count - 2
    skip_last_frame = (jma_anim.anim_type != "overlay")

    # calculate the keyframes and their counts based on the keyframes
    # in the jma_anim as well as the node transform flags
    for ni in range(jma_anim.node_count):
        # make sure to remove keyframe 0 since its stored in the default data
        if rot_flags[ni]:
            rot_keyframes_by_nodes[ni] = make_clean_keyframes_copy(
                jma_anim.rot_keyframes[ni],
                skip_last_frame, last_keyframe)

        if trans_flags[ni]:
            trans_keyframes_by_nodes[ni] = make_clean_keyframes_copy(
                jma_anim.trans_keyframes[ni],
                skip_last_frame, last_keyframe)

        if scale_flags[ni]:
            scale_keyframes_by_nodes[ni] = make_clean_keyframes_copy(
                jma_anim.scale_keyframes[ni],
                skip_last_frame, last_keyframe)

    # make the keyframe arrays big enough to fill in the keyframe numbers
    rot_keyframes.append(0)
    trans_keyframes.append(0)
    scale_keyframes.append(0)
    rot_keyframes   *= sum(len(kfs) for kfs in rot_keyframes_by_nodes)
    trans_keyframes *= sum(len(kfs) for kfs in trans_keyframes_by_nodes)
    scale_keyframes *= sum(len(kfs) for kfs in scale_keyframes_by_nodes)

    # make the default data arrays big enough to fill in the default data
    rot_def_data.append(0)
    trans_def_data.append(0)
    scale_def_data.append(0)
    rot_def_data   *= 3 * jma_anim.node_count
    trans_def_data *= 3 * jma_anim.node_count
    scale_def_data *= sum(bool(f) for f in scale_flags)

    # make the frame data arrays big enough to fill in the frame data
    rot_keyframe_data.append(0)
    trans_keyframe_data.append(0)
    scale_keyframe_data.append(0)
    rot_keyframe_data   *= 3 * len(rot_keyframes)
    trans_keyframe_data *= 3 * len(trans_keyframes)
    scale_keyframe_data *= len(scale_keyframes)


    comp_quat = compression.compress_quaternion48
    sqrt = math.sqrt

    ri = ti = si = 0
    def_ri = def_ti = def_si = 0

    def_frame = jma_anim.frames[0]

    for ni in range(jma_anim.node_count):
        curr_rot_kfs   = array(rot_keyframes.typecode,
                               rot_keyframes_by_nodes[ni])
        curr_trans_kfs = array(trans_keyframes.typecode,
                               trans_keyframes_by_nodes[ni])
        curr_scale_kfs = array(scale_keyframes.typecode,
                               scale_keyframes_by_nodes[ni])

        keyframes_sane = True
        if curr_rot_kfs:
            keyframes_sane &= last_keyframe in curr_rot_kfs

        if curr_trans_kfs:
            keyframes_sane &= last_keyframe in curr_trans_kfs

        if curr_scale_kfs:
            keyframes_sane &= last_keyframe in curr_scale_kfs

        assert keyframes_sane, (
            "Compressed animations must contain either no "
            "keyframes, or at least the last stored keyframe."
            )

        # copy the keyframe indices for this node into the block
        rot_keyframes[ri: ri + len(curr_rot_kfs)] = curr_rot_kfs
        trans_keyframes[ti: ti + len(curr_trans_kfs)] = curr_trans_kfs
        scale_keyframes[si: si + len(curr_scale_kfs)] = curr_scale_kfs

        # fill in the default data for this node
        def_node_state = def_frame[ni]

        w0, w1, w2 = comp_quat(
            def_node_state.rot_i, def_node_state.rot_j,
            def_node_state.rot_k, def_node_state.rot_w)
        rot_def_data[def_ri] = w0
        rot_def_data[def_ri + 1] = w1
        rot_def_data[def_ri + 2] = w2
        def_ri += 3

        trans_def_data[def_ti] = def_node_state.pos_x / 100
        trans_def_data[def_ti + 1] = def_node_state.pos_y / 100
        trans_def_data[def_ti + 2] = def_node_state.pos_z / 100
        def_ti += 3

        if scale_flags[ni]:
            # only write a default scale if scale is animated
            scale_def_data[def_si] = def_node_state.scale
            def_si += 1

        # fill in the keyframe data for this node
        for kfi in curr_rot_kfs:
            node_state = jma_anim.frames[kfi][ni]
            w0, w1, w2 = comp_quat(
                node_state.rot_i, node_state.rot_j,
                node_state.rot_k, node_state.rot_w)
            rot_keyframe_data[3*ri] = w0
            rot_keyframe_data[3*ri + 1] = w1
            rot_keyframe_data[3*ri + 2] = w2

            ri += 1

        for kfi in curr_trans_kfs:
            node_state = jma_anim.frames[kfi][ni]
            trans_keyframe_data[3*ti] = node_state.pos_x / 100
            trans_keyframe_data[3*ti + 1] = node_state.pos_y / 100
            trans_keyframe_data[3*ti + 2] = node_state.pos_z / 100
            ti += 1

        for kfi in curr_scale_kfs:
            scale_keyframe_data[si] = jma_anim.frames[kfi][ni].scale
            si += 1


    # setup the keyframe counts, offsets, data stream offsets
    calc_keyframe_header_data(
        comp_anim_block,
        [len(rot_keyframes_by_nodes[i]) for i in
         range(len(rot_keyframes_by_nodes)) if rot_flags[i]],

        [len(trans_keyframes_by_nodes[i]) for i in
         range(len(trans_keyframes_by_nodes)) if trans_flags[i]],

        [len(scale_keyframes_by_nodes[i]) for i in
         range(len(scale_keyframes_by_nodes)) if scale_flags[i]],
        )

    #print("RECOMP")
    #print(comp_anim_block)
    return comp_anim_block.serialize(calc_pointers=False)


def deserialize_compressed_frame_data(anim):
    rot_keyframes_by_nodes = []
    trans_keyframes_by_nodes = []
    scale_keyframes_by_nodes = []

    keyframes = (rot_keyframes_by_nodes,
                 trans_keyframes_by_nodes,
                 scale_keyframes_by_nodes)
    if not anim.flags.compressed_data:
        return keyframes, ()

    # make a bunch of frames we can fill in below
    frames = [[JmaNodeState() for n in range(anim.node_count)]
              for f in range(anim.frame_count + 1)]

    rot_flags, trans_flags, scale_flags = get_anim_flags(anim)

    comp_anim_block = compressed_frames_def.build(
        rawdata=anim.frame_data.STEPTREE,
        root_offset=anim.offset_to_compressed_data)
    #print("ORIG")
    #print(comp_anim_block)

    # get the keyframe counts and keyframe offsets
    rot_keyframe_headers   = [(v & 4095, v >> 12) for v in
                              comp_anim_block.rotation.keyframe_head]
    trans_keyframe_headers = [(v & 4095, v >> 12) for v in
                              comp_anim_block.translation.keyframe_head]
    scale_keyframe_headers = [(v & 4095, v >> 12) for v in
                              comp_anim_block.scale.keyframe_head]

    rot_keyframes   = comp_anim_block.rotation.keyframes
    trans_keyframes = comp_anim_block.translation.keyframes
    scale_keyframes = comp_anim_block.scale.keyframes

    rot_def_data   = comp_anim_block.rotation.default_data
    trans_def_data = comp_anim_block.translation.default_data
    scale_def_data = comp_anim_block.scale.default_data

    rot_keyframe_data   = comp_anim_block.rotation.keyframe_data
    trans_keyframe_data = comp_anim_block.translation.keyframe_data
    scale_keyframe_data = comp_anim_block.scale.keyframe_data

    decomp_quat = compression.decompress_quaternion48
    blend_trans = matrices.lerp_blend_vectors
    blend_quats = matrices.nlerp_blend_quaternions
    sqrt = math.sqrt

    ri = ti = si = 0
    for ni in range(anim.node_count):
        rot_kf_ct  = trans_kf_ct  = scale_kf_ct  = 0
        rot_kf_off = trans_kf_off = scale_kf_off = 0

        rot_def = decomp_quat(*rot_def_data[3 * ni: 3 * (ni + 1)])
        trans_def = trans_def_data[3 * ni: 3 * (ni + 1)]
        scale_def = 1.0

        if rot_flags[ni]:
            rot_kf_ct, rot_kf_off = rot_keyframe_headers[ri]
            ri += 1

        if trans_flags[ni]:
            trans_kf_ct, trans_kf_off = trans_keyframe_headers[ti]
            ti += 1

        if scale_flags[ni]:
            scale_kf_ct, scale_kf_off = scale_keyframe_headers[si]
            scale_def = scale_def_data[si]
            si += 1

        # add this nodes keyframes to the keyframe lists in the jma_anim
        for kf_ct, kf_off, all_kfs, kfs_by_nodes in (
                (rot_kf_ct, rot_kf_off, rot_keyframes,
                 rot_keyframes_by_nodes),
                (trans_kf_ct, trans_kf_off, trans_keyframes,
                 trans_keyframes_by_nodes),
                (scale_kf_ct, scale_kf_off, scale_keyframes,
                 scale_keyframes_by_nodes)):
            kfs_by_nodes.append(list(all_kfs[kf_off: kf_off + kf_ct]))


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
            scale_first = scale_keyframe_data[scale_kf_off]
            scale_last  = scale_keyframe_data[scale_kf_off + scale_kf_ct - 1]

        for fi in range(anim.frame_count):
            node_frame = frames[fi][ni]

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
                    scale = scale_keyframes[kf_i]
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
                node_frame.rot_i = i * nmag
                node_frame.rot_j = j * nmag
                node_frame.rot_k = k * nmag
                node_frame.rot_w = w * nmag

            node_frame.pos_x = x * 100
            node_frame.pos_y = y * 100
            node_frame.pos_z = z * 100

            node_frame.scale = scale

    if anim.type.enum_name != "overlay":
        # duplicate the first frame to the last frame for non-overlays
        frames[-1] = deepcopy(frames[0])

    return keyframes, frames


def get_keyframe_index_of_frame(frame, keyframes,
                                keyframe_count=None, offset=0):
    if keyframe_count is None:
        keyframe_count = len(keyframes) - offset

    # TODO: make this more efficent using a binary search
    for i in range(offset, offset + keyframe_count - 1):
        if keyframes[i] <= frame and frame < keyframes[i + 1]:
            return i

    raise ValueError(
        "No keyframes pairs containing frame %s" % frame)


def get_anim_flags(anim):
    rot_flags   = anim.rot_flags0   | (anim.rot_flags1 << 32)
    trans_flags = anim.trans_flags0 | (anim.trans_flags1 << 32)
    scale_flags = anim.scale_flags0 | (anim.scale_flags1 << 32)

    rot_flags   = [bool(rot_flags   & (1 << i)) for i in range(anim.node_count)]
    trans_flags = [bool(trans_flags & (1 << i)) for i in range(anim.node_count)]
    scale_flags = [bool(scale_flags & (1 << i)) for i in range(anim.node_count)]
    return rot_flags, trans_flags, scale_flags


def make_clean_keyframes_copy(keyframes, skip_last_frame, last_keyframe):
    kfs = list(keyframes)
    if not kfs:
        return kfs

    if kfs[0] == 0:
        kfs.pop(0)

    if kfs and skip_last_frame and kfs[-1] == last_keyframe + 1:
        kfs.pop(-1)

    return kfs


def calc_keyframe_header_data(comp_anim_block, rot_keyframe_counts,
                              trans_keyframe_counts, scale_keyframe_counts):

    for keyframe_counts, keyframe_header in (
            (rot_keyframe_counts,   comp_anim_block.rotation.keyframe_head),
            (trans_keyframe_counts, comp_anim_block.translation.keyframe_head),
            (scale_keyframe_counts, comp_anim_block.scale.keyframe_head)):
        if not keyframe_counts:
            pass
        elif max(keyframe_counts) >= 4096:
            raise ValueError(
                "Too many keyframes to compress per node. Must be < 4096, "
                "but got %s" % max(keyframe_counts))
        elif sum(keyframe_counts) >= 1048576:
            raise ValueError(
                "Too many keyframes to compress in total. Must be < 1048576 "
                "but got %s" % sum(keyframe_counts))

        keyframe_header.append(0)
        keyframe_header *= len(keyframe_counts)

        off = i = 0
        for ct in keyframe_counts:
            keyframe_header[i] = ct | (off << 12)
            off += ct
            i += 1

    # setup the data stream offsets
    off = None
    for offs, data in (
            (comp_anim_block.rotation_offsets, comp_anim_block.rotation),
            (comp_anim_block.translation_offsets, comp_anim_block.translation),
            (comp_anim_block.scale_offsets, comp_anim_block.scale)):
        for i in range(4):
            if off is None:
                off = 44
            else:
                offs[i] = off

            off += len(data[i]) * data[i].itemsize
