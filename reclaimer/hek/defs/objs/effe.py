#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.util.matrices import euler_2d_to_vector_3d
from reclaimer.enums import object_types
from reclaimer.util import fourcc_to_int

object_tag_class_ids = tuple(
    fourcc_to_int(fourcc, byteorder='big') for fourcc in object_types
    )

class EffeTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        dont_cull = False
        for event in self.data.tagdata.events.STEPTREE:
            for part in event.parts.STEPTREE:
                tag_cls = part.type.tag_class
                if tag_cls.data in object_tag_class_ids:
                    dont_cull = True
                    part.effect_class.set_to('object')
                elif tag_cls.enum_name in ("damage_effect", "light"):
                    dont_cull = True
                    part.effect_class.set_to(tag_cls.enum_name)

            for particle in event.particles.STEPTREE:
                particle.relative_direction_vector[:] = euler_2d_to_vector_3d(
                    *particle.relative_direction
                    )
        self.data.tagdata.flags.must_be_deterministic = dont_cull
