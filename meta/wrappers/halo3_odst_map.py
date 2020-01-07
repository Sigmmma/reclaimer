#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .halo3_map import Halo3Map

class Halo3OdstMap(Halo3Map):
    tag_defs_module = ""
    tag_classes_to_load = tuple()
