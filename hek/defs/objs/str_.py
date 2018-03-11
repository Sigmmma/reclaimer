from .tag import *

class Str_Tag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        strings = self.data.tagdata.strings.STEPTREE

        for i in range(len(strings)):
            # replace all instances of \r and \n with \r\n
            new_string = ""
            for s in strings[i].data.split('\r'):
                for ss in s.split('\n'):
                    new_string += ss + "\r\n"

            strings[i].data = new_string
