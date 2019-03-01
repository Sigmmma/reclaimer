from .halo_map import HaloMap
from .halo1_map import Halo1Map
from reclaimer.shadowrun_prototype.handler import ShadowrunPrototypeHandler
from reclaimer.shadowrun_prototype.constants import sr_tag_class_fcc_to_ext


class ShadowrunMap(Halo1Map):
    defs = None

    handler_class = ShadowrunPrototypeHandler
    tag_defs_module = "reclaimer.shadowrun_prototype.defs"
    tag_classes_to_load = tuple(sorted(sr_tag_class_fcc_to_ext.keys()))

    def setup_defs(self):
        HaloMap.setup_defs(self)
        type(self).handler = self.handler_class(
            build_reflexive_cache=False, build_raw_data_cache=False)
