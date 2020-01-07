#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.util.matrices import Matrix, quaternion_to_matrix


__all__ = ("compile_physics", )


def compile_physics(phys_tag, jms_model_markers, updating=True):
    tagdata = phys_tag.data.tagdata
    mass_points = tagdata.mass_points.STEPTREE

    if not updating:
        # making fresh physics tag. use default values
        tagdata.radius = -1.0
        tagdata.moment_scale = 0.3
        tagdata.mass = 1.0
        tagdata.density = 1.0
        tagdata.gravity_scale = 1.0
        tagdata.ground_friction = 0.2
        tagdata.ground_depth = 0.2
        tagdata.ground_damp_fraction = 0.05
        tagdata.ground_normal_k1 = 0.7071068
        tagdata.ground_normal_k0 = 0.5
        tagdata.water_friction = 0.05
        tagdata.water_depth = 0.25
        tagdata.water_density = 1.0
        tagdata.air_friction = 0.001

    existing_mp_names = {}
    for i in range(len(mass_points)):
        existing_mp_names[mass_points[i].name.lower()] = i

    mass_points_to_update = {}
    for marker in jms_model_markers:
        name = marker.name.lower()
        if name in existing_mp_names:
            mass_points_to_update[name] = mass_points[existing_mp_names[name]]

    del mass_points[:]

    # update the mass points and/or make new ones
    for marker in jms_model_markers:
        rotation = quaternion_to_matrix(
            marker.rot_i, marker.rot_j,
            marker.rot_k, marker.rot_w)

        name = marker.name
        if name in existing_mp_names:
            mass_points.append(mass_points_to_update[name])
        else:
            mass_points.append()

        mp = mass_points[-1]
        if name not in existing_mp_names:
            # set default values
            mp.relative_mass = 1.0
            mp.relative_density = 1.0
            mp.friction_parallel_scale = 1.0
            mp.friction_perpendicular_scale = 1.0

        forward = rotation * Matrix(((1, ), (0, ), (0, )))
        up      = rotation * Matrix(((0, ), (0, ), (1, )))
        mp.up[:]       = up[0][0],      up[1][0],      up[2][0]
        mp.forward[:]  = forward[0][0], forward[1][0], forward[2][0]
        mp.position[:] = marker.pos_x/100, marker.pos_y/100, marker.pos_z/100
        mp.name = name
        mp.radius = marker.radius/100
        mp.model_node = marker.parent

    phys_tag.calc_internal_data()
