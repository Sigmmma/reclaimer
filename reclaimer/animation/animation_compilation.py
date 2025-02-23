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
from reclaimer.animation import animation_compression, constants as const,\
     serialization, util

__all__ = ("compile_animation", "compile_model_animations")

def compile_animation(anim, jma_anim, endian=">", ignore_size_limits=False):
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

    max_frame_info_size   = util.get_block_max(anim.frame_info)
    max_default_data_size = util.get_block_max(anim.default_data)
    max_frame_data_size   = util.get_block_max(anim.frame_data)

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

    if ((jma_anim.root_node_info_applied and jma_anim.has_frame_info) or
        (jma_anim.overlay_base_applied   and jma_anim.is_overlay)):
        # clone the anim since we need to modify all the frames
        jma_anim = deepcopy(jma_anim)

        # remove root info from other frames, and make
        # overlay frames relative to the initial frame
        jma_anim.apply_base_pose_to_states(True)
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
    frame_data = serialization.serialize_uncomp_frame_data(jma_anim, endian)

    anim.frame_info.STEPTREE = frame_info
    anim.default_data.STEPTREE = def_data
    anim.frame_data.STEPTREE = frame_data

    return errors


def compile_model_animations(
        antr_tag, jma_anim_set, ignore_size_limits=False,
        update_mode=const.ANIMATION_COMPILE_MODE_PRESERVE,
        compression_mode=const.ANIMATION_COMPRESS_MODE_USE_FLAG,
        delta_tolerance=None, compress_quality=1.0,
        endian=">", fix_anim_types=True,
        physics_calc_mode=const.PHYSICS_CALC_MODE_GUESS,
        rename_map=()
        ):
    make_new = (update_mode == const.ANIMATION_COMPILE_MODE_NEW)
    add_only = (update_mode == const.ANIMATION_COMPILE_MODE_ADDITIVE)
    preserve = (update_mode == const.ANIMATION_COMPILE_MODE_PRESERVE)
    errors = []

    tagdata = antr_tag.data.tagdata
    flags = tagdata.flags
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
    if add_only and antr_nodes:
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
    prev_antr_nodes    = list(antr_nodes)
    prev_antr_anims    = list(antr_anims)
    assert update_mode in (const.ANIMATION_COMPILE_MODE_NEW,
                           const.ANIMATION_COMPILE_MODE_PRESERVE,
                           const.ANIMATION_COMPILE_MODE_ADDITIVE)
    if make_new:
        del tagdata.sound_references.STEPTREE[:]
        tagdata.limp_body_node_radius = 0.0
        flags.data = 0
        del prev_antr_objects[:]
        del prev_antr_units[:]
        del prev_antr_vehicles[:]
        del prev_antr_nodes[:]
        del prev_antr_anims[:]

    if not add_only:
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

            prev_antr_node = prev_antr_nodes[i]
            if prev_antr_node.name.lower() == antr_node.name.lower():
                antr_node.node_joint_flags.data = prev_antr_node.node_joint_flags.data
                antr_node.base_vector[:] = prev_antr_node.base_vector
                antr_node.vector_range   = prev_antr_node.vector_range

    use_tag_fields  = compression_mode == const.ANIMATION_COMPRESS_MODE_USE_FLAG
    compress_all    = use_tag_fields and flags.compress_all_animations
    compress_idle   = use_tag_fields and flags.force_idle_compression

    if compression_mode == const.ANIMATION_COMPRESS_MODE_IF_BETTER:
        compress_all = True

    has_mozz_fields = hasattr(flags, "mozz_enable_compress_fields")
    use_mozz_fields = (use_tag_fields and has_mozz_fields and
                       flags.mozz_enable_compress_fields)
    can_compress = not (use_mozz_fields and flags.mozz_never_compress)

    if use_mozz_fields:
        compress_quality  = tagdata.mozz_compress_quality
    elif has_mozz_fields and not add_only:
        tagdata.mozz_compress_quality = int(max(min(compress_quality, 100), 0))

    # cache the old animations by their names
    for i in range(len(prev_antr_anims)):
        anim = prev_antr_anims[i]
        name_key = util.split_anim_name_into_type_strings(anim.name.strip())
        prev_antr_anims_by_type_strings[name_key] = anim

    # cache the existing animation indices by their names
    for i in range(len(antr_anims)):
        anim = antr_anims[i]
        name_key = util.split_anim_name_into_type_strings(anim.name.lower().strip())
        antr_indices_by_type_strings[name_key] = i


    indices_to_retain   = set()
    indices_modified    = set()
    total_uncomp_sizes  = dict()
    total_comp_sizes    = dict()
    # loop over the animations to add/replace them
    for jma_anim_name in sorted(jma_anim_set.animations):
        name = jma_anim_name.strip()
        name_key = util.split_anim_name_into_type_strings(name.lower())
        has_purpose, name_pieces, perm_name = name_key

        jma_anim = jma_anim_set.animations[jma_anim_name]

        # find where to put this animation
        anim_index = antr_indices_by_type_strings.get(name_key, len(antr_anims))

        if anim_index >= util.get_block_max(tagdata.animations):
            errors.append(
                "Too many animations. Cannot add '%s'" % jma_anim_name)
            continue

        if has_purpose:
            expected = util.get_expected_anim_types(name)
            if expected and jma_anim.anim_type not in expected:
                print("Warning: Expected type of %s for '%s', but got %s.%s" %
                      (expected, jma_anim_name, jma_anim.anim_type,
                       " Fixing." if fix_anim_types else ""))
                if fix_anim_types:
                    jma_anim.anim_type = expected[0]

        is_idle    = has_purpose and "idle" in name_pieces
        anim_added = False
        if anim_index == len(antr_anims):
            anim_added = True
            antr_anims.append()
            print("Adding '%s'" % jma_anim_name)
        else:
            print("Replacing '%s'" % jma_anim_name)

        anim  = antr_anims[anim_index]
        flags = anim.flags
        try:
            jma_anim.calculate_animation_flags(delta_tolerance)
            errors.extend(compile_animation(
                anim, jma_anim, endian, ignore_size_limits
                ))
        except Exception:
            errors.append(traceback.format_exc())
            errors.append("Could not compile '%s'" % jma_anim_name)
            if anim_added:
                antr_anims.pop(anim_index)

            continue

        # update the antr indices with this animations index
        antr_indices_by_type_strings[name_key] = anim_index

        prev_anim = prev_antr_anims_by_type_strings.get(name_key)
        if prev_anim:
            # update the animation with the old ones keyframe values and such
            anim.weight, anim.sound     = prev_anim.weight, prev_anim.sound
            anim.loop_frame_index       = prev_anim.loop_frame_index
            anim.key_frame_index        = prev_anim.key_frame_index
            anim.second_key_frame_index = prev_anim.second_key_frame_index
            anim.sound_frame_index      = prev_anim.sound_frame_index
            anim.left_foot_frame_index  = prev_anim.left_foot_frame_index
            anim.right_foot_frame_index = prev_anim.right_foot_frame_index
            if has_mozz_fields:
                flags.mozz_override_quality = prev_anim.flags.mozz_override_quality
                flags.mozz_always_compress  = prev_anim.flags.mozz_always_compress
                flags.mozz_never_compress   = prev_anim.flags.mozz_never_compress
                anim.mozz_compress_quality  = prev_anim.mozz_compress_quality

        # determine if we're able to try to compress this animation
        if can_compress and not jma_anim.is_overlay and (
                (compress_idle and is_idle) or compress_all
                ):
            jma_anim.compress_quality = compress_quality

            if (use_mozz_fields and flags.mozz_override_quality and
                anim.mozz_compress_quality >= 0 and
                anim.mozz_compress_quality <= 100):
                jma_anim.compress_quality = anim.mozz_compress_quality/100

            # do the compression
            animation_compression.compress_animation(
                anim, jma_anim=jma_anim, recalculate_keyframes=True
                )

            uncomp_len = anim.offset_to_compressed_data
            comp_len   = len(anim.frame_data.STEPTREE) - uncomp_len

            if comp_len >= uncomp_len:
                # not worth compressing
                flags.compressed_data = False
                anim.frame_data.STEPTREE = anim.frame_data.STEPTREE[: uncomp_len]
            else:
                total_uncomp_sizes[jma_anim_name] = uncomp_len
                total_comp_sizes[jma_anim_name]   = comp_len

        has_purpose or print("Could not determine a purpose for '%s'" % jma_anim_name)
        if not has_purpose or add_only:
            continue

        try:
            if util.set_animation_index(antr_tag, jma_anim_name, anim_index,
                                        indices_to_retain):
                # successfully found an animation index to use this animation
                indices_to_retain.add(anim_index)
            indices_modified.add(anim_index)
        except Exception:
            errors.append(traceback.format_exc())

    # loop over the animation map to map existing anims to them
    for dst_name in sorted([] if add_only else rename_map):
        src_name = rename_map[dst_name]
        name_key = util.split_anim_name_into_type_strings(src_name.lower())
        purpose  = util.split_anim_name_into_type_strings(dst_name.lower())[0]

        if not purpose:
            print("Could not determine a purpose for '%s'" % dst_name)
            continue

        # find which anim we're reusing
        anim_index = antr_indices_by_type_strings.get(name_key)
        if anim_index is None:
            print("Warning: No existing animation '%s' to reuse." % src_name)
            continue

        src_type = antr_anims[anim_index].type.enum_name
        expected = util.get_expected_anim_types(dst_name)
        if expected and src_type not in expected:
            print("Warning: Expected type of %s for '%s', but got '%s'." %
                  (expected, dst_name, src_type))

        try:
            if util.set_animation_index(antr_tag, dst_name, anim_index,
                                        indices_to_retain):
                # successfully found an animation index to use this animation
                print("Reusing '%s' for '%s'" % (src_name, dst_name))
                indices_to_retain.add(anim_index)
            indices_modified.add(anim_index)
        except Exception:
            errors.append(traceback.format_exc())

    if total_comp_sizes:
        print("Compression savings:")
        total_uncomp_size  = sum(total_uncomp_sizes.values())
        total_comp_size    = sum(total_comp_sizes.values())
        names              = [*sorted(total_uncomp_sizes), "Total"]
        total_uncomp_sizes["Total"] = total_uncomp_size
        total_comp_sizes["Total"]   = total_comp_size
        max_width          = max(9, *(len(name) for name in total_uncomp_sizes))

        print("  animation name  %sbytes removed   \t%% of total removed" % (
            " "*(max_width - 12)
            ))
        for name in names:
            usize, csize = total_uncomp_sizes[name], total_comp_sizes[name]
            diff = usize - csize
            print("  %s   %s%d bytes (%0.1f%%) \t%0.3f%% of total" % (
                name, " "*(1 + max_width - len(name)), diff,
                100*diff/usize, 100*diff/total_uncomp_size,
                ))

    if preserve:
        for i, prev_obje in enumerate(prev_antr_objects):
            if prev_obje.animation not in range(len(prev_antr_anims)):
                continue

            name_key = util.split_anim_name_into_type_strings(
                prev_antr_anims[prev_obje.animation].name.strip())

            new_anim_index = antr_indices_by_type_strings.get(name_key)
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


    # setup permutation indices
    last_perm_anim_index = -1
    last_perm_name_pieces = ()
    # loop over the name pieces in a sorted manner so the lowest
    # permutations come first and are followed by the rest of them
    for name_key in sorted(antr_indices_by_type_strings):
        anim_index = antr_indices_by_type_strings[name_key]
        _, name_pieces, perm_num = name_key
        if (anim_index in indices_modified and
            name_pieces == last_perm_name_pieces and
            last_perm_anim_index != -1):
            antr_anims[last_perm_anim_index].next_animation = anim_index

        last_perm_anim_index = anim_index
        last_perm_name_pieces = name_pieces

    if add_only:
        # don't touch blocks in additive mode
        return errors

    is_biped = antr_units and not antr_vehicles
    if (physics_calc_mode == const.PHYSICS_CALC_MODE_ALWAYS or
        (physics_calc_mode == const.PHYSICS_CALC_MODE_GUESS and is_biped)):
        print("Calculating limp physics vectors")
        # calculate the biped limp node vectors
        jma_anim_set.calculate_limp_node_data()

        for antr_node, info in zip(
                antr_nodes, jma_anim_set.limp_node_infos
                ):
            antr_node.node_joint_flags.data = info.joint_flags
            antr_node.base_vector[:]        = info.vector_ortho
            antr_node.vector_range          = info.vector_range

    # final tag cleanup(i.e. fill missing anims, remove unused blocks, etc.)
    util.sanitize_animation_indices(antr_tag)

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
