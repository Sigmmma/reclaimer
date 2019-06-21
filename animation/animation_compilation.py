import traceback

from copy import deepcopy
from math import pi
from struct import Struct as PyStruct

from reclaimer.enums import unit_animation_names, unit_weapon_animation_names,\
     unit_weapon_type_animation_names, vehicle_animation_names,\
     weapon_animation_names, device_animation_names, fp_animation_names,\
     unit_damage_animation_names

__all__ = ("compile_animation", "compile_model_animations",
           "ANIMATION_COMPILE_MODE_NEW", "ANIMATION_COMPILE_MODE_PRESERVE",
           "ANIMATION_COMPILE_MODE_ADDITIVE")

ANIMATION_COMPILE_MODE_NEW = 0
ANIMATION_COMPILE_MODE_PRESERVE = 1
ANIMATION_COMPILE_MODE_ADDITIVE = 2


def compile_animation(anim, jma_anim, ignore_size_limits=False):
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

    has_dxdy = "dx"   in jma_anim.frame_info_type
    has_dz   = "dz"   in jma_anim.frame_info_type
    has_dyaw = "dyaw" in jma_anim.frame_info_type

    anim.name = jma_anim.name
    anim.type.set_to(jma_anim.anim_type)
    anim.frame_count = stored_frame_count
    anim.frame_size = jma_anim.frame_data_frame_size
    anim.node_list_checksum = jma_anim.node_list_checksum
    anim.node_count = jma_anim.node_count
    anim.next_animation = -1

    if has_dz:
        anim.frame_info_type.data = 3
    elif has_dyaw:
        anim.frame_info_type.data = 2
    elif has_dxdy:
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


    anim.frame_info.STEPTREE   = bytearray(b'\x00' * frame_info_size)
    anim.default_data.STEPTREE = bytearray(b'\x00' * default_data_size)
    anim.frame_data.STEPTREE   = bytearray(b'\x00' * frame_data_size)

    frame_info   = anim.frame_info.STEPTREE
    default_data = anim.default_data.STEPTREE
    frame_data   = anim.frame_data.STEPTREE

    rot_flags   = jma_anim.rot_flags
    trans_flags = jma_anim.trans_flags
    scale_flags = jma_anim.scale_flags

    pack_1_float_into = PyStruct(">f").pack_into
    pack_2_float_into = PyStruct(">2f").pack_into
    pack_3_float_into = PyStruct(">3f").pack_into
    pack_4_float_into = PyStruct(">4f").pack_into
    pack_4_int16_into = PyStruct(">4h").pack_into

    is_overlay = jma_anim.anim_type == "overlay"
    def_state = None
    i = j = k = 0

    for f in range(jma_anim.frame_count):
        if not is_overlay and f == stored_frame_count:
            # skip the last frame for non-overlays
            break

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


        # write to the default_data
        if f == 0:
            for n in range(anim.node_count):
                node_state = jma_anim.frames[f][n]
                if not rot_flags[n]:
                    pack_4_int16_into(default_data, j,
                        int(node_state.rot_i*32767),
                        int(node_state.rot_j*32767),
                        int(node_state.rot_k*32767),
                        int(node_state.rot_w*32767))
                    j += 8

                if not trans_flags[n]:
                    pack_3_float_into(default_data, j,
                        node_state.pos_x / 100,
                        node_state.pos_y / 100,
                        node_state.pos_z / 100)
                    j += 12

                if not scale_flags[n]:
                    pack_1_float_into(default_data, j, node_state.scale)
                    j += 4

            if is_overlay:
                # skip the first frame for overlays
                continue


        # write to the frame_data
        for n in range(anim.node_count):
            node_state = jma_anim.frames[f][n]

            if rot_flags[n]:
                pack_4_int16_into(frame_data, k,
                    int(node_state.rot_i*32767),
                    int(node_state.rot_j*32767),
                    int(node_state.rot_k*32767),
                    int(node_state.rot_w*32767))
                k += 8

            if trans_flags[n]:
                pack_3_float_into(frame_data, k,
                    node_state.pos_x / 100,
                    node_state.pos_y / 100,
                    node_state.pos_z / 100)
                k += 12

            if scale_flags[n]:
                pack_1_float_into(frame_data, k, node_state.scale)
                k += 4

    return errors


def compile_model_animations(antr_tag, jma_anim_set, ignore_size_limits=False,
                             animation_count_limit=256, delta_tolerance=None,
                             update_mode=ANIMATION_COMPILE_MODE_PRESERVE):
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
                antr_node.parent_node_index       != jma_node.parent_index or
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

        if i not in range(len(prev_antr_nodes)):
            continue

        prev_antr_node = prev_antr_nodes[i]
        if prev_antr_node.name.lower() == antr_node.name.lower():
            antr_node.node_joint_flags.data = prev_antr_node.node_joint_flags.data
            antr_node.base_vector[:] = prev_antr_node.base_vector
            antr_node.vector_range   = prev_antr_node.vector_range

    # cache the old animations by their names
    for i in range(len(prev_antr_anims)):
        anim = prev_antr_anims[i]
        _, name_pieces = split_anim_name_into_type_strings(anim.name.strip())
        prev_antr_anims_by_type_strings[name_pieces] = anim

    # cache the existing animation indices by their names
    for i in range(len(antr_anims)):
        anim = antr_anims[i]
        _, name_pieces = split_anim_name_into_type_strings(anim.name.strip())
        antr_indices_by_type_strings[name_pieces] = i


    indices_to_not_overwrite = set()
    for jma_anim_name in sorted(jma_anim_set.animations):
        name = jma_anim_name.strip()
        has_purpose, name_pieces = split_anim_name_into_type_strings(name)

        # find where to put this animation
        anim_index = antr_indices_by_type_strings.get(
            name_pieces, len(antr_anims))

        if anim_index > animation_count_limit:
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
            errors.append("Couldnt compile '%s'" % jma_anim_name)
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
            print("    No determinable purpose for this animation")
            continue

        try:
            if set_animation_index(antr_tag, jma_anim_name, anim_index,
                                   indices_to_not_overwrite):
                # successfully found an animation index to use this animation
                indices_to_not_overwrite.add(anim_index)
        except Exception:
            errors.append(traceback.format_exc())
            

    if update_mode == ANIMATION_COMPILE_MODE_PRESERVE:
        for i in range(len(prev_antr_objects)):
            prev_obje = prev_antr_objects[i]
            if prev_obje.animation not in range(len(prev_antr_anims)):
                continue

            _, name_pieces = split_anim_name_into_type_strings(
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

    # fill in the remaining unit damages
    if antr_unit_damages:
        if len(antr_unit_damages) < 176:
            antr_unit_damages.extend(176 - len(antr_unit_damages))

        # loop over  s-ping, h-ping, s-kill, h-kill
        for i in range(0, len(antr_unit_damages), 44):
            # loop over each of the 11 animations per set
            for j in range(11):
                # all sides default to front
                def_anim_index = -1
                for k in range(0, 44, 11):
                    def_anim_index = antr_unit_damages[i + j + k].animation
                    if def_anim_index >= 0: break

                if def_anim_index < 0:
                    continue

                # fill in the rest of the unit damage sides
                for k in (0, 11, 22, 33):
                    block = antr_unit_damages[i + j + k]
                    if block.animation < 0:
                        block.animation = def_anim_index

    # setup permutation indices
    last_perm_anim_index = -1
    last_perm_name_pieces = ()
    # loop over the name pieces in a sorted manner so the lowest
    # permutations come first and are followed by the rest of them
    for name_pieces in sorted(antr_indices_by_type_strings):
        anim_index = antr_indices_by_type_strings[name_pieces]

        name_pieces, perm_num = name_pieces[: -1], name_pieces[-1]
        if name_pieces == last_perm_name_pieces and last_perm_anim_index != -1:
            antr_anims[last_perm_anim_index].next_animation = anim_index

        last_perm_anim_index = anim_index
        last_perm_name_pieces = name_pieces


    # TODO: fill in missing unit animations with ones from units that have them
    #   for the first 12 unit animations, any that are undefined
    #   for that specific unit will default to the first one found.
    #       Ex: "P-riderLB02 emotions" defaulting to "stand emotions"
    #   same thing for each unit weapon across ALL weapons across ALL units
    #   same thing for each unit weapon type across ALL weapons across ALL
    #       units, EXCEPT that the label of the weapon types must match

    # TODO: Calculate node base vectors and vector ranges

    return errors


def set_animation_index(antr_tag, anim_name, anim_index,
                        indices_to_not_overwrite=()):
    orig_anim_name = anim_name

    tagdata = antr_tag.data.tagdata
    antr_units    = tagdata.units.STEPTREE
    antr_weapons  = tagdata.weapons.STEPTREE
    antr_vehicles = tagdata.vehicles.STEPTREE
    antr_devices  = tagdata.devices.STEPTREE
    antr_unit_damages  = tagdata.unit_damages.STEPTREE
    antr_fp_animations = tagdata.fp_animations.STEPTREE
    antr_anims = tagdata.animations.STEPTREE
    antr_nodes = tagdata.nodes.STEPTREE

    _, name_pieces = split_anim_name_into_type_strings(anim_name)
    name_pieces = list(name_pieces)
    perm_num = name_pieces.pop(-1)

    part1 = name_pieces[0] if len(name_pieces) > 0 else ""
    part2 = name_pieces[1] if len(name_pieces) > 1 else ""
    part3 = name_pieces[2] if len(name_pieces) > 2 else ""
    part4 = name_pieces[3] if len(name_pieces) > 3 else ""

    if part1 in ("vehicle", "suspension") and len(antr_vehicles) < 1:
        # default right/left yaw/pitch to 1 frame count
        # and yaw and pitch to 60 each
        antr_vehicles.append()
        block = antr_vehicles[0]
        block.right_frame_count = block.left_frame_count = 1
        block.down_frame_count  = block.up_frame_count   = 1
        block.right_yaw_per_frame  = block.left_yaw_per_frame = pi / 3
        block.down_pitch_per_frame = block.up_pitch_per_frame = pi / 3

    if part1 == "suspension":
        anim_name = anim_name.split(" ", 1)[1]
        anim_enums = antr_vehicles[0].suspension_animations.STEPTREE
        if len(anim_enums) >= 8:
            # max of 8 suspension animations
            return False

        anim_enums.append()
        anim_enums[-1].animation = anim_index
        return True

    elif part1 in ("first-person", "device", "vehicle"):
        if part1 == "first-person":
            options = fp_animation_names
            block = antr_fp_animations
        elif part1 == "device":
            options = device_animation_names
            block = antr_devices
        elif part1 == "vehicle":
            options = vehicle_animation_names
            block = antr_vehicles

        if not block:
            block.append()

        try:
            enum_index = options.index(part2)
        except ValueError:
            return False

        return set_animation_enum_index(block[0].animations.STEPTREE, enum_index,
                                        anim_index, indices_to_not_overwrite)

    elif part1 in ("s-ping", "h-ping", "s-kill", "h-kill"):
        # divided into 16 chunks of 11 sets of animations
        #   NOTE: Defaults to "gut" if no matches can be found
        #         Otherwise, defaults to the first matching
        #         region. Ex:  l-hand will default to chest if
        #                      l-hand and l-arm are missing
        #  0  ==  gut                       1  ==  chest
        #  2  ==  head / chest              3  ==  l-arm / chest
        #  4  ==  l-hand / l-arm / chest    5  ==  l-leg
        #  6  ==  l-foot / l-leg            7  ==  r-arm / chest
        #  8  ==  r-hand / l-arm / chest    9  ==  r-leg
        # 10  ==  r-foot / r-leg
        #
        # this means that the unit-damages should be set in this order:
        #     r-foot, r-leg, r-hand, r-arm,
        #     l-foot, l-leg, l-hand, l-arm,
        #     head, chest, gut
        #
        # and make sure to set lowest number permutation first
        #
        # each of these sections of 44 is divided into 4
        # sections of 11 animations, each in this order:
        #     front, left, right, back
        #
        #   0 -  43  ==  s-ping
        #  44 -  87  ==  h-ping
        #  88 - 131  ==  s-kill
        # 132 - 175  ==  h-kill
        #
        # so for example, "s-kill right l-foot" would be
        # 88 + 11*2 + 6   which is index 116

        try:
            enum_index = unit_damage_animation_names.index(
                " ".join((part1, part2, part3))
                )
            base = (enum_index // 11) * 11
            enum_index = enum_index % 11
        except ValueError:
            return False

        if len(antr_unit_damages) < 176:
            antr_unit_damages.extend(176 - len(antr_unit_damages))

        indices_to_set = range(1, 11)
        if   enum_index == 1: indices_to_set = [2, 3, 4, 7, 8]
        elif enum_index == 3: indices_to_set = [4]
        elif enum_index == 5: indices_to_set = [6]
        elif enum_index == 7: indices_to_set = [8]
        elif enum_index == 9: indices_to_set = [10]

        if not set_animation_enum_index(antr_unit_damages, base + enum_index,
                                        anim_index, indices_to_not_overwrite):
            return False

        # set any that havent been set to anything
        for i in indices_to_set:
            block = antr_unit_damages[base + i]
            if block.animation < 0:
                block.animation = anim_index

        return True

    elif part1 in weapon_animation_names:
        enum_index = weapon_animation_names.index(part1)
        if len(antr_weapons) < 1:
            antr_weapons.append()

        return set_animation_enum_index(antr_weapons[0].animations.STEPTREE,
                                        enum_index, anim_index,
                                        indices_to_not_overwrite)

    # something in the units
    if part2 in unit_animation_names:
        typ = 1
        enum_index = unit_animation_names.index(part2)
    elif part3 in unit_weapon_animation_names:
        typ = 2
        enum_index = unit_weapon_animation_names.index(part3)
    elif part4 in unit_weapon_type_animation_names:
        typ = 3
        enum_index = unit_weapon_type_animation_names.index(part4)
    else:
        return False

    unit = None
    for block in antr_units:
        if block.label == part1:
            unit = block
            break

    if unit is None:
        if len(antr_units) >= antr_units.MAX:
            return False

        antr_units.append()
        unit = antr_units[-1]

        unit.label = part1
        # default right/left yaw/pitch to 1 frame count
        # and yaw and pitch to 60 each
        unit.right_frame_count = unit.left_frame_count = 1
        unit.down_frame_count  = unit.up_frame_count   = 1
        unit.right_yaw_per_frame  = unit.left_yaw_per_frame = pi / 3
        unit.down_pitch_per_frame = unit.up_pitch_per_frame = pi / 3

        # tool likes to have the first 12 always exist, even if unset
        unit.animations.STEPTREE.extend(12)

    if typ == 1:
        # unit animation
        return set_animation_enum_index(unit.animations.STEPTREE, enum_index,
                                        anim_index, indices_to_not_overwrite)


    unit_weaps = unit.weapons.STEPTREE
    unit_weap = None
    for block in unit_weaps:
        if block.name == part2:
            unit_weap = block
            break

    if unit_weap is None:
        if len(unit_weaps) >= unit_weaps.MAX:
            return False

        unit_weaps.append()
        unit_weap = unit_weaps[-1]

        unit_weap.name = part2
        # default right/left yaw/pitch to 1 frame count
        # and yaw and pitch to 60 each
        unit_weap.right_frame_count = unit_weap.left_frame_count = 1
        unit_weap.down_frame_count  = unit_weap.up_frame_count   = 1
        unit_weap.right_yaw_per_frame  = unit_weap.left_yaw_per_frame = pi / 3
        unit_weap.down_pitch_per_frame = unit_weap.up_pitch_per_frame = pi / 3

    if typ == 2:
        # unit weapon animation
        return set_animation_enum_index(unit_weap.animations.STEPTREE,
                                        enum_index, anim_index,
                                        indices_to_not_overwrite)

    unit_weap_types = unit_weap.weapon_types.STEPTREE
    unit_weap_type = None
    for block in unit_weap_types:
        if block.label == part2:
            unit_weap_type = block
            break

    if unit_weap_type is None:
        if len(unit_weap_types) >= unit_weap_types.MAX:
            return False

        unit_weap_types.append()
        unit_weap_type = unit_weap_types[-1]
        unit_weap_type.label = part3

    # unit weapon type animation
    return set_animation_enum_index(unit_weap_type.animations.STEPTREE,
                                    enum_index, anim_index,
                                    indices_to_not_overwrite)


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

        unit.ik_points.STEPTREE = deepcopy(prev_unit.ik_points.STEPTREE)

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

            unit_weap.ik_points.STEPTREE = deepcopy(prev_unit_weap.ik_points.STEPTREE)


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


def split_anim_name_into_type_strings(anim_name):
    anim_name_len = -1
    while len(anim_name) != anim_name_len:
        anim_name_len = len(anim_name)
        anim_name = anim_name.replace("  ", " ")

    name_pieces = anim_name.split(" ", 4)
    part1 = name_pieces[0] if len(name_pieces) > 0 else ""
    part2 = name_pieces[1] if len(name_pieces) > 1 else ""
    part3 = name_pieces[2] if len(name_pieces) > 2 else ""
    part4 = name_pieces[3] if len(name_pieces) > 3 else ""

    part1_sani = part1.lower().replace("_", "-")
    part2_sani = part2.lower().replace("_", "-")
    part3_sani = part3.lower().replace("_", "-")
    part4_sani = part4.lower().replace("_", "-")

    remainder = " ".join(name_pieces[4: ])

    type_strings = ()
    perm_num = ""

    if part1_sani == "suspension":
        if part4: remainder = " ".join((part4, remainder))
        if part3: remainder = " ".join((part3, remainder))
        if part2: remainder = " ".join((part2, remainder))

        remainder, _, perm_num = split_permutation_number(remainder)
        type_strings = part1_sani, remainder.lower(), perm_num
        remainder = ""

    elif part1_sani in ("first-person", "device", "vehicle"):
        if part4: remainder = " ".join((part4, remainder))
        if part3: remainder = " ".join((part3, remainder))

        part2, part2_sani, perm_num = split_permutation_number(part2, remainder)
        if ((part1_sani == "first-person" and part2_sani in fp_animation_names) or
            (part1_sani == "vehicle" and part2_sani in vehicle_animation_names) or
            (part1_sani == "device"  and part2_sani in device_animation_names)):
            type_strings = part1_sani, part2_sani, perm_num

    elif (part1_sani in ("s-ping", "h-ping", "s-kill", "h-kill") and
          part2_sani in ("front", "left", "right", "back")):

        if part4: remainder = " ".join((part4, remainder))

        part3, part3_sani, perm_num = split_permutation_number(part3, remainder)
        if part3_sani in ("gut", "chest", "head", "l-arm", "l-hand", "l-leg",
                          "l-foot", "r-arm", "r-hand", "r-leg", "r-foot"):
            type_strings = part1_sani, part2_sani, part3_sani, perm_num

    else:
        part4, part4_sani, perm_num = split_permutation_number(part4, remainder)
        if part4_sani in unit_weapon_type_animation_names:
            type_strings = part1, part2, part3, part4_sani, perm_num

        else:
            part3, part3_sani, perm_num = split_permutation_number(part3, remainder)
            if part3_sani in unit_weapon_animation_names:
                if part4: remainder = " ".join((part4, remainder))

                type_strings = part1, part2, part3_sani, perm_num

            else:
                part2, part2_sani, perm_num = split_permutation_number(part2, remainder)
                if part2_sani in unit_animation_names:
                    if part4: remainder = " ".join((part4, remainder))
                    if part3: remainder = " ".join((part3, remainder))

                    type_strings = part1, part2_sani, perm_num
                else:
                    remainder = True
    
    # nothing should have a remainder. if it does, it doesnt fit the criteria,
    # and we should just return it split at the permutation character
    if remainder:
        name_pieces = anim_name.lower().split("%")
        if len(name_pieces) > 1:
            anim_name = "%".join(name_pieces[: -1])
            perm_num  = name_pieces[-1]

        return False, (anim_name, perm_num)
    
    return True, type_strings


def split_permutation_number(*strings):
    string = " ".join(s for s in strings if s)
    pieces = string.split("%")
    part0 = pieces[0]
    sani_part0 = part0.lower().replace("_", "-")
    if len(pieces) > 1:
        return part0, sani_part0, pieces[1].lstrip()
    return part0, sani_part0, ""


def set_animation_enum_index(anim_enums, enum_index, anim_index,
                             indices_to_not_overwrite):
    if enum_index >= len(anim_enums):
        anim_enums.extend(enum_index + 1 - len(anim_enums))

    if anim_enums[enum_index].animation in indices_to_not_overwrite:
        return False
    anim_enums[enum_index].animation = anim_index
    return True
