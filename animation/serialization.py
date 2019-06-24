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
    pack_4_int16_into = PyStruct(">4h").pack_into

    is_overlay = jma_anim.anim_type == "overlay"

    i = j = 0
    for f in range(jma_anim.frame_count):
        if not is_overlay and f == stored_frame_count:
            # skip the last frame for non-overlays
            break

        # write to the default_data
        if f == 0:
            for n in range(anim.node_count):
                node_state = jma_anim.frames[f][n]
                if not rot_flags[n]:
                    pack_4_int16_into(default_data, i,
                        int(node_state.rot_i*32767),
                        int(node_state.rot_j*32767),
                        int(node_state.rot_k*32767),
                        int(node_state.rot_w*32767))
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
                pack_4_int16_into(frame_data, j,
                    int(node_state.rot_i*32767),
                    int(node_state.rot_j*32767),
                    int(node_state.rot_k*32767),
                    int(node_state.rot_w*32767))
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
