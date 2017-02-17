from supyr_struct.tag import *

class MapTag(Tag):
    index_magic = None

    def __init__(self, *args, **kwargs):
        self.calc_pointers = False

        # the TagDef that describes this object
        definition = kwargs.get("definition")
        if definition:
            self.index_magic = definition.index_magic

        Tag.__init__(self, *args, **kwargs)
