import os

from .defs import __all__ as all_def_names
from ..hek.handler import HaloHandler
from reclaimer.data_extraction import h3_data_extractors

class Halo3Handler(HaloHandler):
    frozen_imp_paths = all_def_names
    tag_header_engine_id = "b3am"
    default_defs_path = "reclaimer.h3.defs"

    tag_data_extractors = h3_data_extractors
