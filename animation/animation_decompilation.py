import os
import traceback

from copy import deepcopy
from math import sqrt
from struct import Struct as PyStruct

from reclaimer.util.matrices import axis_angle_to_quat, multiply_quaternions
from reclaimer.animation.jma import JmsNode, JmaAnimation, JmaRootNodeState,\
     JmaNodeState, write_jma, get_anim_ext
from reclaimer.model.jms import generate_fake_nodes

__all__ = ("extract_animation", )


def antr_nodes_to_jms_nodes(anim_nodes):
    nodes = []
    for anim_node in anim_nodes:
        nodes.append(
            JmsNode(anim_node.name, anim_node.first_child_node_index,
                    anim_node.next_sibling_node_index,
                    parent_index=anim_node.parent_node_index)
            )

    return nodes


def extract_animation(tagdata, tag_path="", **kw):
    write_jma = kw.get('write_jma', True)
    jma_anims = None
    if write_jma:
        jma_anims = []

    animations = tagdata.animations.STEPTREE
    if not animations:
        return jma_anims

    filepath = ""
    filepath_base = os.path.join(
        kw['out_dir'], os.path.dirname(tag_path), "animations")
    endian = ">"
    if kw.get('halo_map') and kw.get('halo_map').engine != "halo1anni":
        endian = "<"

    unpack_trans = PyStruct(endian + "3f").unpack_from
    unpack_ijkw  = PyStruct(endian + "4h").unpack_from
    unpack_float = PyStruct(endian + "f").unpack_from
    unpack_dxdy       = PyStruct(endian + "2f").unpack_from
    unpack_dxdydyaw   = PyStruct(endian + "3f").unpack_from
    unpack_dxdydzdyaw = PyStruct(endian + "4f").unpack_from

    anim_nodes = antr_nodes_to_jms_nodes(tagdata.nodes.STEPTREE)
    if len(anim_nodes) != animations[0].node_count:
        print("WARNING: Animation tag missing nodes.\n"
              "\tFake nodes will be created to allow compiling the animations.\n"
              "\tAnimation tags compiled from these files won't import onto\n"
              "\ttheir gbxmodel in 3DS Max, as their node names won't match.")
        anim_nodes = generate_fake_nodes(animations[0].node_count)

    for anim in animations:
        try:
            if len(anim_nodes) != anim.node_count:
                print("Skipping animation with different number of nodes "
                      "than the tag contains: '%s'" % anim.name)
                continue
            elif anim.flags.compressed_data and sum(anim.default_data.STEPTREE) == 0:
                print("Skipping compressed animation without uncompressed "
                      "animation data: '%s'" % anim.name)
                continue

            anim_ext = get_anim_ext(anim.type.enum_name,
                                    anim.frame_info_type.enum_name,
                                    anim.flags.world_relative)

            if write_jma:
                filepath = os.path.join(filepath_base, anim.name + anim_ext)
                if not kw.get('overwrite', True) and os.path.isfile(filepath):
                    continue

            # make blank JmaNodeStates to fill in below with frame_data
            frames = [[JmaNodeState() for n in range(anim.node_count)]
                      for f in range(anim.frame_count)]

            jma_anim = JmaAnimation(
                anim.name, anim.node_list_checksum, anim.type.enum_name,
                anim.frame_info_type.enum_name, anim.flags.world_relative,
                anim_nodes, frames
                )
            jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
            jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
            jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

            # make blank JmaNodeStates to fill in below with default_data
            def_node_states = [JmaNodeState() for n in range(anim.node_count)]

            # make blank JmaRootNodeStates to fill in below with frame_info
            jma_anim.calculate_root_node_info()

            has_dxdy = "dx"   in jma_anim.frame_info_type
            has_dz   = "dz"   in jma_anim.frame_info_type
            has_dyaw = "dyaw" in jma_anim.frame_info_type

            trans_flags = jma_anim.trans_flags
            rot_flags   = jma_anim.rot_flags
            scale_flags = jma_anim.scale_flags

            frame_info   = anim.frame_info.STEPTREE
            default_data = anim.default_data.STEPTREE
            frame_data   = anim.frame_data.STEPTREE

            frame_info_node_size = jma_anim.root_node_info_frame_size

            if len(frame_info) < jma_anim.root_node_info_frame_size * anim.frame_count:
                print("Skipping animation with less frame_info data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif len(default_data) < jma_anim.default_data_size:
                print("Skipping animation with less default_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif len(frame_data) < jma_anim.frame_data_frame_size * anim.frame_count:
                print("Skipping animation with less frame_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue


            # sum the frame info changes for each frame from the frame_info
            if frame_info_node_size:
                off = 0
                dx = dy = dz = dyaw = 0.0
                x = y = z = yaw = 0.0
                for f in range(anim.frame_count):
                    if has_dz:
                        dx, dy, dz, dyaw = unpack_dxdydzdyaw(frame_info, off)
                    elif has_dyaw:
                        dx, dy, dyaw = unpack_dxdydyaw(frame_info, off)
                    elif has_dxdy:
                        dx, dy = unpack_dxdy(frame_info, off)

                    dx *= 100
                    dy *= 100
                    dz *= 100

                    off += frame_info_node_size

                    info = jma_anim.root_node_info[f]
                    info.dx, info.dy, info.dz, info.dyaw = dx, dy, dz, dyaw
                    info.x, info.y, info.z, info.yaw = x, y, z, yaw
                    x, y, z, yaw = x + dx, y + dy, z + dz, yaw + dyaw


            off = 0
            # create the default node states from the default_data
            for n in range(jma_anim.node_count):
                i = j = k = x = y = z = 0.0
                w = scale = 1.0
                if not rot_flags[n]:
                    i, j, k, w = unpack_ijkw(default_data, off)
                    off += 8

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

                if not trans_flags[n]:
                    x, y, z = unpack_trans(default_data, off)
                    x *= 100
                    y *= 100
                    z *= 100
                    off += 12

                if not scale_flags[n]:
                    scale = unpack_float(default_data, off)[0]
                    off += 4

                state = def_node_states[n]
                state.pos_x, state.pos_y, state.pos_z = x, y, z
                state.rot_i, state.rot_j, state.rot_k, state.rot_w = i, j, k, w
                state.scale = scale


            # create the node states from the frame_data
            off = 0
            for f in range(anim.frame_count):
                node_states = jma_anim.frames[f]
                for n in range(jma_anim.node_count):
                    def_state = def_node_states[n]
                    state     = node_states[n]
                    if rot_flags[n]:
                        i, j, k, w = unpack_ijkw(frame_data, off)
                        off += 8

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
                    else:
                        i, j, k, w = (def_state.rot_i, def_state.rot_j,
                                      def_state.rot_k, def_state.rot_w)

                    if trans_flags[n]:
                        x, y, z = unpack_trans(frame_data, off)
                        x *= 100
                        y *= 100
                        z *= 100
                        off += 12
                    else:
                        x, y, z = def_state.pos_x, def_state.pos_y, def_state.pos_z

                    if scale_flags[n]:
                        scale = unpack_float(frame_data, off)[0]
                        off += 4
                    else:
                        scale = def_state.scale

                    state.pos_x, state.pos_y, state.pos_z = x, y, z
                    state.rot_i, state.rot_j, state.rot_k, state.rot_w = i, j, k, w
                    state.scale = scale

            if jma_anim.last_frame_loops_to_first:
                # duplicate the first frame to the last frame for non-overlays
                jma_anim.frames.append(deepcopy(jma_anim.frames[0]))
                if jma_anim.root_node_info:
                    # duplicate the last frame and apply the change
                    # that frame to the total change at that frame.
                    last_root_node_info = deepcopy(jma_anim.root_node_info[-1])
                    last_root_node_info.x += last_root_node_info.dx
                    last_root_node_info.y += last_root_node_info.dy
                    last_root_node_info.z += last_root_node_info.dz
                    last_root_node_info.yaw += last_root_node_info.dyaw

                    # no delta on last frame. zero it out
                    last_root_node_info.dx = 0.0
                    last_root_node_info.dy = 0.0
                    last_root_node_info.dz = 0.0
                    last_root_node_info.dyaw = 0.0

                    jma_anim.root_node_info.append(last_root_node_info)

                # this is set to True on instantiation.
                # Set it to False since we had to provide root node info
                jma_anim.root_node_info_applied = False
                jma_anim.apply_root_node_info_to_states()
            else:
                # overlay animations start with frame 0 being
                # in the same state as the default node states
                jma_anim.frames.insert(0, def_node_states)

            if write_jma:
                write_jma(filepath, jma_anim)
            else:
                jma_anims.append(jma_anim)
        except Exception:
            print(traceback.format_exc())
            print("Could not extract animation.")

    return jma_anims
