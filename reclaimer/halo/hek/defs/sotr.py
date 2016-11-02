from .shdr import *
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
    'expand normal',
    )


sotr_color_inputs = (
    'zero',
    'one',
    'one half',
    'negative one',
    'negative one half',

    'map color 0',
    'map color 1',
    'map color 2',
    'map color 3',
    {NAME: 'vertex_color_0', GUI_NAME: 'vertex color 0 / diffuse light'},
    {NAME: 'vertex_color_1', GUI_NAME: 'vertex color 1 / fade(perpendicular)'},
    'scratch color 0',
    'scratch color 1',
    'constant color 0',
    'constant color 1',

    'map alpha 0',
    'map alpha 1',
    'map alpha 2',
    'map alpha 3',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / diffuse light'},
    {NAME: 'vertex_alpha_1', GUI_NAME: 'vertex alpha 1 / fade(perpendicular)'},
    'scratch alpha 0',
    'scratch alpha 1',
    'constant alpha 0',
    'constant alpha 1',
    )
sotr_color_outputs = (
    'discard',
    {NAME:'scratch_color_0', GUI_NAME: 'scratch color 0 / final color'},
    'scratch color 1',
    'vertex color 0',
    'vertex color 1',
    'map color 0',
    'map color 1',
    'map color 2',
    'map color 3',
    )
sotr_color_output_functions = (
    'multiply',
    'dot product',
    )


sotr_alpha_inputs = (
    'zero',
    'one',
    'one half',
    'negative one',
    'negative one half',

    'map alpha 0',
    'map alpha 1',
    'map alpha 2',
    'map alpha 3',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / diffuse light'},
    {NAME: 'vertex_alpha_1', GUI_NAME: 'vertex alpha 1 / fade(perpendicular)'},
    'scratch alpha 0',
    'scratch alpha 1',
    'constant alpha 0',
    'constant alpha 1',

    'map blue 0',
    'map blue 1',
    'map blue 2',
    'map blue 3',
    {NAME: 'vertex_blue_0', GUI_NAME: 'vertex blue 0 / diffuse light'},
    {NAME: 'vertex_blue_1', GUI_NAME: 'vertex blue 1 / fade(perpendicular)'},
    'scratch blue 0',
    'scratch blue 1',
    'constant blue 0',
    'constant blue 1',
    )
sotr_alpha_outputs = (
    'discard',
    {NAME: 'scratch_alpha_0', GUI_NAME: 'scratch alpha 0 / final alpha'},
    'scratch alpha 1',
    {NAME: 'vertex_alpha_0', GUI_NAME: 'vertex alpha 0 / fog'},
    'vertex alpha 1',
    'map alpha 0',
    'map alpha 1',
    'map alpha 2',
    'map alpha 3',
    )


stage = Struct("stage",
    BBool16("flags" ,
        "color mux",
        "alpha mux",
        "A-out controls color0 animation",
        ),
    Pad(2),

    BSEnum16("color0 source", *function_names),
    BSEnum16("color0 anim function", *animation_functions),
    BFloat("color0 anim period"),
    QStruct("color0 anim lower bound", INCLUDE=argb_float),
    QStruct("color0 anim upper bound", INCLUDE=argb_float),
    QStruct("color1", INCLUDE=argb_float),

    Struct('color input',
        BSEnum16('A', *sotr_color_inputs),
        BSEnum16('A mapping', *sotr_input_mappings),
        BSEnum16('B', *sotr_color_inputs),
        BSEnum16('B mapping', *sotr_input_mappings),
        BSEnum16('C', *sotr_color_inputs),
        BSEnum16('C mapping', *sotr_input_mappings),
        BSEnum16('D', *sotr_color_inputs),
        BSEnum16('D mapping', *sotr_input_mappings)
        ),

    Struct('color output',
        BSEnum16('AB', *sotr_color_outputs),
        BSEnum16('AB function', *sotr_color_output_functions),
        BSEnum16('CD', *sotr_color_outputs),
        BSEnum16('CD function', *sotr_color_output_functions),
        BSEnum16('AB CD mux/sum', *sotr_color_outputs),
        BSEnum16('mapping', *sotr_output_mappings)
        ),

    Struct('alpha input',
        BSEnum16('A', *sotr_alpha_inputs),
        BSEnum16('A mapping', *sotr_input_mappings),
        BSEnum16('B', *sotr_alpha_inputs),
        BSEnum16('B mapping', *sotr_input_mappings),
        BSEnum16('C', *sotr_alpha_inputs),
        BSEnum16('C mapping', *sotr_input_mappings),
        BSEnum16('D', *sotr_alpha_inputs),
        BSEnum16('D mapping', *sotr_input_mappings)
        ),

    Struct('alpha output',
        BSEnum16('AB', *sotr_alpha_outputs),
        BSEnum16('CD', *sotr_alpha_outputs),
        BSEnum16('AB CD mux/sum', *sotr_alpha_outputs),
        BSEnum16('mapping', *sotr_output_mappings)
        ),

    SIZE=112
    )

map = Struct("map",
    BBool16("flags" ,
        "unfiltered",
        "u-clamped",
        "v-clamped",
        ),
    Pad(2),
    #shader transformations
    BFloat("map u-scale"),
    BFloat("map v-scale"),
    BFloat("map u-offset"),
    BFloat("map v-offset"),
    BFloat("map rotation"),#degrees
    BFloat("map bias", MIN=0.0, MAX=1.0),
    dependency("bitmap", valid_bitmaps),
                              
    #shader animations
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),

    QStruct("rotation center", INCLUDE=xy_float),
    SIZE=100,
    )

sotr_body = Struct("tagdata",
    shader_attrs,

    #Generic Transparent Shader
    UInt8("numeric counter limit", MIN=0, MAX=255),
    Bool8("flags",
        "alpha tested",
        "decal",
        "two-sided",
        "first map is in screenspace",
        "draw before water",
        "ignore effect",
        "scale first map with distance",
        "numeric",
        ),
    BSEnum16("first map type",             *trans_shdr_first_map_type),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode",      *render_fade_mode),
    BSEnum16("framebuffer fade source",    *function_outputs),

    Pad(2),

    #Lens Flare
    BFloat("lens flare spacing"),#world units
    dependency("lens flare"),
    reflexive("extra layers", extra_layers_block, 4),
    reflexive("maps", map, 4),
    reflexive("stages", stage, 7),

    SIZE=108,
    )

    
def get():
    return sotr_def

sotr_def = TagDef("sotr",
    blam_header("sotr"),
    sotr_body,

    ext=".shader_transparent_generic", endian=">",
    )
