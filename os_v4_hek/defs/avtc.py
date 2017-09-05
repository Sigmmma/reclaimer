from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

transform_states_comment = """
The transform out tag determines the cause of the transformation(such as low health),
the animation to play on the attacked unit, and what attachments to add, if any.
The transformation in tag determines the possible actors to transform into.
"""

transform = Struct("transform",
    Bool16("flags",
        'scripted only',
        ),
    Pad(2),
    ascii_str32("transform name"),
    QStruct("selection chances",
        Float("easy"), Float("normal"), Float("hard"), Float("imposs"),
        ORIENT="h"
        ),
    Struct("transform stages",
        dependency_os("transform out", 'avto'),
        Pad(4),
        dependency_os("transform in", 'avti'),
        COMMENT=transform_states_comment
        ),
    SIZE=116
    )

actor_variant_transform = Struct("actor variant transform",
    dependency_os("actor variant", 'actv'),
    reflexive("transforms",
        transform, 32, DYN_NAME_PATH='.transform_name'),
    SIZE=52
    )

avtc_body = Struct("tagdata",
    reflexive("actor variant transforms",
        actor_variant_transform, 32, DYN_NAME_PATH='.actor_variant.filepath'),
    SIZE=36
    )

def get():
    return avtc_def

avtc_def = TagDef("avtc",
    blam_header_os('avtc', 1),
    avtc_body,

    ext=".actor_variant_transform_collection", endian=">", tag_cls=HekTag
    )
