from ....fields import *
from supyr_struct.tag import *

class MetaTag(Tag):
    __slots__ = ('Tag_Conversion_Settings',
                 'handler', 'constructor', 'definition',
                 'root_offset', 'calc_pointers',
                 'tagsourcepath', 'tagpath', 'tagdata')
    
    def __init__(self, **kwargs):
        calc_pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.Tag_Conversion_Settings = []
        Tag.__init__(self, **kwargs)
