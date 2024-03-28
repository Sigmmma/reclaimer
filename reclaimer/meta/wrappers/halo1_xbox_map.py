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
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None

    def is_indexed(self, tag_id):
        return False

    @property
    def resource_maps_folder(self): return None
    @property
    def uses_bitmaps_map(self): return False
    @property
    def uses_loc_map(self): return False
    @property
    def uses_sounds_map(self): return False