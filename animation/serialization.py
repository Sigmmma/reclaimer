import math

from struct import Struct as PyStruct
from reclaimer.animation.jma import JmaRootNodeState, JmaNodeState

__all__ = ("serialize_frame_info", "deserialize_frame_info",
           "serialize_default_data", "deserialize_default_data",
           "serialize_frame_data", "deserialize_frame_data" )


def serialize_frame_info(jma_anim, endian=">"):
    frame_ct = jma_anim.frame_count - 1
    data = bytearray(jma_anim.root_node_info_frame_size * frame_ct)

    pack_2_float_into = PyStruct(endian + "2f").pack_into
    pack_3_float_into = PyStruct(endian + "3f").pack_into
    pack_4_float_into = PyStruct(endian + "4f").pack_into
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


def deserialize_frame_info(anim, endian=">"):
    i = 0
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = [JmaRootNodeState() for i in range(anim.frame_count)]
    frame_info = anim.frame_info.data

    # write to the data
    if "dz" in anim.frame_info_type.enum_name:
        unpack = PyStruct(endian + "4f").unpack_from
        for f in range(anim.frame_count):
            dx, dy, dz, dyaw = unpack(frame_info, i)
            dx *= 100; dy *= 100; dz *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dz = dz; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.z  = z;  info.yaw  = yaw

            x += dx; y += dy; z += dz; yaw += dyaw
            i += 16

    elif "dyaw" in anim.frame_info_type.enum_name:
        unpack = PyStruct(endian + "3f").unpack_from
        for f in range(anim.frame_count):
            dx, dy, dyaw = unpack(frame_info, i)
            dx *= 100; dy *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.yaw  = yaw

            x += dx; y += dy; yaw += dyaw
            i += 12

    elif "dx" in anim.frame_info_type.enum_name:
        unpack = PyStruct(endian + "2f").unpack_from
        for f in range(anim.frame_count):
            dx, dy = unpack(frame_info, i)
            dx *= 100; dy *= 100

            info = root_node_info[f]
            info.dx = dx; info.dy = dy
            info.x  = x;  info.y  = y

            x += dx; y += dy
            i += 8

    return root_node_info


def serialize_default_data(jma_anim, endian=">"):
    data = bytearray(jma_anim.default_data_size)

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    pack_1_float_into = PyStruct(endian +  "f").pack_into
    pack_3_float_into = PyStruct(endian + "3f").pack_into
    pack_4_int16_into = PyStruct(endian + "4h").pack_into

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

    pack_1_float_into  = PyStruct(endian +  "f").pack_into
    pack_3_float_into  = PyStruct(endian + "3f").pack_into
    pack_4_int16_into = PyStruct(endian + "4h").pack_into

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


def deserialize_frame_data(anim, def_node_states=None, endian=">"):
    if def_node_states is None:
        def_node_states = deserialize_default_data(anim, endian)
    return _deserialize_frame_data(anim, False, def_node_states, endian)


def _deserialize_frame_data(anim, get_default_data, def_node_states, endian):
    unpack_trans = PyStruct(endian + "3f").unpack_from
    unpack_ijkw  = PyStruct(endian + "4h").unpack_from
    unpack_float = PyStruct(endian +  "f").unpack_from
    sqrt = math.sqrt

    rot_flags   = anim.rot_flags0   | (anim.rot_flags1 << 32)
    trans_flags = anim.trans_flags0 | (anim.trans_flags1 << 32)
    scale_flags = anim.scale_flags0 | (anim.scale_flags1 << 32)

    rot_flags   = [bool(rot_flags   & (1 << i)) for i in range(anim.node_count)]
    trans_flags = [bool(trans_flags & (1 << i)) for i in range(anim.node_count)]
    scale_flags = [bool(scale_flags & (1 << i)) for i in range(anim.node_count)]

    if get_default_data:
        rot_flags   = [not v for v in rot_flags]
        trans_flags = [not v for v in trans_flags]
        scale_flags = [not v for v in scale_flags]
        stored_frame_count = 1
        data = anim.default_data.data
    else:
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
            if rot_flags[n]:
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

            if trans_flags[n]:
                x, y, z = unpack_trans(data, i)
                i += 12

                x *= 100
                y *= 100
                z *= 100
            else:
                x = def_node_state.pos_x
                y = def_node_state.pos_y
                z = def_node_state.pos_z

            if scale_flags[n]:
                scale = unpack_float(data, i)[0]
                i += 4
            else:
                scale = def_node_state.scale

            state.pos_x = x; state.pos_y = y; state.pos_z = z
            state.rot_i = qi; state.rot_j = qj
            state.rot_k = qk; state.rot_w = qw
            state.scale = scale

    return all_node_states
