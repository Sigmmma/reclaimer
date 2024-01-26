#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from reclaimer.meta.wrappers.halo1_map import Halo1Map
from reclaimer.hek.handler             import HaloHandler

class Halo1XboxMap(Halo1Map):
    '''Halo 1 Xbox map'''

    # Module path printed when loading the tag defs
    tag_defs_module = "reclaimer.hek.defs"
    # Handler that controls how to load tags, eg tag definitions
    handler_class = HaloHandler

    def __init__(self, maps=None):
        super().__init__(maps)
