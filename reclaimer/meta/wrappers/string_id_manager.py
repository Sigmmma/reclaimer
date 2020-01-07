#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

class StringIdManager:
    strings = ()
    set_offsets = ()

    def __init__(self, strings, sets):
        self.strings = strings
        self.set_offsets = tuple((s[0], s[1]) for s in sets)

    def get_string(self, string_id_block):
        string_id = string_id_block.string_id
        idx_bit_ct = string_id_block.STRINGID_IDX_BITS
        set_bit_ct = string_id_block.STRINGID_SET_BITS

        set_id = (string_id >> idx_bit_ct) & ((1 << set_bit_ct) - 1)
        index = string_id & ((1 << idx_bit_ct) - 1)
        if set_id in range(len(self.set_offsets)):
            set_offset = self.set_offsets[set_id]
            if index < set_offset[0]:
                set_id -= 1
                set_offset = self.set_offsets[set_id]

            if set_id >= 0:
                index += set_offset[1] - set_offset[0]

        if index not in range(len(self.strings)):
            return ""

        return self.strings[index].string
