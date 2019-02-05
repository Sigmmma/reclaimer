from .tag import *

class Str_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        strings = self.data.tagdata.strings.STEPTREE

        for i in range(len(strings)):
            # replace all instances of \r and \n with \r\n
            split_strings = []
            for s in strings[i].data.split("\r\n"):
                for sub_s in s.split('\r'):
                    split_strings.extend(sub_s.split('\n'))

            strings[i].data = "\r\n".join(split_strings)
