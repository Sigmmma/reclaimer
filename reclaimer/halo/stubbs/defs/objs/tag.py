from ....field_types import *
from supyr_struct.tag import *

class StubbsTag(Tag):
    def __init__(self, **kwargs):
        self.calc_pointers = False
        Tag.__init__(self, **kwargs)
