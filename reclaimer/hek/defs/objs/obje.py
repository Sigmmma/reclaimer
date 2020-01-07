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

class ObjeTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)

        full_class_name = self.data.blam_header.tag_class.enum_name

        self.ext = '.' + full_class_name
        self.filepath = os.path.splitext(str(self.filepath))[0] + self.ext

        object_type = self.data.tagdata.obje_attrs.object_type
        if full_class_name == "object":
            object_type.data = -1
        elif full_class_name == "biped":
            object_type.data = 0
        elif full_class_name == "vehicle":
            object_type.data = 1
        elif full_class_name == "weapon":
            object_type.data = 2
        elif full_class_name == "equipment":
            object_type.data = 3
        elif full_class_name == "garbage":
            object_type.data = 4
        elif full_class_name == "projectile":
            object_type.data = 5
        elif full_class_name == "scenery":
            object_type.data = 6
        elif full_class_name == "device_machine":
            object_type.data = 7
        elif full_class_name == "device_control":
            object_type.data = 8
        elif full_class_name == "device_light_fixture":
            object_type.data = 9
        elif full_class_name == "placeholder":
            object_type.data = 10
        elif full_class_name == "sound_scenery":
            object_type.data = 11
        else:
            raise ValueError("Unknown object type '%s'" % full_class_name)
