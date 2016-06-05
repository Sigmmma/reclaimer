from ....fields import *
from supyr_struct.tag import *

class HekTag(Tag):
    __slots__ = ('tag_conversion_settings',
                 'library', 'definition',
                 'root_offset', 'calc_pointers',
                 'sourcepath', 'filepath', 'data')
    
    def __init__(self, **kwargs):
        calc_pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.tag_conversion_settings = []
        Tag.__init__(self, **kwargs)
