#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.wrappers.stubbs_map import *

# so, turns out the steam re-release of stubbs uses 64bit pointers in most
# areas of the map(aside from the header it seems). We're going to "support"
# this enough to load and display the map header and index, but nothing else.
# extracting from 64bit stubbs can come later, but for now lets at least not
# have Reclaimer or Refinery crash when trying to load these maps.
class StubbsMap64Bit(StubbsMap):
    handler_class = StubbsHandler

    tag_defs_module = StubbsHandler.default_defs_path
    tag_classes_to_load = ()
    defs = ()

    def setup_defs(self):
        self.defs = {}
