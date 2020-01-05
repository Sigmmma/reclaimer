#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.wrappers.halo1_map import Halo1Map
from reclaimer.stubbs.constants import stubbs_tag_class_fcc_to_ext
from reclaimer.stubbs.handler   import StubbsHandler
from supyr_struct.defs.frozen_dict import FrozenDict


class StubbsMap(Halo1Map):
    defs = None

    handler_class = StubbsHandler

    tag_defs_module = StubbsHandler.default_defs_path
    tag_classes_to_load = tuple(sorted(stubbs_tag_class_fcc_to_ext.keys()))

    def setup_defs(self):
        this_class = type(self)
        if not this_class.defs:
            print("    Loading definitions in %s" %
                  self.handler_class.default_defs_path)
            this_class.defs = defs = {}

            # these imports were moved here because their defs would otherwise
            # be built when this module was imported, which is not good practice
            from reclaimer.stubbs.defs.antr import antr_def as antr_def
            from reclaimer.stubbs.defs.mode import mode_def as mode_def
            from reclaimer.stubbs.defs.mode import pc_mode_def as pc_mode_def
            from reclaimer.stubbs.defs.coll import fast_coll_def as coll_def
            from reclaimer.stubbs.defs.sbsp import fast_sbsp_def as sbsp_def

            this_class.handler = self.handler_class(
                build_reflexive_cache=False, build_raw_data_cache=False,
                debug=2)
            this_class.defs = dict(this_class.handler.defs)

            if self.engine == "stubbspc":
                this_class.defs["mode"] = pc_mode_def
            else:
                this_class.defs["mode"] = mode_def
            this_class.defs["antr"] = antr_def
            this_class.defs["coll"] = coll_def
            this_class.defs["sbsp"] = sbsp_def
            this_class.defs = FrozenDict(this_class.defs)

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)
