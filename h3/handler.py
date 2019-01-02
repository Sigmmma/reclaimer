import os
from ..hek.handler import HaloHandler
from reclaimer.data_extraction import h3_data_extractors

class Halo3Handler(HaloHandler):
    default_defs_path = "reclaimer.h3.defs"
    tag_header_engine_id = "b3am"

    tag_data_extractors = h3_data_extractors
