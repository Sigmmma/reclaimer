

__all__ = ("compile_animation", "compile_animation_tag", )


def compile_animation(anim, jma_animation):
    # decompress the headers for each of the keyframes
    rot   = comp_data.rotation
    trans = comp_data.translation
    scale = comp_data.scale

    # get the keyframe counts and keyframe offsets
    # Right shift by 13 rather than 12 because we're also dividing by 2
    # to count for the fact that the offsets are in bytes, not entries.
    rot_head   = [(v & 4095, v >> 13) for v in rot.keyframe_head]
    trans_head = [(v & 4095, v >> 13) for v in trans.keyframe_head]
    scale_head = [(v & 4095, v >> 13) for v in scale.keyframe_head]
    
    rot_flags   = jma_animation.rot_flags
    trans_flags = jma_animation.trans_flags
    scale_flags = jma_animation.scale_flags

    anim.frame_count = len(jma_animation.frames)
    anim.node_count = len(jma_animation.nodes)
    anim.frame_size = rot_count*8 + trans_count*12 + scale_count*4
    anim.keyframe_data.STEPTREE = keyframe_data = bytearray(
        b'\x00' * anim.frame_size * anim.frame_count)
    anim.default_data.STEPTREE = def_data = bytearray(
        b'\x00' * (anim.anim.node_count * (12 + 8 + 4) - anim.frame_size))

    anim.offset_to_compressed_data = 0
    anim.flags.compressed_data = False

    # write the rotations, translations, and scales
    # to the keyframe_data and def_data
    i = j = 0
    def_state = None
    for f in range(anim.frame_count):
        for n in range(anim.node_count):
            node_state = jma_animation.frames[f][n]
            def_state = None
            if f == 0 and n in range(len(def_node_states)):
                def_state = def_node_states[n]

            if rot_flags[n]:
                pack_into('>hhhh', keyframe_data, i,
                          int(node_state.rot_i*32767),
                          int(node_state.rot_j*32767),
                          int(node_state.rot_k*32767),
                          int(node_state.rot_w*32767))
                i += 8
            elif def_state:
                pack_into('>hhhh', def_data, j,
                          int(def_state.rot_i*32767),
                          int(def_state.rot_j*32767),
                          int(def_state.rot_k*32767),
                          int(def_state.rot_w*32767))
                j += 8

            if trans_flags[n]:
                pack_into('>fff', keyframe_data, i,
                          node_state.pos_x, node_state.pos_y, node_state.pos_z)
                i += 12
            elif def_state:
                pack_into('>fff', def_data, j,
                          def_state.pos_x, def_state.pos_y, def_state.pos_z)
                j += 12

            if scale_flags[n]:
                pack_into('>f', keyframe_data, i, node_state.scale)
                i += 4
            elif def_state:
                pack_into('>f', def_data, j, def_state.scale)
                j += 4


def compile_animation_tag(antr_tag, jma_animation_set):
    pass
