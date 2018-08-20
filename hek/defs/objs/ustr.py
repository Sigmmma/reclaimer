from .tag import *

class UstrTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        strings = self.data.tagdata.strings.STEPTREE

        for i in range(len(strings)):
            # replace all instances of \r and \n with \r\n
            split_strings = []
            for s in strings[i].data.split('\r'):
                split_strings.extend(s.split('\n'))

            new_string = split_strings.pop(0)
            for s in split_strings:
                new_string += s + "\r\n"

            strings[i].data = new_string
