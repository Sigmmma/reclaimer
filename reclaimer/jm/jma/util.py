#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from math import sqrt
from reclaimer.common_descs import anim_types, anim_frame_info_types
from .. import constants as const


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


def get_anim_ext(anim_type, frame_info_type, world_relative=False):
    anim_type = anim_type.lower()
    frame_info_type = frame_info_type.lower()
    return "." + (
        "jmr" if anim_type == "replacement" else
        "jmo" if anim_type == "overlay"     else
        "jmz" if "dz"   in frame_info_type  else
        "jmt" if "dyaw" in frame_info_type  else
        "jma" if "dx"   in frame_info_type  else
        "jmw" if world_relative             else
        "jmm"
        )


def get_anim_types(anim_ext):
    anim_ext  = anim_ext.lower().strip(".")
    anim_type = {"jmr": anim_types[2],
                 "jmo": anim_types[1],
                 }.get(anim_ext, anim_types[0])
    info_type = {"jmz": anim_frame_info_types[3],
                 "jmt": anim_frame_info_types[2],
                 "jma": anim_frame_info_types[1],
                 }.get(anim_ext, anim_frame_info_types[0])
    world_rel = anim_ext == "jmw"

    return (anim_type, info_type, world_rel)


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


def pack_anim_flags(rot_flags, trans_flags, scale_flags):
    return [
        sum(int(bool(flag)) << n for n, flag in enumerate(flags))
        for flags in (rot_flags, trans_flags, scale_flags)
        ]
