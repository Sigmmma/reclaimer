#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scnr import *
from supyr_struct.util import desc_variant

object_ref_flags = Bool16('not_placed',
    "automatically",
    "on_easy",
    "on_normal",
    "on_hard",
    "use_player_appearance",
    )

# macro to cut down on a lot of duplicated definitions
def add_player_appearance_fields(desc, lpad_size=4, insert=True):
    desc    = desc_variant(desc, ('not_placed', object_ref_flags))
    attr_i  = (object_reference('_') if insert else desc)["ENTRIES"]
    fields  = [
        *(dict(desc[i]) for i in range(attr_i)),
        Pad(lpad_size), SInt8("appearance_player_index"),
        *(dict(desc[i]) for i in range(attr_i, desc["ENTRIES"])),
        ]
    if len(fields)-2 > attr_i:
        # shrink the padding after the appearance_player_index
        # by the lpad_size + the size of appearance_player_index
        fields[attr_i+2]["SIZE"] -= lpad_size + 1

    desc.update({i: fdesc for i, fdesc in enumerate(fields)})
    desc.update(ENTRIES=len(fields))
    return desc

# Object references
scenery         = add_player_appearance_fields(scenery)
equipment       = add_player_appearance_fields(equipment, 0, False)
sound_scenery   = add_player_appearance_fields(sound_scenery)
biped           = add_player_appearance_fields(biped)
vehicle         = add_player_appearance_fields(vehicle)
weapon          = add_player_appearance_fields(weapon)
machine         = add_player_appearance_fields(machine)
control         = add_player_appearance_fields(control)
light_fixture   = add_player_appearance_fields(light_fixture)


starting_equipment_flags = Bool32("flags",
    "no_grenades",
    "plasma_grenades_only",
    "type2_grenades_only",
    "type3_grenades_only",
    )
parameters = Struct("parameters",
    ascii_str32("name", EDITABLE=False),
    SEnum16("return_type", *script_object_types, EDITABLE=False),
    SIZE=36,
    )
halo_script = Struct("script",
    # copy positional fields from halo_script descriptor
    *(halo_script[i] for i in range(halo_script["ENTRIES"])),
    Pad(40),
    reflexive("parameters", parameters, 16),
    SIZE=92,
    )

player_starting_profile = Struct("player_starting_profile",
    # copy positional fields from player_starting_profile descriptor
    *(player_starting_profile[i] for i in range(player_starting_profile["ENTRIES"])),
    SInt8("starting_grenade_type2_count", MIN=0),
    SInt8("starting_grenade_type3_count", MIN=0),
    SIZE=104
    )
netgame_equipment = desc_variant(netgame_equipment,
    ("team_index", SInt16("usage_id")),
    )
starting_equipment = desc_variant(starting_equipment,
    ("flags", starting_equipment_flags),
    )
source_file = desc_variant(source_file,
    ("source", rawdata_ref("source", max_size=1048576, widget=HaloScriptSourceFrame))
    )

cutscene_title = Struct("cutscene_title",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("text_bounds",
        SInt16("t"), SInt16("l"), SInt16("b"), SInt16("r"),
        ORIENT='h',
        ),
    SInt16("string_index"),
    SEnum16("text_style",
        "plain",
        "bold",
        "italic",
        "condense",
        "underline",
        ),
    SEnum16("justification",
        "left",
        "right",
        "center",
        ),
    Pad(2),
    Bool32("flags",
        "wrap horizontally",
        "wrap vertically",
        "center vertically",
        "bottom justify",
        ),
    UInt32("text_color", INCLUDE=argb_uint32),
    UInt32("shadow_color", INCLUDE=argb_uint32),
    float_sec("fade_in_time"),  # seconds
    float_sec("up_time"),  # seconds
    float_sec("fade_out_time"),  # seconds
    SIZE=96
    )

scavenger_hunt_objects = Struct("scavenger_hunt_objects",
    ascii_str32("exported_name"),
    dyn_senum16("scenario_object_name_index", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    Pad(2),
    SIZE=36
    )

scnr_body = Struct("tagdata",
    dependency("DONT_USE", 'sbsp'),
    dependency("WONT_USE", 'sbsp'),
    dependency("CANT_USE", 'sky '),
    reflexive("skies", sky, 8, DYN_NAME_PATH='.sky.filepath'),
    SEnum16("type",
        "singleplayer",
        "multiplayer",
        "main_menu"
        ),
    Bool16("flags",
        "cortana_hack",
        "use_demo_ui",
        {NAME: "color_correction", GUI_NAME: "color correction (ntsc->srgb)"},
        "DO_NOT_apply_bungie_campaign_tag_patches",
        ),
    reflexive("child_scenarios", child_scenario, 16,
        DYN_NAME_PATH='.child_scenario.filepath'),
    float_rad("local_north"),  # radians

    Pad(156),
    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("functions", function, 32,
        DYN_NAME_PATH='.name'),
    rawdata_ref("scenario_editor_data", max_size=65536),
    reflexive("comments", comment, 1024),
    reflexive("scavenger_hunt_objects", scavenger_hunt_objects, 16),

    Pad(212),
    reflexive("object_names", object_name, 640,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("sceneries", scenery, 2000, IGNORE_SAFE_MODE=True),
    reflexive("sceneries_palette", scenery_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("bipeds", biped, 128, IGNORE_SAFE_MODE=True),
    reflexive("bipeds_palette", biped_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("vehicles", vehicle, 256, IGNORE_SAFE_MODE=True),
    reflexive("vehicles_palette", vehicle_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("equipments", equipment, 256, IGNORE_SAFE_MODE=True),
    reflexive("equipments_palette", equipment_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("weapons", weapon, 128, IGNORE_SAFE_MODE=True),
    reflexive("weapons_palette", weapon_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),

    reflexive("device_groups", device_group, 128,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("machines", machine, 400, IGNORE_SAFE_MODE=True),
    reflexive("machines_palette", machine_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("controls", control, 100, IGNORE_SAFE_MODE=True),
    reflexive("controls_palette", control_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("light_fixtures", light_fixture, 500, IGNORE_SAFE_MODE=True),
    reflexive("light_fixtures_palette", light_fixture_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("sound_sceneries", sound_scenery, 256, IGNORE_SAFE_MODE=True),
    reflexive("sound_sceneries_palette", sound_scenery_swatch, 256,
        DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("player_starting_profiles", player_starting_profile, 256,
        DYN_NAME_PATH='.name'),
    reflexive("player_starting_locations", player_starting_location, 256),
    reflexive("trigger_volumes", trigger_volume, 256,
        DYN_NAME_PATH='.name'),
    reflexive("recorded_animations", recorded_animation, 1024,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("netgame_flags", netgame_flag, 200,
        DYN_NAME_PATH='.type.enum_name'),
    reflexive("netgame_equipments", netgame_equipment, 200,
        DYN_NAME_PATH='.item_collection.filepath'),
    reflexive("starting_equipments", starting_equipment, 200),
    reflexive("bsp_switch_trigger_volumes", bsp_switch_trigger_volume, 256),
    reflexive("decals", decal, 65535),
    reflexive("decals_palette", decal_swatch, 128,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("detail_object_collection_palette",
        detail_object_collection_swatch, 32, DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("actors_palette", actor_swatch, 64,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("encounters", encounter, 128, DYN_NAME_PATH='.name'),
    reflexive("command_lists", command_list, 256, DYN_NAME_PATH='.name'),
    reflexive("ai_animation_references", ai_anim_reference, 128,
        DYN_NAME_PATH='.animation_name'),
    reflexive("ai_script_references", ai_script_reference, 128,
        DYN_NAME_PATH='.script_name'),
    reflexive("ai_recording_references", ai_recording_reference, 128,
        DYN_NAME_PATH='.recording_name'),
    reflexive("ai_conversations", ai_conversation, 128,
        DYN_NAME_PATH='.name'),
    rawdata_ref("script_syntax_data", max_size=655396, IGNORE_SAFE_MODE=True),
    rawdata_ref("script_string_data", max_size=819200, IGNORE_SAFE_MODE=True),
    reflexive("scripts", halo_script, 1024, DYN_NAME_PATH='.name'),
    reflexive("globals", halo_global, 512, DYN_NAME_PATH='.name'),
    reflexive("references", reference, 512,
              DYN_NAME_PATH='.reference.filepath'),
    reflexive("source_files", source_file, 16, DYN_NAME_PATH='.source_name'),

    Pad(24),
    reflexive("cutscene_flags", cutscene_flag, 512, DYN_NAME_PATH='.name'),
    reflexive("cutscene_camera_points", cutscene_camera_point, 512,
        DYN_NAME_PATH='.name'),
    reflexive("cutscene_titles", cutscene_title, 64, DYN_NAME_PATH='.name'),
    Pad(108),
    dependency("custom_object_names", 'ustr'),
    dependency("ingame_help_text", 'ustr'),
    dependency("hud_messages", 'hmt '),
    reflexive("structure_bsps", structure_bsp, 16,
        DYN_NAME_PATH='.structure_bsp.filepath'),
    SIZE=1456,
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )
