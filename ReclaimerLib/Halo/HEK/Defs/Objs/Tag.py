from ...Field_Types import *
from supyr_struct.Tag import *

class HEK_Tag(Tag):
    __slots__ = ('Tag_Conversion_Settings',
                 'Library', 'Constructor', 'Definition',
                 'Root_Offset', 'Calc_Pointers',
                 'Tag_Source_Path', 'Tag_Path', 'Tag_Data')
    
    def __init__(self, **kwargs):
        Calc_Pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.Tag_Conversion_Settings = []
        Tag.__init__(self, **kwargs)
