#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import traceback

from math import pi

from reclaimer.enums import unit_animation_names, unit_weapon_animation_names,\
     unit_weapon_type_animation_names, vehicle_animation_names,\
     weapon_animation_names, device_animation_names, fp_animation_names,\
     unit_damage_animation_names
from reclaimer.hek.defs.mod2 import TagDef, Pad, marker as mod2_marker_desc,\
     node as mod2_node_desc, reflexive, Struct

__all__ = (
    'SHARED_UNIT_ANIMATION_NAMES', 'SHARED_UNIT_WEAPON_ANIMATION_NAMES',
    'split_anim_name_into_type_strings', 'split_permutation_number',
    'set_animation_enum_index', 'set_animation_index',
    'get_default_animation_enums', 'set_default_animation_enums',
    'partial_mod2_def', 'calculate_node_vectors'
    )


SHARED_UNIT_ANIMATION_NAMES = frozenset((
    'airborne-dead', 'landing-dead', 'talk', 'emotions'
    ))

SHARED_UNIT_WEAPON_ANIMATION_NAMES = frozenset((
    'dive-front', 'dive-back', 'dive-left', 'dive-right', 'airborne',
    'land-soft', 'land-hard', 'throw-grenade', 'berserk',
    'surprise-front', 'surprise-back', 'evade-left', 'evade-right',
    'signal-move', 'signal-attack', 'warn', 'melee', 'celebrate', 'panic',
    'melee-airborne', 'flaming', 'resurrect-front', 'resurrect-back',
    'melee-continuous', 'feeding', 'leap-start', 'leap-airborne', 'leap-melee'
    ))


partial_mod2_def = TagDef("mod2",
    Pad(64),
    Struct('tagdata',
        Pad(172),
        reflexive("markers", mod2_marker_desc, 256, DYN_NAME_PATH=".name"),
        reflexive("nodes", mod2_node_desc, 64, DYN_NAME_PATH=".name"),
        SIZE=232
        ),
    ext=".gbxmodel", endian=">"
    )


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


def get_default_animation_enums(anim_enums, defaults):
    for i in defaults:
        if i not in range(len(anim_enums)):
            continue
        elif anim_enums[i].animation >= 0 and defaults[i] < 0:
            # this animation is set, and we DON'T have a valid default.
            # set the default to this valid animation enum
            defaults[i] = anim_enums[i].animation


def set_default_animation_enums(anim_enums, defaults):
    for i in defaults:
        if i not in range(len(anim_enums)):
            continue
        elif anim_enums[i].animation < 0 and defaults[i] >= 0:
            # this animation is unset, and we DO have a valid default.
            # set this animation enum to the valid default
            anim_enums[i].animation = defaults[i]


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
        unit.animations.STEPTREE.extend(12 - len(unit.animations.STEPTREE))

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
        if block.label == part3:
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


def calculate_node_vectors(antr_nodes, mod2_nodes, jma_anims):
    # NOTE: The base vector is a ray starting at the node that points
    # relative to the parent node. It points toward the center of the
    # bounds of all the rotations of that node across all animations.
    # The vector range is twice the max rotation in any direction that
    # node will vary across all animations.
    # ball-socket type means the joint can pitch, yaw, and roll freely.
    # hinge type means the joint can pitch and roll freely.

    # The cyborgs head has a base vector of 80 degrees, points up, and
    # the joint is set as a ball socket. This means the head can pitch,
    # yaw, and roll 40 degrees in any direction from the base vector.
    pass
