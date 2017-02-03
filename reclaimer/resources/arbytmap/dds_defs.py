
from array import array
from math import sqrt

#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
ab = None

def combine(main_dict, *dicts):        
    for dct in dicts:
        for key in dct:
            if key in main_dict:
                if (isinstance(dct[key], dict) and
                    isinstance(main_dict[key], dict)):
                    combine(main_dict[key], dct[key])
            else:
                main_dict[key] = dct[key]
    return main_dict


def initialize():
    """FOR DXT FORMATS, ALPHA CHANNELS ARE TREATED SPECIALLY, BUT ARE EXPLICITELY
    PLACED HERE TO MAKE SURE THEY DONT CAUSE THE CHANNEL MAP SWAPPING PROBLEMS"""
    
    ab.FORMAT_DXT1 = "DXT1"
    ab.FORMAT_DXT2 = "DXT2"
    ab.FORMAT_DXT3 = "DXT3"
    ab.FORMAT_DXT4 = "DXT4"
    ab.FORMAT_DXT5 = "DXT5"

    ab.FORMAT_DXT3A = "DXT3A"           #NOT YET IMPLEMENTED
    ab.FORMAT_DXT3A1111 = "DXT3A1111"   #NOT YET IMPLEMENTED
    
    ab.FORMAT_DXT5NM = "DXT5NM"         #NOT YET IMPLEMENTED
    ab.FORMAT_DXN = "DXN"
    ab.FORMAT_DXT5A = "DXT5A"           #NOT YET IMPLEMENTED
    ab.FORMAT_DXT5Y = "DXT5Y"           #NOT YET IMPLEMENTED
    ab.FORMAT_DXT5AY = "DXT5AY"         #NOT YET IMPLEMENTED
    
    ab.FORMAT_CXT1 = "CXT1"             #NOT YET IMPLEMENTED
    ab.FORMAT_U8V8 = "U8V8"             #NOT YET IMPLEMENTED

    dxt_specifications = {'compressed':True, 'dds_format':True,
                          'min_width':4, 'min_height':4,
                          'data_size':'L', 'channel_count':4,
                          'channel_offsets':(0,11,5,0),
                          'channel_masks':(0,63488,2016,31)}


    ab.define_format(**combine({'format_id':ab.FORMAT_DXT1, 'bpp':4,
                                'channel_depths':(1,5,6,5),
                                'unpacker':unpack_dxt1,
                                'packer':pack_dxt1},
                               dxt_specifications) )
    
    for FORMAT in (ab.FORMAT_DXT2, ab.FORMAT_DXT3):
        ab.define_format(**combine({'format_id':FORMAT, 'bpp':8,
                                    'channel_depths':(4,5,6,5),
                                    'unpacker':unpack_dxt2_3,
                                    'packer':pack_dxt2_3},
                                   dxt_specifications) )
        
    for FORMAT in (ab.FORMAT_DXT4, ab.FORMAT_DXT5):
        ab.define_format(**combine({'format_id':FORMAT, 'bpp':8,
                                    'channel_depths':(8,5,6,5),
                                    'unpacker':unpack_dxt4_5,
                                    'packer':pack_dxt4_5},
                                   dxt_specifications) )
        
    ab.define_format(**combine({'format_id':ab.FORMAT_DXN, 'bpp':8,
                                'channel_depths':(0,8,8,8),
                                'unpacker':unpack_dxn,
                                'packer':pack_dxn,
                                'channel_offsets':(0,16,8,0),
                                'three_channels':True,
                                'channel_masks':(0,16711680,65280,255)},
                               dxt_specifications) )
    
    ab.define_format(format_id=ab.FORMAT_U8V8, bpp=16, channel_count=4,
                     unpacker=unpack_u8v8, packer=pack_u8v8,
                     channel_depths=(0,8,8,8), dds_format=True,
                     channel_offsets=(0,0,8,0), channel_masks=(0,255,65280,0))


#used to make dxt1 deciphering faster
DXT1_INDEXING_MASKS = array("L", [])
DXT1_INDEXING_BIT_SHIFTS = range(0, 32, 2)

#used to make dxt3 deciphering faster
DXT3_ALPHA_MASKS = array("Q", [])
DXT3_ALPHA_BIT_SHIFTS = range(0, 64, 4)

#used to make dxt5 deciphering faster
DXT5_ALPHA_MASKS = array("Q", [])
DXT5_ALPHA_BIT_SHIFTS = range(0, 48, 3)

#used to scale DXT pixel values up to 8-bit
DXT_R_SCALE = array("B", [])
DXT_G_SCALE = array("B", [])
DXT_B_SCALE = array("B", [])

range_16 = range(16)


for i in range_16:
    DXT1_INDEXING_MASKS.append(3<<(i*2))
    DXT3_ALPHA_MASKS.append(15<<(i*4))
    DXT5_ALPHA_MASKS.append(7<<(i*3))


for i in range(32):
    DXT_R_SCALE.append(int(round( i*(255/31) )))
    DXT_B_SCALE.append(int(round( i*(255/31) )))
for i in range(64):
    DXT_G_SCALE.append(int(round( i*(255/63) )))



def unpack_dxt1(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    packed_pixel_array = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    unpacked_pixel_array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*width*height*self.unpacked_channel_count )
    upa = unpacked_pixel_array

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]

    ################################################
    """CURRENTLY THE DXT UNPACKING ROUTINES DO NOT
    SUPPORT DROPPING CHANNELS WHILE UNPACKING. I SEE NO
    REASON TO IMPLEMENT IT AS IT WOULD BE VERY SLOW."""
    ################################################

    r_scale = DXT_R_SCALE
    g_scale = DXT_G_SCALE
    b_scale = DXT_B_SCALE
    
    channel_0 = self.channel_mapping.index(0)
    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    texel_pixel_mapping = get_texel_mapping(width, height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    texel_x_pixel_offsets = range(0, texel_width*16, 16)
    texel_y_pixel_offsets = range(0, texel_height*16*width, 16*width)
    
    #loop through each texel
    for curr_index in range(len(packed_pixel_array)//2):

        #get the offset to use
        texel_offset = (texel_x_pixel_offsets[curr_index%texel_width] +
                        texel_y_pixel_offsets[curr_index//texel_width])
        
        """if the format DXT1 then the two entries in the array
        are the colors and the color indexing in that order."""
        COLOR_0 = packed_pixel_array[curr_index*2] & 65535
        COLOR_1 = (packed_pixel_array[curr_index*2] & 4294901760) >> 16
        INDEXING = packed_pixel_array[curr_index*2+1]

        """unpack the colors"""
        color_0[1] = r_scale[(COLOR_0 & 63488) >> 11]
        color_0[2] = g_scale[(COLOR_0 & 2016) >> 5]
        color_0[3] = b_scale[COLOR_0 & 31]
        
        color_1[1] = r_scale[(COLOR_1 & 63488) >> 11]
        color_1[2] = g_scale[(COLOR_1 & 2016) >> 5]
        color_1[3] = b_scale[COLOR_1 & 31]

        #if the first color is a larger integer then color key transparency is NOT used
        if COLOR_0 > COLOR_1:
            color_2[1] = (color_0[1]*2 + color_1[1])//3
            color_2[2] = (color_0[2]*2 + color_1[2])//3
            color_2[3] = (color_0[3]*2 + color_1[3])//3
            colors[3] = [255,(color_0[1] + 2*color_1[1])//3,
                         (color_0[2] + 2*color_1[2])//3,
                         (color_0[3] + 2*color_1[3])//3]
        else:
            color_2[1] = (color_0[1]+color_1[1])//2
            color_2[2] = (color_0[2]+color_1[2])//2
            color_2[3] = (color_0[3]+color_1[3])//2
            colors[3] = [0,0,0,0]
            
        for i in range_16:
            color = colors[(INDEXING & DXT1_INDEXING_MASKS[i]) >> DXT1_INDEXING_BIT_SHIFTS[i]]
            
            upa[texel_pixel_mapping[i] + texel_offset+channel_0] = color[0]
            upa[texel_pixel_mapping[i] + texel_offset+channel_1] = color[1]
            upa[texel_pixel_mapping[i] + texel_offset+channel_2] = color[2]
            upa[texel_pixel_mapping[i] + texel_offset+channel_3] = color[3]

    return unpacked_pixel_array


def unpack_dxt2_3(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT2/3 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    packed_pixel_array = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    unpacked_pixel_array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*width*height*self.unpacked_channel_count )
    upa = unpacked_pixel_array

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]

    alpha_masks, alpha_bit_shifts, alpha_lookup = DXT3_ALPHA_MASKS, DXT3_ALPHA_BIT_SHIFTS, self.channel_upscalers[0]

    r_scale = DXT_R_SCALE
    g_scale = DXT_G_SCALE
    b_scale = DXT_B_SCALE
    
    channel_0 = self.channel_mapping.index(0)
    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    texel_pixel_mapping = get_texel_mapping(width, height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    texel_x_pixel_offsets = range(0, texel_width*16, 16)
    texel_y_pixel_offsets = range(0, texel_height*16*width, 16*width)
    
    #loop through each texel
    for curr_index in range(len(packed_pixel_array)//4):

        #get the offset to use
        texel_offset = (texel_x_pixel_offsets[curr_index%texel_width] +
                        texel_y_pixel_offsets[curr_index//texel_width])
        
        #DXT2/3 is much simpler
        ALPHA = (packed_pixel_array[curr_index*4+1]<<32) + packed_pixel_array[curr_index*4]
        COLOR_0 = packed_pixel_array[curr_index*4+2] & 65535
        COLOR_1 = (packed_pixel_array[curr_index*4+2] & 4294901760) >> 16
        INDEXING = packed_pixel_array[curr_index*4+3]

        """unpack the colors"""
        color_0[1] = r_scale[(COLOR_0 & 63488) >> 11]
        color_0[2] = g_scale[(COLOR_0 & 2016) >> 5]
        color_0[3] = b_scale[COLOR_0 & 31]
        
        color_1[1] = r_scale[(COLOR_1 & 63488) >> 11]
        color_1[2] = g_scale[(COLOR_1 & 2016) >> 5]
        color_1[3] = b_scale[COLOR_1 & 31]

        color_2[1] = (color_0[1]*2 + color_1[1])//3
        color_2[2] = (color_0[2]*2 + color_1[2])//3
        color_2[3] = (color_0[3]*2 + color_1[3])//3
        colors[3] = [255,(color_0[1] + 2*color_1[1])//3,
                     (color_0[2] + 2*color_1[2])//3,
                     (color_0[3] + 2*color_1[3])//3]

        for i in range_16:
            color = colors[(INDEXING & DXT1_INDEXING_MASKS[i]) >> DXT1_INDEXING_BIT_SHIFTS[i]]
            upa[texel_pixel_mapping[i]+texel_offset+channel_0] = alpha_lookup[(ALPHA & alpha_masks[i]) >>
                                                                              alpha_bit_shifts[i]]
            upa[texel_pixel_mapping[i]+texel_offset+channel_1] = color[1]
            upa[texel_pixel_mapping[i]+texel_offset+channel_2] = color[2]
            upa[texel_pixel_mapping[i]+texel_offset+channel_3] = color[3]

    return unpacked_pixel_array



def unpack_dxt4_5(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT5 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    packed_pixel_array = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    unpacked_pixel_array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*width*height*self.unpacked_channel_count )
    upa = unpacked_pixel_array

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]
    
    alpha_masks = DXT5_ALPHA_MASKS
    alpha_bit_shifts = DXT5_ALPHA_BIT_SHIFTS
    alpha_lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    r_scale = DXT_R_SCALE
    g_scale = DXT_G_SCALE
    b_scale = DXT_B_SCALE
    
    channel_0 = self.channel_mapping.index(0)
    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    texel_pixel_mapping = get_texel_mapping(width, height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    texel_x_pixel_offsets = range(0, texel_width*16, 16)
    texel_y_pixel_offsets = range(0, texel_height*16*width, 16*width)
    
    #loop through each texel
    for curr_index in range(len(packed_pixel_array)//4):

        #get the offset to use
        texel_offset = (texel_x_pixel_offsets[curr_index%texel_width] +
                        texel_y_pixel_offsets[curr_index//texel_width])

        alpha_0 = alpha_lookup[0] = packed_pixel_array[curr_index*4]&255
        alpha_1 = alpha_lookup[1] = (packed_pixel_array[curr_index*4]&65280)>>8

        """depending on which alpha value is larger the indexing is calculated differently"""
        if alpha_0 > alpha_1:
            alpha_lookup[2] = (alpha_0*6 + alpha_1)//7
            alpha_lookup[3] = (alpha_0*5 + alpha_1*2)//7
            alpha_lookup[4] = (alpha_0*4 + alpha_1*3)//7
            alpha_lookup[5] = (alpha_0*3 + alpha_1*4)//7
            alpha_lookup[6] = (alpha_0*2 + alpha_1*5)//7
            alpha_lookup[7] = (alpha_0 + alpha_1*6)//7
        else:
            alpha_lookup[2] = (alpha_0*4 + alpha_1)//5
            alpha_lookup[3] = (alpha_0*3 + alpha_1*2)//5
            alpha_lookup[4] = (alpha_0*2 + alpha_1*3)//5
            alpha_lookup[5] = (alpha_0 + alpha_1*4)//5
            alpha_lookup[6] = 0
            alpha_lookup[7] = 255
        
        #half of the first array entry in DXT4/5 format is both
        #alpha values and the first third of the indexing
        ALPHA = (((packed_pixel_array[curr_index*4]&4294901760)>>16) +
                 (packed_pixel_array[curr_index*4+1]<<16))
        COLOR_0 = packed_pixel_array[curr_index*4+2] & 65535
        COLOR_1 = (packed_pixel_array[curr_index*4+2] & 4294901760) >> 16
        INDEXING = packed_pixel_array[curr_index*4+3]

        """unpack the colors"""
        color_0[1] = r_scale[(COLOR_0 & 63488) >> 11]
        color_0[2] = g_scale[(COLOR_0 & 2016) >> 5]
        color_0[3] = b_scale[COLOR_0 & 31]
        
        color_1[1] = r_scale[(COLOR_1 & 63488) >> 11]
        color_1[2] = g_scale[(COLOR_1 & 2016) >> 5]
        color_1[3] = b_scale[COLOR_1 & 31]

        color_2[1] = (color_0[1]*2 + color_1[1])//3
        color_2[2] = (color_0[2]*2 + color_1[2])//3
        color_2[3] = (color_0[3]*2 + color_1[3])//3
        colors[3] = [255,(color_0[1] + 2*color_1[1])//3,
                     (color_0[2] + 2*color_1[2])//3,
                     (color_0[3] + 2*color_1[3])//3]
            
        for i in range_16:
            color = colors[(INDEXING & DXT1_INDEXING_MASKS[i]) >> DXT1_INDEXING_BIT_SHIFTS[i]]
            upa[texel_pixel_mapping[i] + texel_offset+channel_0] = alpha_lookup[(ALPHA & alpha_masks[i]) >>
                                                                                alpha_bit_shifts[i]]
            upa[texel_pixel_mapping[i] + texel_offset+channel_1] = color[1]
            upa[texel_pixel_mapping[i] + texel_offset+channel_2] = color[2]
            upa[texel_pixel_mapping[i] + texel_offset+channel_3] = color[3]

    return unpacked_pixel_array



def unpack_dxn(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXN texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    packed_pixel_array = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    unpacked_pixel_array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*width*height*self.unpacked_channel_count )
    upa = unpacked_pixel_array
    
    dxn_masks = DXT5_ALPHA_MASKS
    dxn_bit_shifts = DXT5_ALPHA_BIT_SHIFTS
    red_lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])
    green_lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    r_scale = DXT_R_SCALE
    g_scale = DXT_G_SCALE
    b_scale = DXT_B_SCALE
    
    channel_0 = self.channel_mapping.index(0)
    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    texel_pixel_mapping = get_texel_mapping(width, height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    texel_x_pixel_offsets = range(0, texel_width*16, 16)
    texel_y_pixel_offsets = range(0, texel_height*16*width, 16*width)
    
    #loop through each texel
    for curr_index in range(len(packed_pixel_array)//4):

        #get the offset to use
        texel_offset = (texel_x_pixel_offsets[curr_index%texel_width] +
                        texel_y_pixel_offsets[curr_index//texel_width])

        r_index = texel_offset + channel_1
        g_index = texel_offset + channel_2
        b_index = texel_offset + channel_3

        red_0 = red_lookup[0] = packed_pixel_array[curr_index*4]&255
        red_1 = red_lookup[1] = (packed_pixel_array[curr_index*4]&65280)>>8
        red_indexing = (((packed_pixel_array[curr_index*4]&4294901760)>>16) +
                        (packed_pixel_array[curr_index*4+1]<<16))
        
        green_0 = green_lookup[0] = packed_pixel_array[curr_index*4+2]&255
        green_1 = green_lookup[1] = (packed_pixel_array[curr_index*4+2]&65280)>>8
        green_indexing = (((packed_pixel_array[curr_index*4+2]&4294901760)>>16) +
                          (packed_pixel_array[curr_index*4+3]<<16))

        """depending on which alpha value is larger the indexing is calculated differently"""
        if red_0 > red_1:
            red_lookup[2] = (red_0*6 + red_1)//7
            red_lookup[3] = (red_0*5 + red_1*2)//7
            red_lookup[4] = (red_0*4 + red_1*3)//7
            red_lookup[5] = (red_0*3 + red_1*4)//7
            red_lookup[6] = (red_0*2 + red_1*5)//7
            red_lookup[7] = (red_0 + red_1*6)//7
        else:
            red_lookup[2] = (red_0*4 + red_1)//5
            red_lookup[3] = (red_0*3 + red_1*2)//5
            red_lookup[4] = (red_0*2 + red_1*3)//5
            red_lookup[5] = (red_0 + red_1*4)//5
            red_lookup[6] = 0
            red_lookup[7] = 255
            
        if green_0 > green_1:
            green_lookup[2] = (green_0*6 + green_1)//7
            green_lookup[3] = (green_0*5 + green_1*2)//7
            green_lookup[4] = (green_0*4 + green_1*3)//7
            green_lookup[5] = (green_0*3 + green_1*4)//7
            green_lookup[6] = (green_0*2 + green_1*5)//7
            green_lookup[7] = (green_0 + green_1*6)//7
        else:
            green_lookup[2] = (green_0*4 + green_1)//5
            green_lookup[3] = (green_0*3 + green_1*2)//5
            green_lookup[4] = (green_0*2 + green_1*3)//5
            green_lookup[5] = (green_0 + green_1*4)//5
            green_lookup[6] = 0
            green_lookup[7] = 255
        
        for i in range_16:
            upa[texel_pixel_mapping[i]+r_index] = red_lookup[(red_indexing & dxn_masks[i]) >> dxn_bit_shifts[i]]
            upa[texel_pixel_mapping[i]+g_index] = green_lookup[(green_indexing & dxn_masks[i]) >> dxn_bit_shifts[i]]
            blue = (16129 - (127-upa[texel_pixel_mapping[i]+r_index])**2
                          - (127-upa[texel_pixel_mapping[i]+g_index])**2)
            
            if blue >= 16129:
                upa[texel_pixel_mapping[i]+b_index] = 255
            elif blue == 0:
                upa[texel_pixel_mapping[i]+b_index] = 128
            elif blue <= -16129:
                upa[texel_pixel_mapping[i]+b_index] = 0
            elif blue < 0:
                upa[texel_pixel_mapping[i]+b_index] = 127-int(sqrt(blue*-1))
            else:
                upa[texel_pixel_mapping[i]+b_index] = 127+int(sqrt(blue))
            
    return unpacked_pixel_array




def unpack_u8v8(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded U8V8 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    packed_pixel_array = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    unpacked_pixel_array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*width*height*self.unpacked_channel_count )
    upa = unpacked_pixel_array
    
    r_scale = self.channel_upscalers[1]
    g_scale = self.channel_upscalers[2]
    b_scale = self.channel_upscalers[3]
    
    red_i = self.channel_mapping.index(1)
    green_i = self.channel_mapping.index(2)
    blue_i = self.channel_mapping.index(3)

    r_max = r_scale[len(r_scale)-1]
    g_max = g_scale[len(g_scale)-1]

    for i in range(0, len(packed_pixel_array)*4, 4):
        upa[i+red_i] = (r_scale[packed_pixel_array[i//4]&255])*2&r_max
        upa[i+green_i] = (g_scale[(packed_pixel_array[i//4]&65280)>>8])*2&g_max
        blue = 16129 - (127-upa[i+red_i])**2 - (127-upa[i+green_i])**2
        
        if blue >= 16129:
            upa[i+blue_i] = b_scale[255]
        elif blue == 0:
            upa[i+blue_i] = b_scale[128]
        elif blue <= -16129:
            upa[i+blue_i] = 0
        elif blue < 0:
            upa[i+blue_i] = b_scale[127-int(sqrt(blue*-1))]
        else:
            upa[i+blue_i] = b_scale[127+int(sqrt(blue))]


    return unpacked_pixel_array
    



########################################
'''######## PACKING ROUTINES ########'''
########################################




def pack_dxt1(self, unpacked_pixel_array, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT1 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    dxt1_transparency = self.color_key_transparency
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    repacked_pixel_array = array("L", [0]*texel_width*texel_height*2 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixel_array = dxt_swizzler.swizzle_single_array(unpacked_pixel_array, True,
                                                                 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixel_array

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_pixel_channel_count = 4*get_texel_pixel_count(width, height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    furthest_colors = array("B", [0,0])
    dists = array("i", [0,0,0,0])

    color_0 = array("B", [0,0,0,0])
    color_1 = array("B", [0,0,0,0])
    color_2 = array("B", [0,0,0,0])
    color_3 = array("B", [0,0,0,0])

    include_transparency = False
    alpha_cutoff = self.one_bit_bias

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    range_pixels = range(0, texel_pixel_channel_count, 4)

    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))
    
    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 2):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//2)*texel_pixel_channel_count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in range_pixels:
            for j in pixel_comp_slices[i//4]:
                dists[1] = (((upa[pxl_i+1+i]-upa[pxl_i+1+j])**2)+
                                ((upa[pxl_i+2+i]-upa[pxl_i+2+j])**2)+
                                ((upa[pxl_i+3+i]-upa[pxl_i+3+j])**2))
                if dists[1] > dists[0]:
                    dists[0] = dists[1]
                    furthest_colors[0] = i
                    furthest_colors[1] = j

        #2: store furthest apart colors for use
        color_0[1] = upa[pxl_i+1+furthest_colors[0]]
        color_0[2] = upa[pxl_i+2+furthest_colors[0]]
        color_0[3] = upa[pxl_i+3+furthest_colors[0]]
        
        color_1[1] = upa[pxl_i+1+furthest_colors[1]]
        color_1[2] = upa[pxl_i+2+furthest_colors[1]]
        color_1[3] = upa[pxl_i+3+furthest_colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (r_scale[color_0[1]]<<11)+(g_scale[color_0[2]]<<5)+b_scale[color_0[3]]
        COLOR_1 = (r_scale[color_1[1]]<<11)+(g_scale[color_1[2]]<<5)+b_scale[color_1[3]]

        #4: figure out if we are using color key transparency for this pixel
        #by seeing if any of the alpha values are below the cutoff bias
        if dxt1_transparency:
            include_transparency = False
            for i in range_pixels:
                if upa[pxl_i+i] < alpha_cutoff:
                    include_transparency = True
                    break
            
        if COLOR_0 == COLOR_1 and not include_transparency:
            #do nothing except save one of the colors to the array
            rpa[txl_i] = COLOR_0
        else:
            #5: if the current color selection doesn't match what we want then
            #we reverse which color is which (if we are using transparency then
            #the first color as an integer must be smaller or equal to the second)
            if include_transparency == (COLOR_0 > COLOR_1):
                color_0, color_1 = color_1, color_0
                rpa[txl_i] = (COLOR_0<<16) + COLOR_1
            else:
                rpa[txl_i] = (COLOR_1<<16) + COLOR_0
        
            #6: calculate the intermediate colors
            """If the target format is DXT2/3/4/5 then no CK transparency will be used.
            CK mode will only be selected if both colors are the same. If both colors
            are the same then it is fine to run non-CK calculation on it since it will
            default to index zero. That is why the DXT3/5 calculation is in this part only"""
            if rpa[txl_i]&65535 > rpa[txl_i]>>16:
                color_2[1] = (color_0[1]*2+color_1[1])//3
                color_2[2] = (color_0[2]*2+color_1[2])//3
                color_2[3] = (color_0[3]*2+color_1[3])//3
                
                color_3[1] = (color_0[1]+color_1[1]*2)//3
                color_3[2] = (color_0[2]+color_1[2]*2)//3
                color_3[3] = (color_0[3]+color_1[3]*2)//3
                
                #7: calculate each pixel's closest match and assign it the proper index
                for i in range_pixels:
                    dists[0] = (((upa[pxl_i+1+i]-color_0[1])**2)+
                                ((upa[pxl_i+2+i]-color_0[2])**2)+
                                ((upa[pxl_i+3+i]-color_0[3])**2))
                    dists[1] = (((upa[pxl_i+1+i]-color_1[1])**2)+
                                ((upa[pxl_i+2+i]-color_1[2])**2)+
                                ((upa[pxl_i+3+i]-color_1[3])**2))
                    
                    #8: add appropriate indexing value to array
                    if dists[0] <= dists[1]: #closer to color 0
                        if (dists[0] > (((upa[pxl_i+1+i]-color_2[1])**2)+
                                        ((upa[pxl_i+2+i]-color_2[2])**2)+
                                        ((upa[pxl_i+3+i]-color_2[3])**2))): #closest to color 2
                            rpa[txl_i+1] += 2<<(i//2)
                    elif (dists[1] < (((upa[pxl_i+1+i]-color_3[1])**2)+
                                      ((upa[pxl_i+2+i]-color_3[2])**2)+
                                      ((upa[pxl_i+3+i]-color_3[3])**2))):
                        #closest to color 1
                        rpa[txl_i+1] += 1<<(i//2)
                    else: #closest to color 3
                        rpa[txl_i+1] += 3<<(i//2)
            else:
                color_2[1] = (color_0[1]+color_1[1])//2
                color_2[2] = (color_0[2]+color_1[2])//2
                color_2[3] = (color_0[3]+color_1[3])//2
                #here, color_3 represents zero color and fully transparent
                
                #7: calculate each pixel's closest match and assign it the proper index
                for i in range_pixels:
                    if upa[pxl_i+i] < alpha_cutoff:
                        rpa[txl_i+1] += 3<<(i//2)
                    else:
                        dists[0] = ((upa[pxl_i+1+i]-color_0[1])**2+
                                    (upa[pxl_i+2+i]-color_0[2])**2+
                                    (upa[pxl_i+3+i]-color_0[3])**2)
                        dists[1] = ((upa[pxl_i+1+i]-color_1[1])**2+
                                    (upa[pxl_i+2+i]-color_1[2])**2+
                                    (upa[pxl_i+3+i]-color_1[3])**2)

                        #8: add appropriate indexing value to array
                        if (dists[1] < dists[0] and
                           (dists[1] < ((upa[pxl_i+1+i]-color_2[1])**2+
                                        (upa[pxl_i+2+i]-color_2[2])**2+
                                        (upa[pxl_i+3+i]-color_2[3])**2))):
                            #closest to color 1
                            rpa[txl_i+1] += 1<<(i//2)
                        elif (dists[2] < dists[0] and
                               (dists[1] >= ((upa[pxl_i+1+i]-color_2[1])**2+
                                             (upa[pxl_i+2+i]-color_2[2])**2+
                                             (upa[pxl_i+3+i]-color_2[3])**2))):
                            #closest to color 2
                            rpa[txl_i+1] += 2<<(i//2)
            
    return repacked_pixel_array




def pack_dxt2_3(self, unpacked_pixel_array, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT2/3 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    repacked_pixel_array = array("L", [0]*texel_width*texel_height*4 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixel_array = dxt_swizzler.swizzle_single_array(unpacked_pixel_array, True,
                                                                 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixel_array

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_pixel_channel_count = 4*get_texel_pixel_count(width, height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    furthest_colors = array("B", [0,0])
    dists = array("i", [0,0,0,0])

    color_0 = array("B", [0,0,0,0])
    color_1 = array("B", [0,0,0,0])
    color_2 = array("B", [0,0,0,0])
    color_3 = array("B", [0,0,0,0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    range_pixels = range(0, texel_pixel_channel_count, 4)

    #these are split apart since the alpha for DXT3 is split into 2, 4byte ints in the array
    dxt3_range_pixels_0 = array("B", range_pixels[:8])
    dxt3_range_pixels_1 = array("B", range_pixels[8:])

    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))
    
    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 4):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//4)*texel_pixel_channel_count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in range_pixels:
            for j in pixel_comp_slices[i//4]:
                dists[1] = (((upa[pxl_i+1+i]-upa[pxl_i+1+j])**2)+
                            ((upa[pxl_i+2+i]-upa[pxl_i+2+j])**2)+
                            ((upa[pxl_i+3+i]-upa[pxl_i+3+j])**2))
                if dists[1] > dists[0]:
                    dists[0] = dists[1]
                    furthest_colors[0] = i
                    furthest_colors[1] = j

        #2: store furthest apart colors for use
        color_0[1] = upa[pxl_i+1+furthest_colors[0]]
        color_0[2] = upa[pxl_i+2+furthest_colors[0]]
        color_0[3] = upa[pxl_i+3+furthest_colors[0]]
        
        color_1[1] = upa[pxl_i+1+furthest_colors[1]]
        color_1[2] = upa[pxl_i+2+furthest_colors[1]]
        color_1[3] = upa[pxl_i+3+furthest_colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (r_scale[color_0[1]]<<11)+(g_scale[color_0[2]]<<5)+b_scale[color_0[3]]
        COLOR_1 = (r_scale[color_1[1]]<<11)+(g_scale[color_1[2]]<<5)+b_scale[color_1[3]]
        
        if COLOR_0 == COLOR_1:
            #do nothing except save one of the colors to the array
            rpa[txl_i+2] = COLOR_0
        else:
            #4: make sure the colors are properly ordered
            if COLOR_0 < COLOR_1:
                color_0, color_1 = color_1, color_0
                rpa[txl_i+2] = (COLOR_0<<16) + COLOR_1
            else: rpa[txl_i+2] = (COLOR_1<<16) + COLOR_0
        
            #5: calculate the intermediate colors
            color_2[1] = (color_0[1]*2+color_1[1])//3
            color_2[2] = (color_0[2]*2+color_1[2])//3
            color_2[3] = (color_0[3]*2+color_1[3])//3
            
            color_3[1] = (color_0[1]+color_1[1]*2)//3
            color_3[2] = (color_0[2]+color_1[2]*2)//3
            color_3[3] = (color_0[3]+color_1[3]*2)//3
            
            #6: calculate each pixel's closest match and assign it the proper index
            for i in range_pixels:
                dists[0] = (((upa[pxl_i+1+i]-color_0[1])**2)+
                                ((upa[pxl_i+2+i]-color_0[2])**2)+
                                ((upa[pxl_i+3+i]-color_0[3])**2))
                dists[1] = (((upa[pxl_i+1+i]-color_1[1])**2)+
                                ((upa[pxl_i+2+i]-color_1[2])**2)+
                                ((upa[pxl_i+3+i]-color_1[3])**2))
                
                #7: add appropriate indexing value to array
                if dists[0] <= dists[1]: #closer to color 0
                    if (dists[0] > (((upa[pxl_i+1+i]-color_2[1])**2)+
                                    ((upa[pxl_i+2+i]-color_2[2])**2)+
                                    ((upa[pxl_i+3+i]-color_2[3])**2))): #closest to color 2
                        rpa[txl_i+3] += 2<<(i//2)
                elif (dists[1] < (((upa[pxl_i+1+i]-color_3[1])**2)+
                                  ((upa[pxl_i+2+i]-color_3[2])**2)+
                                  ((upa[pxl_i+3+i]-color_3[3])**2))):
                    #closest to color 1
                    rpa[txl_i+3] += 1<<(i//2)
                else: #closest to color 3
                    rpa[txl_i+3] += 3<<(i//2)

        #8: calculate alpha channel for DXT 2/3/4/5
        for i in dxt3_range_pixels_0:
            rpa[txl_i] += a_scale[upa[pxl_i+i]]<<i
        for i in dxt3_range_pixels_1:
            rpa[txl_i+1] += a_scale[upa[pxl_i+i]]<<(i-32)
            
    return repacked_pixel_array





def pack_dxt4_5(self, unpacked_pixel_array, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT4/5 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    repacked_pixel_array = array("L", [0]*texel_width*texel_height*4 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixel_array = dxt_swizzler.swizzle_single_array(unpacked_pixel_array, True,
                                                                 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixel_array

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_pixel_channel_count = 4*get_texel_pixel_count(width, height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    furthest_colors = array("B", [0,0])
    dists = array("i", [0,0,0,0])

    color_0 = array("B", [0,0,0,0])
    color_1 = array("B", [0,0,0,0])
    color_2 = array("B", [0,0,0,0])
    color_3 = array("B", [0,0,0,0])
    
    dxt5_values = array("B", [0,0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    range_pixels = range(0, texel_pixel_channel_count, 4)

    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))
    
    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 4):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//4)*texel_pixel_channel_count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in range_pixels:
            for j in pixel_comp_slices[i//4]:
                dists[1] = (((upa[pxl_i+1+i]-upa[pxl_i+1+j])**2)+
                            ((upa[pxl_i+2+i]-upa[pxl_i+2+j])**2)+
                            ((upa[pxl_i+3+i]-upa[pxl_i+3+j])**2))
                if dists[1] > dists[0]:
                    dists[0] = dists[1]
                    furthest_colors[0] = i
                    furthest_colors[1] = j

        #2: store furthest apart colors for use
        color_0[1] = upa[pxl_i+1+furthest_colors[0]]
        color_0[2] = upa[pxl_i+2+furthest_colors[0]]
        color_0[3] = upa[pxl_i+3+furthest_colors[0]]
        
        color_1[1] = upa[pxl_i+1+furthest_colors[1]]
        color_1[2] = upa[pxl_i+2+furthest_colors[1]]
        color_1[3] = upa[pxl_i+3+furthest_colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (r_scale[color_0[1]]<<11)+(g_scale[color_0[2]]<<5)+b_scale[color_0[3]]
        COLOR_1 = (r_scale[color_1[1]]<<11)+(g_scale[color_1[2]]<<5)+b_scale[color_1[3]]
            
        if COLOR_0 == COLOR_1:
            #do nothing except save one of the colors to the array
            rpa[txl_i+2] = COLOR_0
        else:
            #4: make sure the colors are properly ordered
            if COLOR_0 < COLOR_1:
                color_0, color_1 = color_1, color_0
                rpa[txl_i+2] = (COLOR_0<<16) + COLOR_1
            else:
                rpa[txl_i+2] = (COLOR_1<<16) + COLOR_0
            
            #5: calculate the intermediate colors
            color_2[1] = (color_0[1]*2+color_1[1])//3
            color_2[2] = (color_0[2]*2+color_1[2])//3
            color_2[3] = (color_0[3]*2+color_1[3])//3
            
            color_3[1] = (color_0[1]+color_1[1]*2)//3
            color_3[2] = (color_0[2]+color_1[2]*2)//3
            color_3[3] = (color_0[3]+color_1[3]*2)//3
        
            #6: calculate each pixel's closest match and assign it the proper index
            for i in range_pixels:
                dists[0] = (((upa[pxl_i+1+i]-color_0[1])**2)+
                            ((upa[pxl_i+2+i]-color_0[2])**2)+
                            ((upa[pxl_i+3+i]-color_0[3])**2))
                dists[1] = (((upa[pxl_i+1+i]-color_1[1])**2)+
                            ((upa[pxl_i+2+i]-color_1[2])**2)+
                            ((upa[pxl_i+3+i]-color_1[3])**2))
                
                #7: add appropriate indexing value to array
                if dists[0] <= dists[1]: #closer to color 0
                    if (dists[0] > (((upa[pxl_i+1+i]-color_2[1])**2)+
                                    ((upa[pxl_i+2+i]-color_2[2])**2)+
                                    ((upa[pxl_i+3+i]-color_2[3])**2))):
                        #closest to color 2
                        rpa[txl_i+3] += 2<<(i//2)
                elif (dists[1] < (((upa[pxl_i+1+i]-color_3[1])**2)+
                                  ((upa[pxl_i+2+i]-color_3[2])**2)+
                                  ((upa[pxl_i+3+i]-color_3[3])**2))):
                    #closest to color 1
                    rpa[txl_i+3] += 1<<(i//2)
                else: #closest to color 3
                    rpa[txl_i+3] += 3<<(i//2)

        #8: find the most extreme values
        dxt5_values[0] = max(map(lambda i: upa[pxl_i+i], range_pixels))
        dxt5_values[1] = min(map(lambda i: upa[pxl_i+i], range_pixels))

        #reset the alpha data temp value
        dxt5_alpha_data = 0
        #9: if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if dxt5_values[0] != 0 or dxt5_values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""

            #if they are the same number then the indexing can stay at all zero
            if dxt5_values[0] != dxt5_values[1]:
                #10: calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    #0 = color_0                    1 = color_1
                    #2 = (6*color_0 + color_1)/7    3 = (5*color_0 + 2*color_1)/7
                    #4 = (4*color_0 + 3*color_1)/7  5 = (3*color_0 + 4*color_1)/7
                    #6 = (2*color_0 + 5*color_1)/7  7 = (color_0 + 6*color_1)/7

                    #calculate how far between both colors that the value is as a 0 to 7 int
                    dxt5_tmp_val = ( ((upa[pxl_i+i]-dxt5_values[1])*7 +
                                         ((dxt5_values[0]-dxt5_values[1])//2) )//
                                        (dxt5_values[0]-dxt5_values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if dxt5_tmp_val == 0:
                        dxt5_alpha_data += 1<<((i//4)*3 + 16)
                    elif dxt5_tmp_val < 7:
                        dxt5_alpha_data += (8-dxt5_tmp_val)<<((i//4)*3 + 16)
                
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
           
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in range_pixels:
                #store if lowest int so far
                if dxt5_values[0] > upa[pxl_i+i] and upa[pxl_i+i] > 0:
                    dxt5_values[0] = upa[pxl_i+i]
                    
                #store if greatest int so far
                if dxt5_values[1] < upa[pxl_i+i] and upa[pxl_i+i] < 255:
                    dxt5_values[1] = upa[pxl_i+i]

            #if they are the same number then the indexing can stay at all zero
            if dxt5_values[0] != dxt5_values[1]:
                #10: calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    #there are 4 interpolated colors in this mode
                    #0 =  color_0                   1 = color_1
                    #2 = (4*color_0 + color_1)/5    3 = (3*color_0 + 2*color_1)/5
                    #4 = (2*color_0 + 3*color_1)/5  5 = (color_0 + 4*color_1)/5
                    #6 =  0                         7 = 255

                    if upa[pxl_i+i] == 0:
                        #if the value is 0 we set it to index 6
                        dxt5_alpha_data += 6<<((i//4)*3 + 16)
                    elif upa[pxl_i+i] == 255:
                        #if the value is 255 we set it to index 7
                        dxt5_alpha_data += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        dxt5_tmp_val = ( ((upa[pxl_i+i]-dxt5_values[0])*5 +
                                       ((dxt5_values[1]-dxt5_values[0])//2) )//
                                        (dxt5_values[1]-dxt5_values[0])  )
                        if dxt5_tmp_val == 5:
                            dxt5_alpha_data += 1<<((i//4)*3 + 16)
                        elif dxt5_tmp_val > 0:
                            dxt5_alpha_data += (dxt5_tmp_val+1)<<((i//4)*3 + 16)
                      
        #11: store the calculated alpha data to the pixel array
        '''alpha indexing is pre-shifted left by 2 bytes and as such
        just needs to be masked and summed with the alpha values'''
        rpa[txl_i] = (dxt5_alpha_data&4294967295) + (dxt5_values[1]<<8) + dxt5_values[0]
        rpa[txl_i+1] = dxt5_alpha_data>>32
            
    return repacked_pixel_array




def pack_dxn(self, unpacked_pixel_array, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXN THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    
    repacked_pixel_array = array("L", [0]*texel_width*texel_height*4 )
    
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixel_array = dxt_swizzler.swizzle_single_array(unpacked_pixel_array, True, 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixel_array

    #calculate for the unpacked channels
    texel_pixel_channel_count = 4*get_texel_pixel_count(width, height)
    
    green_values = array("B", [0,0])    
    red_values = array("B", [0,0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    range_pixels = range(0, texel_pixel_channel_count, 4)

    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 4):
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//4)*texel_pixel_channel_count
        
        #8: find the most extreme values
        red_values[0] = max(map(lambda i: upa[pxl_i+1+i], range_pixels))
        red_values[1] = min(map(lambda i: upa[pxl_i+1+i], range_pixels))
        
        green_values[0] = max(map(lambda i: upa[pxl_i+2+i], range_pixels))
        green_values[1] = min(map(lambda i: upa[pxl_i+2+i], range_pixels))

        red_indexing = green_indexing = 0
        
        #if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if red_values[0] != 0 or red_values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""
            #if they are the same number then the indexing can stay at all zero
            if red_values[0] != red_values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    #calculate how far between both colors that the value is as a 0 to 7 int
                    tmp = ( ((upa[pxl_i+1+i]-red_values[1])*7 +
                              ((red_values[0]-red_values[1])//2) )//
                             (red_values[0]-red_values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if tmp == 0:
                        red_indexing += 1<<((i//4)*3 + 16)
                    elif tmp < 7:
                        red_indexing += (8-tmp)<<((i//4)*3 + 16)
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in range_pixels:
                #store if lowest int so far
                if red_values[0] > upa[pxl_i+1+i] and upa[pxl_i+1+i] > 0:
                    red_values[0] = upa[pxl_i+1+i]
                #store if greatest int so far
                if red_values[1] < upa[pxl_i+1+i] and upa[pxl_i+1+i] < 255:
                    red_values[1] = upa[pxl_i+1+i]

            #if they are the same number then the indexing can stay at all zero
            if red_values[0] != red_values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    
                    if upa[pxl_i+1+i] == 0:
                        red_indexing += 6<<((i//4)*3 + 16)
                    elif upa[pxl_i+1+i] == 255:
                        red_indexing += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        tmp = ( ((upa[pxl_i+1+i]-red_values[0])*5 +
                                  ((red_values[1]-red_values[0])//2) )//
                                 (red_values[1]-red_values[0])  )
                        if tmp == 5:
                            red_indexing += 1<<((i//4)*3 + 16)
                        elif tmp > 0:
                            red_indexing += (tmp+1)<<((i//4)*3 + 16)

        
        #if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if green_values[0] != 0 or green_values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""
            #if they are the same number then the indexing can stay at all zero
            if green_values[0] != green_values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    #calculate how far between both colors that the value is as a 0 to 7 int
                    tmp = ( ((upa[pxl_i+2+i]-green_values[1])*7 +
                              ((green_values[0]-green_values[1])//2) )//
                             (green_values[0]-green_values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if tmp == 0:
                        green_indexing += 1<<((i//4)*3 + 16)
                    elif tmp < 7:
                        green_indexing += (8-tmp)<<((i//4)*3 + 16)
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in range_pixels:
                #store if lowest int so far
                if green_values[0] > upa[pxl_i+2+i] and upa[pxl_i+2+i] > 0:
                    green_values[0] = upa[pxl_i+2+i]
                #store if greatest int so far
                if green_values[1] < upa[pxl_i+2+i] and upa[pxl_i+2+i] < 255:
                    green_values[1] = upa[pxl_i+2+i]

            #if they are the same number then the indexing can stay at all zero
            if green_values[0] != green_values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in range_pixels:
                    
                    if upa[pxl_i+2+i] == 0:
                        green_indexing += 6<<((i//4)*3 + 16)
                    elif upa[pxl_i+2+i] == 255:
                        green_indexing += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        tmp = ( ((upa[pxl_i+2+i]-green_values[0])*5 +
                                  ((green_values[1]-green_values[0])//2) )//
                                 (green_values[1]-green_values[0])  )
                        if tmp == 5:
                            green_indexing += 1<<((i//4)*3 + 16)
                        elif tmp > 0:
                            green_indexing += (tmp+1)<<((i//4)*3 + 16)
                      
        '''indexing is pre-shifted left by 2 bytes and as such
        just needs to be masked and summed with the channel values'''
        rpa[txl_i] = (red_indexing&4294967295)+(red_values[1]<<8)+red_values[0]
        rpa[txl_i+1] = red_indexing>>32
        rpa[txl_i+2] = (green_indexing&4294967295)+(green_values[1]<<8)+green_values[0]
        rpa[txl_i+3] = green_indexing>>32
            
    return repacked_pixel_array



def pack_u8v8(self, unpacked_pixel_array, width, height, depth=1):
    '''this function takes an unpacked texture and packs it to U8V8'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    if self.unpacked_channel_count < 1:
        print("ERROR: CANNOT CONVERT IMAGE WITHOUT RGB CHANNELS TO U8V8")
        return

    if self.unpacked_channel_count == 2:
        packed_array = array("h", bytes(unpacked_pixel_array))
    else:
        packed_array = array("h", [0]*(len(unpacked_pixel_array)//4))
        red_i   = self.channel_order.index("R")
        green_i = self.channel_order.index("G")
        
        for i in range(0, len(unpacked_pixel_array), 4):
            packed_array[i//4] = ( unpacked_pixel_array[i+red_i]+
                                  (unpacked_pixel_array[i+green_i]<<8))

    return packed_array



def get_texel_mapping(w, h):
    """when we are uncompressing a texture we need to make sure that
    we only read the number of pixels that the width*height SHOULD
    be. Texels are a minimum of 4x4 pixels, but if one is representing
    a 4x2, 4x1, 2x2, 2x1, or 1x1 then we need to restrict our reading
    of the texel to the dimensions it actually represents"""
    if h > 2:
        if w > 2:
            lst =(array("h", (0,   1,     2,     3,
                              w*1, 1+w*1, 2+w*1, 3+w*1,
                              w*2, 1+w*2, 2+w*2, 3+w*2,
                              w*3, 1+w*3, 2+w*3, 3+w*3) ))
        elif w == 2:
            lst =(array("B", (0,1,
                              2,3,
                              4,5,
                              6,7) ))
        elif w == 1:
            lst =(array("B", (0,
                              1,
                              2,
                              3) ))
    elif w > 2:
        if h == 2:
            lst =(array("h", (0, 1,   2,   3,
                              w, 1+w, 2+w, 3+w) ))
        elif h == 1:
            lst =array("B", (0,1,2,3) )
            
    elif w == 2 and h == 2:
        lst =(array("B", (0,1,
                          2,3) ))
    else:
        lst =array("B", (0,) )

    #because there are 4 channels per pixel we can speed things up a little by adjusting for that in here
    lst = array(lst.typecode, map(lambda x: x*4, lst))

    #the list needs to be 16 elements long, so however many are missing we append a
    #list of the array's last index value to it which is the length of 16-(list length)
    lst.extend( [lst[len(lst)-1]]*(16-len(lst)) )
        
    return lst


def get_texel_pixel_count(width, height):
    if width > 2:
        texel_pixel_count = 4
    else:
        texel_pixel_count = width
    if height > 2:
        texel_pixel_count *= 4
    else:
        texel_pixel_count *= height
    
    return texel_pixel_count
