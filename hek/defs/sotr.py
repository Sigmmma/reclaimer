from .shdr import *
from .objs.tag import HekTag
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
    Bool16("flags" ,
        "color mux",
        "alpha mux",
        "A-out controls color0 animation",
        ),
    Pad(2),

    SEnum16("color0 source", *function_names),
    SEnum16("color0 anim function", *animation_functions),
    float_sec("color0 anim period"),
    QStruct("color0 anim lower bound", INCLUDE=argb_float),
    QStruct("color0 anim upper bound", INCLUDE=argb_float),
    QStruct("color1", INCLUDE=argb_float),

    Struct('color',
        Struct('input A', 
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input B', 
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input C', 
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input D', 
            SEnum16('input', GUI_NAME='', *sotr_color_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),

        Struct('output AB', 
            SEnum16('output', GUI_NAME='', *sotr_color_outputs),
            SEnum16('function', *sotr_color_output_functions),
            ORIENT='h'
            ),
        Struct('output CD', 
            SEnum16('output', GUI_NAME='', *sotr_color_outputs),
            SEnum16('function', *sotr_color_output_functions),
            ORIENT='h'
            ),
        SEnum16('output AB CD mux/sum', *sotr_color_outputs),
        SEnum16('output mapping', *sotr_output_mappings)
        ),

    Struct('alpha',
        Struct('input A', 
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input B', 
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input C', 
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),
        Struct('input D', 
            SEnum16('input', GUI_NAME='', *sotr_alpha_inputs),
            SEnum16('mapped_to', *sotr_input_mappings),
            ORIENT='h'
            ),

        SEnum16('output AB', *sotr_alpha_outputs),
        SEnum16('output CD', *sotr_alpha_outputs),
        SEnum16('output AB CD mux/sum', *sotr_alpha_outputs),
        SEnum16('output mapping', *sotr_output_mappings)
        ),

    SIZE=112
    )

map = Struct("map",
    Bool16("flags" ,
        "unfiltered",
        "u-clamped",
        "v-clamped",
        ),
    Pad(2),
    #shader transformations
    Float("map u-scale"),
    Float("map v-scale"),
    Float("map u-offset"),
    Float("map v-offset"),
    float_deg("map rotation"),  # degrees
    float_zero_to_one("map bias"),
    dependency("bitmap", "bitm"),
                              
    #shader animations
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),

    QStruct("rotation center", INCLUDE=xy_float),
    SIZE=100,
    )

sotr_attrs = Struct("sotr attrs",
    #Generic Transparent Shader
    Struct("generic transparent shader",
        UInt8("numeric counter limit", MIN=0, MAX=255, SIDETIP="[0,255]"),
        Bool8("flags", *trans_shdr_properties),
        SEnum16("first map type",             *trans_shdr_first_map_type),
        SEnum16("framebuffer blend function", *framebuffer_blend_functions),
        SEnum16("framebuffer fade mode",      *render_fade_mode),
        SEnum16("framebuffer fade source",    *function_outputs),
        Pad(2),
        ),

    #Lens Flare
    float_wu("lens flare spacing"),  # world units
    dependency("lens flare", "lens"),
    reflexive("extra layers", extra_layers_block, 4,
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

    ext=".shader_transparent_generic", endian=">", tag_cls=HekTag,
    )
