from ...field_types import *
from supyr_struct.tag import *

class H2XTag(Tag):
    def __init__(self, **kwargs):
        self.calc_pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.tag_conversion_settings = []
        Tag.__init__(self, **kwargs)

    def calc_internal_data(self):
        # recalculate the header data
        head = self.data.blam_header

        head.tag_class.data = head.tag_class.get_desc(DEFAULT)
        head.checksum = head.get_desc(DEFAULT, 'checksum')
        head.header_size = head.get_desc(DEFAULT, 'header_size')
        head.version = head.get_desc(DEFAULT, 'version')
        head.integrity0 = head.get_desc(DEFAULT, 'integrity0')
        head.integrity1 = head.get_desc(DEFAULT, 'integrity1')
        head.engine_id.data = head.engine_id.get_desc(DEFAULT)
