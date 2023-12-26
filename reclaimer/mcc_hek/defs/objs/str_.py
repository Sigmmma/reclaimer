#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.util import convert_newlines_to_windows

class Str_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        strings = self.data.tagdata.strings.STEPTREE

        for i in range(len(strings)):
            # Replace all newlines with \r\n.
            strings[i].data = convert_newlines_to_windows(strings[i].data)
