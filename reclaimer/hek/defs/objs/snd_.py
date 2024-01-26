#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag

class Snd_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        tagdata = self.data.tagdata

        for pitch_range in tagdata.pitch_ranges.STEPTREE:
            pitch_range.playback_rate = 1
            if pitch_range.natural_pitch:
                pitch_range.playback_rate = 1 / pitch_range.natural_pitch

        # default sound min and max distance by class
        sound_class = tagdata.sound_class.enum_name
        distance_defaults = None
        if sound_class in (
                "device_door", "device_force_field", "device_machinery",
                "device_nature", "music", "ambient_nature", "ambient_machinery"
                ):
            distance_defaults = (0.9, 5.0)
        elif sound_class in (
                "weapon_ready", "weapon_reload", "weapon_empty",
                "weapon_charge", "weapon_overheat", "weapon_idle"
                ):
            distance_defaults = (1.0, 9.0)
        elif sound_class in (
                "unit_dialog", "scripted_dialog_player",
                "scripted_dialog_other",
                "scripted_dialog_force_unspatialized", "game_event"
                ):
            distance_defaults = (3.0, 20.0)
        elif sound_class in (
                "object_impacts", "particle_impacts", "slow_particle_impacts",
                "device_computers", "ambient_computers", "first_person_damage",
                ):
            distance_defaults = (0.5, 3.0)
        elif sound_class in (
                "projectile_impact", "vehicle_collision", "vehicle_engine"
                ):
            distance_defaults = (1.4, 8.0)
        elif sound_class == "weapon_fire":
            distance_defaults = (4.0, 70.0)
        elif sound_class == "scripted_effect":
            distance_defaults = (2.0, 5.0)
        elif sound_class == "projectile_detonation":
            distance_defaults = (8.0, 120.0)
        elif sound_class == "unit_footsteps":
            distance_defaults = (0.9, 10.0)

        zero_gain_modifier_default = 1.0
        if sound_class in (
                "object_impacts", "particle_impacts", "slow_particle_impacts",
                "unit_dialog", "music", "ambient_nature", "ambient_machinery",
                "ambient_computers", "scripted_dialog_player",
                "scripted_effect", "scripted_dialog_other",
                "scripted_dialog_force_unspatialized"
                ):
            zero_gain_modifier_default = 0.0

        if distance_defaults:
            if not tagdata.minimum_distance:
                tagdata.minimum_distance = distance_defaults[0]

            if not tagdata.maximum_distance:
                tagdata.maximum_distance = distance_defaults[1]

        if (not tagdata.modifiers_when_scale_is_zero.gain and 
            not tagdata.modifiers_when_scale_is_one.gain
            ):
            tagdata.modifiers_when_scale_is_zero.gain = zero_gain_modifier_default
            tagdata.modifiers_when_scale_is_one.gain = 1.0