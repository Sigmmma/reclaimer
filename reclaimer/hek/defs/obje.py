#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.obje import ObjeTag
from supyr_struct.defs.tag_def import TagDef

def get():
    return obje_def

attachment = Struct('attachment',
    dependency('type', valid_attachments),
    ascii_str32('marker'),
    SEnum16('primary_scale', *function_outputs),
    SEnum16('secondary_scale', *function_outputs),
    SEnum16('change_color', *function_names),

    SIZE=72
    )

widget = Struct('widget',
    dependency('reference', valid_widgets),
    SIZE=32
    )

function = Struct('function',
    Bool32('flags',
        'invert',
        'additive',
        'always_active',
        ),
    float_sec('period', UNIT_SCALE=sec_unit_scale),  # seconds
    SEnum16('scale_period_by', *function_inputs_outputs),
    SEnum16('function', *animation_functions),
    SEnum16('scale_function_by', *function_inputs_outputs),
    SEnum16('wobble_function', *animation_functions),
    float_sec('wobble_period', UNIT_SCALE=sec_unit_scale),  # seconds
    Float('wobble_magnitude', SIDETIP="%"),  # percent

    Float('square_wave_threshold'),
    SInt16('step_count'),
    SEnum16('map_to', *fade_functions),
    SInt16('sawtooth_count'),
    SEnum16('add', *function_inputs_outputs),
    SEnum16('scale_result_by', *function_inputs_outputs),
    SEnum16('bounds_mode',
        'clip',
        'clip_and_normalize',
        'scale_to_fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn_off_with', DYN_NAME_PATH="..[DYN_I].usage"),
    Float('scale_by'),

    Pad(268),
    ascii_str32('usage'),

    SIZE=360
    )

permutation = Struct('permutation',
    Float('weight'),
    QStruct('color_lower_bound', INCLUDE=rgb_float),
    QStruct('color_upper_bound', INCLUDE=rgb_float),

    SIZE=28
    )

change_color = Struct('change_color',
    SEnum16('darken_by', *function_inputs_outputs),
    SEnum16('scale_by', *function_inputs_outputs),
    Bool32('flags',
        'blend_in_hsv',
        'more_colors',
        ),
    QStruct('color_lower_bound', INCLUDE=rgb_float),
    QStruct('color_upper_bound', INCLUDE=rgb_float),
    reflexive("permutations", permutation, 8),

    SIZE=44
    )

obje_attrs = Struct('obje_attrs',
    FlSEnum16("object_type",
        *((object_types[i], i - 1) for i in
          range(len(object_types))),
        VISIBLE=False, DEFAULT=-1
        ),
    Bool16('flags',
        'does_not_cast_shadow',
        'transparent_self_occlusion',
        'brighter_than_it_should_be',
        'not_a_pathfinding_obstacle',
        {NAME: 'xbox_unknown_bit_8', VALUE: 1<<8, VISIBLE: False},
        {NAME: 'xbox_unknown_bit_11', VALUE: 1<<11, VISIBLE: False},
        ),
    float_wu('bounding_radius'),
    QStruct('bounding_offset', INCLUDE=xyz_float),
    QStruct('origin_offset', INCLUDE=xyz_float),
    float_zero_to_inf('acceleration_scale', UNIT_SCALE=per_sec_unit_scale),

    Pad(4),
    dependency('model', valid_models),
    dependency('animation_graph', "antr"),

    Pad(40),
    dependency('collision_model', "coll"),
    dependency('physics', "phys"),
    dependency('modifier_shader', valid_shaders),
    dependency('creation_effect', "effe"),
    Pad(84),
    float_wu('render_bounding_radius'),

    #Export to functions
    SEnum16('A_in', *object_export_to),
    SEnum16('B_in', *object_export_to),
    SEnum16('C_in', *object_export_to),
    SEnum16('D_in', *object_export_to),

    Pad(44),
    SInt16('hud_text_message_index'),
    SInt16('forced_shader_permutation_index'),
    reflexive("attachments", attachment, 8, DYN_NAME_PATH='.type.filepath'),
    reflexive("widgets", widget, 4, DYN_NAME_PATH='.reference.filepath'),
    reflexive("functions", function, 4, DYN_NAME_PATH='.usage'),
    reflexive("change_colors", change_color, 4,
        'A', 'B', 'C', 'D'),
    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),

    SIZE=380
    )

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
