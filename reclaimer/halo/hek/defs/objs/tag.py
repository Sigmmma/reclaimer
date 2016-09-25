from ....field_types import *
from supyr_struct.tag import *

class HekTag(Tag):
    def __init__(self, **kwargs):
        self.calc_pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.tag_conversion_settings = []
        Tag.__init__(self, **kwargs)
