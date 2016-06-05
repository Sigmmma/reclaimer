from array import array
from math import sqrt

hash_multiplier = 10000

class P8Palette():

    def __init__(self):
        #caching these values in dictionaries this way will
        #really speed up converting normal maps to p8 bump

        #this is the set of cached colors abailable to the
        #dominant color channel, which is selected by the bias.
        #the keys are 0 - 255 and the values are the closest
        #to that value that is available in the palette
        cached_dom_colors = dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                                      16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
                                      32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
                                      48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,
                                      64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
                                      80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,
                                      96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,
                                      112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,
                                      128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,
                                      144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,
                                      160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,
                                      176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,
                                      192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,
                                      208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,
                                      224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,
                                      240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255],
                                      [25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,
                                       25,25,25,25,25,25,25,25,25,25,25,25,25,25,47,47,47,47,47,47,47,47,47,
                                       47,47,47,47,47,47,47,47,47,47,47,47,66,66,66,66,66,66,66,66,66,66,66,
                                       66,66,66,66,66,66,82,82,82,82,82,82,82,82,82,82,82,82,82,82,82,96,96,
                                       96,96,96,96,96,96,96,96,96,96,96,107,107,107,107,107,107,107,107,107,
                                       107,116,116,116,116,116,116,116,122,122,122,122,126,126,126,126,128,129,
                                       129,129,133,133,133,133,139,139,139,139,139,139,139,139,148,148,148,148,
                                       148,148,148,148,148,148,159,159,159,159,159,159,159,159,159,159,159,159,
                                       173,173,173,173,173,173,173,173,173,173,173,173,173,173,173,189,189,189,
                                       189,189,189,189,189,189,189,189,189,189,189,189,189,189,189,208,208,208,
                                       208,208,208,208,208,208,208,208,208,208,208,208,208,208,208,208,208,229,
                                       229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,
                                       229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229,229]
                                     )
                                 )


        cached_sub_colors = []

        #this function is used for building the dictionaries that will be cached in the dictionary below
        #since there are 20 possible red or green values we build 20 lists
        for loop_count in range(20):
            if loop_count == 0:
                available_colors = [0]
            elif (loop_count == 1 or loop_count == 19):
                available_colors = [122,126,128,129,133]
            elif (loop_count == 2 or loop_count == 18):
                available_colors = [116,122,126,128,129,133,139]
            elif (loop_count == 3 or loop_count == 17):
                available_colors = [107,116,122,126,128,129,133,139,148]
            elif (loop_count == 4 or loop_count == 16):
                available_colors = [96,107,116,122,126,
                                    128,129,133,139,148,159]
            elif (loop_count == 5 or loop_count == 15):
                available_colors = [82,96,107,116,122,126,128,
                                    129,133,139,148,159,173]
            elif (loop_count == 6 or loop_count == 14):
                available_colors = [66,82,96,107,116,122,126,128,
                                    129,133,139,148,159,173,189]
            elif (loop_count == 7 or loop_count == 13):
                available_colors = [47,66,82,96,107,116,122,126,128,
                                    129,133,139,148,159,173,189,208]
            else:
                available_colors = [25,47,66,82,96,107,116,122,126,128,
                                    129,133,139,148,159,173,189,208,229]


            keys_list = []
            values_list = []
            
            if (len(available_colors) > 1):
                value_index = 0
                #we need to figure out the difference between the two values so we
                #know when to switch to the other color
                
                for value in range(256):
                    keys_list.append(value)
                    
                    #we check this so we don't try to read past the end of the list
                    if (value_index < (len(available_colors) - 1)):
                        
                        #check if the value we are at is past the midpoint of the two colors
                        if (value >= (available_colors[value_index] +
                                      (available_colors[value_index + 1] -
                                       available_colors[value_index]) // 2)):
                            value_index += 1
                          
                    values_list.append(available_colors[value_index])
            else:
                #if the red value is zero all the values are 0
                for value in range(256):
                    keys_list.append(value)
                    values_list.append(0)
                    
            cached_sub_in_dom_set = dict(zip(keys_list, values_list))

            cached_sub_colors.append(cached_sub_in_dom_set)

        #the keys in this are the red values available in the palette and their values are
        #lists of the closest available green values associated with that red value
        dom_idx_sub_colors = dict(zip([25,47,66,82,96,107,116,122,126,128,
                                       129,133,139,148,159,173,189,208,229],
                                        [cached_sub_colors[1],cached_sub_colors[2],
                                         cached_sub_colors[3],cached_sub_colors[4],
                                         cached_sub_colors[5],cached_sub_colors[6],
                                         cached_sub_colors[7],cached_sub_colors[8],
                                         cached_sub_colors[9],cached_sub_colors[10],
                                         cached_sub_colors[11],cached_sub_colors[12],
                                         cached_sub_colors[13],cached_sub_colors[14],
                                         cached_sub_colors[15],cached_sub_colors[16],
                                         cached_sub_colors[17],cached_sub_colors[18],
                                         cached_sub_colors[19]
                                         ]
                                        )
                                    )

        
        cached_palette_keys = []
        cached_palette_values = []
        
        red_colors = [          122,126,128,129,133,
                            116,122,126,128,129,133,139,
                        107,116,122,126,128,129,133,139,148,
                    96, 107,116,122,126,128,129,133,139,148,159,
                82, 96, 107,116,122,126,128,129,133,139,148,159,173,
            66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,
        47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,
    25, 47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,229,
    25, 47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,229,
    25, 47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,229,
    25, 47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,229,
    25, 47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,229,
        47, 66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,208,
            66, 82, 96, 107,116,122,126,128,129,133,139,148,159,173,189,
                82, 96, 107,116,122,126,128,129,133,139,148,159,173,
                    96, 107,116,122,126,128,129,133,139,148,159,
                        107,116,122,126,128,129,133,139,148,
                            116,122,126,128,129,133,139,
                                122,126,128,129,133,
                      0,-1,-2,-3,-4,-5,-6]

        green_colors = [         25, 25, 25, 25, 25,
                             47, 47, 47, 47, 47, 47, 47,
                         66, 66, 66, 66, 66, 66, 66, 66, 66,
                     82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82,
                 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96,
            107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,
        116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,
    122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,122,
    126,126,126,126,126,126,126,126,126,126,126,126,126,126,126,126,126,126,126,
    128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,
    129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,129,
    133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,133,
        139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,
            148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,
                159,159,159,159,159,159,159,159,159,159,159,159,159,
                    173,173,173,173,173,173,173,173,173,173,173,
                        189,189,189,189,189,189,189,189,189,
                            208,208,208,208,208,208,208,
                                229,229,229,229,229,
                        0,0,0,0,0,0,0]


        #now we construct the pallet keys
        #these are unique numbers obtained by combining the red and green values
        #in order to get a quick "hash" used to look up which palette index to assign
        for index in range(256):
            #add the new hash to the list of keys
            cached_palette_keys.append((red_colors[index]*hash_multiplier) + green_colors[index])
            cached_palette_values.append(index)

        #the keys in this are a combination of the red and green values and
        #the values are the palette index that that specific combination yields
        cached_palette = dict(zip(cached_palette_keys, cached_palette_values))
        
        self.palette = {0:cached_dom_colors, 1:dom_idx_sub_colors, 2:cached_palette}
        
        #now lets build the array to convert p8 back to 32 bit
        self.p8_palette_32bit = array("B", [])
        self.p8_palette_32bit_packed = array("I", [])
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
                    
                blue = int(scaler*(sqrt(65536-(red_abs**2 + green_abs**2) ) ))
                if blue > 255:
                    self.p8_palette_32bit.extend(array("B", [255, red, green, 255]))
                    self.p8_palette_32bit_packed.append( (255<<24) + (red<<16) +
                                                         (green<<8) + 255)
                else:
                    self.p8_palette_32bit.extend(array("B", [255, red, green, blue]))
                    self.p8_palette_32bit_packed.append( (255<<24) + (red<<16) +
                                                         (green<<8) + blue)
                    
            elif index == 255:
                self.p8_palette_32bit.extend(array("B", [0, 128, 128, 255]))
                self.p8_palette_32bit_packed.append( (128<<16) + (128<<8) + 255)
            else:
                self.p8_palette_32bit.extend(array("B", [0, 0, 0, 0]))
                self.p8_palette_32bit_packed.append(0)
                

        #stick the palette in a list since that's how it'll
        #need to be referenced by the bitmap convertor
        self.p8_palette_32bit = [self.p8_palette_32bit]
        self.p8_palette_32bit_packed = [self.p8_palette_32bit_packed]



    ###################################################################################
    """THE BELOW FUNCTIONS ARE FOR CONVERTING AN ENTIRE ARRAY TO OR FROM P8/ARGB/RGB"""
    ###################################################################################


    def argb_array_to_p8_array_average_alpha(self, unpacked_pix_array):
        palette_0 = self.palette[0]
        palette_1 = self.palette[1]
        palette_2 = self.palette[2]
        multi = hash_multiplier
        
        indexing_array = array("B", [0]*(len(unpacked_pix_array)//4 ))
        
        for i in range(0, len(indexing_array)*4, 4):
            if unpacked_pix_array[i] == 0:
                indexing_array[i//4] = 255
            else:
                src_red = unpacked_pix_array[i+1]
                src_green = unpacked_pix_array[i+2]
                
                green = palette_0[src_green]
                best_red_in_green = palette_1[green][src_red]
                
                red = palette_0[src_red]
                best_green_in_red = palette_1[red][src_green]
                
                src_green = best_green_in_red + (src_green - best_green_in_red)//2
                src_red = best_red_in_green + (src_red - best_red_in_green)//2
                
                red = palette_0[src_red]
                
                indexing_array[i] = palette_2[((red*multi) + palette_1[red][src_green])]

        return(self.p8_palette_32bit[0], indexing_array)

    

    def argb_array_to_p8_array_average(self, unpacked_pix_array):
        palette_0 = self.palette[0]
        palette_1 = self.palette[1]
        palette_2 = self.palette[2]
        multi = hash_multiplier
        
        indexing_array = array("B", [0]*(len(unpacked_pix_array)//4 ))
        
        for i in range(0, len(indexing_array)*4, 4):
            src_red = unpacked_pix_array[i+1]
            src_green = unpacked_pix_array[i+2]
            
            green = palette_0[src_green]
            best_red_in_green = palette_1[green][src_red]
            
            red = palette_0[src_red]
            best_green_in_red = palette_1[red][src_green]
            
            src_green = best_green_in_red + (src_green - best_green_in_red)//2
            src_red = best_red_in_green + (src_red - best_red_in_green)//2
            
            red = palette_0[src_red]
            
            indexing_array[i] = palette_2[((red*multi)+palette_1[red][src_green])]

        return(self.p8_palette_32bit[0], indexing_array)

            

    def argb_array_to_p8_array_auto_alpha(self, unpacked_pix_array):
        palette_0 = self.palette[0]
        palette_1 = self.palette[1]
        palette_2 = self.palette[2]
        multi = hash_multiplier
        
        indexing_array = array("B", [0]*(len(unpacked_pix_array)//4 ))
        
        for i in range(0, len(unpacked_pix_array), 4):
            if unpacked_pix_array[i] == 0:
                indexing_array[i//4] = 255
            else:
                red = unpacked_pix_array[i+1]
                green = unpacked_pix_array[i+2]
                
                if abs(red - 127) > abs(green - 127):
                    red = palette_0[red]
                    indexing_array[i//4] = palette_2[((red*multi)+palette_1[red][green])]
                else:
                    green = palette_0[green]
                    indexing_array[i//4] = palette_2[((palette_1[green][red]*multi)+green)]
                    
        return(self.p8_palette_32bit[0], indexing_array)

            

    def argb_array_to_p8_array_auto(self, unpacked_pix_array):
        palette_0 = self.palette[0]
        palette_1 = self.palette[1]
        palette_2 = self.palette[2]
        multi = hash_multiplier
        
        indexing_array = array("B", [0]*(len(unpacked_pix_array)//4 ))
        
        for i in range(0, len(unpacked_pix_array), 4):
            red = unpacked_pix_array[i+1]
            green = unpacked_pix_array[i+2]
            
            if abs(red - 127) > abs(green - 127):
                red = palette_0[red]
                indexing_array[i//4] = palette_2[((red*multi) + palette_1[red][green])]
            else:
                green = palette_0[green]
                indexing_array[i//4] = palette_2[((palette_1[green][red]*multi) + green)]

        return(self.p8_palette_32bit[0], indexing_array)


def load_palette():
    #construct the palette object
    return(P8Palette())
