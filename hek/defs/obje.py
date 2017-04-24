from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get():
    return obje_def

attachment = Struct('attachment',
    dependency('type', valid_attachments),
    ascii_str32('marker'),
    BSEnum16('primary scale', *function_outputs),
    BSEnum16('secondary scale', *function_outputs),
    BSEnum16('change color', *function_names),

    SIZE=72
    )

widget = Struct('widget',
    dependency('reference', valid_widgets),
    SIZE=32
    )

function = Struct('function',
    BBool32('flags',
        'invert',
        'additive',
        'always active',
        ),
    float_sec('period', UNIT_SCALE=sec_unit_scale),  # seconds
    BSEnum16('scale period by', *function_inputs_outputs),
    BSEnum16('function', *animation_functions),
    BSEnum16('scale function by', *function_inputs_outputs),
    BSEnum16('wobble function', *animation_functions),
    float_sec('wobble period', UNIT_SCALE=sec_unit_scale),  # seconds
    BFloat('wobble magnitude', SIDETIP="%"),  # percent

    BFloat('square wave threshold'),
    BSInt16('step count'),
    BSEnum16('map to', *fade_functions),
    BSInt16('sawtooth count'),
    BSEnum16('add', *function_inputs_outputs),
    BSEnum16('scale result by', *function_inputs_outputs),
    BSEnum16('bounds mode',
        'clip',
        'clip and normalize',
        'scale to fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn off with', DYN_NAME_PATH="..[DYN_I].usage"),
    BFloat('scale by'),

    Pad(268),
    ascii_str32('usage'),

    SIZE=360
    )

permutation = Struct('permutation',
    BFloat('weight'),
    QStruct('color lower bound', INCLUDE=rgb_float),
    QStruct('color upper bound', INCLUDE=rgb_float),

    SIZE=28
    )

change_color = Struct('change_color',
    BSEnum16('darken by', *function_inputs_outputs),
    BSEnum16('scale by', *function_inputs_outputs),
    BBool32('flags',
        'blend in hsv',
        'more colors',
        ),
    QStruct('color lower bound', INCLUDE=rgb_float),
    QStruct('color upper bound', INCLUDE=rgb_float),
    reflexive("permutations", permutation, 8),

    SIZE=44
    )

obje_attrs = Struct('obje attrs',
    FlSEnum16("object type",
        "bipd",
        "vehi",
        "weap",
        "eqip",
        "garb",
        "proj",
        "scen",
        "mach",
        "ctrl",
        "lifi",
        "plac",
        "ssce",
        ("obje", -1),
        VISIBLE=False, DEFAULT=-1
        ),
    BBool16('flags',
        'does not cast shadow',
        'transparent self-occlusion',
        'brighter than it should be',
        'not a pathfinding obstacle',
        ('xbox_unknown_bit_8', 1<<8),
        ('xbox_unknown_bit_11', 1<<11),
        ),
    float_wu('bounding radius'),
    QStruct('bounding offset', INCLUDE=xyz_float),
    QStruct('origin offset', INCLUDE=xyz_float),
    float_zero_to_inf('acceleration scale', UNIT_SCALE=per_sec_unit_scale),

    Pad(4),
    dependency('model', valid_models),
    dependency('animation graph', "antr"),

    Pad(40),
    dependency('collision model', "coll"),
    dependency('physics', "phys"),
    dependency('modifier shader', valid_shaders),
    dependency('creation effect', "effe"),
    Pad(84),
    float_wu('render bounding radius'),

    #Export to functions
    BSEnum16('A in', *object_export_to),
    BSEnum16('B in', *object_export_to),
    BSEnum16('C in', *object_export_to),
    BSEnum16('D in', *object_export_to),

    Pad(44),
    BSInt16('hud text message index'),
    BSInt16('forced shader permutation index'),
    reflexive("attachments", attachment, 8, DYN_NAME_PATH='.type.filepath'),
    reflexive("widgets", widget, 4, DYN_NAME_PATH='.reference.filepath'),
    reflexive("functions", function, 4, DYN_NAME_PATH='.usage'),
    reflexive("change colors", change_color, 4,
        'A', 'B', 'C', 'D'),
    reflexive("predicted resources", predicted_resource, 1024),

    SIZE=380
    )

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=HekTag
    )
