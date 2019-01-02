import os
from .defs import __all__ as all_def_names
from ..hek.handler import HaloHandler
from os.path import abspath, basename, exists, isfile, normpath, splitext
from reclaimer.data_extraction import h2_data_extractors

class Halo2Handler(HaloHandler):
    frozen_imp_paths = all_def_names
    tag_header_engine_id = "b2am"
    default_defs_path = "reclaimer.h2.defs"

    tag_data_extractors = h2_data_extractors
