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
# revision: 2		author: Lord Zedd
# 	Done
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

styl_combat_status_decay_options = (
    "latch_at_idle",
    "latch_at_alert",
    "latch_at_combat",
    )


styl_special_movement = Struct("special_movement",
    Bool32("special_movement_1",
        "jump",
        "climb",
        "vault",
        "mount",
        "hoist",
        "wall_jump",
        "n_a",
        ),
    ENDIAN=">", SIZE=4
    )


styl_behavior_list = Struct("behavior_list",
    ascii_str32("behavior_name"),
    ENDIAN=">", SIZE=32
    )


styl_body = Struct("tagdata",
    ascii_str32("name"),
    SEnum16("combat_status_decay_options", *styl_combat_status_decay_options),
    SInt16("unknown", VISIBLE=False),
    Bool32("style_control",
        "new_behaviors_default_to_on",
        ),
    Bool32("behaviors1",
        "general",
        "root",
        "null",
        "null_discrete",
        "obey",
        "guard",
        "follow_behavior",
        "ready",
        "smash_obstacle",
        "destroy_obstacle",
        "perch",
        "cover_friend",
        "blind_panic",
        "combat",
        "broken",
        "broken_behavior",
        "huddle_impulse",
        "huddle_behavior",
        "kamikaze_behavior",
        "broken_kamikaze_impulse",
        "broken_berserk_impulse",
        "broken_flee_impulse",
        "broken_scatter_impulse",
        "engage_0",
        "equipment",
        "engage_1",
        "fight",
        "melee_charge",
        "melee_leaping_charge",
        "surprise",
        "grenade_impulse",
        "anti_vehicle_grenade",
        ),
    Bool32("behaviors2",
        "stalk",
        "flank",
        "berserk_wander_impulse",
        "stalker_camo_control",
        "leader_abandoned_berserk",
        "unassailable_grenade_impulse",
        "perimeter",
        "perimeter_timeout_morph",
        "perimeter_infection_spew",
        "berserk",
        "shield_depleted_berserk",
        "last_man_berserk",
        "stuck_with_grenade_berserk",
        "presearch_0",
        "presearch_1",
        "presearch_uncover",
        "destroy_cover",
        "suppressing_fire",
        "grenade_uncover",
        "leap_on_cover",
        "leader",
        "search_sync",
        "engage_sync",
        "search_0",
        "search_1",
        "uncover",
        "investigate",
        "pursuit_sync",
        "pursuit",
        "refresh_target",
        "sense_target",
        "postsearch",
        ),
    Bool32("behaviors3",
        "coverme_investigate",
        "self_defense",
        "self_preservation",
        "cover",
        "cover_peek",
        "avoid",
        "evasion_impulse",
        "dive_impulse",
        "danger_cover_impulse",
        "danger_crouch_impulse",
        "proximity_melee",
        "proximity_self_preservation",
        "unreachable_enemy_cover",
        "unassailable_enemy_cover",
        "scary_target_cover",
        "group_emerge",
        "shield_depleted_cover",
        "retreat_0",
        "retreat_1",
        "retreat_grenade",
        "flee",
        "cower",
        "low_shield_retreat",
        "scary_target_retreat",
        "leader_dead_retreat",
        "peer_dead_retreat",
        "danger_retreat",
        "proximity_retreat",
        "charge_when_cornered",
        "surprise_retreat",
        "overheated_weapon_retreat",
        "ambush",
        ),
    Bool32("behaviors4",
        "ambush",
        "coordinated_ambush",
        "proximity_ambush",
        "vulnerable_enemy_ambush",
        "nowhere_to_run_ambush",
        "vehicle",
        "enter_vehicle",
        "enter_friendly_vehicle",
        "vehicle_enter_impulse",
        "vehicle_entry_engage_impulse",
        "vehicle_board",
        "vehicle_fight",
        "vehicle_fight_boost",
        "vehicle_charge",
        "vehicle_ram_behavior",
        "vehicle_cover",
        "damage_vehicle_cover",
        "exposed_rear_cover_impulse",
        "player_endagered_cover_impulse",
        "vehicle_avoid",
        "vehicle_pickup",
        "vehicle_player_pickup",
        "vehicle_exit_impulse",
        "danger_vehicle_exit_impulse",
        "vehicle_flip_impulse",
        "vehicle_flip",
        "vehicle_turtle",
        "vehicle_engage_patrol_impulse",
        "vehicle_engage_wander_impulse",
        "postcombat_0",
        "postcombat_1",
        "post_postcombat",
        ),
    Bool32("behaviors5",
        "check_friend",
        "shoot_corpse",
        "postcombat_approach",
        "alert_0",
        "alert_1",
        "idle_0",
        "idle_1",
        "wander_behavior",
        "flight_wander",
        "patrol",
        "fall_sleep",
        "buggers",
        "bugger_ground_uncover",
        "swarms",
        "swarm_root",
        "swarm_attack",
        "support_attack",
        "infect",
        "scatter",
        "combatforms",
        "combat_form_berserk_control",
        "eject_parasite",
        "sentinels",
        "enforcer_weapon_control",
        "grapple",
        "guardians",
        "guardian_surge",
        "guardian_proximity_surge",
        "guardian_danger_surge",
        "guardian_isolation_surge",
        "pureforms",
        "group_morph_impulse",
        ),
    Bool32("behaviors6",
        "arrival_morph_impulse",
        "pureform_default_impulse",
        "search_morph",
        "stealth_active_camo_control",
        "stealth_damage_morph",
        "stealth_stalk",
        "stealth_stalk_thwarted",
        "stealth_stalk_group",
        "stealth_charge_recover",
        "ranged_proximity_morph",
        "tank_distance_damage_morph",
        "tank_throttle_control",
        "stealth_morph",
        "tank_morph",
        "ranged_morph",
        "ranged_turtle",
        "ranged_uncover",
        "scarab",
        "scarab_root",
        "scarab_cure_isolation",
        "scarab_combat",
        "scarab_fight",
        "scarab_target_lock",
        "scarab_search",
        "scarab_search_pause",
        "atoms",
        "go_to",
        "activities",
        "activity",
        "posture",
        "activity_default",
        "special",
        ),
    Bool32("behaviors7",
        "formation",
        "grunt_scared_by_elite",
        "stunned",
        "cure_isolation",
        "deploy_turret",
        ),
    h3_reflexive("special_movement", styl_special_movement),
    h3_reflexive("behavior_list", styl_behavior_list),
    ENDIAN=">", SIZE=92
    )


def get():
    return styl_def

styl_def = TagDef("styl",
    h3_blam_header('styl'),
    styl_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["styl"], endian=">", tag_cls=H3Tag
    )
