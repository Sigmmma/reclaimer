#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .halo3_map import Halo3Map
from reclaimer.h3.defs.bitm import bitm_def
from reclaimer.h3.defs.play import play_def
from reclaimer.h3.defs.zone import zone_def_odst_partial
from supyr_struct.defs.frozen_dict import FrozenDict

class Halo3OdstMap(Halo3Map):
    tag_defs_module = ""
    tag_classes_to_load = (
        "play", "bitm", "zone"
        )
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None

    def setup_defs(self):
        this_class = type(self)
        if this_class.defs is None:
            this_class.defs = FrozenDict({
                "zone": zone_def_odst_partial,
                "bitm": bitm_def,
                "play": play_def,
                })

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)