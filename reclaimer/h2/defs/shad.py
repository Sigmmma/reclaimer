#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.h2.common_descs import *
from reclaimer.h2.defs.objs.tag import H2Tag
from supyr_struct.defs.tag_def import TagDef

# This is the reflexive that needs the MMAP struct headering the tbfd inside
rawdata_reflexive = h2_reflexive("data",
    SInt8("byte", COMMENT=(
        "\n            DONT TOUCH THIS!\n\n" +
        "It is actually rawdata treated as a reflexive.\n")),
    1024, EDITABLE=False
    )

runtime_property = Struct("runtime property",
    h2_dependency("diffuse map", "bitm"),
    Struct("lightmap",
        h2_dependency("emissive map", "bitm"),
        QStruct("emissive color", INCLUDE=rgb_float),
        Float("emissive power"),
        Float("resolution scale"),
        Float("half life"),
        Float("diffuse scale"),
        ),
    h2_dependency("alpha test map", "bitm"),
    h2_dependency("translucent map", "bitm"),
    Struct("more lightmap",
        QStruct("transparent color", INCLUDE=rgb_float),
        Float("transparent alpha"),
        Float("foliage scale")
        ),
    SIZE=80
    )

animation_property = Struct("animation property",
    UEnum16("type",
        "bitmap scale uniform",
        "bitmap scale x",
        "bitmap scale y",
        "bitmap scale z",
        "bitmap translation x",
        "bitmap translation y",
        "bitmap translation z",
        "bitmap rotation angle",
        "bitmap rotation axis x",
        "bitmap rotation axis y",
        "bitmap rotation axis z",
        "value",
        "color",
        "bitmap index",
        ),
    Pad(2),
    h2_string_id("input name"),
    h2_string_id("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=24
    )

global_parameters = Struct("global parameters",
    h2_string_id("material name"),
    UEnum16("type",
        "bitmap",
        "value",
        "color",
        "switch",
        ),
    Pad(2),
    h2_dependency("bitmap", "bitm"),
    Float("constant value"),
    QStruct("constant color", INCLUDE=rgb_float),
    h2_reflexive("animation properties", animation_property, 1024),
    SIZE=40
    )

postprocess_bitmap = QStruct("postprocess bitmap",
    UInt32("bitmap reference"),
    UInt32("bitmap index"),
    Float("log bitmap dimension"),
    SIZE=12, EDITABLE=False
    )

pixel_constants = QStruct("pixel constants", INCLUDE=argb_float, SIZE=16)

vertex_constants = QStruct("vertex constants",
    INCLUDE=ijkw_float, SIZE=16, EDITABLE=False)

level_of_detail = Struct("level of detail",
    Bool32("available layers", *["layer %s" % i for i in range(32)]),
    UInt16("block index data"),
    SIZE=6, EDITABLE=False
    )

block_index = UInt16("block index", EDITABLE=False)

implementation = QStruct("implementation",
    UInt16("block index data1"),
    UInt16("block index data2"),
    UInt16("block index data3"),
    UInt16("block index data4"),
    UInt16("block index data5"),
    SIZE=10, EDITABLE=False
    )

overlay = Struct("overlay",
    h2_string_id("input name"),
    h2_string_id("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=20
    )

overlay_reference = QStruct("overlay reference",
    UInt16("overlay index"),
    UInt16("transform index"),
    SIZE=4, EDITABLE=False
    )

animated_parameter_reference = QStruct("animated parameter reference",
    Pad(3),
    UInt8("parameter index"),
    SIZE=4, EDITABLE=False
    )

bitmap_property = QStruct("bitmap property",
    UInt16("bitmap index"),
    UInt16("animated parameter index"),
    SIZE=4, EDITABLE=False
    )

color_property = QStruct("color property",
    INCLUDE=rgb_float, EDITABLE=False)

shader_pass = Struct("pass",
    h2_dependency("template", "spas"),
    block_index,
    SIZE=10
    )

old_implementation = QStruct("implementation",
    *[UInt16("block index data%s" % (i+1)) for i in range(22)],
    SIZE=44, EDITABLE=False
    )

bitmap_index = UInt8("bitmap index", EDITABLE=False)


# ALL OF THE BLOCKS BELOW HERE DONT SEEM RIGHT.
# You don't just put a data in a spot that is off alignment.
bitmap_transform = Struct("bitmap transform",
    UInt8("parameter index"),
    UInt8("bitmap transform index"),
    Float("value"),
    SIZE=6, EDITABLE=False
    )

value = QStruct("value",
    UInt8("parameter index"),
    Float("value"),
    SIZE=5, EDITABLE=False
    )

color = Struct("color",
    UInt8("parameter index", EDITABLE=False),
    QStruct("color", INCLUDE=rgb_float),
    SIZE=13
    )

bitmap_transform_overlay = Struct("bitmap transform overlay",
    UInt8("parameter index", EDITABLE=False),
    UInt8("transform index", EDITABLE=False),
    UInt8("animation property type", EDITABLE=False),
    h2_string_id("input name"),
    h2_string_id("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=23
    )

value_overlay = Struct("value overlay",
    UInt8("parameter index", EDITABLE=False),
    h2_string_id("input name"),
    h2_string_id("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=21
    )

color_overlay = Struct("color overlay", INCLUDE=value_overlay)

spp_vertex_shader_constant = QStruct("vertex shader constant",
    UInt8("register index"),
    UInt8("register bank"),
    Float("data1"),
    Float("data2"),
    Float("data3"),
    Float("data4"),
    SIZE=18, EDITABLE=False
    )

render_state = QStruct("texture stage state",
    UInt8("state index"),
    UInt32("state value"),
    SIZE=5, EDITABLE=False
    )

texture_stage_state = QStruct("texture stage state",
    UInt8("state index"),
    UInt8("stage index"),
    UInt32("state value"),
    SIZE=6, EDITABLE=False
    )

# ALL OF THE BLOCKS ABOVE HERE DONT SEEM RIGHT.
# You don't just put a data in a spot that is off alignment.

render_state_parameter = QStruct("render state parameter",
    UInt8("parameter index"),
    UInt8("parameter type"),
    UInt8("state index"),
    SIZE=3, EDITABLE=False
    )

texture_stage_state_parameter = QStruct("texture stage state parameter",
    UInt8("parameter index"),
    UInt8("parameter type"),
    UInt8("state index"),
    UInt8("stage index"),
    SIZE=4, EDITABLE=False
    )

texture = QStruct("texture",
    UInt8("stage index"),
    UInt8("parameter index"),
    UInt8("global texture index"),
    UInt8("flags"),
    SIZE=4, EDITABLE=False
    )

vertex_shader_constant = QStruct("vertex shader constant",
    UInt8("register index"),
    UInt8("parameter index"),
    UInt8("destination mask"),
    UInt8("scale by texture stage"),
    SIZE=4, EDITABLE=False
    )

old_level_of_detail = Struct("old level of detail",
    Float("projected height percentage"),
    Bool32("available layers",
        *["layer%s" % i for i in range(25)], EDITABLE=False),
    Struct("postprocess",
        h2_reflexive("layers", block_index, 25),
        h2_reflexive("passes", shader_pass, 1024),
        h2_reflexive("implementations", old_implementation, 1024),
        h2_reflexive("bitmaps", bitmap_index, 1024),
        h2_reflexive("bitmap transforms", bitmap_transform, 1024),
        h2_reflexive("values", value, 1024),
        h2_reflexive("colors", color, 1024),
        h2_reflexive("bitmap transform overlays",
            bitmap_transform_overlay, 1024),
        h2_reflexive("value overlays", value_overlay, 1024),
        h2_reflexive("color overlays", color_overlay, 1024),
        h2_reflexive("vertex shader constants",
            spp_vertex_shader_constant, 1024),
        ),
    h2_reflexive("render states", render_state, 1024),
    h2_reflexive("texture stage states", texture_stage_state, 1024),
    h2_reflexive("render state parameters", render_state_parameter, 1024),
    h2_reflexive("texture stage state parameters",
        texture_stage_state_parameter, 1024),
    h2_reflexive("textures", texture, 1024),
    h2_reflexive("vn constants", vertex_shader_constant, 1024),
    h2_reflexive("cn constants", vertex_shader_constant, 1024),
    SIZE=152
    )

postprocess_definition = Struct("postprocess definitions",
    UInt32("shader template index", EDITABLE=False),
    h2_reflexive("bitmaps",          global_parameters,   1024),
    h2_reflexive("pixel constants",  pixel_constants,     1024),
    h2_reflexive("vertex constants", vertex_constants,    1024),
    h2_reflexive("levels of detail", level_of_detail,     1024),
    h2_reflexive("layers",           block_index,         1024),
    h2_reflexive("passes",           block_index,         1024),
    h2_reflexive("implementations",  implementation,      1024),
    h2_reflexive("overlays",         overlay,             1024),
    h2_reflexive("overlay references", overlay_reference, 1024),
    h2_reflexive("animated parameters", block_index,      1024),
    h2_reflexive("animated parameter references",
        animated_parameter_reference, 1024
        ),
    h2_reflexive("bitmap properties", bitmap_property, 5),
    h2_reflexive("color properties",  color_property,  2),
    h2_reflexive("value properties",  Float("value"),  6),
    h2_reflexive("old levels of detail", old_level_of_detail,  1024),
    SIZE=124
    )

predicted_resource = Struct("predicted resource",
    UEnum16("type",
        "bitmap",
        "sound",
        "render model geometry",
        "cluster geometry",
        "cluster instanced geometry",
        "lightmap geometry object buckets",
        "lightmap geometry instance buckets",
        "lightmap cluster bitmaps",
        "lightmap instance bitmaps"
        ),
    UInt16("resource index"),
    UInt32("predicted resource tag"),
    SIZE=8, EDITABLE=False
    )

shad_body = Struct("tagdata",
    h2_dependency("template", "stem"),
    h2_string_id("material name"),
    h2_reflexive("runtime properties", runtime_property, 1),
    Pad(2),
    Bool16("flags",
        "water",
        "sort first",
        "no active camo",
        ),
    h2_reflexive("global parameters", global_parameters, 64),
    h2_reflexive("postprocess definition", postprocess_definition, 1),
    Pad(4),
    h2_reflexive("predicted resources", predicted_resource, 2048),
    h2_dependency("light response", "slit"),
    UEnum16("shader lod bias",
        "none",
        {NAME: "times_4", GUI_NAME: "4x size"},
        {NAME: "times_2", GUI_NAME: "2x size"},
        {NAME: "times_half", GUI_NAME: "1/2x size"},
        {NAME: "times_quarter", GUI_NAME: "1/4x size"},
        "never",
        "cinematic"
        ),
    UEnum16("specular type",
        "none",
        "default",
        "dull",
        "shiny",
        ),
    UEnum16("lightmap type",
        "diffuse",
        "default specular",
        "dull specular",
        "shiny specular",
        ),
    Pad(2),
    Float("lightmap specular brightness"),
    float_neg_one_to_one("lightmap ambient bias"),
    h2_reflexive("postprocess properties", UInt32("bitmap group index"), 5),
    Float("added depth bias offset"),
    Float("added depth bias slope scale"),
    ENDIAN="<", SIZE=84
    )


def get():
    return shad_def

shad_def = TagDef("shad",
    h2_blam_header('shad'),
    shad_body,

    ext=".%s" % h2_tag_class_fcc_to_ext["shad"], endian="<"
    )
