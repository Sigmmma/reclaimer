#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from reclaimer.meta.wrappers.halo1_map import Halo1Map
from reclaimer.os_v4_hek.handler       import OsV4HaloHandler

class Halo1YeloMap(Halo1Map):
    '''Generation 1 Yelo map'''

    # Module path printed when loading the tag defs
    tag_defs_module = "reclaimer.os_v4_hek.defs"
    # Handler that controls how to load tags, eg tag definitions
    handler_class = OsV4HaloHandler

    def __init__(self, maps=None):
        Halo1Map.__init__(self, maps)
