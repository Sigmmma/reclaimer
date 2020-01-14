#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.animation import animation_decompilation
from reclaimer.bitmaps import bitmap_decompilation
from reclaimer.halo_script import hsc_decompilation
from reclaimer.model import model_decompilation
from reclaimer.physics import physics_decompilation
from reclaimer.sounds import sound_decompilation
from reclaimer.strings import strings_decompilation


h1_data_extractors = {
    'phys': physics_decompilation.extract_physics,
    'mode': model_decompilation.extract_model,
    'mod2': model_decompilation.extract_model,
    'antr': animation_decompilation.extract_model_animations,
    'magy': animation_decompilation.extract_model_animations,
    #'coll': extract_collision,
    #'sbsp': None, 'font': None, 'unic': None,
    'str#': strings_decompilation.extract_string_list,
    'ustr': strings_decompilation.extract_unicode_string_list,
    "hmt ": strings_decompilation.extract_hud_message_text,
    "bitm": bitmap_decompilation.extract_bitmaps,
    "snd!": sound_decompilation.extract_h1_sounds,
    'scnr': hsc_decompilation.extract_h1_scripts,
    }

h2_data_extractors = {
    #'mode', 'coll', 'phmo', 'jmad',
    #'sbsp',

    #'unic',
    "bitm": bitmap_decompilation.extract_bitmaps,
    "snd!": sound_decompilation.extract_h2_sounds,
    }

h3_data_extractors = {
    "bitm": bitmap_decompilation.extract_bitmaps,
    }
