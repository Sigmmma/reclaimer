import os
from array import array
from math import sqrt

class P8Palette():
    palette = ()

    def __init__(self, palette_filename):
        return
        with open("%s\\%s" % (os.path.dirname(__file__),
                              palette_filename), 'rb') as f:
            palette_data = f.read(1024)

        red_values = [0]*256
        green_values = [0]*256
        red_value_counts = {}
        green_value_counts = {}
        for i in range(256):
            r, g = palette_data[i*4 + 1: i*4 + 3]
            red_values[i], green_values[i] = r, g
            red_value_counts[r]   = red_value_counts.get(r, 0) + 1
            green_value_counts[g] = green_value_counts.get(g, 0) + 1

        # caching these values in dictionaries this way
        # will speed up converting normal maps to p8 bump
        dom_colors = []
        valid_values = [0] * len(red_value_counts)
        for i in range(len(valid_values)):
            dom_colors.extend([valid_values[i]] * value_counts[i])

        cached_dom_colors = {i: dom_colors[i] for i in range(256)}
        cached_sub_colors = []

        # the keys in this are the red values available in the
        # palette and their values are lists of the closest
        # available green values associated with that red value
        dom_idx_sub_colors = {valid_values[i]: cached_sub_colors[i]
                              for i in range(len(cached_sub_colors))}

        # the keys in this are a combination of the red and green values, and
        # the values are the palette index that specific combination yields
        cached_palette = {}
        seen = set()
        for i in range(256):
            color = (red_values[i] << 8) + green_values[i]
            if color not in seen:
                # don't cache repeats
                seen.add(color)
                cached_palette[color] = i

        self.palette = {
            0:cached_dom_colors,
            1:dom_idx_sub_colors,
            2:cached_palette}

        # now build the array to convert p8 back to 32 bit
        self.p8_palette_32bit = unpacked = array("B", palette_data)
        self.p8_palette_32bit_packed = packed = array("L")
        for i in range(0, 1024, 4):
            packed.append((unpacked[i]<<24)    + (unpacked[i + 1]<<16) +
                          (unpacked[i + 2]<<8) +  unpacked[i + 3])

    def argb_array_to_p8_array_average_alpha(self, unpacked_pix):
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]

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
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]

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
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]

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
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]

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


HALO_P8_PALETTE = P8Palette("p8_palette_halo")
STUBBS_P8_PALETTE = P8Palette("p8_palette_stubbs")
