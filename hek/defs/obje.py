from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get():
    return obje_def

attachment = Struct('attachment',
    dependency('type', valid_attachments),
    ascii_str32('marker'),
    SEnum16('primary scale', *function_outputs),
    SEnum16('secondary scale', *function_outputs),
    SEnum16('change color', *function_names),

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
        'always active',
        ),
    float_sec('period', UNIT_SCALE=sec_unit_scale),  # seconds
    SEnum16('scale period by', *function_inputs_outputs),
    SEnum16('function', *animation_functions),
    SEnum16('scale function by', *function_inputs_outputs),
    SEnum16('wobble function', *animation_functions),
    float_sec('wobble period', UNIT_SCALE=sec_unit_scale),  # seconds
    Float('wobble magnitude', SIDETIP="%"),  # percent

    Float('square wave threshold'),
    SInt16('step count'),
    SEnum16('map to', *fade_functions),
    SInt16('sawtooth count'),
    SEnum16('add', *function_inputs_outputs),
    SEnum16('scale result by', *function_inputs_outputs),
    SEnum16('bounds mode',
        'clip',
        'clip and normalize',
        'scale to fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn off with', DYN_NAME_PATH="..[DYN_I].usage"),
    Float('scale by'),

    Pad(268),
    ascii_str32('usage'),

    SIZE=360
    )

permutation = Struct('permutation',
    Float('weight'),
    QStruct('color lower bound', INCLUDE=rgb_float),
    QStruct('color upper bound', INCLUDE=rgb_float),

    SIZE=28
    )

change_color = Struct('change_color',
    SEnum16('darken by', *function_inputs_outputs),
    SEnum16('scale by', *function_inputs_outputs),
    Bool32('flags',
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
    Bool16('flags',
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
    SEnum16('A in', *object_export_to),
    SEnum16('B in', *object_export_to),
    SEnum16('C in', *object_export_to),
    SEnum16('D in', *object_export_to),

    Pad(44),
    SInt16('hud text message index'),
    SInt16('forced shader permutation index'),
    reflexive("attachments", attachment, 8, DYN_NAME_PATH='.type.filepath'),
    reflexive("widgets", widget, 4, DYN_NAME_PATH='.reference.filepath'),
    reflexive("functions", function, 4, DYN_NAME_PATH='.usage'),
    reflexive("change colors", change_color, 4,
        'A', 'B', 'C', 'D'),
    reflexive("predicted resources", predicted_resource, 1024, VISIBLE=False),

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
