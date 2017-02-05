
from array import array
from math import sqrt

#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
ab = None

def combine(main_dict, *dicts):        
    for dct in dicts:
        for key in dct:
            if key not in main_dict:
                main_dict[key] = dct[key]
            elif (isinstance(dct[key], dict) and
                  isinstance(main_dict[key], dict)):
                combine(main_dict[key], dct[key])
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
    ab.FORMAT_DXT5A = "DXT5A"
    ab.FORMAT_DXT5Y = "DXT5Y"           #NOT YET IMPLEMENTED
    ab.FORMAT_DXT5AY = "DXT5AY"         #NOT YET IMPLEMENTED
    
    ab.FORMAT_CTX1 = "CTX1"
    ab.FORMAT_U8V8 = "U8V8"

    dxt_specifications = {
        'compressed':True, 'dds_format':True,
        'min_width':4, 'min_height':4,
        'data_size':'L', 'channel_count':4,
        'channel_offsets':(0,11,5,0),
        'channel_masks':(0,63488,2016,31)}

    ab.define_format(**combine({
        'format_id':ab.FORMAT_DXT1, 'bpp':4,
        'channel_depths':(1,5,6,5),
        'unpacker':unpack_dxt1,
        'packer':pack_dxt1},
       dxt_specifications) )
    
    for FORMAT in (ab.FORMAT_DXT2, ab.FORMAT_DXT3):
        ab.define_format(**combine({
            'format_id':FORMAT, 'bpp':8,
            'channel_depths':(4,5,6,5),
            'unpacker':unpack_dxt2_3,
            'packer':pack_dxt2_3},
           dxt_specifications) )
        
    for FORMAT in (ab.FORMAT_DXT4, ab.FORMAT_DXT5):
        ab.define_format(**combine({
            'format_id':FORMAT, 'bpp':8,
            'channel_depths':(8,5,6,5),
            'unpacker':unpack_dxt4_5,
            'packer':pack_dxt4_5},
           dxt_specifications) )
        
    ab.define_format(**combine({
        'format_id':ab.FORMAT_DXN, 'bpp':8,
        'channel_depths':(0,8,8,8),
        'unpacker':unpack_dxn,
        'packer':pack_dxn,
        'channel_offsets':(0,16,8,0),
        'three_channels':True,
        'channel_masks':(0,16711680,65280,255)},
       dxt_specifications) )
        
    ab.define_format(**combine({
        'format_id':ab.FORMAT_DXT5A, 'bpp':8,
        'unpacker':unpack_dxt5_a_or_y,
        'packer':pack_dxt5_a,
        'channel_depths':(8,), 'channel_count':1,
        'channel_offsets':(0,),
        'channel_masks':(255,)},
       dxt_specifications) )
        
    '''ab.define_format(**combine({
        'format_id':ab.FORMAT_DXT5Y, 'bpp':8,
        'unpacker':unpack_dxt5_a_or_y,
        'packer':pack_dxt5_a_or_y,
        'channel_depths':(8,), 'channel_count':1,
        'channel_offsets':(0,),
        'channel_masks':(255,)},
       dxt_specifications) )'''
        
    ab.define_format(**combine({
        'format_id':ab.FORMAT_CTX1, 'bpp':4,
        'unpacker':unpack_ctx1,
        'packer':pack_ctx1,
        'channel_depths':(0,8,8,8),
        'channel_offsets':(0,16,8,0),
        'channel_masks':(0,16711680,65280,255)},
       dxt_specifications) )
    
    ab.define_format(format_id=ab.FORMAT_U8V8, bpp=16, channel_count=4,
                     unpacker=unpack_u8v8, packer=pack_u8v8,
                     channel_depths=(0,8,8,8),
                     dds_format=True, three_channels=True,
                     channel_offsets=(0,0,8,0), channel_masks=(0,255,65280,0))


#used to make dxt1 deciphering faster
DXT1_INDEXING_BIT_SHIFTS = range(0, 32, 2)

#used to make dxt3 deciphering faster
DXT3_ALPHA_BIT_SHIFTS = range(0, 64, 4)

#used to make dxt5 deciphering faster
DXT5_ALPHA_BIT_SHIFTS = range(0, 48, 3)

#used to scale DXT pixel values up to 8-bit
DXT_R_SCALE = array("B", [])
DXT_G_SCALE = array("B", [])
DXT_B_SCALE = array("B", [])

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
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO UNPACK DXT1 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))

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
    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = self.unpacked_channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    bytes_per_unpacked_pixel = self.unpacked_channel_count*unpacked_pixels.itemsize
    
    #loop through each texel
    for i in range(len(packed_pixels)//2):
        pixel_block_off = i*channels_per_texel
        
        """if the format DXT1 then the two entries in the array
        are the colors and the color indexing in that order."""
        COLOR_0 = packed_pixels[i*2] & 65535
        COLOR_1 = (packed_pixels[i*2] & 4294901760) >> 16
        INDEXING = packed_pixels[i*2+1]

        """unpack the colors"""
        color_0[1] = g_scale[(COLOR_0>>11) & 31]
        color_0[2] = g_scale[(COLOR_0>>5) & 63]
        color_0[3] = b_scale[(COLOR_0) & 31]

        color_1[1] = g_scale[(COLOR_1>>11) & 31]
        color_1[2] = g_scale[(COLOR_1>>5) & 63]
        color_1[3] = b_scale[(COLOR_1) & 31]

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
            
        for j in pixel_range:
            color = colors[(INDEXING >> DXT1_INDEXING_BIT_SHIFTS[j])&3]
            off = j*bytes_per_unpacked_pixel + pixel_block_off
            unpacked_pixels[off + channel_0] = color[0]
            unpacked_pixels[off + channel_1] = color[1]
            unpacked_pixels[off + channel_2] = color[2]
            unpacked_pixels[off + channel_3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 4, width, height)

    return unpacked_pixels


def unpack_dxt2_3(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO UNPACK DXT2/3 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp) )

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]

    alpha_bit_shifts = DXT3_ALPHA_BIT_SHIFTS
    alpha_lookup = self.channel_upscalers[0]

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
    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = self.unpacked_channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    bytes_per_unpacked_pixel = self.unpacked_channel_count*unpacked_pixels.itemsize
    
    #loop through each texel
    for i in range(len(packed_pixels)//4):
        pixel_block_off = i*channels_per_texel
        
        #DXT2/3 is much simpler than DXT4/5
        ALPHA = (packed_pixels[i*4+1]<<32) + packed_pixels[i*4]
        COLOR_0 = packed_pixels[i*4+2] & 65535
        COLOR_1 = (packed_pixels[i*4+2] & 4294901760) >> 16
        INDEXING = packed_pixels[i*4+3]

        """unpack the colors"""
        color_0[1] = g_scale[(COLOR_0>>11) & 31]
        color_0[2] = g_scale[(COLOR_0>>5) & 63]
        color_0[3] = b_scale[(COLOR_0) & 31]

        color_1[1] = g_scale[(COLOR_1>>11) & 31]
        color_1[2] = g_scale[(COLOR_1>>5) & 63]
        color_1[3] = b_scale[(COLOR_1) & 31]
            
        for j in pixel_range:
            color = colors[(INDEXING >> DXT1_INDEXING_BIT_SHIFTS[j])&3]
            off = j*bytes_per_unpacked_pixel + pixel_block_off

            unpacked_pixels[off + channel_0] = alpha_lookup[(ALPHA >> alpha_bit_shifts[j])&15]
            unpacked_pixels[off + channel_1] = color[1]
            unpacked_pixels[off + channel_2] = color[2]
            unpacked_pixels[off + channel_3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 4, width, height)

    return unpacked_pixels


def unpack_dxt4_5(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO UNPACK DXT4/5 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]

    alpha_bit_shifts = DXT5_ALPHA_BIT_SHIFTS
    alpha_lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

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
    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = self.unpacked_channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    bytes_per_unpacked_pixel = self.unpacked_channel_count*unpacked_pixels.itemsize
    
    #loop through each texel
    for i in range(len(packed_pixels)//4):
        pixel_block_off = i*channels_per_texel

        alpha_0 = alpha_lookup[0] = packed_pixels[i*4]&255
        alpha_1 = alpha_lookup[1] = (packed_pixels[i*4]&65280)>>8

        """depending on which alpha value is larger
        the indexing is calculated differently"""
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
        ALPHA = (((packed_pixels[i*4]&4294901760)>>16) +
                 (packed_pixels[i*4+1]<<16))
        COLOR_0 = packed_pixels[i*4+2] & 65535
        COLOR_1 = (packed_pixels[i*4+2] & 4294901760) >> 16
        INDEXING = packed_pixels[i*4+3]

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
            
        for j in pixel_range:
            color = colors[(INDEXING >> DXT1_INDEXING_BIT_SHIFTS[j])&3]
            off = j*bytes_per_unpacked_pixel + pixel_block_off

            unpacked_pixels[off + channel_0] = alpha_lookup[(ALPHA >> alpha_bit_shifts[j])&7]
            unpacked_pixels[off + channel_1] = color[1]
            unpacked_pixels[off + channel_2] = color[2]
            unpacked_pixels[off + channel_3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 4, width, height)

    return unpacked_pixels


def unpack_dxt5_a_or_y(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXT1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO UNPACK DXT5A/Y THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))

    alpha_bit_shifts = DXT5_ALPHA_BIT_SHIFTS
    alpha_lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    channel_0 = self.channel_mapping.index(0)

    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = self.unpacked_channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    bytes_per_unpacked_pixel = self.unpacked_channel_count*unpacked_pixels.itemsize
    
    #loop through each texel
    for i in range(len(packed_pixels)//2):
        pixel_block_off = i*channels_per_texel + channel_0

        alpha_0 = alpha_lookup[0] = packed_pixels[i*2]&255
        alpha_1 = alpha_lookup[1] = (packed_pixels[i*2]>>8)&255

        """depending on which alpha value is larger
        the indexing is calculated differently"""
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
        ALPHA = (((packed_pixels[i*2]&4294901760)>>16) +
                 (packed_pixels[i*2+1]<<16))
            
        for j in pixel_range:
            unpacked_pixels[j*bytes_per_unpacked_pixel+pixel_block_off] = alpha_lookup[
                (ALPHA >> alpha_bit_shifts[j])&7]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 1, width, height)

    return unpacked_pixels


def unpack_dxn(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded DXN texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))
    
    dxn_shifts = DXT5_ALPHA_BIT_SHIFTS
    red = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])
    green = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    r_scale = DXT_R_SCALE
    g_scale = DXT_G_SCALE
    b_scale = DXT_B_SCALE
    
    channel_0 = self.channel_mapping.index(0)
    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channel_count = self.unpacked_channel_count
    channels_per_texel = channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    
    #loop through each texel
    for i in range(0, len(packed_pixels), 4):
        j = (i//4)*channels_per_texel
        r_index = j + channel_1
        g_index = j + channel_2
        b_index = j + channel_3

        red_0 = red[0] = packed_pixels[i]&255
        red_1 = red[1] = (packed_pixels[i]>>8)&255
        red_idx = ((packed_pixels[i]>>16)&65535) + (packed_pixels[i+1]<<16)

        green_0 = green[0] = packed_pixels[i+2]&255
        green_1 = green[1] = (packed_pixels[i+2]>>8)&255
        green_idx = ((packed_pixels[i+2]>>16)&65535) + (packed_pixels[i+3]<<16)

        #depending on which alpha value is larger the indexing is calculated differently
        if red_0 > red_1:
            red[2] = (red_0*6 + red_1)//7
            red[3] = (red_0*5 + red_1*2)//7
            red[4] = (red_0*4 + red_1*3)//7
            red[5] = (red_0*3 + red_1*4)//7
            red[6] = (red_0*2 + red_1*5)//7
            red[7] = (red_0 + red_1*6)//7
        else:
            red[2] = (red_0*4 + red_1)//5
            red[3] = (red_0*3 + red_1*2)//5
            red[4] = (red_0*2 + red_1*3)//5
            red[5] = (red_0 + red_1*4)//5
            red[6] = 0
            red[7] = 255
            
        if green_0 > green_1:
            green[2] = (green_0*6 + green_1)//7
            green[3] = (green_0*5 + green_1*2)//7
            green[4] = (green_0*4 + green_1*3)//7
            green[5] = (green_0*3 + green_1*4)//7
            green[6] = (green_0*2 + green_1*5)//7
            green[7] = (green_0 + green_1*6)//7
        else:
            green[2] = (green_0*4 + green_1)//5
            green[3] = (green_0*3 + green_1*2)//5
            green[4] = (green_0*2 + green_1*3)//5
            green[5] = (green_0 + green_1*4)//5
            green[6] = 0
            green[7] = 255

        for k in pixel_range:
            shift = dxn_shifts[k]
            k *= channel_count
            x = r = red[(red_idx >> shift)&7]
            y = g = green[(green_idx >> shift)&7]

            # we're normalizing the coordinates here, not just unpacking them
            x = r&127 if r&128 else 127 - r
            y = g&127 if g&128 else 127 - g

            d = 16129 - x**2 - y**2  # 16129 == 127**2
            if d > 0:
                b = int(sqrt(d)) + 128
            else:
                n_len = sqrt(16129 - d)/127
                x = int(x/n_len)
                y = int(y/n_len)

                r = x+128 if r&128 else 127 - x
                g = y+128 if g&128 else 127 - y
                b = 128

            unpacked_pixels[k + r_index] = r
            unpacked_pixels[k + g_index] = g
            unpacked_pixels[k + b_index] = b

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 4, width, height)
    return unpacked_pixels


def unpack_ctx1(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded CTX1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT in (ab.FORMAT_A8R8G8B8, ab.FORMAT_R8G8B8):
        print("ERROR: TO UNPACK CTX1 THE UNPACK FORMAT MUST BE A8R8G8B8 OR R8G8B8")
        return
    
    packed_pixels = self.texture_block[bitmap_index]
    if packed_pixels.typecode != 'L':
        packed_pixels = array('L', bytes(packed_pixels))
        
    #create a new array to hold the pixels after we unpack them
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*self.unpacked_channel_count
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))

    #create the arrays to hold the color channel data
    color_0 = array(self._UNPACK_ARRAY_CODE, [0,0,0,0])
    color_1 = array(self._UNPACK_ARRAY_CODE, [0,0,0,0])
    color_2 = array(self._UNPACK_ARRAY_CODE, [0,0,0,0])
    color_3 = array(self._UNPACK_ARRAY_CODE, [0,0,0,0])

    #stores the colors in a way we can easily access them
    colors = [color_0, color_1, color_2, color_3]

    channel_1 = self.channel_mapping.index(1)
    channel_2 = self.channel_mapping.index(2)
    channel_3 = self.channel_mapping.index(3)

    r_scale = self.channel_upscalers[1]
    g_scale = self.channel_upscalers[2]
    b_scale = self.channel_upscalers[3]
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = self.unpacked_channel_count*pixels_per_texel
    pixel_range = range(pixels_per_texel)
    bytes_per_unpacked_pixel = self.unpacked_channel_count*unpacked_pixels.itemsize
    
    #loop through each texel
    for i in range(len(packed_pixels)//2):
        pixel_block_off = i*channels_per_texel
        
        """if the format DXT1 then the two entries in the array
        are the colors and the color indexing in that order."""
        COLORS = packed_pixels[i*2]
        INDEXING = packed_pixels[i*2+1]

        """unpack the colors"""
        color_0[1] = x0 = r0 = r_scale[(COLORS) & 255]
        color_0[2] = y0 = g0 = g_scale[(COLORS>>8) & 255]
        color_1[1] = x1 = r1 = r_scale[(COLORS>>16) & 255]
        color_1[2] = y1 = g1 = g_scale[(COLORS>>24) & 255]

        """calculate the z-components"""
        # we're normalizing the coordinates here, not just unpacking them
        x0 = x0&127 if x0&128 else 127 - x0
        y0 = y0&127 if y0&128 else 127 - y0
        x1 = x1&127 if x1&128 else 127 - x1
        y1 = y1&127 if y1&128 else 127 - y1

        d = 16129 - x0**2 - y0**2  # 16129 == 127**2
        if d > 0:
            b0 = int(sqrt(d)) + 128
        else:
            n_len = sqrt(16129 - d)/127
            x0 = int(x0/n_len)
            y0 = int(y0/n_len)

            r0 = x0+128 if r0&128 else 127 - x0
            g0 = y0+128 if g0&128 else 127 - y0

        d = 16129 - x1**2 - y1**2  # 16129 == 127**2
        if d > 0:
            b1 = int(sqrt(d)) + 128
        else:
            n_len = sqrt(16129 - d)/127
            x1 = int(x1/n_len)
            y1 = int(y1/n_len)

            r1 = x1+128 if r1&128 else 127 - x1
            g1 = y1+128 if g1&128 else 127 - y1

        # store the normalized colors
        color_0[1] = r0; color_1[1] = r1
        color_0[2] = g0; color_1[2] = g1
        color_0[3] = b0; color_1[3] = b1

        # calculate the in-between colors
        color_2[1] = (color_0[1]*2 + color_1[1])//3
        color_2[2] = (color_0[2]*2 + color_1[2])//3
        color_2[3] = (color_0[3]*2 + color_1[3])//3

        color_3[1] = (color_0[1] + color_1[1]*2)//3
        color_3[2] = (color_0[2] + color_1[2]*2)//3
        color_3[3] = (color_0[3] + color_1[3]*2)//3

        for j in pixel_range:
            color = colors[(INDEXING >> DXT1_INDEXING_BIT_SHIFTS[j])&3]
            off = j*bytes_per_unpacked_pixel + pixel_block_off
            unpacked_pixels[off + channel_1] = color[1]
            unpacked_pixels[off + channel_2] = color[2]
            unpacked_pixels[off + channel_3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter=self, mask_type="DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, False, 4, width, height)

    return unpacked_pixels


def unpack_u8v8(self, bitmap_index, width, height, depth=1):
    '''this function takes the loaded U8V8 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    packed_pixels = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    ucc = self.unpacked_channel_count
    bpp = ab.PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]*ucc
    unpacked_pixels = array(self._UNPACK_ARRAY_CODE, bytearray(width*height*bpp))
    
    r_scale = self.channel_upscalers[1]
    g_scale = self.channel_upscalers[2]
    b_scale = self.channel_upscalers[3]
    
    r_i = self.channel_mapping.index(1)
    g_i = self.channel_mapping.index(2)
    b_i = self.channel_mapping.index(3)

    for i in range(0, len(packed_pixels)):
        j = ucc*i
        x = r = r_scale[packed_pixels[i]&255]
        y = g = g_scale[(packed_pixels[i]>>8)&255]

        # we're normalizing the coordinates here, not just unpacking them
        x = x&127 if x&128 else 127 - x
        y = y&127 if y&128 else 127 - y

        d = 16129 - x**2 - y**2  # 16129 == 127**2
        if d > 0:
            b = int(sqrt(d)) + 128
        else:
            n_len = sqrt(16129 - d)/127
            x = int(x/n_len)
            y = int(y/n_len)

            r = x+128 if r&128 else 127 - x
            g = y+128 if g&128 else 127 - y
            b = 128

        unpacked_pixels[j+r_i] = r
        unpacked_pixels[j+g_i] = g
        unpacked_pixels[j+b_i] = b

    return unpacked_pixels



########################################
'''######## PACKING ROUTINES ########'''
########################################



def pack_dxt1(self, unpacked_pixels, width, height, depth=1):
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
    bpt = 8
    repacked_pixel_array = array("L", bytearray(texel_width*texel_height*bpt))

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, True, 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixels

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_channel_count = 4*get_texel_pixel_count(width, height)

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
    range_pixels = range(0, texel_channel_count, 4)

    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))
    
    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 2):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//2)*texel_channel_count
        
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


def pack_dxt2_3(self, unpacked_pixels, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT2/3 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    bpt = 16
    repacked_pixel_array = array("L", bytearray(texel_width*texel_height*bpt))

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, True, 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixels

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_channel_count = 4*get_texel_pixel_count(width, height)

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
    range_pixels = range(0, texel_channel_count, 4)

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
        pxl_i = (txl_i//4)*texel_channel_count
        
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



def pack_dxt4_5():
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT4/5 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    bpt = 16
    repacked_pixel_array = array("L", bytearray(texel_width*texel_height*bpt))

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, True, 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixels

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers

    #calculate for the unpacked channels
    texel_channel_count = 4*get_texel_pixel_count(width, height)

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
    range_pixels = range(0, texel_channel_count, 4)

    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))
    
    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 4):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//4)*texel_channel_count
        
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


def pack_dxt5_a(self, unpacked_pixels, width, height, depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == ab.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT5A/Y THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    bpt = 8
    ucc = self.unpacked_channel_count
    repacked_pixel_array = array("L", bytearray(texel_width*texel_height*bpt))

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, True, ucc, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixels

    scale = self.channel_downscalers[0]

    texel_channel_count = ucc*get_texel_pixel_count(width, height)
    range_pixels = range(0, texel_channel_count, ucc)

    values = array("B", [0,0])

    #loop for each texel
    for i in range(0, len(repacked_pixel_array), 2):
        #cache so it doesn't have to keep being calculated
        pxl_i = (i//2)*texel_channel_count
        values[0] = 0
        values[1] = 255

        #8: find the most extreme values
        for j in range_pixels:
            val = upa[pxl_i+j]
            values[0] = max(values[0], val)
            values[1] = min(values[1], val)

        #reset the alpha data temp value
        alpha_data = 0
        # if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if values[0] != 0 or values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""

            #if they are the same number then the indexing can stay at all zero
            if values[0] != values[1]:
                # calculate and store which interpolated index each alpha value is closest to
                for j in range_pixels:
                    tmp_val = ( ((upa[pxl_i+j]-values[1])*7 +
                                ((values[0]-values[1])//2))//
                                 (values[0]-values[1]))
                    """Because the colors are stored in reverse
                    order, we need to invert the index"""
                    if tmp_val == 0:
                        alpha_data += 1<<((j//4)*3 + 16)
                    elif tmp_val < 7:
                        alpha_data += (8-tmp_val)<<((j//4)*3 + 16)
                
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for j in range_pixels:
                if values[0] > upa[pxl_i+j] and upa[pxl_i+j] > 0:
                    values[0] = upa[pxl_i+j]

                if values[1] < upa[pxl_i+j] and upa[pxl_i+j] < 255:
                    values[1] = upa[pxl_i+j]

            #if they are the same number then the indexing can stay at all zero
            if values[0] != values[1]:
                # calculate and store which interpolated
                # index each alpha value is closest to
                for j in range_pixels:
                    if upa[pxl_i+j] == 0:
                        alpha_data += 6<<((j//4)*3 + 16)
                    elif upa[pxl_i+j] == 255:
                        alpha_data += 7<<((j//4)*3 + 16)
                    else:
                        tmp_val = ( ((upa[pxl_i+j]-values[0])*5 +
                                       ((values[1]-values[0])//2) )//
                                        (values[1]-values[0])  )
                        if tmp_val == 5:
                            alpha_data += 1<<((j//4)*3 + 16)
                        elif tmp_val > 0:
                            alpha_data += (tmp_val+1)<<((j//4)*3 + 16)
                      
        # store the calculated alpha data to the pixel array
        '''alpha indexing is pre-shifted left by 2 bytes and as such
        just needs to be masked and summed with the alpha values'''
        rpa[i] = (alpha_data&4294967295) + (values[1]<<8) + values[0]
        rpa[i+1] = alpha_data>>32
            
    return repacked_pixel_array


def pack_dxn(self, unpacked_pixels, width, height, depth=1):
    raise NotImplementedError


def pack_ctx1():
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    if not self._UNPACK_FORMAT in ab.FORMAT_A8R8G8B8:
        print("ERROR: TO UNPACK CTX1 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return

    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #create a new array to hold the texels after we repack them
    bpt = 8
    repacked_pixel_array = array("L", bytearray(texel_width*texel_height*bpt))

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(
            texture_converter = self, mask_type = "DXT_CALC")
        unpacked_pixels = dxt_swizzler.swizzle_single_array(
            unpacked_pixels, True, 4, width, height)

    #shorthand names
    rpa = repacked_pixel_array
    upa = unpacked_pixels

    _, r_scale, g_scale, __ = self.channel_downscalers
    texel_channel_count = 4*get_texel_pixel_count(width, height)
    furthest_colors = array("B", [0,0])
    dists = array("i", [0,0])

    color_0 = array("B", [0,0])
    color_1 = array("B", [0,0])
    color_2 = array("B", [0,0])
    color_3 = array("B", [0,0])

    range_pixels = range(0, texel_channel_count, 4)
    pixel_comp_slices = list(map(lambda x: range_pixels[x//4+1:], range_pixels))

    #loop for each texel
    for txl_i in range(0, len(repacked_pixel_array), 2):
        furthest_colors[0] = 0
        furthest_colors[1] = 0
        dists[0] = -1

        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//2)*texel_channel_count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in range_pixels:
            for j in pixel_comp_slices[i//4]:
                dists[1] = (((upa[pxl_i+1+i]-upa[pxl_i+1+j])**2)+
                            ((upa[pxl_i+2+i]-upa[pxl_i+2+j])**2))
                if dists[1] > dists[0]:
                    dists[0] = dists[1]
                    furthest_colors[0] = i
                    furthest_colors[1] = j

        #2: store furthest apart colors for use
        color_0[0] = upa[pxl_i+1+furthest_colors[0]]
        color_0[1] = upa[pxl_i+2+furthest_colors[0]]
        
        color_1[0] = upa[pxl_i+1+furthest_colors[1]]
        color_1[1] = upa[pxl_i+2+furthest_colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = color_0[0] + (color_1[0]<<8)
        COLOR_1 = color_0[1] + (color_1[1]<<8)
            
        if COLOR_0 == COLOR_1:
            #do nothing except save one of the colors to the array
            rpa[txl_i] = COLOR_0
        else:
            rpa[txl_i] = COLOR_0 + (COLOR_1<<16)

            #6: calculate the intermediate colors
            color_2[0] = (color_0[1]*2+color_1[1])//3
            color_2[1] = (color_0[2]*2+color_1[2])//3
            
            color_3[0] = (color_0[1]+color_1[1]*2)//3
            color_3[1] = (color_0[2]+color_1[2]*2)//3
            
            #7: calculate each pixel's closest match and assign it the proper index
            for i in range_pixels:
                dists[0] = (((upa[pxl_i+1+i]-color_0[0])**2)+
                            ((upa[pxl_i+2+i]-color_0[1])**2))
                dists[1] = (((upa[pxl_i+1+i]-color_1[0])**2)+
                            ((upa[pxl_i+2+i]-color_1[1])**2))
                
                #8: add appropriate indexing value to array
                if dists[0] <= dists[1]: #closer to color 0
                    if (dists[0] > (((upa[pxl_i+1+i]-color_2[0])**2)+
                                    ((upa[pxl_i+2+i]-color_2[1])**2))): #closest to color 2
                        rpa[txl_i+1] += 2<<(i//2)
                elif (dists[1] < (((upa[pxl_i+1+i]-color_3[0])**2)+
                                  ((upa[pxl_i+2+i]-color_3[1])**2))):
                    #closest to color 1
                    rpa[txl_i+1] += 1<<(i//2)
                else: #closest to color 3
                    rpa[txl_i+1] += 3<<(i//2)
            
    return repacked_pixel_array


def pack_u8v8(self, unpacked_pixels, width, height, depth=1):
    '''this function takes an unpacked texture and packs it to U8V8'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    ucc = self.unpacked_channel_count
    if ucc < 2:
        raise TypeError("Cannot convert image with less than 2 channels to U8V8.")

    packed_array = array("H", bytearray(2*len(unpacked_pixels)//ucc))
    for i in range(0, len(unpacked_pixels), ucc):
        packed_array[i//ucc] = unpacked_pixels[i+1] + (unpacked_pixels[i+2]<<8)

    return packed_array


def get_texel_pixel_count(width, height):
    return min(width, 4) * min(height, 4)
