import traceback

from copy import deepcopy
from math import pi
from struct import Struct as PyStruct

from reclaimer.enums import unit_animation_names, unit_weapon_animation_names,\
     unit_weapon_type_animation_names, vehicle_animation_names,\
     weapon_animation_names, device_animation_names, fp_animation_names,\
     unit_damage_animation_names

__all__ = ("compile_animation", "compile_model_animations", )


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


def compile_model_animations(antr_tag, jma_anim_set, ignore_size_limits=False,
                             animation_delta_tolerance=None, additive=False,
                             preserve_old_values=True):
    # TODO: Make this function able to be additive to where
    #       it doesn't remove anything, only adds. If an
    #       animation already exists with the name of one in
    #       the jma_anim_set, it'll update it
    errors = []

    antr_units = antr_tag.data.tagdata.units.STEPTREE
    antr_weapons = antr_tag.data.tagdata.weapons.STEPTREE
    antr_vehicles = antr_tag.data.tagdata.vehicles.STEPTREE
    antr_devices = antr_tag.data.tagdata.devices.STEPTREE
    antr_unit_damages = antr_tag.data.tagdata.unit_damages.STEPTREE
    antr_fp_animations = antr_tag.data.tagdata.fp_animations.STEPTREE
    antr_anims = antr_tag.data.tagdata.animations.STEPTREE
    antr_nodes = antr_tag.data.tagdata.nodes.STEPTREE

    old_antr_weapons = []
    old_antr_vehicles = []
    if not additive:
        if preserve_old_values:
            old_antr_weapons[:] = antr_weapons
            old_antr_vehicles[:] = antr_vehicles
        del antr_weapons[:]
        del antr_vehicles[:]
        del antr_devices[:]
        del antr_unit_damages[:]
        del antr_fp_animations[:]
        del antr_nodes[:]
        del antr_anims[:]

    for jma_node in jma_anim_set.nodes:
        antr_nodes.append()
        antr_node = antr_nodes[-1]
        antr_node.name = jma_node.name
        antr_node.next_sibling_node_index = jma_node.sibling_index
        antr_node.first_child_node_index = jma_node.first_child
        antr_node.parent_node_index = jma_node.parent_index

    indices_to_not_overwrite = set()
    for jma_anim_name in sorted(jma_anim_set.animations):
        anim_index = len(antr_anims)
        antr_anims.append()
        try:
            jma_anim = jma_anim_set.animations[jma_anim_name]
            jma_anim.calculate_animation_flags(animation_delta_tolerance)
            compile_animation(antr_anims[-1], jma_anim,
                              ignore_size_limits)
        except Exception:
            errors.append(traceback.format_exc())
            print("Couldnt compile '%s'" % jma_anim_name)
            antr_anims.pop(-1)
            continue

        # determine where this animation is to be used
        name_pieces = jma_anim_name.strip().split(" ", 1)
        prefix = ""
        if len(name_pieces) > 1:
            prefix = name_pieces[0].lower().replace("_", "-")

        if prefix in weapon_animation_names and len(antr_weapons) < 1:
            antr_weapons.append()
        elif prefix == "vehicle" and len(antr_vehicles) < 1:
            # default right/left yaw/pitch to 1 frame count
            # and yaw and pitch to 60 each
            antr_vehicles.append()
            block = antr_vehicles[0]
            block.right_frame_count = block.left_frame_count = 1
            block.down_frame_count  = block.up_frame_count   = 1
            block.right_yaw_per_frame  = block.left_yaw_per_frame = pi / 3
            block.down_pitch_per_frame = block.up_pitch_per_frame = pi / 3
        elif prefix == "device" and len(antr_devices) < 1:
            antr_devices.append()
        elif prefix in ("s-ping", "h-ping", "s-kill", "h-kill"):
            antr_unit_damages.extend(176 - len(antr_unit_damages))
        elif prefix == "first-person" and len(antr_fp_animations) < 1:
            antr_fp_animations.append()
        else:
            # setup unit entries
            pass

        if set_animation_index(antr_tag, jma_anim_name, anim_index,
                               indices_to_not_overwrite):
            # successfully found an animation index to use this animation
            indices_to_not_overwrite.add(anim_index)

    if antr_units and old_antr_units:
        # preserve any old unit pitch/yaw/weapon values
        copy_unit_animation_block_data(antr_units, old_antr_units)

    if antr_vehicles and old_antr_vehicles:
        # preserve any old vehicle pitch/yaw/suspension values
        copy_vehicles_animation_block_data(antr_vehicles, old_antr_vehicles)

    if antr_unit_damages:
        # loop over  s-ping, h-ping, s-kill, h-kill
        for i in range(0, len(antr_unit_damages), 44):
            # fill in the rest of the unit damage sides
            for j in range(11):
                # all sides default to front
                def_anim_index = -1
                for k in range(0, 44, 11):
                    def_anim_index = antr_unit_damages[i + j + k].animation
                    if def_anim_index >= 0: break

                if def_anim_index < 0:
                    continue

                for k in range(0, 44, 11):
                    block = antr_unit_damages[i + j + k]
                    if block.animation < 0:
                        block.animation = def_anim_index

    # TODO: Setup permutation indices
    #       Calculate node base vectors and vector ranges

    return errors


def copy_units_animation_block_data(antr_units, old_antr_units):
    for unit in antr_units:
        old_unit = None
        # find the old unit with a label matching this one
        for block in old_antr_units:
            if block.label == unit.label:
                old_unit = block
                break

        if old_unit is None: continue
        unit.right_yaw_per_frame  = old_unit.right_yaw_per_frame
        unit.left_yaw_per_frame   = old_unit.left_yaw_per_frame
        unit.right_frame_count    = old_unit.right_frame_count
        unit.left_frame_count     = old_unit.left_frame_count

        unit.down_pitch_per_frame = old_unit.down_pitch_per_frame
        unit.up_pitch_per_frame   = old_unit.up_pitch_per_frame
        unit.down_frame_count     = old_unit.down_frame_count
        unit.up_frame_count       = old_unit.up_frame_count

        unit.ik_points.STEPTREE = deepcopy(old_unit.ik_points.STEPTREE)

        for unit_weap in unit.weapons.STEPTREE:
            old_unit_weap = None
            # find the old unit with a label matching this one
            for block in old_unit.weapons.STEPTREE:
                if block.name == unit_weap.name:
                    old_unit_weap = block
                    break

            if old_unit_weap is None: continue
            unit_weap.grip_marker  = old_unit_weap.grip_marker
            unit_weap.hand_marker  = old_unit_weap.hand_marker

            unit_weap.right_yaw_per_frame  = old_unit_weap.right_yaw_per_frame
            unit_weap.left_yaw_per_frame   = old_unit_weap.left_yaw_per_frame
            unit_weap.right_frame_count    = old_unit_weap.right_frame_count
            unit_weap.left_frame_count     = old_unit_weap.left_frame_count

            unit_weap.down_pitch_per_frame = old_unit_weap.down_pitch_per_frame
            unit_weap.up_pitch_per_frame   = old_unit_weap.up_pitch_per_frame
            unit_weap.down_frame_count     = old_unit_weap.down_frame_count
            unit_weap.up_frame_count       = old_unit_weap.up_frame_count

            unit_weap.ik_points.STEPTREE = deepcopy(old_unit_weap.ik_points.STEPTREE)


def copy_vehicles_animation_block_data(antr_vehicles, old_antr_vehicles):
    vehicle = antr_vehicles[0]
    old_vehicle = old_antr_vehicles[0]
    vehicle.right_yaw_per_frame  = old_vehicle.right_yaw_per_frame
    vehicle.left_yaw_per_frame   = old_vehicle.left_yaw_per_frame
    vehicle.right_frame_count    = old_vehicle.right_frame_count
    vehicle.left_frame_count     = old_vehicle.left_frame_count

    vehicle.down_pitch_per_frame = old_vehicle.down_pitch_per_frame
    vehicle.up_pitch_per_frame   = old_vehicle.up_pitch_per_frame
    vehicle.down_frame_count     = old_vehicle.down_frame_count
    vehicle.up_frame_count       = old_vehicle.up_frame_count

    suspensions = vehicle.suspension_animations.STEPTREE
    old_suspensions = old_vehicle.suspension_animations.STEPTREE
    for old, new in zip(old_suspensions, suspensions):
        new.mass_point_index = old.mass_point_index
        new.full_extension_ground_depth   = old.full_extension_ground_depth
        new.full_compression_ground_depth = old.full_compression_ground_depth


def set_animation_index(antr_tag, anim_name, anim_index,
                        indices_to_not_overwrite=()):
    orig_anim_name = anim_name

    antr_units = antr_tag.data.tagdata.units.STEPTREE
    antr_weapons = antr_tag.data.tagdata.weapons.STEPTREE
    antr_vehicles = antr_tag.data.tagdata.vehicles.STEPTREE
    antr_devices = antr_tag.data.tagdata.devices.STEPTREE
    antr_unit_damages = antr_tag.data.tagdata.unit_damages.STEPTREE
    antr_fp_animations = antr_tag.data.tagdata.fp_animations.STEPTREE
    antr_anims = antr_tag.data.tagdata.animations.STEPTREE
    antr_nodes = antr_tag.data.tagdata.nodes.STEPTREE

    name_pieces = anim_name.strip().split("%")
    perm_num = ""
    if len(name_pieces) > 1:
        anim_name = "%".join(name_pieces[: -1]).strip()
        perm_num = name_pieces[-1]

    prefix = ""
    # determine where this animation is to be used
    name_pieces = anim_name.split(" ", 1)
    if len(name_pieces) > 1:
        prefix = name_pieces[0].lower().replace("_", "-")
        anim_name = name_pieces[1]

    prefix2 = ""
    name_pieces = anim_name.split(" ", 1)
    if len(name_pieces) > 1:
        prefix2 = name_pieces[0].lower().replace("_", "-")

    if prefix == "vehicle" and prefix2 == "suspension":
        anim_name = anim_name.split(" ", 1)[1]
        block = antr_vehicles[0]
        anim_enums = block.suspension_animations.STEPTREE
        if anim_enum_index >= 8:
            # max of 8 suspension animations
            return False

        anim_enums.append()
        anim_enums[-1].animation = anim_index

    elif prefix in ("first-person", "device", "vehicle"):
        if prefix == "first-person":
            options = fp_animation_names
            block = antr_fp_animations[0]
        elif prefix == "device":
            options = device_animation_names
            block = antr_devices[0]
        elif prefix == "vehicle":
            options = vehicle_animation_names
            block = antr_vehicles[0]

        try:
            anim_enum_index = options.index(anim_name)
        except ValueError:
            return False

        anim_enums = block.animations.STEPTREE
        anim_enums.extend(anim_enum_index + 1 - len(anim_enums))
        block = anim_enums[anim_enum_index]
        if block.animation in indices_to_not_overwrite:
            return False
        block.animation = anim_index
        return True

    elif prefix in ("s-ping", "h-ping", "s-kill", "h-kill"):
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
            anim_enum_index = unit_damage_animation_names.index(
                orig_anim_name.split("%")[0].strip().lower().replace("_", "-")
                )
            base_index = (anim_enum_index // 11) * 11
            anim_enum_index = anim_enum_index % 11
        except ValueError:
            return False

        if len(antr_unit_damages) != 176:
            antr_unit_damages.extend(176 - len(antr_unit_damages))

        indices_to_set = range(1, 11)
        if   anim_enum_index == 1: indices_to_set = [2, 3, 4, 7, 8]
        elif anim_enum_index == 3: indices_to_set = [4]
        elif anim_enum_index == 5: indices_to_set = [6]
        elif anim_enum_index == 7: indices_to_set = [8]
        elif anim_enum_index == 9: indices_to_set = [10]

        block = antr_unit_damages[base_index + anim_enum_index]
        if block.animation in indices_to_not_overwrite:
            return False

        # set the animation blocks enum
        antr_unit_damages[base_index + anim_enum_index].animation = anim_index
        # set any that havent been set to anything
        for i in indices_to_set:
            block = antr_unit_damages[base_index + i]
            if block.animation < 0:
                block.animation = anim_index

        return True

    # weapon animations have no prefix
    try:
        weap_anim_enum_index = weapon_animation_names.index(
            anim_name.lower().replace("_", "-")
            )
    except ValueError:
        weap_anim_enum_index = None


    if weap_anim_enum_index is not None:
        # do stuff
        if len(antr_weapons) < 1:
            antr_weapons.append()

        weapon_anims = antr_weapons[0].animations.STEPTREE
        weapon_anims.extend(weap_anim_enum_index + 1)
        block = weapon_anims[weap_anim_enum_index]
        if block.animation in indices_to_not_overwrite:
            return False

        block.animation = anim_index
        return True

    try:
        unit_anim_enum_index = unit_animation_names.index(
            anim_name.lower().replace("_", "-")
            )
    except ValueError:
        unit_anim_enum_index = None

    # TODO: Finish up everything below here
    if unit_anim_enum_index is not None:
        # do stuff
        return True

    name_pieces = anim_name.split(" ", 1)
    if len(name_pieces) < 1:
        return False

    # unit animations are prefixed with the unit label
    #   NOTE: Default right/left yaw/pitch to 1 frame count
    #
    #   for the first 12 unit animations, any that are undefined
    #   for that specific unit will default to the first one found.
    #       Ex: "P-riderLB02 emotions" defaulting to "stand emotions"
    #
    #   second prefix can be weapon label("stand unarmed idle")
    #     third prefix can be weapon type label("stand pistol pp fire-1")

    unit_label = prefix
    weap_name, anim_name = name_pieces
    try:
        unit_weap_anim_enum_index = unit_weapon_animation_names.index(
            anim_name.lower().replace("_", "-")
            )
    except ValueError:
        unit_weap_anim_enum_index = None

    if unit_weap_anim_enum_index is not None:
        # do stuff
        return True

    name_pieces = anim_name.split(" ", 1)
    if len(name_pieces) < 2:
        return False

    weap_type_label, anim_name = name_pieces
    try:
        unit_weap_type_anim_enum_index = unit_weapon_type_animation_names.index(
            anim_name.lower().replace("_", "-")
            )
    except ValueError:
        return False

    return True
