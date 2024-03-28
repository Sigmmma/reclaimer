#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scnr import *

object_ref_flags = Bool16('not_placed',
    "automatically",
    "on_easy",
    "on_normal",
    "on_hard",
    "use_player_appearance",
    )

starting_equipment_flags = Bool32("flags",
    "no_grenades",
    "plasma_grenades_only",
    "type2_grenades_only",
    "type3_grenades_only",
    )
parameter = Struct("parameter",
    ascii_str32("name", EDITABLE=False),
    SEnum16("return_type", *script_object_types, EDITABLE=False),
    Pad(2),
    SIZE=36,
    )
cutscene_title_flags = Bool32("flags",
    "wrap_horizontally",
    "wrap_vertically",
    "center_vertically",
    "bottom_justify",
    )
scavenger_hunt_objects = Struct("scavenger_hunt_objects",
    ascii_str32("exported_name"),
    dyn_senum16("scenario_object_name_index", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    Pad(2),
    SIZE=36
    )

# Object references
object_ref_replacements = (
    ('not_placed', object_ref_flags),
    ("pad_8", SInt8("appearance_player_index")),
    )

scenery         = desc_variant(scenery, *object_ref_replacements)
equipment       = desc_variant(equipment, *object_ref_replacements)
sound_scenery   = desc_variant(sound_scenery, *object_ref_replacements)
biped           = desc_variant(biped, *object_ref_replacements)
vehicle         = desc_variant(vehicle, *object_ref_replacements)
weapon          = desc_variant(weapon, *object_ref_replacements)
machine         = desc_variant(machine, *object_ref_replacements)
control         = desc_variant(control, *object_ref_replacements)
light_fixture   = desc_variant(light_fixture, *object_ref_replacements)

player_starting_profile = desc_variant(player_starting_profile,
    ("pad_11", SInt8("starting_grenade_type2_count", MIN=0)),
    ("pad_12", SInt8("starting_grenade_type3_count", MIN=0)),
    )
netgame_equipment = desc_variant(netgame_equipment,
    ("team_index", SInt16("usage_id")),
    )
starting_equipment = desc_variant(starting_equipment,
    starting_equipment_flags
    )
halo_script = desc_variant(halo_script,
    ("pad_6", reflexive("parameters", parameter, 16))
    )
source_file = desc_variant(source_file,
    rawdata_ref("source", max_size=1048576, widget=HaloScriptSourceFrame),
    )
cutscene_title = desc_variant(cutscene_title,
    ("pad_8", cutscene_title_flags),
    )

scnr_flags = Bool16("flags",
    "cortana_hack",
    "use_demo_ui",
    {NAME: "color_correction", GUI_NAME: "color correction (ntsc->srgb)"},
    "DO_NOT_apply_bungie_campaign_tag_patches",
    )

scnr_body = desc_variant(scnr_body,
    scnr_flags,
    ("pad_13",       reflexive("scavenger_hunt_objects", scavenger_hunt_objects, 16)),
    reflexive("object_names", object_name,   640, DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("sceneries",  scenery,  2000, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("bipeds",     biped,     128, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("vehicles",   vehicle,   256, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("equipments", equipment, 256, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("weapons",    weapon,    128, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("machines",   machine,   400, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("controls",   control,   100, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("light_fixtures",  light_fixture, 500, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("sound_sceneries", sound_scenery, 256, IGNORE_SAFE_MODE=True, EXT_MAX=SINT16_MAX),
    reflexive("sceneries_palette",  scenery_swatch,   256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("bipeds_palette",     biped_swatch,     256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("vehicles_palette",   vehicle_swatch,   256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("equipments_palette", equipment_swatch, 256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("weapons_palette",    weapon_swatch,    256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("machines_palette",   machine_swatch,   256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("controls_palette",   control_swatch,   256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("light_fixtures_palette",   light_fixture_swatch,    256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("sound_sceneries_palette",  sound_scenery_swatch,    256, DYN_NAME_PATH='.name.filepath', EXT_MAX=SINT16_MAX),
    reflexive("player_starting_profiles", player_starting_profile, 256, DYN_NAME_PATH='.name', EXT_MAX=SINT16_MAX),
    reflexive("netgame_equipments",  netgame_equipment, 200, DYN_NAME_PATH='.item_collection.filepath', EXT_MAX=SINT16_MAX),
    reflexive("starting_equipments", starting_equipment, 200, EXT_MAX=SINT16_MAX),
    rawdata_ref("script_syntax_data", max_size=655396, IGNORE_SAFE_MODE=True),
    rawdata_ref("script_string_data", max_size=819200, IGNORE_SAFE_MODE=True),
    reflexive("scripts", halo_script, 1024, DYN_NAME_PATH='.name'),
    reflexive("globals", halo_global, 512, DYN_NAME_PATH='.name'),
    reflexive("references", reference, 512, DYN_NAME_PATH='.reference.filepath'),
    reflexive("source_files", source_file, 16, DYN_NAME_PATH='.source_name'),
    reflexive("cutscene_titles", cutscene_title, 64, DYN_NAME_PATH='.name'),
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=ScnrTag
    )
