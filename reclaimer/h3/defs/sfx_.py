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
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


sfx__sound_effect_filter = Struct("filter",
    SInt32("filter_type"),
    SInt32("filter_width"),
    Pad(64),
    ENDIAN=">", SIZE=72
    )


sfx__sound_effect_pitch_lfo = Struct("pitch_lfo",
    Pad(48),
    ENDIAN=">", SIZE=48
    )


sfx__sound_effect_filter_lfo = Struct("filter_lfo",
    Pad(64),
    ENDIAN=">", SIZE=48
    )


sfx__sound_effect_sound_effect_component = Struct("component",
    h3_dependency("sound"),
    Pad(4),
    SInt32("flags"),
    ENDIAN=">", SIZE=24
    )


sfx__sound_effect_sound_effect_template_collection_parameter = Struct("parameter",
    h3_string_id("name"),
    Pad(20),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=44
    )


sfx__sound_effect_sound_effect_template_collection = Struct("template_collection",
    h3_string_id("dsp_effect"),
    h3_reflexive("parameters", sfx__sound_effect_sound_effect_template_collection_parameter),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


sfx__sound_effect_sound_effect = Struct("sound_effect",
    h3_dependency("unknown_0"),
    h3_reflexive("components", sfx__sound_effect_sound_effect_component),
    h3_reflexive("template_collection", sfx__sound_effect_sound_effect_template_collection),
    BytesRaw("unknown_1", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=72
    )


sfx__sound_effect = Struct("sound_effect",
    h3_string_id("name"),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    Bool32("flags",
        "use_3d_radio_hack",
        ),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_reflexive("filter", sfx__sound_effect_filter),
    h3_reflexive("pitch_lfo", sfx__sound_effect_pitch_lfo),
    h3_reflexive("filter_lfo", sfx__sound_effect_filter_lfo),
    h3_reflexive("sound_effect", sfx__sound_effect_sound_effect),
    ENDIAN=">", SIZE=76
    )


sfx__body = Struct("tagdata",
    h3_reflexive("sound_effects", sfx__sound_effect),
    ENDIAN=">", SIZE=12
    )


def get():
    return sfx__def

sfx__def = TagDef("sfx+",
    h3_blam_header('sfx+'),
    sfx__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["sfx+"], endian=">", tag_cls=H3Tag
    )
