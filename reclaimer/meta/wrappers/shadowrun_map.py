#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.wrappers.halo1_xbox_map import Halo1XboxMap
from reclaimer.shadowrun_prototype.handler import ShadowrunPrototypeHandler
from reclaimer.shadowrun_prototype.constants import sr_tag_class_fcc_to_ext
from supyr_struct.defs.frozen_dict import FrozenDict


class ShadowrunMap(Halo1XboxMap):
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None

    handler_class = ShadowrunPrototypeHandler
    tag_defs_module = "reclaimer.shadowrun_prototype.defs"
    tag_classes_to_load = tuple(sorted(sr_tag_class_fcc_to_ext.keys()))

    def setup_defs(self):
        this_class = type(self)
        if not this_class.defs:
            print("    Loading definitions in %s" %
                  self.handler_class.default_defs_path)
            # these imports were moved here because their defs would otherwise
            # be built when this module was imported, which is not good practice
            from reclaimer.shadowrun_prototype.defs.coll import fast_coll_def
            from reclaimer.shadowrun_prototype.defs.sbsp import fast_sbsp_def

            handler = self.handler_class(
                build_reflexive_cache=False, build_raw_data_cache=False,
                debug=2)

            defs = dict(handler.defs)
            defs.update(coll=fast_coll_def, sbsp=fast_sbsp_def)
            this_class.defs = FrozenDict(defs)
            this_class.handler = handler

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)
