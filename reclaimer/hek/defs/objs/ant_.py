#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import sin, cos

from reclaimer.hek.defs.objs.tag import HekTag

class Ant_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        tagdata = self.data.tagdata
        tagdata.length = 0
        for vertex in tagdata.vertices.STEPTREE:
            sin_y = sin(vertex.angles.y)
            sin_p = sin(vertex.angles.p)
            cos_y = cos(vertex.angles.y)
            cos_p = cos(vertex.angles.p)

            vertex.offset.x = vertex.length * sin_p * cos_y
            vertex.offset.y = vertex.length * sin_y * sin_p
            vertex.offset.z = vertex.length * cos_p

            tagdata.length += vertex.length
