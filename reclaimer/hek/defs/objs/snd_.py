#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class Snd_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        for pitch_range in self.data.tagdata.pitch_ranges.STEPTREE:
            pitch_range.playback_rate = 1
            if pitch_range.natural_pitch:
                pitch_range.playback_rate = 1 / pitch_range.natural_pitch
