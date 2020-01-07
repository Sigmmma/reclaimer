#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Named Velocity and Sounds Reflexive
# revision: 3		author: Lord Zedd
# 	Portin'
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

mach_collision_response = (
    "pause_until_crushed",
    "reverse_directions",
    "discs",
    )

mach_pathfinding_policy = (
    "discs",
    "sectors",
    "cut_out",
    "none",
    )

mach_type = (
    "door",
    "platform",
    "gear",
    )


mach_early_mover_propertie = Struct("early_mover_propertie",
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


mach_ai_propertie = Struct("ai_propertie",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    h3_string_id("ai_type_name"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    SEnum16("size", *bloc_ai_propertie_size),
    SEnum16("leap_jump_speed", *bloc_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


mach_function = Struct("function",
    Bool32("flags",
        "invert",
        "mapping_does_not_controls_active",
        "always_active",
        "random_time_offset",
        ),
    h3_string_id("import_name"),
    h3_string_id("export_name"),
    h3_string_id("turn_off_with"),
    Float("minimum_value"),
    h3_rawdata_ref("default_function"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=44
    )


mach_attachment = Struct("attachment",
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


mach_widget = Struct("widget",
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


mach_change_color_initial_permutation = Struct("initial_permutation",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


mach_change_color_function = Struct("function",
    Bool32("scale_flags",
        "blend_in_hsv",
        "more_colors",
        ),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("darken_by"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=32
    )


mach_change_color = Struct("change_color",
    h3_reflexive("initial_permutations", mach_change_color_initial_permutation),
    h3_reflexive("functions", mach_change_color_function),
    ENDIAN=">", SIZE=24
    )


mach_predicted_resource = Struct("predicted_resource",
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


mach_multiplayer_object_propertie = Struct("multiplayer_object_propertie",
    Bool16("engine_flags",
        "capture_the_flag",
        "slayer",
        "oddball",
        "king_of_the_hill",
        "juggernaut",
        "territories",
        "assault",
        "vip",
        "infection",
        ),
    SEnum8("object_type", *bloc_multiplayer_object_propertie_object_type),
    Bool8("teleporter_flags",
        "disallows_players",
        "allows_land_vehicles",
        "allows_heavy_vehicles",
        "allows_flying_vehicles",
        "allows_projectiles",
        ),
    Bool16("flags",
        "editor_only",
        ),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *bloc_multiplayer_object_propertie_spawn_timer_mode),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    Float("radius_width"),
    Float("length"),
    Float("top"),
    Float("bottom"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    SInt32("unknown_3", VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    h3_dependency("child_object"),
    SInt32("unknown_5"),
    h3_dependency("shape_shader"),
    h3_dependency("unknown_shader"),
    h3_dependency("unknown_6"),
    h3_dependency("unknown_7"),
    h3_dependency("unknown_8"),
    h3_dependency("unknown_9"),
    h3_dependency("unknown_10"),
    h3_dependency("unknown_11"),
    ENDIAN=">", SIZE=196
    )


mach_body = Struct("tagdata",
    SEnum16("object_type", *bloc_object_type),
    Bool16("flags_0",
        "does_not_cast_shadow",
        "search_cardinal_direction_lightmaps",
        ("not_a_pathfinding_obstacle", 1 << 3),
        "extension_of_parent",
        "does_not_cause_collision_damage",
        "early_mover",
        "early_mover_localized_physics",
        "use_static_massive_lightmap_sample",
        "object_scales_attachments",
        "inherits_player_s_appearance",
        "dead_bipeds_can_t_localize",
        "attach_to_clusters_by_dynamic_sphere",
        "effects_created_by_this_object_do_not_spawn_objects_in_multiplayer",
        ),
    Float("bounding_radius"),
    QStruct("bounding_offset", INCLUDE=xyz_float),
    Float("acceleration_scale"),
    SEnum16("lightmap_shadow_mode_size", *bloc_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *bloc_sweetener_size),
    SEnum8("water_density", *bloc_water_density),
    SInt32("unknown_0", VISIBLE=False),
    Float("dynamic_light_sphere_radius"),
    QStruct("dynamic_light_sphere_offset", INCLUDE=xyz_float),
    h3_string_id("default_model_variant"),
    h3_dependency("model"),
    h3_dependency("crate_object"),
    h3_dependency("collision_damage"),
    h3_reflexive("early_mover_properties", mach_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", mach_ai_propertie),
    h3_reflexive("functions", mach_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", mach_attachment),
    h3_reflexive("widgets", mach_widget),
    h3_reflexive("change_colors", mach_change_color),
    h3_reflexive("predicted_resources", mach_predicted_resource),
    h3_reflexive("multiplayer_object_properties", mach_multiplayer_object_propertie),
    Bool32("flags_1",
        "position_loops",
        ("position_interpolation", 1 << 2),
        ),
    Float("power_transition_time"),
    Float("power_acceleration_time"),
    Float("position_transition_time"),
    Float("position_acceleration_time"),
    Float("depowered_position_transition_time"),
    Float("depowered_position_acceleration_time"),
    Bool32("lightmap_flags",
        "dont_use_in_lightmap",
        "dont_use_in_lightprobe",
        ),
    h3_dependency("open_up"),
    h3_dependency("close_down"),
    h3_dependency("opened"),
    h3_dependency("closed"),
    h3_dependency("depowered"),
    h3_dependency("repowered"),
    Float("delay_time"),
    h3_dependency("delay_effect"),
    Float("automatic_activation_radius"),
    SEnum16("type", *mach_type),
    Bool16("flags_2",
        "pathfinding_obstacle",
        "but_not_when_open",
        "elevator",
        ),
    Float("door_open_time"),
    QStruct("occlusion_bounds", INCLUDE=from_to),
    SEnum16("collision_response", *mach_collision_response),
    SInt16("elevator_node"),
    SEnum16("pathfinding_policy", *mach_pathfinding_policy),
    SInt16("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=424
    )


def get():
    return mach_def

mach_def = TagDef("mach",
    h3_blam_header('mach'),
    mach_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["mach"], endian=">", tag_cls=H3Tag
    )
