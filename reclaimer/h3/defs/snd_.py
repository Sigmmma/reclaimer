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
# 	Labelled Raw Identifier
# revision: 3		author: Xerax
#
# revision: 4		author: Lord Zedd
# 	Standardized
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


snd__body = Struct("tagdata",
    Bool16("flags",
        "fit_to_adpcm_blocksize",
        "split_long_sound_into_permutations",
        "always spatialize",
        "never obstruct",
        {NAME: "INTERNAL DONT TOUCH", EDITABLE:False},
        "use huge sound transmission"
        "link count to owner unit",
        "pitch range is language",
        "dont use sound class speaker flags",
        "dont use lipsync data",
        ),
    SEnum8("sound_class", *snd__sound_class),
    UEnum8("compression",
        "xma",
        ),
    SInt16("platform_codec_index"),
    SInt16("pitch_range_index"),
    SInt16("language_b_index"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("playback_parameter_index"),
    SInt16("scale_index"),
    SInt8("promotion_index"),
    SInt8("custom_playback_index"),
    SInt16("extra_info_index"),
    SInt32("maximum_play_time"),
    zone_asset("asset_data"),
    ENDIAN=">", SIZE=32
    )


def get():
    return snd__def

snd__def = TagDef("snd!",
    h3_blam_header('snd!'),
    snd__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["snd!"], endian=">", tag_cls=H3Tag
    )
