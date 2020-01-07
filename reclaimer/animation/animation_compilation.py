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

from reclaimer import enums
from reclaimer.animation import util
from reclaimer.animation import serialization

__all__ = ("compile_animation", "compile_model_animations",
           "ANIMATION_COMPILE_MODE_NEW", "ANIMATION_COMPILE_MODE_PRESERVE",
           "ANIMATION_COMPILE_MODE_ADDITIVE")

ANIMATION_COMPILE_MODE_NEW = 0
ANIMATION_COMPILE_MODE_PRESERVE = 1
ANIMATION_COMPILE_MODE_ADDITIVE = 2


def compile_animation(anim, jma_anim, ignore_size_limits=False, endian=">"):
    '''
    Compiles the provided JmaAnimation into the provided antr animation block.
    '''
    errors = []

    # determine the sizes of the frame_info, default_data, and frame_data
    frame_info_node_size = jma_anim.root_node_info_frame_size

    stored_frame_count = jma_anim.frame_count - 1  # subtract the base frame

    frame_info_size   = frame_info_node_size * stored_frame_count
    default_data_size = jma_anim.default_data_size
    frame_data_size   = jma_anim.frame_data_frame_size * stored_frame_count

    max_frame_info_size   = anim.frame_info.get_desc('MAX', 'size')
    max_default_data_size = anim.default_data.get_desc('MAX', 'size')
    max_frame_data_size   = anim.frame_data.get_desc('MAX', 'size')

    if not ignore_size_limits:
        if frame_info_size > max_frame_info_size:
            errors.append("Too much frame_info data. Max is %s bytes, got %s" %
                          (max_frame_info_size, frame_info_size))

        if default_data_size > max_default_data_size:
            errors.append("Too much default data. Max is %s bytes, got %s" %
                          (max_default_data_size, default_data_size))

        if frame_data_size > max_frame_data_size:
            errors.append("Too much frame data. Max is %s bytes, got %s" %
                          (max_frame_data_size, frame_data_size))

    if errors:
        return errors

    if jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states(True)

    anim.name = jma_anim.name
    anim.type.set_to(jma_anim.anim_type)
    anim.frame_count = stored_frame_count
    anim.frame_size = jma_anim.frame_data_frame_size
    anim.node_list_checksum = jma_anim.node_list_checksum
    anim.node_count = jma_anim.node_count
    anim.next_animation = -1

    if jma_anim.has_dz:
        anim.frame_info_type.data = 3
    elif jma_anim.has_dyaw:
        anim.frame_info_type.data = 2
    elif jma_anim.has_dxdy:
        anim.frame_info_type.data = 1
    else:
        anim.frame_info_type.data = 0

    # cant compress animations yet
    anim.flags.data = 0
    anim.flags.world_relative = jma_anim.world_relative
    anim.offset_to_compressed_data = 0

    anim.trans_flags0 =  jma_anim.trans_flags_int & 0xFFffFFff
    anim.trans_flags1 = (jma_anim.trans_flags_int >> 32) & 0xFFffFFff
    anim.rot_flags0   =  jma_anim.rot_flags_int & 0xFFffFFff
    anim.rot_flags1   = (jma_anim.rot_flags_int >> 32) & 0xFFffFFff
    anim.scale_flags0 =  jma_anim.scale_flags_int & 0xFFffFFff
    anim.scale_flags1 = (jma_anim.scale_flags_int >> 32) & 0xFFffFFff

    frame_info = serialization.serialize_frame_info(jma_anim, endian)
    def_data   = serialization.serialize_default_data(jma_anim, endian)
    frame_data = serialization.serialize_frame_data(jma_anim, endian)

    anim.frame_info.STEPTREE = frame_info
    anim.default_data.STEPTREE = def_data
    anim.frame_data.STEPTREE = frame_data

    return errors


def compile_model_animations(antr_tag, jma_anim_set, ignore_size_limits=False,
                             animation_count_limit=256, delta_tolerance=None,
                             update_mode=ANIMATION_COMPILE_MODE_PRESERVE,
                             mod2_nodes=None):
    errors = []

    tagdata = antr_tag.data.tagdata
    antr_objects = tagdata.objects.STEPTREE
    antr_units = tagdata.units.STEPTREE
    antr_weapons = tagdata.weapons.STEPTREE
    antr_vehicles = tagdata.vehicles.STEPTREE
    antr_devices = tagdata.devices.STEPTREE
    antr_unit_damages = tagdata.unit_damages.STEPTREE
    antr_fp_animations = tagdata.fp_animations.STEPTREE
    antr_anims = tagdata.animations.STEPTREE
    antr_nodes = tagdata.nodes.STEPTREE

    # make sure the new animations share nodes with the existing animations
    if update_mode == ANIMATION_COMPILE_MODE_ADDITIVE and antr_nodes:
        if len(antr_nodes) != len(jma_anim_set.nodes):
            errors.append("Node count of these animations differs from the "
                          "node count of the model_animations tag.")
            return errors

        for i in range(len(jma_anim_set.nodes)):
            jma_node = jma_anim_set.nodes[i]
            antr_node = antr_nodes[i]

            if (antr_node.next_sibling_node_index != jma_node.sibling_index or
                antr_node.first_child_node_index  != jma_node.first_child or
                # dont check the parent node. root node references itself in
                # animation nodes. it's weird. Sibling and child are enough.
                #antr_node.parent_node_index       != jma_node.parent_index or
                antr_node.name != jma_node.name):

                errors.append("Node(s) in these animations differ from the "
                              "node(s) of the model_animations tag.")
                return errors


    prev_antr_anims_by_type_strings = {}
    antr_indices_by_type_strings = {}

    prev_antr_objects  = list(antr_objects)
    prev_antr_units    = list(antr_units)
    prev_antr_vehicles = list(antr_vehicles)
    prev_antr_nodes  = list(antr_nodes)
    prev_antr_anims  = list(antr_anims)
    assert update_mode in (ANIMATION_COMPILE_MODE_NEW,
                           ANIMATION_COMPILE_MODE_PRESERVE,
                           ANIMATION_COMPILE_MODE_ADDITIVE)
    if update_mode != ANIMATION_COMPILE_MODE_ADDITIVE:
        if update_mode == ANIMATION_COMPILE_MODE_NEW:
            del tagdata.sound_references.STEPTREE[:]
            tagdata.limp_body_node_radius = 0.0
            tagdata.flags.data = 0
            del prev_antr_objects[:]
            del prev_antr_units[:]
            del prev_antr_vehicles[:]
            del prev_antr_nodes[:]
            del prev_antr_anims[:]

        del antr_objects[:]
        del antr_units[:]
        del antr_weapons[:]
        del antr_vehicles[:]
        del antr_devices[:]
        del antr_unit_damages[:]
        del antr_fp_animations[:]
        del antr_anims[:]
        del antr_nodes[:]

        for i in range(len(jma_anim_set.nodes)):
            jma_node = jma_anim_set.nodes[i]
            antr_nodes.append()
            antr_node = antr_nodes[-1]
            antr_node.name = jma_node.name
            antr_node.next_sibling_node_index = jma_node.sibling_index
            antr_node.first_child_node_index  = jma_node.first_child
            antr_node.parent_node_index       = jma_node.parent_index
            if antr_node.parent_node_index == -1:
                antr_node.parent_node_index = 0

            if i not in range(len(prev_antr_nodes)):
                continue

        if prev_antr_nodes:
            prev_antr_node = prev_antr_nodes[i]
            if prev_antr_node.name.lower() == antr_node.name.lower():
                antr_node.node_joint_flags.data = prev_antr_node.node_joint_flags.data
                antr_node.base_vector[:] = prev_antr_node.base_vector
                antr_node.vector_range   = prev_antr_node.vector_range

    # cache the old animations by their names
    for i in range(len(prev_antr_anims)):
        anim = prev_antr_anims[i]
        _, name_pieces = util.split_anim_name_into_type_strings(anim.name.strip())
        prev_antr_anims_by_type_strings[name_pieces] = anim

    # cache the existing animation indices by their names
    for i in range(len(antr_anims)):
        anim = antr_anims[i]
        _, name_pieces = util.split_anim_name_into_type_strings(anim.name.strip())
        antr_indices_by_type_strings[name_pieces] = i


    indices_to_not_overwrite = set()
    indices_modified = set()
    # loop over the animations to add and add/replace them
    for jma_anim_name in sorted(jma_anim_set.animations):
        name = jma_anim_name.strip()
        has_purpose, name_pieces = util.split_anim_name_into_type_strings(name)

        # find where to put this animation
        anim_index = antr_indices_by_type_strings.get(
            name_pieces, len(antr_anims))

        if anim_index >= animation_count_limit:
            errors.append(
                "Too many animations. Cannot add '%s'" % jma_anim_name)
            continue

        anim_added = False
        if anim_index == len(antr_anims):
            anim_added = True
            antr_anims.append()
            print("Adding '%s'" % jma_anim_name)
        else:
            print("Replacing '%s'" % jma_anim_name)

        anim = antr_anims[anim_index]
        try:
            jma_anim = jma_anim_set.animations[jma_anim_name]
            jma_anim.calculate_animation_flags(delta_tolerance)
            errors.extend(compile_animation(anim, jma_anim, ignore_size_limits))
        except Exception:
            errors.append(traceback.format_exc())
            errors.append("Could not compile '%s'" % jma_anim_name)
            if anim_added:
                antr_anims.pop(anim_index)

            continue

        # update the antr indices with this animations index
        antr_indices_by_type_strings[name_pieces] = anim_index

        if name_pieces in prev_antr_anims_by_type_strings:
            # update the animation with the old ones keyframe values and such
            prev_anim = prev_antr_anims_by_type_strings[name_pieces]
            anim.weight = prev_anim.weight
            anim.sound  = prev_anim.sound
            anim.loop_frame_index       = prev_anim.loop_frame_index
            anim.key_frame_index        = prev_anim.key_frame_index
            anim.second_key_frame_index = prev_anim.second_key_frame_index
            anim.sound_frame_index      = prev_anim.sound_frame_index
            anim.left_foot_frame_index  = prev_anim.left_foot_frame_index
            anim.right_foot_frame_index = prev_anim.right_foot_frame_index


        if not has_purpose:
            print("    Could not determine a purpose for this animation")
            continue

        try:
            if util.set_animation_index(antr_tag, jma_anim_name, anim_index,
                                        indices_to_not_overwrite):
                # successfully found an animation index to use this animation
                indices_to_not_overwrite.add(anim_index)
            indices_modified.add(anim_index)
        except Exception:
            errors.append(traceback.format_exc())

    if update_mode == ANIMATION_COMPILE_MODE_PRESERVE:
        for i in range(len(prev_antr_objects)):
            prev_obje = prev_antr_objects[i]
            if prev_obje.animation not in range(len(prev_antr_anims)):
                continue

            _, name_pieces = util.split_anim_name_into_type_strings(
                prev_antr_anims[prev_obje.animation].name.strip())

            new_anim_index = antr_indices_by_type_strings.get(name_pieces)
            if new_anim_index is None:
                continue

            antr_objects.append()
            obje = antr_objects[-1]

            obje.animation = new_anim_index
            obje.function.data = prev_obje.function.data
            obje.function_controls.data = prev_obje.function_controls.data

        if antr_units and prev_antr_units:
            # preserve any old unit pitch/yaw/weapon values
            copy_unit_animation_block_data(antr_units, prev_antr_units)

        if antr_vehicles and prev_antr_vehicles:
            # preserve any old vehicle pitch/yaw/suspension values
            copy_vehicle_animation_block_data(antr_vehicles, prev_antr_vehicles)


    if (update_mode != ANIMATION_COMPILE_MODE_ADDITIVE and
        mod2_nodes and antr_units and not antr_vehicles):
        # only calculate node vectors for units that are not vehicles
        if len(antr_nodes) != len(mod2_nodes):
            errors.append("Gbxmodel node count does not match node "
                          "count in the model_animations tag.")
            return errors
        util.calculate_node_vectors(antr_nodes, mod2_nodes,
                                    jma_anim_set.animations.values())

    # fill in the remaining unit damages
    if antr_unit_damages:
        if len(antr_unit_damages) < 176:
            antr_unit_damages.extend(176 - len(antr_unit_damages))

        # loop over  s-ping, h-ping, s-kill, h-kill
        for i in range(0, len(antr_unit_damages), 44):
            # loop over each of the 11 animations per set
            for j in range(11):
                # make a collection of defaults for all sides of this region
                defaults = {i + j + k: -1 for k in (0, 11, 22, 33)}
                util.get_default_animation_enums(antr_unit_damages, defaults)

                # default any unset sides for this region
                util.set_default_animation_enums(antr_unit_damages, defaults)


    unit_anim_defaults = {enums.unit_animation_names.index(name): -1
                          for name in util.SHARED_UNIT_ANIMATION_NAMES}
    unit_weap_anim_defaults = {enums.unit_weapon_animation_names.index(name): -1
                               for name in util.SHARED_UNIT_WEAPON_ANIMATION_NAMES}

    # get the unit animations with applicable ones from all units.
    # do this in reverse since thats what tool seems to do.
    for unit in antr_units[::-1]:
        anim_enums = unit.animations.STEPTREE
        util.get_default_animation_enums(anim_enums, unit_anim_defaults)
        for unit_weap in unit.weapons.STEPTREE:
            anim_enums = unit_weap.animations.STEPTREE
            util.get_default_animation_enums(anim_enums, unit_weap_anim_defaults)

    # strip any unused animation indices
    unit_anim_defaults = {
        k: v for k, v in unit_anim_defaults.items() if v != -1}
    unit_weap_anim_defaults = {
        k: v for k, v in unit_weap_anim_defaults.items() if v != -1}

    for unit in antr_units:
        if unit_anim_defaults:
            anim_enums = unit.animations.STEPTREE
            anim_enums.extend(max(unit_anim_defaults) + 1 - len(anim_enums))

        if unit_weap_anim_defaults:
            for unit_weap in unit.weapons.STEPTREE:
                anim_enums = unit_weap.animations.STEPTREE
                anim_enums.extend(max(unit_weap_anim_defaults) + 1 - len(anim_enums))

    # default any unset unit animations with the found defaults.
    for unit in antr_units:
        util.set_default_animation_enums(unit.animations.STEPTREE,
                                         unit_anim_defaults)
        for unit_weap in unit.weapons.STEPTREE:
            util.set_default_animation_enums(unit_weap.animations.STEPTREE,
                                             unit_weap_anim_defaults)

    # setup permutation indices
    last_perm_anim_index = -1
    last_perm_name_pieces = ()
    # loop over the name pieces in a sorted manner so the lowest
    # permutations come first and are followed by the rest of them
    for name_pieces in sorted(antr_indices_by_type_strings):
        anim_index = antr_indices_by_type_strings[name_pieces]
        name_pieces, perm_num = name_pieces[: -1], name_pieces[-1]
        if (anim_index in indices_modified and
            name_pieces == last_perm_name_pieces and
            last_perm_anim_index != -1):
            antr_anims[last_perm_anim_index].next_animation = anim_index

        last_perm_anim_index = anim_index
        last_perm_name_pieces = name_pieces

    return errors


def copy_unit_animation_block_data(antr_units, prev_antr_units):
    for unit in antr_units:
        prev_unit = None
        # find the old unit with a label matching this one
        for block in prev_antr_units:
            if block.label == unit.label:
                prev_unit = block
                break

        if prev_unit is None: continue
        unit.right_yaw_per_frame  = prev_unit.right_yaw_per_frame
        unit.left_yaw_per_frame   = prev_unit.left_yaw_per_frame
        unit.right_frame_count    = prev_unit.right_frame_count
        unit.left_frame_count     = prev_unit.left_frame_count

        unit.down_pitch_per_frame = prev_unit.down_pitch_per_frame
        unit.up_pitch_per_frame   = prev_unit.up_pitch_per_frame
        unit.down_frame_count     = prev_unit.down_frame_count
        unit.up_frame_count       = prev_unit.up_frame_count

        unit.ik_points = deepcopy(prev_unit.ik_points)

        for unit_weap in unit.weapons.STEPTREE:
            prev_unit_weap = None
            # find the old unit with a label matching this one
            for block in prev_unit.weapons.STEPTREE:
                if block.name == unit_weap.name:
                    prev_unit_weap = block
                    break

            if prev_unit_weap is None: continue
            unit_weap.grip_marker  = prev_unit_weap.grip_marker
            unit_weap.hand_marker  = prev_unit_weap.hand_marker

            unit_weap.right_yaw_per_frame  = prev_unit_weap.right_yaw_per_frame
            unit_weap.left_yaw_per_frame   = prev_unit_weap.left_yaw_per_frame
            unit_weap.right_frame_count    = prev_unit_weap.right_frame_count
            unit_weap.left_frame_count     = prev_unit_weap.left_frame_count

            unit_weap.down_pitch_per_frame = prev_unit_weap.down_pitch_per_frame
            unit_weap.up_pitch_per_frame   = prev_unit_weap.up_pitch_per_frame
            unit_weap.down_frame_count     = prev_unit_weap.down_frame_count
            unit_weap.up_frame_count       = prev_unit_weap.up_frame_count

            unit_weap.ik_points = deepcopy(prev_unit_weap.ik_points)


def copy_vehicle_animation_block_data(antr_vehicles, prev_antr_vehicles):
    vehicle = antr_vehicles[0]
    prev_vehicle = prev_antr_vehicles[0]
    vehicle.right_yaw_per_frame  = prev_vehicle.right_yaw_per_frame
    vehicle.left_yaw_per_frame   = prev_vehicle.left_yaw_per_frame
    vehicle.right_frame_count    = prev_vehicle.right_frame_count
    vehicle.left_frame_count     = prev_vehicle.left_frame_count

    vehicle.down_pitch_per_frame = prev_vehicle.down_pitch_per_frame
    vehicle.up_pitch_per_frame   = prev_vehicle.up_pitch_per_frame
    vehicle.down_frame_count     = prev_vehicle.down_frame_count
    vehicle.up_frame_count       = prev_vehicle.up_frame_count

    suspensions = vehicle.suspension_animations.STEPTREE
    prev_suspensions = prev_vehicle.suspension_animations.STEPTREE
    for prev, new in zip(prev_suspensions, suspensions):
        new.mass_point_index = prev.mass_point_index
        new.full_extension_ground_depth   = prev.full_extension_ground_depth
        new.full_compression_ground_depth = prev.full_compression_ground_depth
