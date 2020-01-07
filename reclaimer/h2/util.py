#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.h2.constants import HALO2_MAP_TYPES


def split_raw_pointer(ptr):
    return ptr & 0x3FffFFff, HALO2_MAP_TYPES[(ptr>>30)&3]
