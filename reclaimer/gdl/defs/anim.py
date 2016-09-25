from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descs import *
from ..field_types import *
from .objs.anim import AnimPs2Tag

# This definition doesnt actually work. They store stuff weirdly.
# def get(): return anim_ps2_def

anim_header = QStruct('header',
    LUInt16('skeletons count'),
    LUInt16('unknown count'),
    LPointer32('skeletons pointer'),
    LUInt32('texture_anims count'),
    LPointer32('texture_anims pointer'),
    SIZE=16
    )

node = Struct('node',
    StrRawLatin1('name', SIZE=32),
    LFloat('rel y'),
    LFloat('rel z'),
    LFloat('rel x'),
    LSInt16('unknown0'),
    LSInt16('unknown1'),
    LSInt32('unknown2'),
    LSInt32('unknown3'),
    LSInt32('parent node'),
    SIZE=60,
    )

# All the entries in the skeleton array exist in a sequence before any
# of the 'nodes' arrays. This means all of the skeletons need to be read
# and then have the offset of the end of the skeletons array used as the
# start of the 'nodes' arrays. This needs to be specially coded in......
skeleton = Container('skeleton',
    LPointer32('unknown0'),
    LPointer32('unknown1'),
    LPointer32('unknown2'),
    LPointer32('unknown3'),
    LSInt32('node count'),
    Pad(4),
    StrRawLatin1('name', SIZE=32),

    Array('nodes',
          SIZE='.node_count',
          SUB_STRUCT=node
          ),
    SIZE=56, POINTER='.pointer'
    )

skeleton_header = Container('skeleton header',
    StrRawLatin1('name', SIZE=32),
    LPointer32('pointer'),
    skeleton,
    SIZE=36,
    )

texture_anim = Struct('texture anim',
    LSInt16('unknown0'),#index of some sort?
    LSInt16('unknown1'),#index of some sort?
    StrRawLatin1('name', SIZE=32),
    StrRawLatin1('start frame', SIZE=32),#name is a guess
    LSInt32('unknown2'),
    LSInt32('unknown3'),
    LSInt16('unknown4'),
    LSInt16('unknown5'),
    LSInt32('unknown6'),
    LSInt32('unknown7'),
    LSInt16('unknown8'),
    LSInt16('unknown9'),
    SIZE=88
    )

skeletons_array = Array('skeleton_headers',
    SIZE='.header.skeletons_count',
    POINTER='.header.skeletons_pointer',
    SUB_STRUCT=skeleton_header,
    )

texture_anims_array = Array('texture_anims',
    SIZE='.header.texture_anims_count',
    POINTER='.header.texture_anims_pointer',
    SUB_STRUCT=texture_anim,
    )

unknown_footer = QStruct('footer',
    LSInt32('unknown0'),
    LSInt32('unknown1'),
    LSInt32('unknown2'),
    LSInt32('unknown3'),
    LSInt32('unknown4'),
    LSInt32('unknown5'),
    LSInt32('unknown6'),
    LSInt32('unknown7'),
    LSInt32('unknown8'),
    )

anim_ps2_def = TagDef("anim",
    anim_header,
    skeletons_array,
    texture_anims_array,
    #unknown_footer,

    ext=".ps2", tag_cls=AnimPs2Tag, incomplete=True
    )
