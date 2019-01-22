import os
from array import array
from math import sqrt


def generate_best_fit_map(valid_values, max_value=255):
    best_fit_values = []
    last_val = None
    for i in range(len(valid_values)):
        curr_val = valid_values[i]
        if last_val is None:
            val_ct = curr_val + 1
        else:
            val_ct = int((curr_val - last_val + 1) / 2)

        if i + 1 < len(valid_values):
            val_ct += int((valid_values[i + 1] - curr_val) / 2)
        else:
            val_ct += max_value - curr_val

        best_fit_values.extend([curr_val] * val_ct)
        last_val = curr_val

    return best_fit_values


class P8Palette():
    # maps each red or green value to the
    # closest equivalent value in the palette
    doms_by_value = ()

    # Maps each possible dom_value to a list.
    # That list maps each 0-255 sub_value to its
    # closest equivalent value in the palette.
    # if red is dom, green is sub, and vice versa.
    subs_by_doms = ()

    # maps [(red << 8) + green]  to its palette index
    # where red and green are NOT sub/dom values.
    # contains EXACTLY 2^16 entries
    smallest_diff_map = ()

    # maps [(red << 8) + green]  to its palette index
    # where red and green are sub/dom values.
    # contains no more than 256 entries
    palette = ()

    palette_directory = os.path.dirname(__file__)
    palette_filename = ""

    def __init__(self, palette_filename=""):
        if palette_filename:
            self.palette_filename = palette_filename

        with open("%s\\%s" % (self.palette_directory,
                              self.palette_filename), 'rb') as f:
            palette_data = f.read(1024)

        colors = [0]*256
        green_subs_by_red_doms = {}
        red_subs_by_green_doms = {}
        for i in range(256):
            a, r, g, b = palette_data[i*4: i*4 + 4]
            if (r != 0 or g != 0) and a != 0:
                # don't cache zero color or zero alpha, as
                # they'll just throw off good palette usage
                colors[i] = (r << 8) + g
                green_subs_by_red_doms.setdefault(r, set()).add(g)
                red_subs_by_green_doms.setdefault(g, set()).add(r)

        assert green_subs_by_red_doms == red_subs_by_green_doms

        subs_by_doms = green_subs_by_red_doms
        valid_values = sorted(subs_by_doms.keys())

        self.smallest_diff_map = [0] * 65536
        self.doms_by_value = generate_best_fit_map(valid_values)
        self.subs_by_doms = {dom: generate_best_fit_map(sorted(subs))
                             for dom, subs in subs_by_doms.items()}
        self.palette = {}

        for i in range(256):
            self.subs_by_doms[i] = self.subs_by_doms[self.doms_by_value[i]]
            if colors[i] not in self.palette or colors[i] == 0:
                # don't cache repeats or all zero colors
                self.palette[colors[i]] = i

        # now build the array to convert p8 back to 32 bit
        self.p8_palette_32bit = unpacked = array("B", palette_data)
        self.p8_palette_32bit_packed = packed = array("L")
        for i in range(0, 1024, 4):
            packed.append((unpacked[i]<<24)    + (unpacked[i + 1]<<16) +
                          (unpacked[i + 2]<<8) +  unpacked[i + 3])

        self.load_smallest_diff_map()

    def write_palette_image(self):
        width = height = 256
        with open("%s\\%s.bmp" % (self.palette_directory,
                                  self.palette_filename), 'wb+') as f:
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
                    i = self.smallest_diff_map[(r << 8) + g] * 4
                    f.write(self.p8_palette_32bit[i: i + 4][::-1])

    def load_smallest_diff_map(self):
        try:
            with open("%s\\%s_diff_map" % (self.palette_directory,
                                           self.palette_filename), 'rb') as f:
                self.smallest_diff_map = list(f.read(65536))
                if len(self.smallest_diff_map) != 65536:
                    raise ValueError("Cached smallest diff map is invalid.")
        except Exception:
            self.generate_smallest_diff_map()
            try:
                self.cache_smallest_diff_map()
            except Exception:
                pass

    def cache_smallest_diff_map(self):
        with open("%s\\%s_diff_map" % (self.palette_directory,
                                       self.palette_filename), 'wb+') as f:
            f.write(array("B", self.smallest_diff_map))

    def generate_smallest_diff_map(self):
        diff_map = [65536] * 65536
        smallest_diff_map = self.smallest_diff_map
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
                        smallest_diff_map[true_rg] = i

    def argb_array_to_p8_array_average_alpha(self, unpacked_pix):
        pal0 = self.doms_by_value
        pal1 = self.subs_by_doms
        pal2 = self.palette

        indexing = array("B", bytearray(len(unpacked_pix)//4) )

        for i in range(0, len(indexing)*4, 4):
            if unpacked_pix[i]:
                src_red = unpacked_pix[i+1]
                src_green = unpacked_pix[i+2]

                green = pal0[src_green]
                best_r_in_g = pal1[green][src_red]

                red = pal0[src_red]
                best_g_in_r = pal1[red][src_green]

                src_green = best_g_in_r + (src_green - best_g_in_r)//2
                src_red = best_r_in_g + (src_red - best_r_in_g)//2

                red = pal0[src_red]

                indexing[i>>2] = pal2[((red<<8) + pal1[red][src_green])]
            else:
                indexing[i>>2] = 255

        return (self.p8_palette_32bit, indexing)

    def argb_array_to_p8_array_average(self, unpacked_pix):
        pal0 = self.doms_by_value
        pal1 = self.subs_by_doms
        pal2 = self.palette

        indexing = array("B", bytearray(len(unpacked_pix)//4) )

        for i in range(0, len(indexing)*4, 4):
            src_red = unpacked_pix[i+1]
            src_green = unpacked_pix[i+2]

            green = pal0[src_green]
            best_r_in_g = pal1[green][src_red]

            red = pal0[src_red]
            best_g_in_r = pal1[red][src_green]

            src_green = best_g_in_r + (src_green - best_g_in_r)//2
            src_red = best_r_in_g + (src_red - best_r_in_g)//2

            red = pal0[src_red]

            indexing[i>>2] = pal2[((red<<8)+pal1[red][src_green])]

        return (self.p8_palette_32bit, indexing)

    def argb_array_to_p8_array_auto_alpha(self, unpacked_pix):
        pal0 = self.doms_by_value
        pal1 = self.subs_by_doms
        pal2 = self.palette

        indexing = array("B", bytearray(len(unpacked_pix)//4) )

        for i in range(0, len(unpacked_pix), 4):
            if unpacked_pix[i]:
                red = unpacked_pix[i+1]
                green = unpacked_pix[i+2]

                if abs(red - 127) > abs(green - 127):
                    red = pal0[red]
                    indexing[i>>2] = pal2[((red<<8)+pal1[red][green])]
                else:
                    green = pal0[green]
                    indexing[i>>2] = pal2[((pal1[green][red]<<8)+green)]
            else:
                indexing[i>>2] = 255

        return (self.p8_palette_32bit, indexing)

    def argb_array_to_p8_array_auto(self, unpacked_pix):
        pal0 = self.doms_by_value
        pal1 = self.subs_by_doms
        pal2 = self.palette

        indexing = array("B", bytearray(len(unpacked_pix)//4) )

        for i in range(0, len(unpacked_pix), 4):
            red = unpacked_pix[i+1]
            green = unpacked_pix[i+2]

            if abs(red - 127) > abs(green - 127):
                red = pal0[red]
                indexing[i>>2] = pal2[((red<<8) + pal1[red][green])]
            else:
                green = pal0[green]
                indexing[i>>2] = pal2[((pal1[green][red]<<8) + green)]

        return (self.p8_palette_32bit, indexing)

    def argb_array_to_p8_array_best_fit_alpha(self, unpacked_pix):
        color_map = self.smallest_diff_map
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
        color_map = self.smallest_diff_map
        indexing = array("B", bytearray(len(unpacked_pix)//4))
        for i in range(0, len(unpacked_pix), 4):
            red = unpacked_pix[i+1]
            green = unpacked_pix[i+2]
            indexing[i>>2] = color_map[(red<<8)+green]

        return (self.p8_palette_32bit, indexing)


HALO_P8_PALETTE = P8Palette("p8_palette_halo")
STUBBS_P8_PALETTE = P8Palette("p8_palette_stubbs")
