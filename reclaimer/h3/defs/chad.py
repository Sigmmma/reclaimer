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
# revision: 2		author: DarkShallFall-
# 	Labeled some reflexives and acouple values(Sep 26 2008)
# revision: 3		author: OrangeMohawk
# 	Position, Rotation, Scaling, Flashing/Fading, Bitmap Skewing.
# revision: 4		author: Lord Zedd
# 	Updated some things
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


chad_position_animation = Struct("animation",
    SInt32("frame_number"),
    QStruct("position", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=16
    )


chad_position = Struct("position",
    h3_reflexive("animation", chad_position_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_rotation_animation = Struct("animation",
    SInt32("frame_number"),
    ypr_float_rad("angle"),
    ENDIAN=">", SIZE=16
    )


chad_rotation = Struct("rotation",
    h3_reflexive("animation", chad_rotation_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_size_animation = Struct("animation",
    SInt32("frame_number"),
    QStruct("stretch", INCLUDE=xy_float),
    ENDIAN=">", SIZE=12
    )


chad_size = Struct("size",
    h3_reflexive("animation", chad_size_animation),
    h3_rawdata_ref("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


chad_color_animation = Struct("animation",
    SInt32("frame_number"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


chad_color = Struct("color",
    h3_reflexive("animation", chad_color_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_alpha_animation = Struct("animation",
    SInt32("frame_number"),
    Float("alpha"),
    ENDIAN=">", SIZE=8
    )


chad_alpha = Struct("alpha",
    h3_reflexive("animation", chad_alpha_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_alpha_unknown_animation = Struct("animation",
    SInt32("frame_number"),
    Float("alpha"),
    ENDIAN=">", SIZE=8
    )


chad_alpha_unknown = Struct("alpha_unknown",
    h3_reflexive("animation", chad_alpha_unknown_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_bitmap_animation = Struct("animation",
    SInt32("frame_number"),
    QStruct("movement_1", INCLUDE=xy_float),
    QStruct("movement_2", INCLUDE=xy_float),
    ENDIAN=">", SIZE=20
    )


chad_bitmap = Struct("bitmap",
    h3_reflexive("animation", chad_bitmap_animation),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_body = Struct("tagdata",
    Bool16("flags",
        ("loops", 1 << 1),
        ),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("position", chad_position),
    h3_reflexive("rotation", chad_rotation),
    h3_reflexive("size", chad_size),
    h3_reflexive("color", chad_color),
    h3_reflexive("alpha", chad_alpha),
    h3_reflexive("alpha_unknown", chad_alpha_unknown),
    h3_reflexive("bitmap", chad_bitmap),
    SInt32("number_of_frames", VISIBLE=False),
    ENDIAN=">", SIZE=92
    )


def get():
    return chad_def

chad_def = TagDef("chad",
    h3_blam_header('chad'),
    chad_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["chad"], endian=">", tag_cls=H3Tag
    )
