from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

infection_form = Struct("infection form",
    dependency_os("infection form", valid_devices_items_objects_units),
    SIZE=16
    )

infectable_unit = Struct("infectable unit",
    Pad(2),
    dyn_senum16("infection form",
        DYN_NAME_PATH=".....infection_forms.STEPTREE" +
        "[DYN_I].infection_form.filepath"),
    dependency_os("infectable unit", valid_units),
    Float("health threshold"),
    dependency_os("infected unit", valid_units),
    dependency_os("infected unit actor variant", "actv"),
    dependency_os("transition effect", "effe"),
    dependency_os("attachment object", valid_devices_items_objects_units),
    ascii_str32("attachment marker"),
    SInt16("attachment marker count"),
    SIZE=144
    )

unit_infection = Struct("unit infection",
    Pad(4),
    reflexive("infection forms", infection_form, 8,
        DYN_NAME_PATH='.infection_form.filepath'),
    reflexive("infectable units", infectable_unit, 64,
        DYN_NAME_PATH='.infectable_unit.filepath'),
    SIZE=52
    )

boarding_seat = Struct("boarding seat",
    Bool16("flags",
        "boarding ejects target seat",
        "boarding enters target seat",
        "controls open and close",
        ),
    Pad(6),
    ascii_str32("seat label"),
    ascii_str32("target seat label"),
    dependency_os("boarding damage", "jpt!"),
    SIZE=120
    )

unit_external_upgrade = Struct("unit external upgrade",
    Pad(4),
    dependency_os("unit", valid_units),
    reflexive("boarding seats", boarding_seat, 32,
        DYN_NAME_PATH='.seat_label'),
    SIZE=68
    )

gelc_body = Struct("tagdata",
    SInt16("version"),
    Bool16("flags",
        "allow unit infections during cinematics",
        ),
    reflexive("unit infections", unit_infection, 1),
    reflexive("unit external upgrades", unit_external_upgrade, 64,
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
