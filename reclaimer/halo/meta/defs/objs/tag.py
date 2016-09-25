from ....field_types import *
from supyr_struct.tag import *

class MetaTag(Tag):    
    def __init__(self, **kwargs):
        calc_pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.Tag_Conversion_Settings = []
        Tag.__init__(self, **kwargs)
