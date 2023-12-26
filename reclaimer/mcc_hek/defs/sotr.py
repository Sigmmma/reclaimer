#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .shdr import *
from .objs.shdr import ShdrTag
from supyr_struct.defs.tag_def import TagDef

sotr_input_mappings = (
    {NAME: 'clamp_x', GUI_NAME: 'clamp(x)'},
    {NAME: 'one_minus_clamp_x', GUI_NAME: '1 - clamp(x)'},
    {NAME: 'clamp_x_times_two_minus_one', GUI_NAME: '2*clamp(x) - 1'},
    {NAME: 'one_minus_clamp_x_times_two', GUI_NAME: '1 - 2*clamp(x)'},
    {NAME: 'clamp_x_minus_one_half', GUI_NAME: 'clamp(x) - 1/2'},
    {NAME: 'one_half_minus_clamp_x', GUI_NAME: '1/2 - clamp(x)'},
    {NAME: 'x', GUI_NAME: 'x'},
    {NAME: 'minus_x', GUI_NAME: '-x'},
    )
sotr_output_mappings = (
    'identity',
    {NAME: 'scale_by_one_half', GUI_NAME: 'scale by 1/2'},
    {NAME: 'scale_by_two', GUI_NAME: 'scale by 2'},
    {NAME: 'scale_by_four', GUI_NAME: 'scale by 4'},
    {NAME: 'bias_by_minus_one_half', GUI_NAME: 'bias by -1/2'},
    'expand_normal',
    )


sotr_color_inputs = (
    'zero',
    'one',
    'one_half',
    'negative_one',
    'negative_one_half',

    'map_color_0',
    'map_color_1',
    'map_color_2',
    'map_color_3',
    {NAME: 'vertex_color_0', GUI_NAME: 'vertex color 0 / diffuse light'},
    {NAME: 'vertex_color_1', GUI_NAME: 'vertex color 1 / fade(perpendicular)'},
    'scratch_color_0',
    'scratch_color_1',
    'constant_color_0',
    'constant_color_1',

    'map_alpha_0',
    'map_alpha_1',
    'map_alpha_2',
    'map_alpha_3',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / diffuse light'},
    {NAME: 'vertex_alpha_1', GUI_NAME: 'vertex alpha 1 / fade(perpendicular)'},
    'scratch_alpha_0',
    'scratch_alpha_1',
    'constant_alpha_0',
    'constant_alpha_1',
    )
sotr_color_outputs = (
    'discard',
    {NAME:'scratch_color_0', GUI_NAME: 'scratch color 0 / final color'},
    'scratch_color_1',
    'vertex_color_0',
    'vertex_color_1',
    'map_color_0',
    'map_color_1',
    'map_color_2',
    'map_color_3',
    )
sotr_color_output_functions = (
    'multiply',
    'dot_product',
    )


sotr_alpha_inputs = (
    'zero',
    'one',
    'one_half',
    'negative_one',
    'negative_one_half',

    'map_blue_0',
    'map_blue_1',
    'map_blue_2',
    'map_blue_3',
    {NAME: 'vertex_blue_0', GUI_NAME: 'vertex blue 0 / diffuse light'},
    {NAME: 'vertex_blue_1', GUI_NAME: 'vertex blue 1 / fade(perpendicular)'},
    'scratch_blue_0',
    'scratch_blue_1',
    'constant_blue_0',
    'constant_blue_1',

    'map_alpha_0',
    'map_alpha_1',
    'map_alpha_2',
    'map_alpha_3',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / diffuse light'},
    {NAME: 'vertex_alpha_1', GUI_NAME: 'vertex alpha 1 / fade(perpendicular)'},
    'scratch_alpha_0',
    'scratch_alpha_1',
    'constant_alpha_0',
    'constant_alpha_1',
    )
sotr_alpha_outputs = (
    'discard',
    {NAME: 'scratch_alpha_0', GUI_NAME: 'scratch alpha 0 / final alpha'},
    'scratch_alpha_1',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / fog'},
    'vertex_alpha_1',
    'map_alpha_0',
    'map_alpha_1',
    'map_alpha_2',
    'map_alpha_3',
    )


stage = Struct("stage",
    Bool16("flags" ,
        "color_mux",
        "alpha_mux",
        "a_out_controls_color0_animation",
        ),
    Pad(2),

    SEnum16("color0_source", *function_names,
        COMMENT="If set to 'none', color0 is calculated by blending the\n"
                "two bounds below based on the 'color0 anim function'."),
    SEnum16("color0_anim_function", *animation_functions),
    float_sec("color0_anim_period"),
    QStruct("color0_anim_lower_bound", INCLUDE=argb_float),
    QStruct("color0_anim_upper_bound", INCLUDE=argb_float),
    QStruct("color1", INCLUDE=argb_float),

    Struct('color',
        Struct('input_A',
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_B',
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_C',
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_D',
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),

        Struct('output_AB',
            SEnum16('output', GUI_NAME='', *sotr_color_outputs),
            SEnum16('function', *sotr_color_output_functions),
            ORIENT='h'
            ),
        Struct('output_CD',
            SEnum16('output', GUI_NAME='', *sotr_color_outputs),
            SEnum16('function', *sotr_color_output_functions),
            ORIENT='h'
            ),
        SEnum16('output_AB_CD_mux_sum', *sotr_color_outputs),
        SEnum16('output_mapping', *sotr_output_mappings)
        ),

    Struct('alpha',
        Struct('input_A',
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_B',
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_C',
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input_D',
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),

        SEnum16('output_AB', *sotr_alpha_outputs),
        SEnum16('output_CD', *sotr_alpha_outputs),
        SEnum16('output_AB_CD_mux_sum', *sotr_alpha_outputs),
        SEnum16('output_mapping', *sotr_output_mappings)
        ),

    SIZE=112
    )

map = Struct("map",
    Bool16("flags" ,
        "unfiltered",
        "u_clamped",
        "v_clamped",
        ),
    Pad(2),
    #shader_transformations
    Float("map_u_scale"),
    Float("map_v_scale"),
    Float("map_u_offset"),
    Float("map_v_offset"),
    float_deg("map_rotation"),  # degrees
    float_zero_to_one("map_bias"),
    dependency("bitmap", "bitm"),

    #shader animations
    Struct("u_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v_animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation_animation", INCLUDE=anim_src_func_per_pha_sca_rot),

    QStruct("rotation_center", INCLUDE=xy_float),
    SIZE=100,
    )

sotr_attrs = Struct("sotr_attrs",
    #Generic Transparent Shader
    Struct("generic_transparent_shader",
        UInt8("numeric_counter_limit", MIN=0, MAX=255, SIDETIP="[0,255]"),
        Bool8("flags", *trans_shdr_properties),
        SEnum16("first_map_type",             *trans_shdr_first_map_type),
        SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
        SEnum16("framebuffer_fade_mode",      *render_fade_mode),
        SEnum16("framebuffer_fade_source",    *function_outputs),
        Pad(2),
        ),

    #Lens Flare
    float_wu("lens_flare_spacing"),  # world units
    dependency("lens_flare", "lens"),
    reflexive("extra_layers", extra_layers_block, 4,
        DYN_NAME_PATH='.filepath'),
    reflexive("maps", map, 4, DYN_NAME_PATH='.bitmap.filepath'),
    reflexive("stages", stage, 7),
    SIZE=68
    )

sotr_body = Struct("tagdata",
    shdr_attrs,
    sotr_attrs,

    SIZE=108,
    )


def get():
    return sotr_def

sotr_def = TagDef("sotr",
    blam_header("sotr"),
    sotr_body,

    ext=".shader_transparent_generic", endian=">", tag_cls=ShdrTag,
    )
