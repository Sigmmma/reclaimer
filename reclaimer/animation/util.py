#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import traceback

from math import pi, sqrt
from pathlib import Path

from reclaimer.animation import constants as const
from reclaimer.util import get_block_max
from reclaimer.enums import unit_animation_names, unit_weapon_animation_names,\
     unit_weapon_type_animation_names, vehicle_animation_names,\
     weapon_animation_names, device_animation_names,\
     fp_animation_names, fp_animation_names_mcc,\
     unit_damage_animation_names, unit_damage_types,\
     unit_damage_regions, unit_damage_sides
from supyr_struct.util import tagpath_to_fullpath

__all__ = (
    'split_anim_name_into_type_strings', 'split_permutation_number',
    'set_animation_enum_index', 'set_animation_index',
    'get_default_enums', 'set_default_enums',
    )


def get_curve_derivative(curve, order=1):
    if order == 0:
        diff = [list(v) for v in curve]

    ct  = len(curve)
    for i in range(order):
        diff = [None for i in range(ct)]
        if ct == 1:
            diff[0] = [0]*len(curve[0])
            return diff
        elif ct > 2:
            diff[1: -1] = (
                [(v1-v0)/2 for v0, v1 in zip(p0, p1)]
                for p0, p1 in zip(curve[:-1], curve[2:])
                )

        diff[-1] = [(v1-v0)/2 for v0,v1 in zip(*curve[ct-2: ct])]
        diff[0]  = [(v1-v0)/2 for v0,v1 in zip(*curve[:2])]
        curve = diff

    return diff


def get_anim_flags(anim):
    rot_flags, trans_flags, scale_flags = [], [], []
    for flags, flags_int in (
        [rot_flags,   anim.rot_flags0   | (anim.rot_flags1<<32)  ],
        [trans_flags, anim.trans_flags0 | (anim.trans_flags1<<32)],
        [scale_flags, anim.scale_flags0 | (anim.scale_flags1<<32)],
        ):
        flags.extend(bool(flags_int & (1 << i)) for i in range(anim.node_count))

    return rot_flags, trans_flags, scale_flags


def get_frame_size(anim):
    r_flags, t_flags, s_flags = get_anim_flags(anim)
    return 12*sum(t_flags) + 8*sum(r_flags) + 4*sum(s_flags)


def get_default_data_size(anim):
    return anim.node_count * 24 - get_frame_size(anim)


def get_frame_info_size(anim):
    typ     = anim.frame_info_type.data
    fields  = (1 + typ) if typ in (1, 2, 3) else 0
    return anim.frame_count * 4 * fields


def pack_anim_flags(rot_flags, trans_flags, scale_flags):
    return [
        sum(int(bool(flag)) << n for n, flag in enumerate(flags))
        for flags in (rot_flags, trans_flags, scale_flags)
        ]


def calculate_anim_flags(frames, tolerance=1.0):
    # determine which transforms types of each node are animated
    # by seeing how much they change from the starting frame
    f0          = frames[0]
    r_abs_diffs = [0]*len(f0)
    t_abs_diffs = [0]*len(f0)
    s_abs_diffs = [0]*len(f0)

    tolerance = abs(max(0, tolerance) or 1.0)
    ep_r = const.QUAT_EPSILON  * tolerance
    ep_t = const.TRANS_EPSILON * tolerance
    ep_s = const.SCALE_EPSILON * tolerance

    for n, s0 in enumerate(f0):
        r_diffs, t_diffs, s_diffs = [0], [0], [0]
        s0_i, s0_j, s0_k, s0_w  = s0.rot_i, s0.rot_j, s0.rot_k, s0.rot_w
        s0_x, s0_y, s0_z        = s0.pos_x, s0.pos_y, s0.pos_z
        for f in range(1, len(frames)):
            s1 = frames[f][n]
            r_diffs.append((s0_i - s1.rot_i)**2 +
                           (s0_j - s1.rot_j)**2 +
                           (s0_k - s1.rot_k)**2 +
                           (s0_w - s1.rot_w)**2)
            t_diffs.append((s0_x - s1.pos_x)**2 +
                           (s0_y - s1.pos_y)**2 +
                           (s0_z - s1.pos_z)**2)

            # scale is calculated a bit differently. we ALWAYS store scale
            # frame data for a node if its scale is ever not 1.0, even if
            # it is static for the entire animation length. This seems to
            # be due to how compressed animations handle default scales.
            s_diffs.append((1 - s1.scale)**2)

        r_abs_diffs[n] = sqrt(max(r_diffs))
        t_abs_diffs[n] = sqrt(max(t_diffs))
        s_abs_diffs[n] = sqrt(max(s_diffs))

    r_flags = [(diff >= ep_r) << n for n, diff in enumerate(r_abs_diffs)]
    t_flags = [(diff >= ep_t) << n for n, diff in enumerate(t_abs_diffs)]
    s_flags = [(diff >= ep_s) << n for n, diff in enumerate(s_abs_diffs)]
    return r_flags, t_flags, s_flags


def get_anim_rename_map(folder="", name=""):
    rename_map = {}
    filepath = tagpath_to_fullpath(folder, name or "rename.txt", "", not name)
    if not filepath:
        return rename_map

    try:
        with open(filepath, "r", encoding="latin-1") as f:
            for line in (line for line in f if "=" in line):
                new, old = [op.strip() for op in line.split("=", 1)]
                rename_map[new] = old
    except Exception:
        print(traceback.format_exc())

    return rename_map


def get_expected_anim_types(anim_name):
    has_purpose, pieces, perm = split_anim_name_into_type_strings(anim_name)
    anim_types = []
    if not has_purpose:
        return anim_types

    part1, part2, part3, part4 = pieces
    if part4:
        if part4 in unit_weapon_type_animation_names:
            if part3 in ('fire-1', 'fire-2', 'charged-1', 'charged-2'):
                anim_types.append("overlay")
            elif part3 == 'melee':
                anim_types.append("replacement")
            else:
                anim_types.append("overlay")
                anim_types.append("replacement")

    elif part3:
        if (part1 in unit_damage_types and  part2 in unit_damage_sides and
            part3 in unit_damage_regions):
            anim_types.append(
                "overlay" if part1 in ("s-ping", "h-ping") else "base"
                )

        elif part3 in unit_weapon_animation_names:
            if part3 in ('aim-still', 'aim-move'):
                anim_types.append("overlay")
            elif part3 in ('throw-grenade', 'melee', 'ready'):
                anim_types.append("replacement")
                anim_types.append("base")
            elif not part3.startswith('unused'):
                anim_types.append("base")

    elif part2:
        if ((part1 == "device"  and part2 in device_animation_names) or
            (part1 == "vehicle" and part2 in vehicle_animation_names)):
            anim_types.append("overlay")

        elif part1 == "first-person" and part2 in fp_animation_names:
            if part2 in ('moving', 'overlays', 'ammunition',
                         'overcharged-jitter'):
                anim_types.append("overlay")
            elif not part2.startswith('light-'):
                anim_types.append("base")

        elif part2 in unit_animation_names:
            if (part2.startswith("acc") or part2.startswith("flying-") or
                part2 in ('push', 'twist', 'look', 'talk', 'emotions')):
                anim_types.append("overlay")

            elif part2 in ('enter', 'exit', 'opening', 'closing', 'hovering'):
                anim_types.append("base")

    elif part1 in weapon_animation_names:
        anim_types.append("base")

    return anim_types


def split_anim_name_into_type_strings(anim_name):
    anim_name = ' '.join(s for s in anim_name.split(" ") if s)

    pieces = anim_name.split(" ", 4)
    part1, part2, part3, part4 = (pieces.pop(0) if pieces else "" for i in range(4))

    part1_sani, part2_sani, part3_sani, part4_sani = (
        s.lower().replace("_", "-") for s in [part1, part2, part3, part4]
        )

    remainder = " ".join(pieces)

    type_strings = ()
    perm_num = ""

    if part1_sani == "suspension":
        if part4: remainder = " ".join((part4, remainder))
        if part3: remainder = " ".join((part3, remainder))
        if part2: remainder = " ".join((part2, remainder))

        remainder, _, perm_num = split_permutation_number(remainder)
        type_strings = part1_sani, remainder.lower(), '', ''
        remainder = ""

    elif part1_sani in ("first-person", "device", "vehicle"):
        if part4: remainder = " ".join((part4, remainder))
        if part3: remainder = " ".join((part3, remainder))

        part2, part2_sani, perm_num = split_permutation_number(part2, remainder)
        if ((part1_sani == "first-person" and part2_sani in fp_animation_names_mcc) or
            (part1_sani == "vehicle" and part2_sani in vehicle_animation_names) or
            (part1_sani == "device"  and part2_sani in device_animation_names)):
            type_strings = part1_sani, part2_sani, '', ''

    elif (part1_sani in unit_damage_types and part2_sani in unit_damage_sides):
        if part4:
            remainder = " ".join((part4, remainder))

        part3, part3_sani, perm_num = split_permutation_number(part3, remainder)
        if part3_sani in unit_damage_regions:
            type_strings = part1_sani, part2_sani, part3_sani, ''

    else:
        part4, part4_sani, perm_num = split_permutation_number(part4, remainder)
        if part4_sani in unit_weapon_type_animation_names:
            type_strings = part1, part2, part3, part4_sani

        else:
            part3, part3_sani, perm_num = split_permutation_number(part3, remainder)
            if part3_sani in unit_weapon_animation_names:
                if part4: remainder = " ".join((part4, remainder))

                type_strings = part1, part2, part3_sani, ''

            else:
                part2, part2_sani, perm_num = split_permutation_number(part2, remainder)
                if part2_sani in unit_animation_names:
                    if part4: remainder = " ".join((part4, remainder))
                    if part3: remainder = " ".join((part3, remainder))

                    type_strings = part1, part2_sani, '', ''
                else:
                    remainder = True

    # nothing should have a remainder. if it does, it doesnt fit the criteria,
    # and we should just return it split at the permutation character
    if remainder:
        pieces = anim_name.lower().split("%")
        if len(pieces) > 1:
            anim_name = "%".join(pieces[: -1])
            perm_num  = pieces[-1]

        return False, (anim_name, '', '', ''), perm_num

    return True, type_strings, perm_num


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


def _get_set_default_enums(anim_enums, defaults, extend, do_set):
    if extend:
        anim_enums.extend(max([-1, *defaults]) + 1 - len(anim_enums))

    for i, anim in enumerate(anim_enums):
        curr_idx, def_idx = anim.animation, defaults.get(i, -1)

        if not do_set and i in defaults and curr_idx >= 0 and def_idx < 0:
            # this animation is set, and we DON'T have a valid default.
            # set the default to this valid animation enum
            defaults[i] = curr_idx
        elif do_set and curr_idx < 0 and def_idx >= 0:
            # this animation is unset, and we DO have a valid default.
            # set this animation enum to the valid default
            anim.animation = def_idx


def get_default_enums(anim_enums, defaults, extend=False):
    _get_set_default_enums(anim_enums, defaults, extend, False)


def set_default_enums(anim_enums, defaults, extend=False):
    _get_set_default_enums(anim_enums, defaults, extend, True)


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

    _, pieces, perm_num = split_anim_name_into_type_strings(anim_name)
    part1, part2, part3, part4 = pieces

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
        susp_anims = antr_vehicles[0].suspension_animations
        anim_enums = susp_anims.STEPTREE
        if len(anim_enums) >= get_block_max(susp_anims):
            # at the limit of suspension animations
            return False

        anim_enums.append()
        anim_enums[-1].animation = anim_index
        return True

    elif part1 in ("first-person", "device", "vehicle"):
        if part1 == "first-person":
            # NOTE: using mcc because they're the same, with an extension
            options = fp_animation_names_mcc
            block = antr_fp_animations
        elif part1 == "device":
            options = device_animation_names
            block = antr_devices
        elif part1 == "vehicle":
            options = vehicle_animation_names
            block = antr_vehicles

        if not block:
            block.append()

        # trim the options to how many are actually allowed
        # NOTE: this is really just for fp_animation_names_mcc
        max_anims   = get_block_max(block[0].animations)
        options     = options[:max_anims]
        try:
            enum_index = options.index(part2)
        except ValueError:
            return False

        return set_animation_enum_index(
            block[0].animations.STEPTREE, enum_index,
            anim_index, indices_to_not_overwrite)

    elif part1 in unit_damage_types:
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
        # NOTE: left, right, and back default to front
        #       they do NOT default to any of each other
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

        if len(antr_unit_damages) < 11*4*4:
            antr_unit_damages.extend(11*4*4 - len(antr_unit_damages))

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
        if len(antr_units) >= get_block_max(antr_units.parent):
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
        if len(unit_weaps) >= get_block_max(unit_weaps.parent):
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
        if len(unit_weap_types) >= get_block_max(unit_weap_types.parent):
            return False

        unit_weap_types.append()
        unit_weap_type = unit_weap_types[-1]
        unit_weap_type.label = part3

    # unit weapon type animation
    return set_animation_enum_index(unit_weap_type.animations.STEPTREE,
                                    enum_index, anim_index,
                                    indices_to_not_overwrite)


def sanitize_animation_indices(antr_tag):
    tagdata = antr_tag.data.tagdata
    antr_units        = tagdata.units.STEPTREE
    antr_unit_damages = tagdata.unit_damages.STEPTREE

    # fill in the remaining unit damages
    max_dmg_ct = 11*4*4 if antr_unit_damages else 0
    antr_unit_damages.extend(max_dmg_ct - len(antr_unit_damages))

    # loop over  s-ping, h-ping, s-kill, h-kill
    for i in range(0, max_dmg_ct, 4*11):
        # the left, right, and back sides default to the front
        # make a collection of defaults for all sides of this region
        defs = {}
        for j in range(11):
            idx = antr_unit_damages[i + j].animation
            defs.update({k: idx for k in range(i+j+11, i+j+44, 11)})

        set_default_enums(antr_unit_damages, defs)

    unit_defs = {
        i: -1 for i, name in
        enumerate(unit_animation_names)
        if name in const.SHARED_UNIT_ANIMATION_NAMES
        }
    all_weap_defs = [{
        i: -1 for i, name in
        enumerate(unit_weapon_animation_names)
        if name in const.SHARED_UNIT_WEAPON_ANIMATION_NAMES
        } for _ in antr_units]

    # get the unit animations with applicable ones from all units.
    # do this in reverse since thats what tool seems to do.
    for unit, weap_defs in zip(antr_units[::-1], reversed(all_weap_defs)):
        get_default_enums(unit.animations.STEPTREE, unit_defs)
        for weap in unit.weapons.STEPTREE:
            get_default_enums(weap.animations.STEPTREE, weap_defs)

    # strip any unused animation indices
    unit_defs     =  {k: v for k, v in unit_defs.items() if v >= 0}
    all_weap_defs = [{k: v for k, v in weap_defs.items() if v >= 0}
                     for weap_defs in all_weap_defs]

    # default any unset unit animations with the found defaults.
    for unit, weap_defs in zip(antr_units, all_weap_defs):
        set_default_enums(unit.animations.STEPTREE, unit_defs, True)

        for weap in unit.weapons.STEPTREE:
            set_default_enums(weap.animations.STEPTREE, weap_defs, True)

            # ensure each unit weapon at least has an empty types block
            # to ensure they are able to enter gunner seats of vehicles
            if not weap.weapon_types.STEPTREE:
                weap.weapon_types.STEPTREE.append()
