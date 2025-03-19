#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
import traceback

from copy import deepcopy
from pathlib import Path

from . import animation, util
from .node_state import JmaNodeState
from .root_node_state import JmaRootNodeState
from .. import constants as const, jm_reader
from ..jms import JmsNode
from reclaimer.util import float_to_str,\
    float_to_str_truncate,\
    parse_jm_float,\
    parse_jm_int


def read_jma(jma_string, stop_at="", anim_name=""):
    '''
    Converts a jma data string/stream into a JmaAnimation instance.
    '''
    if anim_name is None:
        anim_name = "__unnamed"

    anim_name, ext = os.path.splitext(anim_name)
    anim_type, frame_info_type, world_relative = util.get_anim_types(ext) ###

    jm_iter = jm_reader.JMReader(jma_string)
    version = jm_iter.next_int

    jma_anim = animation.JmaAnimation(
        anim_name, 0, anim_type, frame_info_type,
        world_relative, version=version
        )

    if version not in const.JMA_VER_ALL:
        print("Unknown JMA version '%s' found." % version)
        return jma_anim

    try:
        frame_count = jm_iter.next_int & 0xFFffFFff
    except Exception:
        print(traceback.format_exc())
        print("Could not read frame count.")
        return jma_anim

    if frame_count > 2048:
        raise ValueError("Cannot parse jma files with more than 2048 frames.")

    try:
        frame_rate = jm_iter.next_int
    except Exception:
        print(traceback.format_exc())
        print("Could not frame rate.")
        return jma_anim

    if stop_at == "actors": return jma_anim

    try:
        actor_count = jm_iter.next_int
    except Exception:
        print(traceback.format_exc())
        print("Failed to read actor count.")
        return jma_anim

    if actor_count != 1:
        raise ValueError("Cannot parse jma files with more than one actor.")

    # read the actors
    for actor_i in range(actor_count):
        try:
            jma_anim.actors.append(jm_iter.next)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read actors.")
            return jma_anim

        # TODO: update getting these if multiple actors are ever supported
        nodes  = jma_anim.nodes
        frames = jma_anim.frames
        try:
            node_count = jm_iter.next_int
        except Exception:
            print(traceback.format_exc())
            print("Could not node count.")
            return jma_anim

        if node_count > 256:
            raise ValueError("Cannot parse jma files with more than 256 nodes.")

        if stop_at == "checksum": continue

        try:
            jma_anim.node_list_checksum = jm_iter.next_int
        except Exception:
            print(traceback.format_exc())
            print("Could not read node list checksum.")
            return jma_anim

        if jma_anim.node_list_checksum >= 0x80000000:
            # jma gave us an unsigned checksum.... sign it
            jma_anim.node_list_checksum -= 0x100000000

        if stop_at == "nodes": continue

        # read the nodes
        try:
            for i in range(node_count):
                if jma_anim.has_node_hierarchy:
                    node_data = (
                        jm_iter.next, jm_iter.next_int, jm_iter.next_int
                        )
                elif jma_anim.has_node_names:
                    node_data = (jm_iter.next, )
                else:
                    node_data = ("fake_node_%d" % i, )

                nodes.append(JmsNode(*node_data))
            JmsNode.setup_node_hierarchy(nodes)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read nodes.")
            return jma_anim


        if stop_at == "frames": continue

        # read the frame data
        try:
            i = 0 # make sure i is defined in case of exception
            for i in range(frame_count):
                frame = []
                for j in range(node_count):
                    frame.append(JmaNodeState(
                        *(jm_iter.next_float for _ in range(8))
                        ))
                frames.append(frame)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read frames.")
            return jma_anim

    jma_anim.calculate_root_node_info()
    jma_anim.apply_root_node_info_to_states(True)
    jma_anim.calculate_animation_flags()
    return jma_anim


def write_jma(filepath, jma_anim, use_blitzkrieg_rounding=False):
    if jma_anim.actor_count != 1:
        raise ValueError("Cannot write jma files with more than one actor.")

    to_str = (
        float_to_str if not use_blitzkrieg_rounding else
        (lambda f: float_to_str_truncate(f, 6))
        )

    # If the path doesnt exist, create it
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)

    if not jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states()

    with filepath.open("w", encoding='latin1', newline="\r\n") as f:
        f.write("%d\n" % jma_anim.version)
        f.write("%s\n" % jma_anim.frame_count)
        f.write("%s\n" % jma_anim.frame_rate)

        f.write("%s\n" % jma_anim.actor_count)

        for actor_name in jma_anim.actors:
            # TODO: update getting these if multiple actors are ever supported
            nodes  = jma_anim.nodes
            frames = jma_anim.frames

            f.write("%s\n" % actor_name)
            f.write("%s\n" % len(nodes))
            f.write("%s\n" % int(jma_anim.node_list_checksum))

            if jma_anim.has_node_hierarchy:
                for node in nodes:
                    f.write("%s\n%s\n%s\n" %
                        (node.name[: 31], node.first_child, node.sibling_index)
                    )
            elif jma_anim.has_node_names:
                for node in nodes:
                    f.write("%s\n" % node.name[: 31])

            for frame in frames:
                for nf in frame:
                    f.write("%s\t%s\t%s\n%s\t%s\t%s\t%s\n%s\n" % (
                        to_str(nf.pos_x), to_str(nf.pos_y), to_str(nf.pos_z),
                        to_str(nf.rot_i), to_str(nf.rot_j),
                        to_str(nf.rot_k), to_str(nf.rot_w),
                        to_str(nf.scale))
                    )

#jma_file = open(r'C:\Users\Moses\Desktop\halo\data\characters\cyborg\animations\alert unarmed turn-right.jmt', 'r')
#data = read_jma(jma_file.read(), "", "alert unarmed turn-right.jmt")
