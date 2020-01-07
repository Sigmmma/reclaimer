#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

infection_form = Struct("infection_form",
    dependency_os("infection_form", valid_devices_items_objects_units),
    SIZE=16
    )

infectable_unit = Struct("infectable_unit",
    Pad(2),
    dyn_senum16("infection_form",
        DYN_NAME_PATH=".....infection_forms.STEPTREE" +
        "[DYN_I].infection_form.filepath"),
    dependency_os("infectable_unit", valid_units),
    Float("health_threshold"),
    dependency_os("infected_unit", valid_units),
    dependency_os("infected_unit_actor_variant", "actv"),
    dependency_os("transition_effect", "effe"),
    dependency_os("attachment_object", valid_devices_items_objects_units),
    ascii_str32("attachment_marker"),
    SInt16("attachment_marker_count"),
    SIZE=144
    )

unit_infection = Struct("unit_infection",
    Pad(4),
    reflexive("infection_forms", infection_form, 8,
        DYN_NAME_PATH='.infection_form.filepath'),
    reflexive("infectable_units", infectable_unit, 64,
        DYN_NAME_PATH='.infectable_unit.filepath'),
    SIZE=52
    )

boarding_seat = Struct("boarding_seat",
    Bool16("flags",
        "boarding_ejects_target_seat",
        "boarding_enters_target_seat",
        "controls_open_and_close",
        ),
    Pad(6),
    ascii_str32("seat_label"),
    ascii_str32("target_seat_label"),
    dependency_os("boarding_damage", "jpt!"),
    SIZE=120
    )

unit_external_upgrade = Struct("unit_external_upgrade",
    Pad(4),
    dependency_os("unit", valid_units),
    reflexive("boarding_seats", boarding_seat, 32,
        DYN_NAME_PATH='.seat_label'),
    SIZE=68
    )

gelc_body = Struct("tagdata",
    SInt16("version"),
    Bool16("flags",
        "allow_unit_infections_during_cinematics",
        ),
    reflexive("unit_infections", unit_infection, 1),
    reflexive("unit_external_upgrades", unit_external_upgrade, 64,
        DYN_NAME_PATH='.unit.filepath'),
    SIZE=172
    )

def get():
    return gelc_def

gelc_def = TagDef("gelc",
    blam_header_os('gelc'),
    gelc_body,

    ext=".project_yellow_globals_cv", endian=">", tag_cls=HekTag
    )
