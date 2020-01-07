#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
from array import array
from math import sqrt


class P8Palette():
    # Maps [(red << 8) + green]  to its palette index,
    # where the red/green pairs are restricted to
    # being those found in the 256 color palette.
    # and are in the range of [0, 255]
    # Contains EXACTLY 2^8 entries
    palette_rg = ()

    # Maps [(red << 8) + green]  to its palette index,
    # where red and green are independent of one another
    # and are in the range of [0, 255]
    # Contains EXACTLY 2^16 entries
    palette_map = ()

    palette_directory = os.path.dirname(__file__)
    palette_filename = ""

    palette_map_filename = ""

    def __init__(self, palette_filename=""):
        if palette_filename:
            self.palette_filename = palette_filename

        self.palette_map_filename = self.palette_filename + "_diff_map"

        with open(os.path.join(self.palette_directory,
                               self.palette_filename), 'rb') as f:
            palette_data = f.read(1024)

        # now build the array to convert p8 back to 32 bit
        self.p8_palette_32bit = unpacked = array("B", palette_data)
        self.p8_palette_32bit_packed = packed = array("L")
        self.palette_rg = array("H", [0] * 256)
        for i in range(256):
            a, r, g, b = unpacked[i * 4: i * 4 + 4]
            self.palette_rg[i] = (r << 8) + g
            packed.append((a<<24) + (r<<16) + (g<<8) + b)

        self.load_palette_map(False)

    @property
    def palette_map_loaded(self):
        return self.palette_map and len(self.palette_map) == 65536

    def write_palette_image(self):
        width = height = 256
        with open(os.path.join(self.palette_directory,
                               self.palette_filename + ".bmp"), 'wb+') as f:
            base = 138
            size = base + (width * height * 4)
            f.write(b"BM" + size.to_bytes(4, 'little'))
            f.write(b"\x00\x00\x00\x00\x8A\x00\x00\x00\x7C\x00\x00\x00")
            f.write(width.to_bytes(4, 'little') + height.to_bytes(4, 'little'))
            f.write(b"\x01\x00\x20\x00")
            f.write(b'\x00' * (size - f.tell()))
            for r in range(256):
                for g in range(256):
                    f.seek((g * width + r) * 4 + base)
                    color = (r << 8) + g
                    if color in self.palette_rg:
                        continue
                    i = self.palette_map[color] * 4
                    f.write(self.p8_palette_32bit[i: i + 4][::-1])

    def load_palette_map(self, generate_on_fail=True):
        try:
            with open(os.path.join(self.palette_directory,
                                   self.palette_map_filename), 'rb') as f:
                data = f.read(65536)
                if len(data) != 65536:
                    raise ValueError("Cached smallest diff map is invalid.")
                self.palette_map = list(data)
        except Exception:
            if generate_on_fail:
                self.generate_palette_map()
                try:
                    self.cache_palette_map()
                except Exception:
                    pass

    def cache_palette_map(self):
        with open(os.path.join(self.palette_directory,
                               self.palette_map_filename), 'wb+') as f:
            f.write(array("B", self.palette_map))

    def generate_palette_map(self):
        diff_map = [65536] * 65536
        palette_map = self.palette_map = [0] * 65536
        range_256 = tuple(range(256))

        colors = list(((color >> 8) & 0xFFff)
                      for color in self.p8_palette_32bit_packed)
        for i in range(len(colors)):
            if colors[i] == 0:
                continue

            pal_r = colors[i] >> 8
            pal_g = colors[i] & 0xFF
            for r in range_256:
                r_diff = (pal_r - r) ** 2
                r = r << 8
                for g in range_256:
                    diff = r_diff + (pal_g - g) ** 2
                    true_rg = r | g
                    if diff < diff_map[true_rg]:
                        diff_map[true_rg] = diff
                        palette_map[true_rg] = i

    def argb_array_to_p8_array_best_fit_alpha(self, unpacked_pix):
        if not self.palette_map_loaded:
            self.load_palette_map()

        color_map = self.palette_map
        indexing = array("B", bytearray(len(unpacked_pix)//4))
        for i in range(0, len(unpacked_pix), 4):
            if unpacked_pix[i]:
                red = unpacked_pix[i+1]
                green = unpacked_pix[i+2]
                indexing[i>>2] = color_map[(red<<8)+green]
            else:
                indexing[i>>2] = 255

        return (self.p8_palette_32bit, indexing)

    def argb_array_to_p8_array_best_fit(self, unpacked_pix):
        if not self.palette_map_loaded:
            self.load_palette_map()

        color_map = self.palette_map
        indexing = array("B", bytearray(len(unpacked_pix)//4))
        for i in range(0, len(unpacked_pix), 4):
            red = unpacked_pix[i+1]
            green = unpacked_pix[i+2]
            indexing[i>>2] = color_map[(red<<8)+green]

        return (self.p8_palette_32bit, indexing)


HALO_P8_PALETTE = P8Palette("p8_palette_halo")
STUBBS_P8_PALETTE = P8Palette("p8_palette_stubbs")
