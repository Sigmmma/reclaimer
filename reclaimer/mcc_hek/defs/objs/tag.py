#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from pathlib import Path

from supyr_struct.defs.constants import DEFAULT
from supyr_struct.tag import Tag

from reclaimer.util import calc_halo_crc32

class HekTag(Tag):
    def __init__(self, **kwargs):
        self.calc_pointers = False
        Tag.__init__(self, **kwargs)

    def serialize(self, **kwargs):
        '''
        Overload of the supyr serialization function that retroactively adds
        a CRC to the tag.
        '''
        head = self.data.blam_header
        filepath = kwargs.get('filepath', self.filepath)
        buffer = kwargs.get('buffer', None)

        # Run the normal serialization.
        result = Tag.serialize(self, **kwargs)

        # If there is neither a buffer or filepath just return the result.
        if (buffer is None) and (not filepath):
            return result

        # Prefer to use the buffer as that is how Tag.serialize does it.
        f = buffer
        if buffer is None:
            f = Path(filepath).open('rb+')

        # Calculate the crc from after the header to the end.
        crc = calc_halo_crc32(f, offset=head.get_desc('SIZE'))
        # Write the crc to the offset of the checksum value in the header.
        # The way we retrieve this offset from supyr is insane.
        attr_index = head.get_desc('NAME_MAP')['checksum']
        f.seek(head.get_desc('ATTR_OFFS')[attr_index])
        f.write(crc.to_bytes(4, byteorder='big', signed=False))
        # Flush the stream.
        f.flush()
        # Only close if it is a file. Because the only case where we own
        # this buffer is if there was no buffer kwarg.
        if not buffer:
            f.close()

        # Update the tag object so it won't have to be deserialized again.
        head.checksum = crc
        return result

    def calc_internal_data(self):
        # recalculate the header data
        head = self.data.blam_header

        head.tag_class.data = head.tag_class.get_desc(DEFAULT)
        head.flags.edited_with_mozz = True
        head.header_size = head.get_desc(DEFAULT, 'header_size')
        head.version = head.get_desc(DEFAULT, 'version')
        head.integrity0 = head.get_desc(DEFAULT, 'integrity0')
        head.integrity1 = head.get_desc(DEFAULT, 'integrity1')
        head.engine_id.data = head.engine_id.get_desc(DEFAULT)
