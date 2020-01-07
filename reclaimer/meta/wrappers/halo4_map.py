#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.wrappers.halo3_map import Halo3Map

class Halo4Map(Halo3Map):
    tag_defs_module = ""
    tag_classes_to_load = tuple()
