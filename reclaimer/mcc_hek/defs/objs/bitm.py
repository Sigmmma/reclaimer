#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from ....hek.defs.objs.bitm import *
from reclaimer.constants import MCC_FORMAT_NAME_MAP

class MccBitmTag(BitmTag):
    @property
    def format_name_map(self):
        return MCC_FORMAT_NAME_MAP