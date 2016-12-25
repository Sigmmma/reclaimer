from math import sqrt

from .tag import *


'''
To calculate center of mass, add up all of the mass point
position vectors multiplied by their relative mass, then
divide the resulting vector by the number of mass points.

This will give the center of mass as a vector.

xx, yy, and zz moments are affected by mass point radius
Remember that moments are the mass times the distance from
the respective axis on a path perpendicular to the axis.

This will mean doing sqrt(y^2+z^2) for xx,
sqrt(x^2+z^2) for yy, and sqrt(x^2+y^2) for zz

The second matrix is an inverse of the first matrix.
Both matricies must exist.

mass = total_mass * rel_mass/total_rel_mass
density = ? * density * (rel_density/t_rel_density)

gotta figure out what ? is. All densities are the same when
they are multiplied by (t_rel_density/rel_density)
I HAVE NO FUCKING CLUE WHAT IT COULD POSSIBLY BE RIGHT NOW

RADIUS MODIFIERS

1  = 0.4
2  = 1.6
3  = 3.6
4  = 6.4
5  = 10
6  = 14.4
7  = 19.6
8  = 25.6
9  = 32.4

1    = 0.4    = 4*10^-1
10   = 40     = 4*10^1
100  = 4000   = 4*10^3
1000 = 400000 = 4*10^5

f(r)=4*10^(2*log10(r)-1)

r = 1.58114 makes inertia = 1


DISTANCE MODIFIERS

0  = 1
1  = 2
2  = 5
3  = 10
4  = 17
5  = 26
6  = 37
7  = 50
8  = 65
9  = 82
10 = 101

f(d)=d^2


MASS IS A SCALAR MODIFIER

f(m,d,r) = m*(d^2 + 4*10^(2*log10(r)-1))


sum up mass points entered into above equation
(distance is distance from center of mass)
and divide by the number of mass points

Equation is not complete
'''


class MatrixRow(list):
    '''Implements the minimal methods required for row reduction'''
    def __add__(self, other):
        new = MatrixRow(self)
        for i in range(len(other)): new[i] += other[i]
        return new
    def __sub__(self, other):
        new = MatrixRow(self)
        for i in range(len(other)): new[i] -= other[i]
        return new
    def __mul__(self, other):
        new = MatrixRow(self)
        for i in range(len(self)): new[i] *= other
        return new
    def __truediv__(self, other):
        new = MatrixRow(self)
        for i in range(len(self)): new[i] /= other
        return new
    def __iadd__(self, other):
        for i in range(len(other)): self[i] += other[i]
        return self
    def __isub__(self, other):
        for i in range(len(other)): self[i] -= other[i]
        return self
    def __imul__(self, other):
        for i in range(len(self)): self[i] *= other
        return self
    def __itruediv__(self, other):
        for i in range(len(self)): self[i] /= other
        return self


class PhysTag(HekTag):

    def calc_masses(self):
        data = self.data.tagdata
        mass_points = data.mass_points.STEPTREE

        total_mass = data.mass
        total_rel_mass = sum([mp.relative_mass for mp in mass_points])
        mass_center = [0,0,0]

        if not len(mass_points):
            data.center_of_mass[:] = mass_center
            return

        for mass_point in mass_points:
            rel_mass = mass_point.relative_mass
            position = mass_point.position

            mass_point.mass = total_mass*(rel_mass/total_rel_mass)
            mass_center[0] += position[0]*rel_mass
            mass_center[1] += position[1]*rel_mass
            mass_center[2] += position[2]*rel_mass

        mass_center[0] /= len(mass_points)
        mass_center[1] /= len(mass_points)
        mass_center[2] /= len(mass_points)

        data.center_of_mass[:] = mass_center

    def calc_densities(self):
        data = self.data.tagdata
        mass_points = data.mass_points.STEPTREE

        total_mass = data.mass
        total_dens = data.density
        total_rel_mass = sum([mp.relative_mass for mp in mass_points])
        total_rel_dens = sum([mp.relative_density for mp in mass_points])

        return
        for mass_point in mass_points:
            rel_mass = mass_point.relative_mass

            # THIS IS INCOMPLETE
            mass_point.density = total_dens * (
                mass_point.relative_density/total_rel_dens)

    def calc_intertia_matricies(self):
        data = self.data.tagdata
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

        for mass_point in mass_points:
            break
            pos = mass_point.position
            # THIS IS INCORRECT
            dist_x = sqrt((com[1] - pos[1])**2 + (com[2] - pos[2])**2)
            dist_y = sqrt((com[0] - pos[0])**2 + (com[2] - pos[2])**2)
            dist_z = sqrt((com[0] - pos[0])**2 + (com[1] - pos[1])**2)

            xx += dist_x * mass_point.mass
            yy += dist_y * mass_point.mass
            zz += dist_z * mass_point.mass
            neg_zx += dist_zx * mass_point.mass
            neg_xy += dist_xy * mass_point.mass
            neg_yz += dist_yz * mass_point.mass

        #print(xx, neg_xy, neg_zx, reg_yy_zz)
        #print(neg_xy, yy, neg_yz, reg_zz_xx)
        #print(neg_zx, neg_yz, zz, reg_xx_yy)

        # place the calculated values into the matrix
        #reg_yy_zz[:] = xx, neg_xy, neg_zx
        #reg_zz_xx[:] = neg_xy, yy, neg_yz
        #reg_xx_yy[:] = neg_zx, neg_yz, zz

        # calculate the remaining matrix values

        # the right side will be the inverse after row reduction
        # and the left side is the regular matrix to be reduced.
        inv_yy_zz = MatrixRow(tuple(reg_yy_zz) + (1.0, 0.0, 0.0))
        inv_zz_xx = MatrixRow(tuple(reg_zz_xx) + (0.0, 1.0, 0.0))
        inv_xx_yy = MatrixRow(tuple(reg_xx_yy) + (0.0, 0.0, 1.0))

        # calculate the inverse matrix through row reduction
        inv_yy_zz /= inv_yy_zz[0]
        inv_zz_xx /= inv_zz_xx[1]
        inv_xx_yy /= inv_xx_yy[2]

        x1 = inv_xx_yy * inv_yy_zz[2]
        x2 = inv_xx_yy * inv_zz_xx[2]

        inv_yy_zz -= x1
        inv_zz_xx -= x2

        x3 = inv_zz_xx * inv_yy_zz[1] / inv_zz_xx[1]
        inv_yy_zz -= x3
        inv_yy_zz /= inv_yy_zz[0]
        inv_zz_xx /= inv_zz_xx[1]

        # INCOMPLETE: NEED TO PLUG IN VALUES TO FIND OTHER VALUES

        # place the inverse matrix into the tag
        inv.yy_zz[:] = inv_yy_zz[3:]
        inv.zz_xx[:] = inv_zz_xx[3:]
        inv.xx_yy[:] = inv_xx_yy[3:]

        # copy the calculated -xy, -zx, -yz from the top right
        # corner of the inverse matrix to the bottom left corner
        inv.zz_xx[0] = inv.yy_zz[1]
        inv.xx_yy[0] = inv.yy_zz[2]
        inv.xx_yy[1] = inv.zz_xx[2]

        # copy the xx, yy, and zz moments form the matrix into the tag body
        data.xx_moment = reg_yy_zz[0]
        data.yy_moment = reg_zz_xx[1]
        data.zz_moment = reg_xx_yy[2]

    def serialize(self, **kwargs):
        return HekTag.serialize(self, **kwargs)
        self.calc_masses()
        self.calc_densities()
        self.calc_intertia_matricies()

        return HekTag.serialize(self, **kwargs)
