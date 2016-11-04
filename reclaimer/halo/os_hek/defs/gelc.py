from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

infection_form = dependency("infected unit", valid_devices_items_objects_units)

infectable_unit = Struct("infectable unit",
    Pad(2),
    BSInt16("infection form"),
    dependency("infectable unit", valid_units),
    BFloat("health threshold"),
    dependency("infected unit", valid_units),
    dependency("infected unit actor variant", valid_actor_variants),
    dependency("transition effect", valid_effects),
    dependency("attachment object", valid_devices_items_objects_units),
    ascii_str32("attachment marker"),
    BSInt16("attachment marker count"),
    SIZE=144
    )

unit_infection = Struct("unit infection",
    Pad(4),
    reflexive("infection forms", infection_form, 8),
    reflexive("infectable units", infectable_unit, 64),
    SIZE=52
    )

boarding_seat = Struct("boarding seat",
    BBool16("flags",
        "boarding ejects target seat",
        "boarding enters target seat",
        "controls open and close",
        ),
    Pad(6),
    ascii_str32("seat label"),
    ascii_str32("target seat label"),
    dependency("boarding damage", valid_damage_effects),
    SIZE=120
    )

unit_external_upgrade = Struct("unit external upgrade",
    Pad(4),
    dependency("unit", valid_units),
    reflexive("infectable units", boarding_seat, 32),
    SIZE=68
    )

gelc_body = Struct("tagdata",
    BSInt16("version"),
    BBool16("flags",
        "allow unit infections during cinematics",
        ),
    reflexive("unit infections", unit_infection, 1),
    reflexive("unit external upgrades", unit_external_upgrade, 64),
    SIZE=172
    )

def get():
    return gelc_def

gelc_def = TagDef("gelc",
    blam_header_os('gelc'),
    gelc_body,

    ext=".project_yellow_globals_cv", endian=">"
    )
