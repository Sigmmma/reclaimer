from .halo1_map import *
from reclaimer.stubbs.constants import stubbs_tag_class_fcc_to_ext
from reclaimer.stubbs.defs.antr import antr_def as stubbs_antr_def
from reclaimer.stubbs.defs.coll import coll_def as stubbs_fast_coll_def
from reclaimer.stubbs.defs.mode import mode_def as stubbs_mode_def
from reclaimer.stubbs.defs.mode import pc_mode_def as stubbs_pc_mode_def
from reclaimer.stubbs.defs.sbsp import fast_sbsp_def as stubbs_fast_sbsp_def
from reclaimer.stubbs.defs.soso import soso_def as stubbs_soso_def
from reclaimer.stubbs.handler   import StubbsHandler
from supyr_struct.defs.frozen_dict import FrozenDict
from supyr_struct.buffer import BytearrayBuffer


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
            this_class.handler = self.handler_class(
                build_reflexive_cache=False, build_raw_data_cache=False)
            this_class.defs = dict(this_class.handler.defs)

            if self.engine == "stubbspc":
                this_class.defs["mode"] = stubbs_pc_mode_def
            else:
                this_class.defs["mode"] = stubbs_mode_def
            this_class.defs["antr"] = stubbs_antr_def
            this_class.defs["coll"] = stubbs_fast_coll_def
            this_class.defs["sbsp"] = stubbs_fast_sbsp_def
            this_class.defs = FrozenDict(this_class.handler.defs)

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)
