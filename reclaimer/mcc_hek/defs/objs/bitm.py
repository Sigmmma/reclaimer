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

    def fix_top_format(self):
        top_format = None
        if self.bitmap_count() > 0:
            pixel_format = self.data.tagdata.bitmaps.bitmaps_array[0].format.enum_name
            if pixel_format == "bc7":
                top_format = "high_quality_compression"

        if top_format is None:
            return super().fix_top_format()

        self.data.tagdata.format.set_to(top_format)