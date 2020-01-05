#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os

from reclaimer.hek.defs.objs.tag import HekTag

class ShdrTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        full_class_name = self.data.blam_header.tag_class.enum_name

        self.ext = '.' + full_class_name
        self.filepath = os.path.splitext(str(self.filepath))[0] + self.ext

        shader_type = self.data.tagdata.shdr_attrs.shader_type
        if full_class_name == "shader":
            shader_type.data = -1
        elif full_class_name == "shader_environment":
            shader_type.data = 3
        elif full_class_name == "shader_model":
            shader_type.data = 4
        elif full_class_name == "shader_transparent_generic":
            shader_type.data = 5
        elif full_class_name == "shader_transparent_chicago":
            shader_type.data = 6
        elif full_class_name == "shader_transparent_chicago_extended":
            shader_type.data = 7
        elif full_class_name == "shader_transparent_water":
            shader_type.data = 8
        elif full_class_name == "shader_transparent_glass":
            shader_type.data = 9
        elif full_class_name == "shader_transparent_meter":
            shader_type.data = 10
        elif full_class_name == "shader_transparent_plasma":
            shader_type.data = 11
        else:
            raise ValueError("Unknown shader type '%s'" % full_class_name)
