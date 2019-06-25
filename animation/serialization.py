import math

from struct import Struct as PyStruct


def serialize_frame_info(anim, jma_anim):
    frame_info   = anim.frame_info.STEPTREE

    has_dxdy = "dx"   in jma_anim.frame_info_type
    has_dz   = "dz"   in jma_anim.frame_info_type
    has_dyaw = "dyaw" in jma_anim.frame_info_type
    if not(has_dxdy or has_dz or has_dyaw) or jma_anim.anim_type == "overlay":
        return

    pack_2_float_into = PyStruct(">2f").pack_into
    pack_3_float_into = PyStruct(">3f").pack_into
    pack_4_float_into = PyStruct(">4f").pack_into

    i = 0
    for f in range(jma_anim.frame_count - 1):
        # write to the frame_info
        info = jma_anim.root_node_info[f]
        if has_dz:
            pack_4_float_into(
                frame_info, i, info.dx / 100, info.dy / 100, info.dz / 100, info.dyaw)
        elif has_dyaw:
            pack_3_float_into(
                frame_info, i, info.dx / 100, info.dy / 100, info.dyaw)
        elif has_dxdy:
            pack_2_float_into(
                frame_info, i, info.dx / 100, info.dy / 100)

        i += frame_info_node_size


def serialize_uncompressed_frame_data(anim, jma_anim):
    default_data = anim.default_data.STEPTREE
    frame_data   = anim.frame_data.STEPTREE

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    pack_1_float_into = PyStruct(">f").pack_into
    pack_3_float_into = PyStruct(">3f").pack_into
    pack_4_uint16_into = PyStruct(">4H").pack_into

    is_overlay = jma_anim.anim_type == "overlay"

    sqrt = math.sqrt

    i = j = 0
    for f in range(jma_anim.frame_count):
        if not is_overlay and f + 1 == jma_anim.frame_count:
            # skip the last frame for non-overlays
            break

        # write to the default_data
        if f == 0:
            for n in range(anim.node_count):
                node_state = jma_anim.frames[f][n]
                if not rot_flags[n]:
                    # components are ones-signed
                    qi = node_state.rot_i
                    qj = node_state.rot_j
                    qk = node_state.rot_k
                    qw = node_state.rot_w
                    nmag = qi**2 + qj**2 + qk**2 + qw**2
                    if nmag:
                        nmag = sqrt(nmag) * 32767.5
                        qi = int(qi*nmag) % 65535
                        qj = int(qj*nmag) % 65535
                        qk = int(qk*nmag) % 65535
                        qw = int(qw*nmag) % 65535
                    else:
                        qi = qj = qk = 0
                        qw = 32767

                    pack_4_uint16_into(default_data, i, qi, qj, qk, qw)
                    i += 8

                if not trans_flags[n]:
                    pack_3_float_into(default_data, i,
                        node_state.pos_x / 100,
                        node_state.pos_y / 100,
                        node_state.pos_z / 100)
                    i += 12

                if not scale_flags[n]:
                    pack_1_float_into(default_data, i, node_state.scale)
                    i += 4

            if is_overlay:
                # skip the first frame for overlays
                continue


        # write to the frame_data
        for n in range(anim.node_count):
            node_state = jma_anim.frames[f][n]

            if rot_flags[n]:
                # components are ones-signed
                qi = node_state.rot_i
                qj = node_state.rot_j
                qk = node_state.rot_k
                qw = node_state.rot_w
                nmag = qi**2 + qj**2 + qk**2 + qw**2
                if nmag:
                    nmag = sqrt(nmag) * 32767.5
                    qi = int(qi*nmag) % 65535
                    qj = int(qj*nmag) % 65535
                    qk = int(qk*nmag) % 65535
                    qw = int(qw*nmag) % 65535
                else:
                    qi = qj = qk = 0
                    qw = 32767

                pack_4_uint16_into(frame_data, j, qi, qj, qk, qw)
                j += 8

            if trans_flags[n]:
                pack_3_float_into(frame_data, j,
                    node_state.pos_x / 100,
                    node_state.pos_y / 100,
                    node_state.pos_z / 100)
                j += 12

            if scale_flags[n]:
                pack_1_float_into(frame_data, j, node_state.scale)
                j += 4
