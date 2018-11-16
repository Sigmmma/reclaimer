from .halo1_map import *
from reclaimer.shadowrun_prototype.handler import ShadowrunPrototypeHandler
from supyr_struct.defs.frozen_dict import FrozenDict


class ShadowrunMap(Halo1Map):
    defs = None

    def setup_tag_headers(self):
        if ShadowrunMap.tag_headers is not None:
            return

        Halo1Map.setup_tag_headers(self)
        tag_headers = ShadowrunMap.tag_headers = dict(Halo1Map.tag_headers)

    def setup_defs(self):
        if not ShadowrunMap.defs:
            print("Loading Shadowrun tag definitions...")
            ShadowrunMap.handler = ShadowrunPrototypeHandler(
                build_reflexive_cache=False, build_raw_data_cache=False)
            ShadowrunMap.defs = FrozenDict(ShadowrunMap.handler.defs)
            print("    Finished")

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)
