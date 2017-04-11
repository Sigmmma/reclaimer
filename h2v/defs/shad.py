from ..common_descs import *
from .objs.tag import H2VTag
from supyr_struct.defs.tag_def import TagDef

# This is the reflexive that needs the MMAP struct headering the tbfd inside
rawdata_reflexive = h2_reflexive("data",
    (SInt8("byte", COMMENT=(
        "\n            DONT TOUCH THIS!\n\n" +
        "It is actually rawdata treated as a reflexive.\n")), 1),
    max_count=1024, EDITABLE=False
    )

runtime_property = Struct("runtime property",
    h2v_dependency("diffuse map", "bitm"),
    Struct("lightmap",
        h2v_dependency("emissive map", "bitm"),
        QStruct("emissive color", INCLUDE=rgb_float),
        Float("emissive power"),
        Float("resolution scale"),
        Float("half life"),
        Float("diffuse scale"),
        ),
    h2v_dependency("alpha test map", "bitm"),
    h2v_dependency("translucent map", "bitm"),
    Struct("more lightmap",
        QStruct("transparent color", INCLUDE=rgb_float),
        Float("transparent alpha"),
        Float("foliage scale")
        ),
    SIZE=112
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
    ascii_str_varlen("input name"),
    ascii_str_varlen("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=28
    )

global_parameters = Struct("global parameters",
    ascii_str_varlen("material name"),
    UEnum16("type",
        "bitmap",
        "value",
        "color",
        "switch",
        ),
    Pad(2),
    h2v_dependency("bitmap", "bitm"),
    Float("constant value"),
    QStruct("constant color", INCLUDE=rgb_float),
    h2_reflexive("animation properties",
        (animation_property, 28), max_count=1024
        ),
    SIZE=52
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
    ascii_str_varlen("input name"),
    ascii_str_varlen("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=24
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
    h2v_dependency("template", "spas"),
    block_index,
    SIZE=18
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
    ascii_str_varlen("input name"),
    ascii_str_varlen("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=27
    )

value_overlay = Struct("value overlay",
    UInt8("parameter index", EDITABLE=False),
    ascii_str_varlen("input name"),
    ascii_str_varlen("range name"),
    float_sec("time period"),
    rawdata_reflexive,
    SIZE=25
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
        h2_reflexive("layers", (block_index, 2),  max_count=25),
        h2_reflexive("passes", (shader_pass, 18), max_count=1024),
        h2_reflexive("implementations", (old_implementation, 44), max_count=1024),
        h2_reflexive("bitmaps", (bitmap_index, 1), max_count=1024),
        h2_reflexive("bitmap transforms", (bitmap_transform, 6), max_count=1024),
        h2_reflexive("values", (value, 5), max_count=1024),
        h2_reflexive("colors", (color, 13), max_count=1024),
        h2_reflexive("bitmap transform overlays",
            (bitmap_transform_overlay, 27), max_count=1024),
        h2_reflexive("value overlays",
            (value_overlay, 25), max_count=1024),
        h2_reflexive("color overlays",
            (color_overlay, 25), max_count=1024),
        h2_reflexive("vertex shader constants",
            (spp_vertex_shader_constant, 18), max_count=1024),
        ),
    h2_reflexive("render states", (render_state, 5), max_count=1024),
    h2_reflexive("texture stage states",
        (texture_stage_state, 6), max_count=1024),
    h2_reflexive("render state parameters",
        (render_state_parameter, 3), max_count=1024),
    h2_reflexive("texture stage state parameters",
        (texture_stage_state_parameter, 4), max_count=1024),
    h2_reflexive("textures", (texture, 4), max_count=1024),
    h2_reflexive("vn constants", (vertex_shader_constant, 4), max_count=1024),
    h2_reflexive("cn constants", (vertex_shader_constant, 4), max_count=1024),
    SIZE=224
    )

postprocess_definition = Struct("postprocess definitions",
    UInt32("shader template index", EDITABLE=False),
    h2_reflexive("bitmaps",          (global_parameters, 12),  max_count=1024),
    h2_reflexive("pixel constants",  (pixel_constants,  16),   max_count=1024),
    h2_reflexive("vertex constants", (vertex_constants, 16),   max_count=1024),
    h2_reflexive("levels of detail", (level_of_detail, 6),     max_count=1024),
    h2_reflexive("layers",           (block_index, 2),         max_count=1024),
    h2_reflexive("passes",           (block_index, 2),         max_count=1024),
    h2_reflexive("implementations",  (implementation, 10),     max_count=1024),
    h2_reflexive("overlays",         (overlay, 24),            max_count=1024),
    h2_reflexive("overlay references", (overlay_reference, 4), max_count=1024),
    h2_reflexive("animated parameters", (block_index, 2),      max_count=1024),
    h2_reflexive("animated parameter references",
        (animated_parameter_reference, 4), max_count=1024
        ),
    h2_reflexive("bitmap properties", (bitmap_property, 4), max_count=5),
    h2_reflexive("color properties",  (color_property, 12), max_count=2),
    h2_reflexive("value properties",  (Float("value"), 4),  max_count=6),
    h2_reflexive("old levels of detail",
        (old_level_of_detail, 224),  max_count=1024
        ),
    SIZE=184
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

BLM_old_body = Struct("tagdata",
    h2v_dependency("template", "stem"),
    ascii_str_varlen("material name"),
    h2_reflexive("runtime properties",
        (runtime_property, 112), max_count=1
        ),
    Pad(2),
    Bool16("flags",
        "water",
        "sort first",
        "no active camo",
        ),
    h2_reflexive("global parameters", (global_parameters, 52), max_count=64),
    h2_reflexive("postprocess definition",
        (postprocess_definition, 184), max_count=1
        ),
    Pad(4),
    h2_reflexive("predicted resources",
        (predicted_resource, 8), max_count=2048
        ),
    h2v_dependency("light response", "slit"),
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
    h2_reflexive("postprocess properties",
        (UInt32("bitmap group index"), 4), max_count=5
        ),
    SIZE=120
    )

# make the BLM_new_body by copying the old one and
# adding the new attributes to the end of the struct
BLM_new_body = dict(BLM_old_body)
BLM_new_body[17] = Float("added depth bias offset")
BLM_new_body[18] = Float("added depth bias slope scale")
BLM_new_body[SIZE] = 128
BLM_new_body[ENTRIES] += 2

# FINISH THE DEFINITION BEFORE ENABLING THIS
def get():
    return shad_def

shad_def = TagDef("shad",
    h2v_blam_header('shad'),
    h2_tagdata_switch(
        (BLM_new_body, 128),
        (BLM_old_body, 120)
        ),
    ext=".shader", endian="<", tag_cls=H2VTag
    )
