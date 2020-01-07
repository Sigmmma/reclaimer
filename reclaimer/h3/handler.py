#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.h3.defs import __all__ as all_def_names
from reclaimer.hek.handler import HaloHandler
from reclaimer.data_extraction import h3_data_extractors

class Halo3Handler(HaloHandler):
    frozen_imp_paths = all_def_names
    tag_header_engine_id = "b3am"
    default_defs_path = "reclaimer.h3.defs"

    tag_data_extractors = h3_data_extractors
