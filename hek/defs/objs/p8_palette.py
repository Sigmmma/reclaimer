import os
from array import array
from math import sqrt

class P8Palette():
    
    hash_multiplier = 10000

    def __init__(self):
        # caching these values in dictionaries this way will
        # really speed up converting normal maps to p8 bump

        # this is the set of cached colors available to the
        # dominant color channel, which is selected by the bias.
        # the keys are 0 - 255 and the values are the closest
        # to that value that is available in the palette
        valid_values = [25, 47, 66, 82, 96, 107, 116, 122, 126, 128,
                        129, 133, 139, 148, 159, 173, 189, 208, 229]
        value_counts = (37, 21, 17, 15, 13, 10, 7, 4, 4,
                        1, 3, 4, 8, 10, 12, 15, 18, 20, 37)
        dom_colors = []
        
        for i in range(len(valid_values)):
            dom_colors.extend([valid_values[i]] * value_counts[i])
        cached_dom_colors = dict(zip(range(256), dom_colors))
        cached_sub_colors = []

        # this function is used for building the dictionaries that
        # will be cached in the dictionary below since there are
        # 20 possible red or green values we build 20 lists
        for i in range(20):
            colors = valid_values
            pad = 8-i if i < 8 else i-12

            if i == 0:
                colors = [0]
            elif pad > 0:
                colors = colors[pad:-pad]

            keys = []
            vals = []
            
            if len(colors) > 1:
                value_index = 0
                # we need to figure out the difference between the two
                # values so we know when to switch to the other color
                
                for value in range(256):
                    keys.append(value)

                    if value_index >= (len(colors) - 1):
                        pass
                    elif (value >= (colors[value_index] +
                                    (colors[value_index + 1] -
                                     colors[value_index]) // 2)):
                        # the value we are at is past the midpoint of the two
                        value_index += 1
                          
                    vals.append(colors[value_index])
            else:
                #if the red value is zero all the values are 0
                for value in range(256):
                    keys.append(value)
                    vals.append(0)
                    
            cached_sub_in_dom_set = dict(zip(keys, vals))

            cached_sub_colors.append(cached_sub_in_dom_set)

        # the keys in this are the red values available in the
        # palette and their values are lists of the closest
        # available green values associated with that red value
        dom_idx_sub_colors = dict(zip(valid_values,
            [cached_sub_colors[1], cached_sub_colors[2],
             cached_sub_colors[3], cached_sub_colors[4],
             cached_sub_colors[5], cached_sub_colors[6],
             cached_sub_colors[7], cached_sub_colors[8],
             cached_sub_colors[9], cached_sub_colors[10],
             cached_sub_colors[11], cached_sub_colors[12],
             cached_sub_colors[13], cached_sub_colors[14],
             cached_sub_colors[15], cached_sub_colors[16],
             cached_sub_colors[17], cached_sub_colors[18],
             cached_sub_colors[19]]
            )
        )
        
        cached_palette_keys = []
        cached_palette_values = []

        red_colors = [0]*250
        green_colors = [0]*250

        with open(os.path.join(os.path.dirname(__file__), "p8.act"), 'rb') as f:
            pal_data = f.read()[:(250)*3]

        for i in range(len(pal_data)//3):
            red_colors[i] = pal_data[i*3]
            green_colors[i] = pal_data[i*3+1]
        red_colors.extend([-1,-2,-3,-4,-5,-6])
        green_colors.extend([0]*6)


        # now we construct the pallet keys.
        # these are unique numbers obtained by combining the
        # red and green values in order to get a quick hash
        # used to look up which palette index to assign
        for index in range(256):
            #add the new hash to the list of keys
            cached_palette_keys.append(
                (red_colors[index]*self.hash_multiplier) + green_colors[index])
            cached_palette_values.append(index)

        # the keys in this are a combination of the red and green values, and
        # the values are the palette index that specific combination yields
        cached_palette = dict(zip(cached_palette_keys, cached_palette_values))
        
        self.palette = {
            0:cached_dom_colors,
            1:dom_idx_sub_colors,
            2:cached_palette}
        
        # now build the array to convert p8 back to 32 bit
        self.p8_palette_32bit = unpacked = array("B")
        self.p8_palette_32bit_packed = packed = array("L")
        for index in range(0, 256):
            if index <= 248:
                red = red_colors[index]
                green = green_colors[index]
                
                red_abs = abs(red-128)
                green_abs = abs(green-128)
                
                if abs(red_abs-127) > abs(green_abs-127):
                    scaler = 1-((red_abs/128) * 0.2)
                else:
                    scaler = 1-((green_abs/128) * 0.2)
                    
                blue = int(scaler*(sqrt(65535-(red_abs**2 + green_abs**2))))
                unpacked.extend((255, red, green, blue))

            elif index == 255:
                unpacked.extend((0, 128, 128, 255))
            else:
                unpacked.extend((0, 0, 0, 0))

            packed.append((unpacked[-4]<<24) + (unpacked[-3]<<16) +
                          (unpacked[-2]<<8)  +  unpacked[-1])

    def argb_array_to_p8_array_average_alpha(self, unpacked_pix):
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]
        multi = self.hash_multiplier
        
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
                
                indexing[i>>2] = pal2[((red*multi) + pal1[red][src_green])]
            else:
                indexing[i>>2] = 255

        return(self.p8_palette_32bit[0], indexing)

    def argb_array_to_p8_array_average(self, unpacked_pix):
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]
        multi = self.hash_multiplier
        
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
            
            indexing[i>>2] = pal2[((red*multi)+pal1[red][src_green])]

        return(self.p8_palette_32bit[0], indexing)

    def argb_array_to_p8_array_auto_alpha(self, unpacked_pix):
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]
        multi = self.hash_multiplier
        
        indexing = array("B", bytearray(len(unpacked_pix)//4) )
        
        for i in range(0, len(unpacked_pix), 4):
            if unpacked_pix[i]:
                red = unpacked_pix[i+1]
                green = unpacked_pix[i+2]
                
                if abs(red - 127) > abs(green - 127):
                    red = pal0[red]
                    indexing[i>>2] = pal2[((red*multi)+pal1[red][green])]
                else:
                    green = pal0[green]
                    indexing[i>>2] = pal2[((pal1[green][red]*multi)+green)]
            else:
                indexing[i>>2] = 255
                    
        return(self.p8_palette_32bit[0], indexing)

    def argb_array_to_p8_array_auto(self, unpacked_pix):
        pal0 = self.palette[0]
        pal1 = self.palette[1]
        pal2 = self.palette[2]
        multi = self.hash_multiplier
        
        indexing = array("B", bytearray(len(unpacked_pix)//4) )
        
        for i in range(0, len(unpacked_pix), 4):
            red = unpacked_pix[i+1]
            green = unpacked_pix[i+2]
            
            if abs(red - 127) > abs(green - 127):
                red = pal0[red]
                indexing[i>>2] = pal2[((red*multi) + pal1[red][green])]
            else:
                green = pal0[green]
                indexing[i>>2] = pal2[((pal1[green][red]*multi) + green)]

        return(self.p8_palette_32bit[0], indexing)


def load_palette():
    #construct the palette object
    return P8Palette()
