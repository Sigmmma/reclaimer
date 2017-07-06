from ...field_types import *
from supyr_struct.tag import *

class H2Tag(Tag):
    def __init__(self, **kwargs):
        self.calc_pointers = False
        
        # this is used by various things to store variables
        # per tag which specify how it is to be changed.
        self.tag_conversion_settings = []
        Tag.__init__(self, **kwargs)

    def calc_internal_data(self):
        # recalculate the header data
        head = self.data.blam_header

        head.tag_class.data = head.tag_class.get_desc(DEFAULT)
        head.checksum = head.get_desc(DEFAULT, 'checksum')
        head.header_size = head.get_desc(DEFAULT, 'header_size')
        head.integrity0 = head.get_desc(DEFAULT, 'integrity0')
        head.integrity1 = head.get_desc(DEFAULT, 'integrity1')

        # enable these only if the code for upgrading tags to BLM! works
        # head.version = head.get_desc(DEFAULT, 'version')
        # head.engine_id.data = head.engine_id.get_desc(DEFAULT)

    def parse(self, **kwargs):
        # might want to insert some kind of check to verify the engine_id isnt
        # set to 'lbma', because if it is then all tbfd structs must be edited
        Tag.parse(self, **kwargs)
