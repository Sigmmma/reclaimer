#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.bitm import *
from supyr_struct.util import desc_variant

format_comment_parts = format_comment.split("NOTE: ", 1)
format_comment = "".join((
    format_comment_parts[0],
    """\
HIGH QUALITY COMPRESSION: ????

NOTE:""",
    format_comment_parts[1],
    ))

bitmap_format = SEnum16("format",
    "a8",
    "y8",
    "ay8",
    "a8y8",
    ("r5g6b5", 6),
    ("a1r5g5b5", 8),
    ("a4r4g4b4", 9),
    ("x8r8g8b8", 10),
    ("a8r8g8b8", 11),
    ("dxt1", 14),
    ("dxt3", 15),
    ("dxt5", 16),
    ("p8_bump", 17),
    ("bc7", 18),
    )
bitmap = desc_variant(bitmap,
    ("format", bitmap_format),
    )
body_format = SEnum16("format",
    "color_key_transparency",
    "explicit_alpha",
    "interpolated_alpha",
    "color_16bit",
    "color_32bit",
    "monochrome",
    "high_quality_compression",
    COMMENT=format_comment
    )
body_flags = Bool16("flags",
    "enable_diffusion_dithering",
    "disable_height_map_compression",
    "uniform_sprite_sequences",
    "sprite_bug_fix",
    "hud_scale_0.5",
    "invert_detail_fade",
    "use_average_color_for_detail_fade"
    )
sprite_processing = Struct("sprite_processing",
    SEnum16("sprite_budget_size",
      {NAME: "x32",   VALUE: 0, GUI_NAME: "32x32"},
      {NAME: "x64",   VALUE: 1, GUI_NAME: "64x64"},
      {NAME: "x128",  VALUE: 2, GUI_NAME: "128x128"},
      {NAME: "x256",  VALUE: 3, GUI_NAME: "256x256"},
      {NAME: "x512",  VALUE: 4, GUI_NAME: "512x512"},
      {NAME: "x1024", VALUE: 5, GUI_NAME: "1024x1024"},
      ),
    UInt16("sprite_budget_count"),
    COMMENT=sprite_processing_comment
    )
bitm_body = desc_variant(bitm_body,
    ("format", body_format),
    ("flags", body_flags),
    ("sprite_processing", sprite_processing),
    ("compressed_color_plate_data", rawdata_ref("compressed_color_plate_data", max_size=1073741824)),
    ("processed_pixel_data", rawdata_ref("processed_pixel_data", max_size=1073741824)),
    ("bitmaps", reflexive("bitmaps", bitmap, 65536, IGNORE_SAFE_MODE=True)),
    )

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=BitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
