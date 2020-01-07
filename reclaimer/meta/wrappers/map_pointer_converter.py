#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

class MapPointerConverter:
    '''Handles converting virtual pointers to/from file pointers in maps.'''
    class PageInfo:
        def __init__(self, v_addr=0, f_addr=0, size=0):
            self.v_addr = v_addr
            self.f_addr = f_addr
            self.size = size
            self.v_addr_range = range(self.v_addr, self.v_addr + self.size)
            self.f_addr_range = range(self.f_addr, self.f_addr + self.size)

    _page_infos = ()

    def __init__(self, *pages):
        self._page_infos = []
        for v_addr, f_addr, size in pages:
            self.add_page_info(v_addr, f_addr, size)

    @property
    def mapped_size(self):
        size = 0
        for page in self._page_infos:
            size += page.size
        return size

    def add_page_info(self, v_addr, f_addr, size):
        if size <= 0:
            return

        new_page = MapPointerConverter.PageInfo(v_addr, f_addr, size)
        i = 0
        for page in self._page_infos:
            # insert the new page based on its virtual pointer
            if v_addr <= page.v_addr:
                break
            i += 1
        self._page_infos.insert(i, new_page)

    def v_ptr_to_f_ptr(self, ptr):
        '''Converts a virtual pointer in a map into a file pointer.'''
        for info in self._page_infos:
            if ptr in info.v_addr_range:
                return ptr - info.v_addr + info.f_addr
        return -0x7FffFFff

    def f_ptr_to_v_ptr(self, ptr):
        '''Converts a file pointer in a map into a virtual pointer.'''
        for info in self._page_infos:
            if ptr in info.f_addr_range:
                return ptr + info.v_addr - info.f_addr
        return -0x7FffFFff
