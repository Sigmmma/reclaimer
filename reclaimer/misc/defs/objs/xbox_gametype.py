#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.misc.defs.objs.pc_gametype import PcGametypeTag

class XboxGametypeTag(PcGametypeTag):
    def __init__(self, *args, **kwargs):
        PcGametypeTag.__init__(self, *args, **kwargs)
        self.is_xbox = True
