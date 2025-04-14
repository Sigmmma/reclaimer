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

from reclaimer.jm.jma import JmsNode, JmaAnimation, JmaRootNodeState,\
     JmaLimpNodeInfo, JmaNodeState, write_jma, util
from reclaimer.animation.constants import JMA_RETAIL_NODES
from reclaimer.animation import serialization
from reclaimer.jm import jms, constants as const

__all__ = ("extract_model_animations", "extract_animation", )



def get_base_anim_for_overlay(anim_index, tagdata):
    # NOTE: this function is quite a bit of best-guess-work and
    #       hopes and prayers. There's not really a simple way
    #       to figure out what base animation is best to use for
    #       an overlay, so this was hand-tuned till it worked out
    unit_anims = list(tagdata.units.STEPTREE)
    fp_sets    = list(tagdata.fp_animations.STEPTREE)
    anims      = list(tagdata.animations.STEPTREE)
    to_check   = set(range(len(anims)))

    o_anim, b_anim = anims[anim_index], None
    fallback_anim_1 = fallback_anim_2 = None
    o_name = o_anim.name.lower()
    o_name_parts = o_name.split(" ") + ["", ""]

    # check for all indices in permutation chains
    o_anim_indices = set([anim_index])
    for i, anim in enumerate(anims):
        anim_chain = set([i])
        while anim.next_animation in to_check:
            anim_chain.add(anim.next_animation)
            anim = anims[anim.next_animation]

        if anim_index in anim_chain:
            o_anim_indices.update(anim_chain)

    anim_sets = [
        [anim.animation for anim in anim_set.animations.STEPTREE
         if anim.animation in to_check]
        for anim_set in fp_sets
        ]

    is_weap = False
    for unit in unit_anims:
        unit_anim_sets = []

        for uw_anim in unit.weapons.STEPTREE:
            unit_anim_sets.append([])
            unit_anim_sets[-1].extend(
                anim.animation for anim in uw_anim.animations.STEPTREE
                if anim.animation in to_check
                )
            for weap_type in uw_anim.weapon_types.STEPTREE:
                unit_anim_sets[-1].extend(
                    anim.animation for anim in weap_type.animations.STEPTREE
                    if anim.animation in to_check
                    )
            is_weap |= (unit.label.lower() in o_name_parts[0] and
                        o_name_parts[1] in uw_anim.name.lower())

        unit_anim_set = []
        [unit_anim_set.extend(anim_set) for anim_set in unit_anim_sets]
        unit_anim_set.extend(
            anim.animation for anim in unit.animations.STEPTREE
            if anim.animation in to_check
            )

        anim_sets.extend([*unit_anim_sets, unit_anim_set])

    for indices in anim_sets:
        # find an idle animation that matches this(and a fallback)
        if b_anim:
            break
        elif not o_anim_indices.intersection(indices):
            continue

        for i in indices:
            anim = anims[i] if i in to_check else None
            to_check.discard(i)

            # find the first valid base animation we can use
            if not anim or anim.type.enum_name != "base":
                continue

            b_name = anim.name.lower()
            b_name_parts = b_name.split(" ") + ["", ""]

            if "idle" not in b_name:
                fallback_anim_2 = anim
            elif b_name_parts[0] == o_name_parts[0]:
                b_anim = anim
                if is_weap and b_name_parts[1] == o_name_parts[1]:
                    break
            else:
                fallback_anim_1 = anim

    for anim in (() if b_anim else anims):
        # find a useful base if we can't find a more fitting one
        if anim.type.enum_name != "base":
            continue

        b_name = anim.name.lower()
        b_name_parts = b_name.split(" ") + ["", ""]

        if "idle" not in b_name:
            continue
        elif ((("stand" in b_name or "alert" in b_name) and
               ("stand" in o_name or "alert" in o_name or
                o_name.startswith("h-ping") or
                o_name.startswith("s-ping"))
               )   or
              ("crouch"  in o_name and "crouch"  in b_name) or
              ("flee"    in o_name and "flee"    in b_name) or
              ("flaming" in o_name and "flaming" in b_name)):
            b_anim = anim
            if is_weap and b_name_parts[1] == o_name_parts[1]:
                break
        elif not fallback_anim_1:
            fallback_anim_1 = anim

    b_anim = b_anim or fallback_anim_1 or fallback_anim_2

    return b_anim


def antr_nodes_to_jms_nodes(anim_nodes, anim):
    nodes = []

    if hasattr(anim_nodes, "parent"):
        # convert from antr node block array to simple list
        anim_nodes = [
            [node.name, node.first_child_node_index,
             node.next_sibling_node_index, node.parent_node_index]
            for node in anim_nodes
            ]

    if not anim_nodes:
        # if no nodes, try to see if it's from retail
        anim_nodes = JMA_RETAIL_NODES.get(
            (anim.node_count, anim.node_list_checksum), []
            )

    for name, child, sibling, parent in anim_nodes:
        nodes.append(JmsNode(name, child, sibling, parent_index=parent))

    return nodes


def extract_model_animations(tagdata, tag_path="", halo_map=None, **kw):
    return_jma = not kw.get('write_jma', True)
    jma_anims = [] if return_jma else None
    if not tagdata.animations.STEPTREE:
        return jma_anims

    for i, anim in enumerate(tagdata.animations.STEPTREE):
        try:
            kw["fake_nodes_warning"] = i == 0
            result = extract_animation(i, tagdata, tag_path, **kw)
            if result and return_jma:
                jma_anims.append(result)
        except Exception as e:
            e = traceback.format_exc()
            print(f"{e} in {tag_path}[{i}] - '{getattr(anim, 'name', '')}'")

    return jma_anims


def extract_animation(anim_index, tagdata, tag_path="", **kw):
    endian    = kw.get("endian", ">")
    serialize = kw.get('write_jma', True)
    pad_nodes = kw.get('pad_nodes', False)
    out_dir   = kw.get("out_dir", "")
    filepath  = Path(tag_path or "")

    anim      = tagdata.animations.STEPTREE[anim_index]
    tag_nodes = tagdata.nodes.STEPTREE
    anim_ext  = util.get_anim_ext(anim.type.enum_name,
                                  anim.frame_info_type.enum_name,
                                  anim.flags.world_relative)
    if serialize:
        filepath = Path(out_dir).joinpath(
            filepath.parent, "animations", anim.name + anim_ext
            )
        if not kw.get('overwrite', True) and filepath.is_file():
            return

    anim_nodes = antr_nodes_to_jms_nodes(tag_nodes, anim)
    limp_node_infos = [
        JmaLimpNodeInfo(node.base_vector, node.vector_range,
                        None, node.node_joint_flags.data)
        for node in tag_nodes
        ]

    version = const.JMA_VER_HALO_1_RETAIL
    if len(anim_nodes) != anim.node_count:
        kw.get("fake_nodes_warning", True) and pad_nodes and print(
            "WARNING: The following tag is missing nodes:\n"
            f"\t'{tag_path}'\n"
            "\tFake nodes will be created to allow compiling the animations.\n"
            "\tAnimation tags compiled from these files won't import onto\n"
            "\ttheir model in 3DSMax/Blender, as the node names won't match.")
        anim_nodes = jms.util.generate_fake_nodes(anim.node_count)
        limp_node_infos = [JmaLimpNodeInfo() for n in range(anim.node_count)]
        if not pad_nodes:
            version = const.JMA_VER_HALO_1_OLDEST_KNOWN

    jma_anim = JmaAnimation(
        anim.name, anim.node_list_checksum, anim.type.enum_name,
        anim.frame_info_type.enum_name, anim.flags.world_relative,
        anim_nodes, actors=["unnamedActor"], version=version
        )
    jma_anim.limp_node_infos = limp_node_infos
    jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    if len(anim.frame_info.STEPTREE) < jma_anim.root_node_info_frame_size * anim.frame_count:
        print("Skipping animation with less frame_info data "
              "than it is expected to contain: '%s'" % anim.name)
        return
    elif anim.flags.compressed_data:
        # checks below don't apply to compressed animations
        pass
    elif len(anim.default_data.STEPTREE) < jma_anim.default_data_size:
        print("Skipping animation with less default_data "
              "than it is expected to contain: '%s'" % anim.name)
        return
    elif len(anim.frame_data.STEPTREE) < jma_anim.frame_data_frame_size * anim.frame_count:
        print("Skipping animation with less frame_data "
              "than it is expected to contain: '%s'" % anim.name)
        return

    # if this is an overlay, try to determine a base
    # animation that it can be applied to, and apply
    # the overlay onto it so it looks good when imported
    base_frame = None
    if jma_anim.is_overlay:
        b_anim      = get_base_anim_for_overlay(anim_index, tagdata)
        base_frame  = [] if not b_anim else serialization.deserialize(
            b_anim, endian)[1][0]

        if base_frame:
            print(f"'{b_anim.name}' used as base for '{anim.name}'")
        else:
            print(f"No base anim found for '{anim.name}'. "
                  "May not look correct when imported.")


    # sum the frame info changes for each frame from the frame_info
    root_node_info = serialization.deserialize_frame_info(anim, True, endian)

    kfs, frames = serialization.deserialize(anim, endian)
    rot_kfs, trans_kfs, scale_kfs = kfs

    jma_anim.root_node_info  = root_node_info
    jma_anim.frames          = frames
    jma_anim.rot_keyframes   = rot_kfs
    jma_anim.trans_keyframes = trans_kfs
    jma_anim.scale_keyframes = scale_kfs

    if jma_anim.has_frame_info:
        # this is set to True on instantiation.
        # set it to False since we had to provide root node info
        jma_anim.root_node_info_applied = False
        jma_anim.apply_root_node_info_to_states()

    elif jma_anim.is_overlay and base_frame:
        # remove whatever base is applied so we can apply a new one
        jma_anim.apply_base_pose_to_states(True)

        # replace the first frame with the chosen base pose
        jma_anim.frames[0] = base_frame
        jma_anim.apply_base_pose_to_states()

    if serialize:
        write_jma(filepath, jma_anim)
    else:
        return jma_anim
