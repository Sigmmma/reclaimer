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

from reclaimer.jm import constants as const
from reclaimer.jm.jma import JmaRootNodeState, JmaNodeState
from reclaimer.animation.structs import compressed_frames_def
from reclaimer.animation import util
from reclaimer.util import compression
from reclaimer.util import matrices

__all__ = (
    "deserialize", "get_frame_from_keyframe_data",
    "deserialize_uncomp_frame_data", "deserialize_frame_info", 
    "deserialize_comp_frame_data",   "deserialize_default_data",
      "serialize_uncomp_frame_data",   "serialize_frame_info",   
      "serialize_comp_frame_data",     "serialize_default_data",
    )


def deserialize(anim, endian=">", pos_scale=1.0):
    if anim.flags.compressed_data:
        # decompress compressed animations
        kfs, frames = deserialize_comp_frame_data(anim, False, True, pos_scale)
    else:
        # create the node states from the frame_data and default_data
        frames = deserialize_uncomp_frame_data(anim, None, True, endian, pos_scale)
        kfs = [], [], []

    return kfs, frames


def serialize_frame_info(jma_anim, endian=">", pos_scale=1.0):
    size  = jma_anim.root_node_info_frame_size
    count = jma_anim.frame_count - 1
    infos = jma_anim.root_node_info[: count]
    data  = bytearray(size * count)
    if not size:
        return data

    pack = MethodType(pack_into, f"{endian}{size//4}f")

    # write to the data
    pos_scale /= const.SCALE_INTERNAL_TO_JMA
    if jma_anim.has_dz:
        for i, info in enumerate(infos):
            pack(data, i*size, info.dx*pos_scale, info.dy*pos_scale,
                 info.dz*pos_scale, info.dyaw)

    elif jma_anim.has_dyaw:
        for i, info in enumerate(infos):
            pack(data, i*size, info.dx*pos_scale, info.dy*pos_scale, info.dyaw)

    elif jma_anim.has_dxdy:
        for i, info in enumerate(infos):
            pack(data, i*size, info.dx*pos_scale, info.dy*pos_scale)

    return data


def deserialize_frame_info(anim, include_extra_base_frame=False,
                           endian=">", pos_scale=1.0):
    i = 0
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = [JmaRootNodeState() for i in range(anim.frame_count)]
    frame_info = anim.frame_info.data
    pos_scale *= const.SCALE_INTERNAL_TO_JMA

    # write to the data
    if "dz" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "4f")
        for f in range(anim.frame_count):
            dx, dy, dz, dyaw = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale; dz *= pos_scale

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dz = dz; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.z  = z;  info.yaw  = yaw

            x += dx; y += dy; z += dz; yaw += dyaw
            i += 16

    elif "dyaw" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "3f")
        for f in range(anim.frame_count):
            dx, dy, dyaw = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.yaw  = yaw

            x += dx; y += dy; yaw += dyaw
            i += 12

    elif "dx" in anim.frame_info_type.enum_name:
        unpack = MethodType(unpack_from, endian + "2f")
        for f in range(anim.frame_count):
            dx, dy = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale

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


def deserialize_default_data(anim, endian=">", pos_scale=1.0):
    if anim.flags.compressed_data:
        _, frames = deserialize_comp_frame_data(anim, True, True, pos_scale)
    else:
        frames = _deserialize_uncomp_frame_data(anim, True, (), endian, pos_scale)

    return frames[0]


def deserialize_comp_frame_data(anim, get_default_data=False,
                                include_extra_base_frame=True, pos_scale=1.0):
    r_kfs_by_nodes = []
    t_kfs_by_nodes = []
    s_kfs_by_nodes = []

    keyframes = (r_kfs_by_nodes, t_kfs_by_nodes, s_kfs_by_nodes)
    if not anim.flags.compressed_data:
        return keyframes, ()

    sqrt        = math.sqrt
    decomp_quat = compression.decompress_quaternion48
    blend_trans = matrices.lerp_blend_vectors
    blend_quats = matrices.nlerp_blend_quaternions
    blend_scale = lambda scale_0, scale_1, ratio: (
        scale_0 * (1 - ratio) + scale_1 * ratio
        )
    pos_scale  *= const.SCALE_INTERNAL_TO_JMA

    frame_count = 1 if get_default_data else anim.frame_count

    # make a bunch of frames we can fill in below
    frames = [[JmaNodeState() for n in range(anim.node_count)]
              for f in range(frame_count)]

    r_flags, t_flags, s_flags = util.get_anim_flags(anim)

    try:
        # parse the compressed animation block
        cab = compressed_frames_def.build(
            rawdata=anim.frame_data.STEPTREE,
            root_offset=anim.offset_to_compressed_data)
    except Exception:
        cab = None

    if not cab:
        raise Exception("Failed to parse compressed animations "
                        "block. It may be corrupt.")

    # shorthands
    cab_r, cab_t, cab_s = cab.rotation, cab.translation, cab.scale

    # get the keyframe counts and keyframe offsets
    r_kf_headers, t_kf_headers, s_kf_headers = [
        [(v&4095, v>>12) for v in block.keyframe_head]
        for block in (cab_r, cab_t, cab_s)
        ]

    r_kfs, t_kfs, s_kfs = cab_r.keyframes, cab_t.keyframes, cab_s.keyframes

    r_ddata, r_fdata = cab_r.default_data, cab_r.keyframe_data
    t_ddata, t_fdata = cab_t.default_data, cab_t.keyframe_data
    s_ddata, s_fdata = cab_s.default_data, cab_s.keyframe_data

    def_node_states = [JmaNodeState() for n in range(anim.node_count)]

    # convert keyframe data into lists of component sets
    r_fdata = [decomp_quat(*r_fdata[i: i+3])
               for i in range(0, len(r_fdata), 3)]
    t_fdata = [t_fdata[i: i+3] for i in range(0, len(t_fdata), 3)]

    is_overlay = anim.type.enum_name == "overlay"
    ri = ti = si = 0
    for ni, def_ns in enumerate(def_node_states):
        r_def = decomp_quat(*r_ddata[3*ni: 3*(ni + 1)])
        t_def = t_ddata[3*ni: 3*(ni + 1)]
        s_def = s_ddata[si] if s_flags[ni] else 1.0

        def_ns.rot_i = r_def[0]
        def_ns.rot_j = r_def[1]
        def_ns.rot_k = r_def[2]
        def_ns.rot_w = r_def[3]

        def_ns.pos_x = t_def[0] * pos_scale
        def_ns.pos_y = t_def[1] * pos_scale
        def_ns.pos_z = t_def[2] * pos_scale

        def_ns.scale = s_def

        ri, r_kf_ct, r_kf_off = ((ri+1, *r_kf_headers[ri])
                                 if r_flags[ni] else (ri, 0, 0))
        ti, t_kf_ct, t_kf_off = ((ti+1, *t_kf_headers[ti])
                                 if t_flags[ni] else (ti, 0, 0))
        si, s_kf_ct, s_kf_off = ((si+1, *s_kf_headers[si])
                                 if s_flags[ni] else (si, 0, 0))

        # add this nodes keyframes to the keyframe lists in the jma_anim
        for kf_ct, kf_off, all_kfs, kfs_by_nodes in (
                (r_kf_ct, r_kf_off, r_kfs, r_kfs_by_nodes),
                (t_kf_ct, t_kf_off, t_kfs, t_kfs_by_nodes),
                (s_kf_ct, s_kf_off, s_kfs, s_kfs_by_nodes)):
            kfs_by_nodes.append(list(all_kfs[kf_off: kf_off + kf_ct]))

        r_kf_end = r_kf_off + r_kf_ct - 1
        t_kf_end = t_kf_off + t_kf_ct - 1
        s_kf_end = s_kf_off + s_kf_ct - 1
        for fi in range(frame_count):
            node_frame = frames[fi][ni]

            # decompress rotation
            qi, qj, qk, qw = get_frame_from_keyframe_data(
                fi, r_kf_off, r_kf_end, r_kfs,
                r_def, r_fdata, blend_quats
                )
            mag         = qi**2 + qj**2 + qk**2 + qw**2
            qw, q_scale = (qw, 1/sqrt(mag)) if mag else (1.0, 1)

            node_frame.rot_i = qi * q_scale
            node_frame.rot_j = qj * q_scale
            node_frame.rot_k = qk * q_scale
            node_frame.rot_w = qw * q_scale

            # decompress position
            x, y, z = get_frame_from_keyframe_data(
                fi, t_kf_off, t_kf_end, t_kfs,
                t_def, t_fdata, blend_trans
                )
            node_frame.pos_x = x * pos_scale
            node_frame.pos_y = y * pos_scale
            node_frame.pos_z = z * pos_scale

            # decompress scale
            node_frame.scale = get_frame_from_keyframe_data(
                fi, s_kf_off, s_kf_end, s_kfs,
                s_def, s_fdata, blend_scale
                )

    if include_extra_base_frame and not get_default_data:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        is_overlay and frames.insert(0, def_node_states)

        # non-overlays duplicate the first frame to the last frame
        is_overlay or  frames.append(deepcopy(frames[0]))

    return keyframes, frames


def deserialize_uncomp_frame_data(
        anim, def_node_states=None, include_extra_base_frame=True,
        endian=">", pos_scale=1.0
        ):
    is_overlay = anim.type.enum_name == "overlay"
    if def_node_states is None:
        def_node_states = _deserialize_uncomp_frame_data(
            anim, True, (), endian, pos_scale
            )[0]

    frame_data = _deserialize_uncomp_frame_data(
        anim, False, def_node_states, endian, pos_scale
        )

    if include_extra_base_frame:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        is_overlay and frame_data.insert(0, def_node_states)

        # non-overlays duplicate the first frame to the last frame
        is_overlay or  frame_data.append(deepcopy(frame_data[0]))

    return frame_data


def _deserialize_uncomp_frame_data(
        anim, get_default_data=False, def_node_states=(),
        endian=">", pos_scale=1.0
        ):
    unpack_rot   = MethodType(unpack_from, endian + "4h")
    unpack_trans = MethodType(unpack_from, endian + "3f")
    unpack_scale = MethodType(unpack_from, endian +  "f")
    sqrt         = math.sqrt
    pos_scale   *= const.SCALE_INTERNAL_TO_JMA

    r_flags, t_flags, s_flags = util.get_anim_flags(anim)
    r_incs = [8  * (f != get_default_data) for f in r_flags]
    t_incs = [12 * (f != get_default_data) for f in t_flags]
    s_incs = [4  * (f != get_default_data) for f in s_flags]

    data, frame_count = ((anim.default_data.data, 1) if get_default_data else
                         (anim.frame_data.data, anim.frame_count))

    all_node_states = [[JmaNodeState() for n in range(anim.node_count)]
                       for f in range(frame_count)]

    if get_default_data or not def_node_states:
        def_node_states = all_node_states[0]

    assert len(def_node_states) == anim.node_count

    i = 0
    for f, node_states in enumerate(all_node_states):
        for r_inc, t_inc, s_inc, def_ns, ns in zip(
                r_incs, t_incs, s_incs,
                def_node_states, node_states
                ):
            if r_inc:
                qi, qj, qk, qw = unpack_rot(data, i)

                mag = qi**2 + qj**2 + qk**2 + qw**2
                qw, q_scale    = (qw, 1/sqrt(mag)) if mag else (1.0, 1)

                qi, qj, qk, qw = (qi*q_scale, qj*q_scale,
                                  qk*q_scale, qw*q_scale)
                i  += r_inc
            else:
                qi, qj, qk, qw = (def_ns.rot_i, def_ns.rot_j,
                                  def_ns.rot_k, def_ns.rot_w)

            x, y, z = (
                (v*pos_scale for v in unpack_trans(data, i)) if t_inc else
                (def_ns.pos_x, def_ns.pos_y, def_ns.pos_z)
                )
            i += t_inc

            s = unpack_scale(data, i)[0] if s_inc else def_ns.scale
            i += s_inc

            ns.rot_i = qi
            ns.rot_j = qj
            ns.rot_k = qk
            ns.rot_w = qw
            ns.pos_x = x
            ns.pos_y = y
            ns.pos_z = z
            ns.scale = s

    return all_node_states


def serialize_default_data(jma_anim, endian=">", pos_scale=1.0):
    return _serialize_uncomp_frame_data(jma_anim, endian, False, pos_scale)


def serialize_comp_frame_data(jma_anim, pos_scale=1.0):
    # make a comp_anim_block to store the data for serialization
    cab = compressed_frames_def.build()

    # shorthands
    cab_r, cab_t, cab_s = cab.rotation, cab.translation, cab.scale

    # local references for all these things to make access faster
    kfs_arrs   = (cab_r.keyframes,     cab_t.keyframes,     cab_s.keyframes)
    ddata_arrs = (cab_r.default_data,  cab_t.default_data,  cab_s.default_data)
    fdata_arrs = (cab_r.keyframe_data, cab_t.keyframe_data, cab_s.keyframe_data)
    nodes_kfs  = [[] for xform_type in range(3)]

    r_ddata,     t_ddata,     s_ddata     = ddata_arrs
    r_fdata,     t_fdata,     s_fdata     = fdata_arrs
    r_nodes_kfs, t_nodes_kfs, s_nodes_kfs = nodes_kfs

    nodes_flags = jma_anim.rot_flags, jma_anim.trans_flags, jma_anim.scale_flags
    jma_nodes_kfs = (jma_anim.rot_keyframes, jma_anim.trans_keyframes,
                     jma_anim.scale_keyframes)

    # calculate the keyframes and their counts based on the keyframes
    # in the jma_anim as well as the node transform flags
    for flags, xf_kfs, jma_xf_kfs in zip(nodes_flags, nodes_kfs, jma_nodes_kfs):
        for flag, jma_kfs in zip(flags, jma_xf_kfs):
            xf_kfs.append([])
            kfs = xf_kfs[-1]

            # NOTE: stubbs may do some stuff here that prevents sorting
            #       the keyframes, and since this code is used for stubbs
            #       as well we'll avoid breaking anything with it.
            flag and kfs.extend(jma_kfs)

            # remove the 0th keyframe since its stored in the default data
            kfs and (kfs[0] or kfs.pop(0))

            # skip the first frame for overlays, otherwise the last frame
            if kfs and jma_anim.last_frame_loops_to_first:
                kfs[-1] + 1 < jma_anim.frame_count or kfs.pop(-1)

            assert not kfs or kfs[-1] == jma_anim.frame_count-2, (
                "Compressed animations must contain either no "
                "keyframes, or at least the last stored keyframe."
                )

    # make the keyframe arrays big enough to fill in the keyframe numbers
    [arr.extend(0 for i in range(sum(len(n_kfs) for n_kfs in xf_kfs)))
     for arr, xf_kfs in zip(kfs_arrs, nodes_kfs)]

    # make the default data arrays big enough to fill in the default data
    [arr.extend(0 for i in range(ct)) for arr, ct in
     zip(ddata_arrs, (3*jma_anim.node_count, 3*jma_anim.node_count,
                      sum(bool(f) for f in jma_anim.scale_flags)))]

    # make the frame data arrays big enough to fill in the frame data
    [arr.extend(0 for i in range(len(kfs)*width)) for arr, kfs, width in
     zip(fdata_arrs, kfs_arrs, (3, 3, 1))]


    sqrt, comp_quat = math.sqrt, compression.compress_quaternion48
    pos_scale /= const.SCALE_INTERNAL_TO_JMA

    # counters to keep track of the default data and frame data
    # index we're writing into in the compressed frame data block
    ri = ti = si = def_ri = def_ti = def_si = 0
    for ni, d_state in enumerate(jma_anim.frames[0]):
        has_scale = bool(jma_anim.scale_flags[ni])

        # copy the keyframe indices for this node into the block
        for kfs, xf_kfs, ki in zip(kfs_arrs, nodes_kfs, (ri, ti, si)):
            kfs[ki: ki + len(xf_kfs[ni])] = array(kfs.typecode, xf_kfs[ni])

        # fill in the default data for this node
        for i, val in enumerate(comp_quat(d_state.rot_i, d_state.rot_j,
                                          d_state.rot_k, d_state.rot_w),
                                def_ri*3):
            r_ddata[i] = val

        for i, val in enumerate((d_state.pos_x, d_state.pos_y, d_state.pos_z),
                                def_ti*3):
            t_ddata[i] = val*pos_scale

        # only write a default scale if scale is animated
        if has_scale:
            s_ddata[def_si] = d_state.scale

        # fill in the keyframe data for this node
        for i, ns in enumerate((jma_anim.frames[kfi][ni]
                                for kfi in r_nodes_kfs[ni]), ri):
            for j, val in enumerate(comp_quat(ns.rot_i, ns.rot_j,
                                              ns.rot_k, ns.rot_w), i*3):
                r_fdata[j] = val

        for i, ns in enumerate((jma_anim.frames[kfi][ni]
                                for kfi in t_nodes_kfs[ni]), ti):
            for j, val in enumerate((ns.pos_x, ns.pos_y, ns.pos_z), i*3):
                t_fdata[j] = val*pos_scale

        for i, ns in enumerate((jma_anim.frames[kfi][ni]
                                for kfi in s_nodes_kfs[ni]), si):
            s_fdata[i] = ns.scale

        ri, def_ri = ri + len(r_nodes_kfs[ni]), def_ri + 1
        ti, def_ti = ti + len(t_nodes_kfs[ni]), def_ti + 1
        si, def_si = si + len(s_nodes_kfs[ni]), def_si + has_scale

    # setup the keyframe counts, offsets, data stream offsets
    calc_keyframe_header_data(cab, *(
        [len(kfs) for i, kfs in enumerate(node_kfs) if flags[i]]
        for node_kfs, flags in zip(nodes_kfs, nodes_flags)
        ))

    return cab.serialize(calc_pointers=False)


def serialize_uncomp_frame_data(jma_anim, endian=">", pos_scale=1.0):
    return _serialize_uncomp_frame_data(jma_anim, endian, True, pos_scale)


def _serialize_uncomp_frame_data(jma_anim, endian, write_flag, pos_scale=1.0):
    sqrt = math.sqrt
    pos_scale /= const.SCALE_INTERNAL_TO_JMA

    # combining the write-pointer increments with the flags
    r_incs = [8  * (f == write_flag) for f in jma_anim.rot_flags]
    t_incs = [12 * (f == write_flag) for f in jma_anim.trans_flags]
    s_incs = [4  * (f == write_flag) for f in jma_anim.scale_flags]

    pack_rot   = MethodType(pack_into, endian + "4h")
    pack_trans = MethodType(pack_into, endian + "3f")
    pack_scale = MethodType(pack_into, endian +  "f")

    # we skip the first frame for the frame_data in overlays, and the
    # last for non-overlays. for overlay default_data, we use frame 0
    frame_start = 1 if jma_anim.is_overlay and write_flag else 0

    # only write frame 0 if writing default_data(write_flag == False)
    frame_count = jma_anim.frame_count - 1 if write_flag else 1
    frame_size  = (jma_anim.frame_data_frame_size if write_flag else
                   jma_anim.default_data_size)

    i, data = 0, bytearray(frame_size * frame_count)
    for frame in jma_anim.frames[frame_start: frame_start + frame_count]:
        # write the data
        for r_inc, t_inc, s_inc, ns in zip(r_incs, t_incs, s_incs, frame):
            if r_inc:
                # components are ones-signed
                qi, qj, qk, qw = ns.rot_i, ns.rot_j, ns.rot_k, ns.rot_w
                mag = sqrt(qi**2 + qj**2 + qk**2 + qw**2)
                q_scale = (32767.5 / mag) if mag else 1

                qi, qj, qk, qw = (
                    int(qi*q_scale), int(qj*q_scale),
                    int(qk*q_scale), int(qw*q_scale)
                    ) if mag else (0, 0, 0, 0x7Fff)

                pack_rot(data, i, qi, qj, qk, qw)
                i += r_inc

            if t_inc:
                x, y, z = ns.pos_x, ns.pos_y, ns.pos_z
                pack_trans(data, i, x*pos_scale, y*pos_scale, z*pos_scale)
                i += t_inc

            s_inc and pack_scale(data, i, ns.scale)
            i += s_inc

    return data


def get_frame_from_keyframe_data(
        frame_index, keyframes_start, keyframes_end, keyframes,
        frame_0, keyframe_data, blender
        ):
    if keyframes_start >= keyframes_end or frame_index == 0:
        # first frame OR only default data stored for this node
        return frame_0

    last_kf  = keyframes[keyframes_end]
    if frame_index == last_kf:
        # frame is the last keyframe. repeat it to the end
        return keyframe_data[keyframes_end]

    first_kf = keyframes[keyframes_start]
    if frame_index < first_kf:
        # frame is before the first stored keyframe.
        # blend from default data to first keyframe.
        frame_b = keyframe_data[keyframes_start]
        ratio   = frame_index / first_kf
        return blender(frame_0, frame_b, ratio)

    # frame is at/past the first stored keyframe.
    # don't need to use default data at all.

    # find the keyframes this frame is between
    for kf_i in range(keyframes_start, keyframes_end):
        # TODO: make this more efficent using a binary search
        if (keyframes[kf_i]  <= frame_index and
            keyframes[kf_i+1] > frame_index):
            break

        # NOTE: unless the animation is broken, this will never
        #       be hit. commenting out for speed, as there's not
        #       really a good reason to keep it in
        #elif kf_i == keyframes_end:
        #    raise ValueError(f"No keyframes pairs containing frame {frame_index}")

    frame_a = keyframe_data[kf_i]
    if frame_index == keyframes[kf_i]:
        # this keyframe is the frame we want.
        # no blending required
        return frame_a

    frame_b = keyframe_data[kf_i+1]
    ratio   = ((      frame_index - keyframes[kf_i]) /
               (keyframes[kf_i+1] - keyframes[kf_i]))

    return blender(frame_a, frame_b, ratio)


def calc_keyframe_header_data(comp_anim_block, rot_kf_counts,
                              trans_kf_counts, scale_kf_counts):
    cab = comp_anim_block
    rot, trans, scale = cab.rotation, cab.translation, cab.scale
    for kf_counts, kf_header in ((rot_kf_counts,   rot.keyframe_head),
                                 (trans_kf_counts, trans.keyframe_head),
                                 (scale_kf_counts, scale.keyframe_head)):
        if not kf_counts:
            pass
        elif max(kf_counts) >= 4096:
            raise ValueError(
                "Too many keyframes to compress per node. Must be < 4096, "
                "but got %s" % max(kf_counts))
        elif sum(kf_counts) >= 1048576:
            raise ValueError(
                "Too many keyframes to compress in total. Must be < 1048576 "
                "but got %s" % sum(kf_counts))

        kf_header.append(0)
        kf_header *= len(kf_counts)

        off = 0
        for i, ct in enumerate(kf_counts):
            kf_header[i] = ct | (off << 12)
            off += ct

    off = 44
    # setup the data stream offsets
    for offs, data in ((cab.rotation_offsets,    rot),
                       (cab.translation_offsets, trans),
                       (cab.scale_offsets,       scale)):
        for i, arr in enumerate(data):
            offs[i], off = off, off+len(arr)*arr.itemsize
