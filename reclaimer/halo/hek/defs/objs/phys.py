from .tag import *

'''
To calculate center of mass, add up all of the mass point
position vectors multiplied by their relative mass, then
divide the resulting vector by:
    (total_relative_mass * number_of_mass_points).
This will give the center of mass as a vector.

xx, yy, and zz moments are affected by mass point radius
Remember that moments are the mass times the distance from
the respective axis on a path perpendicular to the axis.

This will mean doing sqrt(y^2+z^2) for xx,
sqrt(x^2+z^2) for yy, and sqrt(x^2+y^2) for zz

The second matrix is an inverse of the first matrix.
Both matricies must exist.

mass = total_mass * rel_mass/total_rel_mass
density = ? * density * (reldensity/treldensity)

gotta figure out what ? is. All densities are the same when
they are multiplied by (treldensity/reldensity)
I HAVE NO FUCKING CLUE WHAT IT COULD POSSIBLY BE RIGHT NOW
'''

class PhysTag(HekTag):
    
    pass
