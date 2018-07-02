from math import log
from .tag import *
from .matrices import Matrix


class PhysTag(HekTag):

    def calc_masses(self):
        data = self.data.tagdata
        mass_points = data.mass_points.STEPTREE
        mass_center = [0,0,0]

        if not len(mass_points):
            data.center_of_mass[:] = mass_center
            return

        total_mass = data.mass
        total_rel_mass = sum([mp.relative_mass for mp in mass_points])

        for mp in mass_points:
            rel_mass = mp.relative_mass
            position = mp.position

            mp.mass = total_mass*(rel_mass/total_rel_mass)
            mass_center[0] += position[0]*mp.mass
            mass_center[1] += position[1]*mp.mass
            mass_center[2] += position[2]*mp.mass

        mass_center[0] /= total_mass
        mass_center[1] /= total_mass
        mass_center[2] /= total_mass

        data.center_of_mass[:] = mass_center

    def calc_densities(self):
        data = self.data.tagdata
        mass_points = data.mass_points.STEPTREE

        if not len(mass_points):
            return

        total_mass = data.mass
        total_density = data.density

        densities = [mp.relative_density for mp in
                     mass_points if mp.relative_density]
        masses = [mp.relative_mass for mp in
                  mass_points if mp.relative_mass]
        if not densities or not masses:
            for mp in mass_points:
                mp.density = 0
            return

        total_rel_mass = sum(mp.relative_mass for mp in mass_points)
        average_rel_mass = total_rel_mass / len(mass_points)
        #                    total_density      total_density
        # density_scale = ------------------ = ----------------
        #                  avg(mass/density)    avg( m^3   kg )
        #                                          ( --- * -- )
        #                                          ( kg    1  )
        den_scale = total_density / len(mass_points)
        den_scale *= sum(mp.relative_mass / mp.relative_density
                         for mp in mass_points if mp.relative_density)
        mass_scale = 1 / average_rel_mass

        for mp in mass_points:
            mp.density = den_scale * mass_scale * mp.relative_density

    def calc_intertia_matrices(self):
        data = self.data.tagdata
        scale = data.moment_scale
        matrices = data.inertia_matrices.STEPTREE
        com = data.center_of_mass
        mass_points = data.mass_points.STEPTREE

        # make sure the matrix array is only 2 long
        matrices.extend(2 - len(matrices))
        del matrices[2:]

        reg = matrices.regular
        inv = matrices.inverse

        reg_yy_zz, reg_zz_xx, reg_xx_yy = reg.yy_zz, reg.zz_xx, reg.xx_yy
        xx = yy = zz = float('1e-30')  # prevent division by 0
        neg_zx = neg_xy = neg_yz = 0

        # calculate the moments for each mass point and add them up
        for mp in mass_points:
            pos = mp.position

            dist_xx = (com[1] - pos[1])**2 + (com[2] - pos[2])**2
            dist_yy = (com[0] - pos[0])**2 + (com[2] - pos[2])**2
            dist_zz = (com[0] - pos[0])**2 + (com[1] - pos[1])**2

            dist_zx = (com[0] - pos[0])*(com[2] - pos[2])
            dist_xy = (com[0] - pos[0])*(com[1] - pos[1])
            dist_yz = (com[1] - pos[1])*(com[2] - pos[2])

            if mp.radius > 0:
                radius_term = 4*pow(10, (2*log(mp.radius, 10) - 1))
            else:
                radius_term = 0

            xx += (dist_xx + radius_term) * mp.mass
            yy += (dist_yy + radius_term) * mp.mass
            zz += (dist_zz + radius_term) * mp.mass
            neg_zx -= dist_zx * mp.mass
            neg_xy -= dist_xy * mp.mass
            neg_yz -= dist_yz * mp.mass

        xx, yy, zz = xx*scale, yy*scale, zz*scale
        neg_zx, neg_xy, neg_yz = neg_zx*scale, neg_xy*scale, neg_yz*scale

        # place the calculated values into the matrix
        reg_yy_zz[:] = xx, neg_xy, neg_zx
        reg_zz_xx[:] = neg_xy, yy, neg_yz
        reg_xx_yy[:] = neg_zx, neg_yz, zz

        # calculate the inverse inertia matrix
        regular = Matrix((reg_yy_zz, reg_zz_xx, reg_xx_yy))
        try:
            inverse = regular.inverse
        except ZeroDivisionError:
            inverse = Matrix((1, 0, 0), (0, 1, 0), (0, 0, 1))

        # place the inverse matrix into the tag
        inv.yy_zz[:] = inverse[0][:]
        inv.zz_xx[:] = inverse[1][:]
        inv.xx_yy[:] = inverse[2][:]

        # copy the xx, yy, and zz moments form the matrix into the tag body
        data.xx_moment = reg_yy_zz[0]
        data.yy_moment = reg_zz_xx[1]
        data.zz_moment = reg_xx_yy[2]

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        self.calc_masses()
        self.calc_densities()
        self.calc_intertia_matrices()
