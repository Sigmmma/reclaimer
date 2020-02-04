#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import traceback

from copy import deepcopy
from math import sqrt
from pathlib import Path

from reclaimer.util.matrices import axis_angle_to_quat, multiply_quaternions
from reclaimer.animation.jma import JmsNode, JmaAnimation, JmaRootNodeState,\
     JmaNodeState, write_jma, get_anim_ext
from reclaimer.animation import serialization
from reclaimer.model import jms

__all__ = ("extract_model_animations", "extract_animation", )


def antr_nodes_to_jms_nodes(anim_nodes):
    nodes = []
    for anim_node in anim_nodes:
        nodes.append(
            JmsNode(anim_node.name, anim_node.first_child_node_index,
                    anim_node.next_sibling_node_index,
                    parent_index=anim_node.parent_node_index)
            )

    return nodes


def extract_model_animations(tagdata, tag_path="", **kw):
    return_jma = not kw.get('write_jma', True)
    jma_anims = [] if return_jma else None
    if not tagdata.animations.STEPTREE:
        return jma_anims

    for i in range(len(tagdata.animations.STEPTREE)):
        try:
            result = extract_animation(i, tagdata, tag_path, **kw)
            if result and return_jma:
                jma_anims.append(result)
        except Exception:
            print(traceback.format_exc())
            print("Could not extract animation.")

    return jma_anims


def extract_animation(anim_index, tagdata, tag_path="", **kw):
    endian = kw.get("endian", ">")

    anim_nodes = antr_nodes_to_jms_nodes(tagdata.nodes.STEPTREE)
    anim = tagdata.animations.STEPTREE[anim_index]

    anim_ext = get_anim_ext(anim.type.enum_name,
                            anim.frame_info_type.enum_name,
                            anim.flags.world_relative)

    filepath = Path("")
    do_write_jma = kw.get('write_jma', True)
    if do_write_jma:
        filepath = Path(kw.get("out_dir", "")).joinpath(
            Path(tag_path).parent, "animations", anim.name + anim_ext)
        if not kw.get('overwrite', True) and filepath.is_file():
            return

    if len(anim_nodes) != anim.node_count:
        print("WARNING: Animation tag missing nodes.\n"
              "\tFake nodes will be created to allow compiling the animations.\n"
              "\tAnimation tags compiled from these files won't import onto\n"
              "\ttheir gbxmodel in 3DS Max, as their node names won't match.")
        anim_nodes = jms.util.generate_fake_nodes(anim.node_count)

    if len(anim_nodes) != anim.node_count:
        print("Skipping animation with different number of nodes "
              "than the tag contains: '%s'" % anim.name)
        return


    jma_anim = JmaAnimation(
        anim.name, anim.node_list_checksum, anim.type.enum_name,
        anim.frame_info_type.enum_name, anim.flags.world_relative,
        anim_nodes
        )
    jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    if len(anim.frame_info.STEPTREE) < jma_anim.root_node_info_frame_size * anim.frame_count:
        print("Skipping animation with less frame_info data "
              "than it is expected to contain: '%s'" % anim.name)
        return
    elif len(anim.default_data.STEPTREE) < jma_anim.default_data_size:
        print("Skipping animation with less default_data "
              "than it is expected to contain: '%s'" % anim.name)
        return
    elif len(anim.frame_data.STEPTREE) < jma_anim.frame_data_frame_size * anim.frame_count:
        print("Skipping animation with less frame_data "
              "than it is expected to contain: '%s'" % anim.name)
        return

    if anim.flags.compressed_data:
        # decompress compressed animations
        keyframes, jma_anim.frames = serialization.deserialize_compressed_frame_data(anim)
        jma_anim.rot_keyframes   = keyframes[0]
        jma_anim.trans_keyframes = keyframes[1]
        jma_anim.scale_keyframes = keyframes[2]
    else:
        # create the node states from the frame_data and default_data
        jma_anim.frames = serialization.deserialize_frame_data(
            anim, None, True, endian)

    # sum the frame info changes for each frame from the frame_info
    jma_anim.root_node_info = serialization.deserialize_frame_info(
        anim, True, endian)

    if jma_anim.has_dxdy or jma_anim.has_dyaw or jma_anim.has_dz:
        # this is set to True on instantiation.
        # Set it to False since we had to provide root node info
        jma_anim.root_node_info_applied = False
        jma_anim.apply_root_node_info_to_states()

    if do_write_jma:
        write_jma(filepath, jma_anim)
    else:
        return jma_anim
