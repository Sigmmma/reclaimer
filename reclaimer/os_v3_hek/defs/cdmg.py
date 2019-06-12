from ...hek.defs.cdmg import *

damage = Struct("damage",
    SEnum16("priority",
        "none",
        "harmless",
        {NAME: "backstab", GUI_NAME: "lethal to the unsuspecting"},
        "emp",
        ),
    SEnum16("category", *damage_category),
    Bool32("flags",
        "does_not_hurt_owner",
        {NAME: "headshot", GUI_NAME: "causes headshots"},
        "pings_resistant_units",
        "does_not_hurt_friends",
        "does_not_ping_shields",
        "detonates_explosives",
        "only_hurts_shields",
        "causes_flaming_death",
        {NAME: "indicator_points_down",
         GUI_NAME: "damage indicator always points down"},
        "skips_shields",
        "only_hurts_one_infection_form",
        {NAME: "multiplayer_headshot",
         GUI_NAME: "causes multiplayer headshots"},
        "infection_form_pop",
        "YELO_3D_instantaneous_acceleration"
        ),
    Pad(4),
    Float("damage_lower_bound"),
    QStruct("damage_upper_bound", INCLUDE=from_to),
    float_zero_to_one("vehicle_passthrough_penalty"),
    Pad(4),
    float_zero_to_one("stun"),
    float_zero_to_one("maximum_stun"),
    float_sec("stun_time"),
    Pad(4),
    QStruct("instantaneous_acceleration",
        Float("i", UNIT_SCALE=per_sec_unit_scale),
        Float("j", UNIT_SCALE=per_sec_unit_scale),
        Float("k", UNIT_SCALE=per_sec_unit_scale),
        SIDETIP="[-inf,+inf]", ORIENT="h"
        ),
    )

cdmg_body = dict(cdmg_body)
cdmg_body[5] = damage

def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
