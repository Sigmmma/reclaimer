from .halo1_map import *
from reclaimer.shadowrun_prototype.constants import sr_tag_class_fcc_to_ext
from supyr_struct.defs.frozen_dict import FrozenDict


class ShadowrunMap(Halo1Map):
    defs = None

    tag_defs_module = "reclaimer.shadowrun_prototype.defs"
    tag_classes_to_load = tuple(sorted(sr_tag_class_fcc_to_ext.keys()))
