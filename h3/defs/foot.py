from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

foot_effect_old_material_sweetener_mode = (
    "sweetener_default",
    "sweetener_enabled",
    "sweetener_disabled",
    )


foot_effect_old_material = Struct("old_materials",
    dependency("effect"),
    dependency("sound"),
    string_id_meta("material_name"),
    SInt16("global_material_index"),
    SEnum8("sweetener_mode", *foot_effect_old_material_sweetener_mode),
    SInt8("unknown"),
    ENDIAN=">", SIZE=40
    )


foot_effect_sound = Struct("sounds",
    dependency("tag"),
    dependency("secondary_tag"),
    string_id_meta("material_name"),
    SInt16("global_material_index"),
    SEnum8("sweetener_mode", *foot_effect_old_material_sweetener_mode),
    SInt8("unknown"),
    ENDIAN=">", SIZE=40
    )


foot_effect_effect = Struct("effects",
    dependency("tag"),
    dependency("secondary_tag"),
    string_id_meta("material_name"),
    SInt16("global_material_index"),
    SEnum8("sweetener_mode", *foot_effect_old_material_sweetener_mode),
    SInt8("unknown"),
    ENDIAN=">", SIZE=40
    )


foot_effect = Struct("effects",
    reflexive("old_materials", foot_effect_old_material),
    reflexive("sounds", foot_effect_sound),
    reflexive("effects", foot_effect_effect),
    ENDIAN=">", SIZE=36
    )


foot_meta_def = BlockDef("foot",
    reflexive("effects", foot_effect),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )