import os

from math import sqrt
from struct import Struct as PyStruct

from reclaimer.hek.defs.objs.matrices import \
     axis_angle_to_quat, multiply_quaternions
from reclaimer.animation.jma import JmsNode, JmaAnimation, JmaRootNodeState,\
     JmaNodeState, write_jma, get_anim_ext

__all__ = ("extract_animation", "apply_frame_info_to_state", )


def apply_frame_info_to_state(state, dx=0, dy=0, dz=0, dyaw=0):
    x, y, z = state.pos_x + dx, state.pos_y + dy, state.pos_z + dz
    i, j, k, w = multiply_quaternions(
        axis_angle_to_quat(1, 0, 0, -dyaw),
        (state.rot_i, state.rot_j, state.rot_k, state.rot_w),
        )
    return JmaNodeState(x, y, z, i, j, k, w, state.scale)


def extract_animation(tagdata, tag_path, **kw):
    if not tagdata.animations.STEPTREE:
        return

    filepath_base = os.path.join(
        kw['out_dir'], os.path.dirname(tag_path), "animations")
    endian = ">"
    if kw.get('halo_map') and kw.get('halo_map').engine != "halo1anni":
        endian = "<"

    unpack_trans = PyStruct(endian + "3f").unpack
    unpack_ijkw  = PyStruct(endian + "4h").unpack
    unpack_dxdy  = PyStruct(endian + "2f").unpack
    unpack_float = PyStruct(endian + "f").unpack

    anim_nodes = []
    for node in tagdata.nodes.STEPTREE:
        anim_nodes.append(JmsNode(node.name, node.first_child_node_index,
                                  node.next_sibling_node_index))

    if not anim_nodes:
        print("WARNING: Animation tag missing nodes.\n"
              "\tFake nodes will be created to allow compiling the animations.\n"
              "\tAnimation tags compiled from these files won't import onto\n"
              "\ttheir gbxmodel in 3DS Max, as their node names won't match.")
        for i in range(tagdata.animations.STEPTREE[0].node_count):
            anim_nodes.append(JmsNode("fake_node%s" % i, -1, i + 1))

        anim_nodes[0].first_child = 1
        anim_nodes[-1].first_child = -1
        anim_nodes[0].sibling_index = anim_nodes[-1].sibling_index = -1


    for anim in tagdata.animations.STEPTREE:
        try:
            anim_type = anim.type.enum_name
            frame_info_type = anim.frame_info_type.enum_name.lower()
            world_relative = anim.flags.world_relative

            has_dxdy = "dx" in frame_info_type
            has_dz   = "dz" in frame_info_type
            has_dyaw = "dyaw" in frame_info_type

            anim_ext = get_anim_ext(anim_type, frame_info_type, world_relative)

            filepath = os.path.join(filepath_base, anim.name + anim_ext)
            if not kw.get('overwrite', True) and os.path.isfile(filepath):
                return

            frame_count = anim.frame_count
            node_count  = anim.node_count
            trans_int = anim.trans_flags0 + (anim.trans_flags1 << 32)
            rot_int   = anim.rot_flags0   + (anim.rot_flags1   << 32)
            scale_int = anim.scale_flags0 + (anim.scale_flags1 << 32)

            trans_flags = tuple(bool(trans_int & (1 << i)) for i in range(node_count))
            rot_flags   = tuple(bool(rot_int   & (1 << i)) for i in range(node_count))
            scale_flags = tuple(bool(scale_int & (1 << i)) for i in range(node_count))

            frame_info   = anim.frame_info.STEPTREE
            default_data = anim.default_data.STEPTREE
            frame_data   = anim.frame_data.STEPTREE

            anim_frames = []

            frame_info_size = {
                "dx,dy": 8,
                "dx,dy,dyaw": 12,
                "dx,dy,dz,dyaw": 16}.get(frame_info_type, 0) * frame_count
            frame_size = (12 * sum(trans_flags) + 8 * sum(rot_flags) +
                          4  * sum(scale_flags))
            default_data_size = anim.node_count * (12 + 8 + 4) - frame_size
            uncomp_data_size = frame_size * anim.frame_count
            if len(anim_nodes) != anim.node_count:
                print("Skipping animation with different number of nodes "
                      "than the tag contains: '%s'" % anim.name)
                continue
            elif frame_info_size > len(frame_info):
                print("Skipping animation with less frame_info data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif default_data_size > len(default_data):
                print("Skipping animation with less default_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif uncomp_data_size > len(frame_data):
                print("Skipping animation with less frame_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif anim.flags.compressed_data and sum(default_data) == 0:
                print("Skipping compressed animation without uncompressed "
                      "animation data: '%s'" % anim.name)
                continue

            # sum the frame info changes for each frame from the frame_info
            off = 0
            dx = dy = dz = dyaw = 0.0
            x = y = z = yaw = 0.0
            root_node_infos = []
            for f in range(anim.frame_count):
                if has_dxdy:
                    dx, dy = unpack_dxdy(frame_info[off: off + 8])
                    off += 8

                if has_dz:
                    dz = unpack_float(frame_info[off: off + 4])[0]
                    off += 4

                if has_dyaw:
                    dyaw = unpack_float(frame_info[off: off + 4])[0]
                    off += 4

                root_node_info = JmaRootNodeState(dx, dy, dz, dyaw,
                                                  x, y, z, yaw)
                root_node_infos.append(root_node_info)
                x, y, z, yaw = x + dx, y + dy, z + dz, yaw + dyaw


            off = 0
            def_node_states = []
            # overlay animations start with frame 0 being
            # in the same state as the default node states
            if anim_type == "overlay":
                anim_frames.append(def_node_states)

            # create the default node states from the default_data
            for n in range(anim.node_count):
                i = j = k = x = y = z = 0.0
                w = scale = 1.0
                if not rot_flags[n]:
                    i, j, k, w = unpack_ijkw(default_data[off: off + 8])
                    rot_len = i**2 + j**2 + k**2 + w**2
                    if rot_len:
                        rot_len = sqrt(rot_len)
                        i /= rot_len
                        j /= rot_len
                        k /= rot_len
                        w /= rot_len
                    else:
                        i = j = k = 0.0
                        w = 1.0

                    off += 8

                if not trans_flags[n]:
                    x, y, z = unpack_trans(default_data[off: off + 12])
                    off += 12

                if not scale_flags[n]:
                    scale = unpack_float(default_data[off: off + 4])[0]
                    off += 4

                def_node_states.append(JmaNodeState(x, y, z, i, j, k, w, scale))


            # create the node states from the frame_data
            off = 0
            for f in range(anim.frame_count):
                node_states = []
                anim_frames.append(node_states)
                for n in range(anim.node_count):
                    def_state = def_node_states[n]
                    if rot_flags[n]:
                        i, j, k, w = unpack_ijkw(frame_data[off: off + 8])
                        rot_len = i**2 + j**2 + k**2 + w**2
                        if rot_len:
                            rot_len = sqrt(rot_len)
                            i /= rot_len
                            j /= rot_len
                            k /= rot_len
                            w /= rot_len
                        else:
                            i = j = k = 0.0
                            w = 1.0
                        off += 8
                    else:
                        i, j, k, w = (def_state.rot_i, def_state.rot_j,
                                      def_state.rot_k, def_state.rot_w)

                    if trans_flags[n]:
                        x, y, z = unpack_trans(frame_data[off: off + 12])
                        off += 12
                    else:
                        x, y, z = def_state.pos_x, def_state.pos_y, def_state.pos_z

                    if scale_flags[n]:
                        scale = unpack_float(frame_data[off: off + 4])[0]
                        off += 4
                    else:
                        scale = def_state.scale

                    node_states.append(JmaNodeState(x, y, z, i, j, k, w, scale))


            if anim_type != "overlay":
                # duplicate the first frame to the last frame for non-overlays
                anim_frames.append(deepcopy(anim_frames[0]))
                if root_node_infos:
                    # make sure to remove the frame_info from the first frame
                    root_node_infos.append(
                        root_node_infos[-1] - root_node_infos[0])


            jma_animation = JmaAnimation(
                anim.name, anim.node_list_checksum,
                anim_type, frame_info_type, anim.flags.world_relative,
                anim_nodes, anim_frames
                )
            jma_animation.apply_frame_info_to_states()

            write_jma(filepath, jma_animation)
        except Exception:
            print(format_exc())
            print("Could not extract animation.")
