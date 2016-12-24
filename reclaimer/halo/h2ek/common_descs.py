from copy import copy, deepcopy
from math import pi

from ..hek.programs.mozzarilla.field_widgets import *
from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from ..field_types import *
from .constants import *

def h2tag_class(*args, **kwargs):
    pass


def h2reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    pass


def h2rawdata_ref(name, f_type=Rawdata, max_size=None, widget=None):
    pass


def h2dependency(name='tag ref', valid_ids=None):
    pass

def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(h2tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc

h2tag_header = Struct("blam header",
    Pad(36),
    BUEnum32("tag_class", GUI_NAME="tag class", INCLUDE=valid_tags),
    LUInt32("base address", DEFAULT=0),  #random
    LUInt32("header size",  DEFAULT=64),
    Pad(8),
    LUInt16("version", DEFAULT=1),
    LUInt16("unknown", DEFAULT=255),
    LUEnum32("engine id",
        ("halo 2", 'BLM!'),
        DEFAULT='BML!'
        ),
    VISIBLE=False, SIZE=80
    )
