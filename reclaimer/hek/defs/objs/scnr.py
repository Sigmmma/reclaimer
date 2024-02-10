#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
import traceback

from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.halo_script.hsc import HSC_IS_SCRIPT_OR_GLOBAL,\
    get_hsc_data_block, clean_script_syntax_nodes

class ScnrTag(HekTag):
    # used to determine what syntax node block to use when parsing script data
    engine = "halo1ce"

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        self.clean_script_syntax_data()

    def clean_script_syntax_data(self):
        try:
            script_syntax_data = self.data.tagdata.script_syntax_data
            script_nodes = get_hsc_data_block(
                script_syntax_data.data, self.engine
                )
            clean_script_syntax_nodes(script_nodes)

            # replace the sanitized data
            script_syntax_data.data = script_nodes.serialize()
        except Exception:
            print(traceback.format_exc())
            print("Failed to sanitize script syntax data nodes.")