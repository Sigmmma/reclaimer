
from array import array
from math import sqrt

#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
ab = None

try:
    try:
        from .ext import dds_defs_ext
    except Exception:
        from ext import dds_defs_ext
    fast_dds_defs = True
except Exception:
    fast_dds_defs = False


def combine(base, **main):
    for k, v in [(k, base[k]) for k in base if k not in main]:
        main[k] = v
    return main


def get_texel_pixel_count(width, height):
    return min(width, 4) * min(height, 4)


def initialize():
    """FOR DXT FORMATS, ALPHA CHANNELS ARE TREATED SPECIALLY,
    BUT ARE EXPLICITELY PLACED HERE TO MAKE SURE THEY DONT
    CAUSE THE CHANNEL MAP SWAPPING PROBLEMS"""
    
    ab.FORMAT_DXT1 = "DXT1"
    ab.FORMAT_DXT2 = "DXT2"
    ab.FORMAT_DXT3 = "DXT3"
    ab.FORMAT_DXT4 = "DXT4"
    ab.FORMAT_DXT5 = "DXT5"

    # uses only the alpha channel of dxt3
    ab.FORMAT_DXT3A = "DXT3A"           #NOT YET IMPLEMENTED

    # uses only the alpha channel of dxt3, and each bit is
    # used as an on/off mask for each of the ARGB channels.
    # this format is basically A1R1G1B1 with a dxt texel swizzle
    ab.FORMAT_DXT3A1111 = "DXT3A1111"   #NOT YET IMPLEMENTED
    
    ab.FORMAT_DXT5NM = "DXT5NM"         #NOT YET IMPLEMENTED
    ab.FORMAT_DXN = "DXN"
    ab.FORMAT_DXT5A = "DXT5A"
    ab.FORMAT_DXT5Y = "DXT5Y"
    ab.FORMAT_DXT5AY = "DXT5AY"
    
    ab.FORMAT_CTX1 = "CTX1"
    ab.FORMAT_U8V8 = "U8V8"

    dxt_specs = {
        'compressed':True, 'dds_format':True,
        'min_width':4, 'min_height':4,
        'packed_typecode':'L', 'channel_count':4,
        'offsets':(0,11,5,0),
        'masks':(0,63488,2016,31)}

    ab.define_format(**combine(dxt_specs,
        format_id=ab.FORMAT_DXT1, bpp=4, depths=(1,5,6,5),
        unpacker=unpack_dxt1, packer=pack_dxt1))

    for fmt in (ab.FORMAT_DXT2, ab.FORMAT_DXT3):
        ab.define_format(**combine(dxt_specs,
            format_id=fmt, bpp=8, depths=(4,5,6,5),
            unpacker=unpack_dxt2_3, packer=pack_dxt2_3))

    for fmt in (ab.FORMAT_DXT4, ab.FORMAT_DXT5):
        ab.define_format(**combine(dxt_specs,
            format_id=fmt, bpp=8, depths=(8,5,6,5),
            unpacker=unpack_dxt4_5, packer=pack_dxt4_5))

    for fmt in (ab.FORMAT_DXT5A, ab.FORMAT_DXT5Y):
        ab.define_format(**combine(dxt_specs,
            format_id=fmt, bpp=4, unpacker=unpack_dxt5a, packer=pack_dxt5a,
            depths=(8,), offsets=(0,), channel_count=1, masks=(255,)))

    ab.define_format(**combine(dxt_specs,
        format_id=ab.FORMAT_DXT5AY, bpp=8,
        unpacker=unpack_dxt5a, packer=pack_dxt5a,
        depths=(8,8), offsets=(8,0),
        channel_count=2, masks=(65280,255)))

    ab.define_format(**combine(dxt_specs,
        format_id=ab.FORMAT_DXN, bpp=8, three_channels=True,
        depths=(0,8,8,8), offsets=(0,16,8,0),
        unpacker=unpack_dxn, packer=pack_dxn,
        masks=(0,16711680,65280,255)))

    ab.define_format(**combine(dxt_specs,
        format_id=ab.FORMAT_CTX1, bpp=4, three_channels=True,
        unpacker=unpack_ctx1, packer=pack_ctx1,
        depths=(0,8,8,8), offsets=(0,16,8,0),
        masks=(0,16711680,65280,255)))

    ab.define_format(
        format_id=ab.FORMAT_U8V8, bpp=16,
        channel_count=4, dds_format=True, three_channels=True,
        unpacker=unpack_u8v8, packer=pack_u8v8,
        depths=(0,8,8,8), offsets=(0,0,8,0), masks=(0,255,65280,0))


def unpack_dxt1(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1

    ucc = self.unpacked_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    try:
        chan0 = self.channel_mapping.index(0)
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack DXT texture. Channel mapping must include " +
              "channels 0, 1, 2, and 3, not %s" % self.channel_mapping)
    a_scale = self.channel_upscalers[chan0]
    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    b_scale = self.channel_upscalers[chan3]

    if fast_dds_defs:
        dds_defs_ext.unpack_dxt1(
            unpacked, packed, r_scale, g_scale, b_scale,
            pixels_per_texel, chan0, chan1, chan2, chan3, unpack_max)
    else:
        channels_per_texel = ucc*pixels_per_texel
        pixel_indices = range(pixels_per_texel)

        #create the arrays to hold the color channel data
        c_0 = [unpack_max,0,0,0]
        c_1 = [unpack_max,0,0,0]
        c_2 = [unpack_max,0,0,0]
        c_3 = [unpack_max,0,0,0]
        transparent = [0,0,0,0]

        #stores the colors in a way we can easily access them
        colors = [c_0, c_1, c_2, c_3]

        #loop through each texel
        for i in range(len(packed)//2):
            pxl_i = i*channels_per_texel
            j = i*2
            
            """if the format DXT1 then the two entries in the array
            are the colors and the color indexing in that order."""
            color0 = packed[j] & 65535
            color1 = (packed[j] >> 16) & 65535
            color_idx = packed[j+1]

            """unpack the colors"""
            c_0[1] = r_scale[(color0>>11) & 31]
            c_0[2] = g_scale[(color0>>5) & 63]
            c_0[3] = b_scale[(color0) & 31]

            c_1[1] = r_scale[(color1>>11) & 31]
            c_1[2] = g_scale[(color1>>5) & 63]
            c_1[3] = b_scale[(color1) & 31]

            #if the first color is a larger integer
            #then color key transparency is NOT used
            if color0 > color1:
                c_2[1] = (c_0[1]*2 + c_1[1])//3
                c_2[2] = (c_0[2]*2 + c_1[2])//3
                c_2[3] = (c_0[3]*2 + c_1[3])//3
                colors[3] = [
                    unpack_max,
                    (c_0[1] + 2*c_1[1])//3,
                    (c_0[2] + 2*c_1[2])//3,
                    (c_0[3] + 2*c_1[3])//3]
            else:
                c_2[1] = (c_0[1]+c_1[1])//2
                c_2[2] = (c_0[2]+c_1[2])//2
                c_2[3] = (c_0[3]+c_1[3])//2
                colors[3] = transparent
                
            for j in pixel_indices:
                color = colors[(color_idx >> (j*2))&3]
                off = j*ucc + pxl_i
                unpacked[off + chan0] = color[0]
                unpacked[off + chan1] = color[1]
                unpacked[off + chan2] = color[2]
                unpacked[off + chan3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, ucc, width, height)

    return unpacked


def unpack_dxt2_3(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1

    ucc = self.unpacked_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = ucc*pixels_per_texel

    pixel_indices = range(pixels_per_texel)

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    #create the arrays to hold the color channel data
    c_0 = [unpack_max,0,0,0]
    c_1 = [unpack_max,0,0,0]
    c_2 = [unpack_max,0,0,0]
    c_3 = [unpack_max,0,0,0]

    #stores the colors in a way we can easily access them
    colors = [c_0, c_1, c_2, c_3]

    try:
        chan0 = self.channel_mapping.index(0)
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack DXT texture. Channel mapping must include " +
              "channels 0, 1, 2, and 3, not %s" % self.channel_mapping)
    a_scale = self.channel_upscalers[chan0]
    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    b_scale = self.channel_upscalers[chan3]

    if fast_dds_defs:
        dds_defs_ext.unpack_dxt2_3(
            unpacked, packed, a_scale, r_scale, g_scale, b_scale,
            pixels_per_texel, chan0, chan1, chan2, chan3)
    else:
        #loop through each texel
        for i in range(len(packed)//4):
            pxl_i = i*channels_per_texel
            j = i*4
            
            #DXT2/3 is much simpler than DXT4/5
            alpha = (packed[j+1]<<32) + packed[j]
            color0 = packed[j+2] & 65535
            color1 = (packed[j+2] >> 16) & 65535
            color_idx = packed[j+3]

            """unpack the colors"""
            c_0[1] = r_scale[(color0>>11) & 31]
            c_0[2] = g_scale[(color0>>5) & 63]
            c_0[3] = b_scale[(color0) & 31]

            c_1[1] = r_scale[(color1>>11) & 31]
            c_1[2] = g_scale[(color1>>5) & 63]
            c_1[3] = b_scale[(color1) & 31]

            if color0 < color1:
                color0, color1 = color1, color0

            c_2[1] = (c_0[1]*2 + c_1[1])//3
            c_2[2] = (c_0[2]*2 + c_1[2])//3
            c_2[3] = (c_0[3]*2 + c_1[3])//3

            c_3[1] = (c_0[1] + c_1[1]*2)//3
            c_3[2] = (c_0[2] + c_1[2]*2)//3
            c_3[3] = (c_0[3] + c_1[3]*2)//3
                
            for j in pixel_indices:
                color = colors[(color_idx >> (j*2))&3]
                off = j*ucc + pxl_i

                unpacked[off + chan0] = a_scale[(alpha >> (j*4))&15]
                unpacked[off + chan1] = color[1]
                unpacked[off + chan2] = color[2]
                unpacked[off + chan3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, ucc, width, height)

    return unpacked


def unpack_dxt4_5(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1

    ucc = self.unpacked_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = ucc*pixels_per_texel

    pixel_indices = range(pixels_per_texel)

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    #create the arrays to hold the color channel data
    c_0 = [unpack_max,0,0,0]
    c_1 = [unpack_max,0,0,0]
    c_2 = [unpack_max,0,0,0]
    c_3 = [unpack_max,0,0,0]

    #stores the colors in a way we can easily access them
    colors = [c_0, c_1, c_2, c_3]

    a_lookup = [0,0,0,0,0,0,0,0]

    try:
        chan0 = self.channel_mapping.index(0)
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack DXT texture. Channel mapping must include " +
              "channels 0, 1, 2, and 3, not %s" % self.channel_mapping)

    a_scale = self.channel_upscalers[chan0]
    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    b_scale = self.channel_upscalers[chan3]

    if fast_dds_defs:
        dds_defs_ext.unpack_dxt4_5(
            unpacked, packed, a_scale, r_scale, g_scale, b_scale,
            pixels_per_texel, chan0, chan1, chan2, chan3)
    else:
        #loop through each texel
        for i in range(len(packed)//4):
            pxl_i = i*channels_per_texel
            j = i*4

            a_lookup[0] = alpha0 = a_scale[packed[j] & 255]
            a_lookup[1] = alpha1 = a_scale[(packed[j] >> 8) & 255]
            a_idx = ((packed[j]>>16) & 65535) + (packed[j+1] << 16)

            """depending on which value is larger
            the indexing is calculated differently"""
            if alpha0 > alpha1:
                a_lookup[2] = (alpha0*6 + alpha1)//7
                a_lookup[3] = (alpha0*5 + alpha1*2)//7
                a_lookup[4] = (alpha0*4 + alpha1*3)//7
                a_lookup[5] = (alpha0*3 + alpha1*4)//7
                a_lookup[6] = (alpha0*2 + alpha1*5)//7
                a_lookup[7] = (alpha0   + alpha1*6)//7
            else:
                a_lookup[2] = (alpha0*4 + alpha1)//5
                a_lookup[3] = (alpha0*3 + alpha1*2)//5
                a_lookup[4] = (alpha0*2 + alpha1*3)//5
                a_lookup[5] = (alpha0   + alpha1*4)//5
                a_lookup[6] = 0
                a_lookup[7] = 255
            
            #half of the first array entry in DXT4/5 format is both
            #alpha values and the first third of the indexing
            color0 = packed[j+2] & 65535
            color1 = (packed[j+2]>>16) & 65535
            color_idx = packed[j+3]

            """unpack the colors"""
            c_0[1] = r_scale[(color0>>11) & 31]
            c_0[2] = g_scale[(color0>>5) & 63]
            c_0[3] = b_scale[(color0) & 31]

            c_1[1] = r_scale[(color1>>11) & 31]
            c_1[2] = g_scale[(color1>>5) & 63]
            c_1[3] = b_scale[(color1) & 31]

            if color0 < color1:
                color0, color1 = color1, color0

            c_2[1] = (c_0[1]*2 + c_1[1])//3
            c_2[2] = (c_0[2]*2 + c_1[2])//3
            c_2[3] = (c_0[3]*2 + c_1[3])//3

            c_3[1] = (c_0[1] + c_1[1]*2)//3
            c_3[2] = (c_0[2] + c_1[2]*2)//3
            c_3[3] = (c_0[3] + c_1[3]*2)//3
                
            for j in pixel_indices:
                color = colors[(color_idx >> (j*2))&3]
                off = j*ucc + pxl_i

                unpacked[off + chan0] = a_lookup[(a_idx >> (j*3))&7]
                unpacked[off + chan1] = color[1]
                unpacked[off + chan2] = color[2]
                unpacked[off + chan3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, ucc, width, height)

    return unpacked


def unpack_dxt5a(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1

    ucc = self.unpacked_channel_count
    scc = self.source_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = ucc*pixels_per_texel

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    # we expect up to 4 channels cna exist, so we put some
    # placeholder arrays in just in case we dont use them all
    scales = [array(unpack_code)]*4
    chans  = [0]*4

    # invert the channel mapping since thats how we'll need to use it
    assert ucc == scc
    channel_map = self.channel_mapping
    for i in range(ucc):
        chan = channel_map[i]
        scales[i] = self.channel_upscalers[chan]
        chans[chan] = i
    
    if fast_dds_defs:
        dds_defs_ext.unpack_dxt5a(
            unpacked, packed, scales[0], scales[1], scales[2], scales[3],
            ucc, pixels_per_texel, chans[0], chans[1], chans[2], chans[3])
    else:
        lookup = [0,0,0,0,0,0,0,0]
        pixel_indices = range(pixels_per_texel)

        #loop through each texel
        for i in range(len(packed)//2):
            chan = chans[i%ucc]
            pxl_i = (i//scc)*channels_per_texel + chan
            scale = scales[chan]
            j = i*2

            lookup[0] = val0 = scale[packed[j] & 255]
            lookup[1] = val1 = scale[(packed[j] >> 8) & 255]
            idx = ((packed[j]>>16) & 65535) + (packed[j+1] << 16)

            """depending on which value is larger
            the indexing is calculated differently"""
            if val0 > val1:
                lookup[2] = (val0*6 + val1)//7
                lookup[3] = (val0*5 + val1*2)//7
                lookup[4] = (val0*4 + val1*3)//7
                lookup[5] = (val0*3 + val1*4)//7
                lookup[6] = (val0*2 + val1*5)//7
                lookup[7] = (val0   + val1*6)//7
            else:
                lookup[2] = (val0*4 + val1)//5
                lookup[3] = (val0*3 + val1*2)//5
                lookup[4] = (val0*2 + val1*3)//5
                lookup[5] = (val0   + val1*4)//5
                lookup[6] = scale[0]
                lookup[7] = scale[255]
                
            for k in pixel_indices:
                unpacked[k*ucc + pxl_i] = lookup[(idx >> (k*3))&7]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, ucc, width, height)

    return unpacked


def unpack_dxn(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1
    mask = (unpack_max+1)//2 - 1
    mask_sq = mask**2

    ucc = self.unpacked_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = ucc*pixels_per_texel

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    try:
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack DXN texture. Channel mapping must include " +
              "channels 1, 2, and 3, not %s" % self.channel_mapping)
    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    b_scale = self.channel_upscalers[chan3]

    if fast_dds_defs:
        dds_defs_ext.unpack_dxn(
            unpacked, packed, r_scale, g_scale,
            ucc, pixels_per_texel, chan1, chan2, chan3)
    else:
        pixel_indices = range(pixels_per_texel)
        red   = [0,0,0,0,0,0,0,0]
        green = [0,0,0,0,0,0,0,0]

        #loop through each texel
        for i in range(len(packed)//4):
            pxl_i = i*channels_per_texel
            j = i*4
            r_index = pxl_i + chan1
            g_index = pxl_i + chan2
            b_index = pxl_i + chan3

            red0 = red[0] = r_scale[packed[j]&255]
            red1 = red[1] = r_scale[(packed[j]>>8)&255]
            red_idx = ((packed[j]>>16)&65535) + (packed[j+1]<<16)

            green0 = green[0] = g_scale[packed[j+2]&255]
            green1 = green[1] = g_scale[(packed[j+2]>>8)&255]
            green_idx = ((packed[j+2]>>16)&65535) + (packed[j+3]<<16)

            #depending on which alpha value is larger
            #the indexing is calculated differently
            if red0 > red1:
                red[2] = (red0*6 + red1)//7
                red[3] = (red0*5 + red1*2)//7
                red[4] = (red0*4 + red1*3)//7
                red[5] = (red0*3 + red1*4)//7
                red[6] = (red0*2 + red1*5)//7
                red[7] = (red0 + red1*6)//7
            else:
                red[2] = (red0*4 + red1)//5
                red[3] = (red0*3 + red1*2)//5
                red[4] = (red0*2 + red1*3)//5
                red[5] = (red0 + red1*4)//5
                red[6] = r_scale[0]
                red[7] = r_scale[255]
                
            if green0 > green1:
                green[2] = (green0*6 + green1)//7
                green[3] = (green0*5 + green1*2)//7
                green[4] = (green0*4 + green1*3)//7
                green[5] = (green0*3 + green1*4)//7
                green[6] = (green0*2 + green1*5)//7
                green[7] = (green0 + green1*6)//7
            else:
                green[2] = (green0*4 + green1)//5
                green[3] = (green0*3 + green1*2)//5
                green[4] = (green0*2 + green1*3)//5
                green[5] = (green0 + green1*4)//5
                green[6] = g_scale[0]
                green[7] = g_scale[255]

            for k in pixel_indices:
                x = r = red[(red_idx >> (k*3))&7]
                y = g = green[(green_idx >> (k*3))&7]

                k *= ucc

                # we're normalizing the coordinates here, not just unpacking them
                x = r&mask if r&(mask+1) else mask - r
                y = g&mask if g&(mask+1) else mask - g

                d = mask_sq - x**2 - y**2
                if d > 0:
                    b = int(sqrt(d)) + mask + 1
                else:
                    n_len = sqrt(mask_sq - d)/mask
                    x = int(x/n_len)
                    y = int(y/n_len)

                    r = x+(mask+1) if r&(mask+1) else mask - x
                    g = y+(mask+1) if g&(mask+1) else mask - y
                    b = mask + 1

                unpacked[k + r_index] = r
                unpacked[k + g_index] = g
                unpacked[k + b_index] = b

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, 4, width, height)
    return unpacked


def unpack_ctx1(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
    assert packed.typecode == 'L'

    # get all sorts of information we need
    unpack_code = self._UNPACK_ARRAY_CODE
    unpack_size = ab.PIXEL_ENCODING_SIZES[unpack_code]
    unpack_max = (1<<(unpack_size*8)) - 1
    mask = (unpack_max + 1)//2 - 1
    mask_sq = mask**2

    ucc = self.unpacked_channel_count
    bpp = unpack_size*ucc
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    pixels_per_texel = (width//texel_width)*(height//texel_height)
    channels_per_texel = ucc*pixels_per_texel

    pixel_indices = range(pixels_per_texel)

    #create a new array to hold the pixels after we unpack them
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)

    #create the arrays to hold the color channel data
    c_0 = [unpack_max,0,0,0]
    c_1 = [unpack_max,0,0,0]
    c_2 = [unpack_max,0,0,0]
    c_3 = [unpack_max,0,0,0]

    #stores the colors in a way we can easily access them
    colors = [c_0, c_1, c_2, c_3]

    try:
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack DXN texture. Channel mapping must include " +
              "channels 1, 2, and 3, not %s" % self.channel_mapping)

    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    
    #loop through each texel
    for i in range(len(packed)//2):
        j = i*2
        pxl_i = i*channels_per_texel
        
        values = packed[j]
        idx = packed[j+1]

        """unpack the colors"""
        c_0[1] = x0 = r0 = r_scale[(values) & 255]
        c_0[2] = y0 = g0 = g_scale[(values>>8) & 255]
        c_1[1] = x1 = r1 = r_scale[(values>>16) & 255]
        c_1[2] = y1 = g1 = g_scale[(values>>24) & 255]

        """calculate the z-components"""
        # we're normalizing the coordinates here, not just unpacking them
        x0 = x0&mask if x0&(mask+1) else mask - x0
        y0 = y0&mask if y0&(mask+1) else mask - y0
        x1 = x1&mask if x1&(mask+1) else mask - x1
        y1 = y1&mask if y1&(mask+1) else mask - y1

        d = mask_sq - x0**2 - y0**2
        if d > 0:
            b0 = int(sqrt(d)) + mask + 1
        else:
            b0 = mask + 1
            n_len = sqrt(mask_sq - d)/mask
            x0 = int(x0/n_len)
            y0 = int(y0/n_len)

            r0 = x0+(mask+1) if r0&(mask+1) else mask - x0
            g0 = y0+(mask+1) if g0&(mask+1) else mask - y0

        d = mask_sq - x1**2 - y1**2
        if d > 0:
            b1 = int(sqrt(d)) + mask + 1
        else:
            b1 = mask + 1
            n_len = sqrt(mask_sq - d)/mask
            x1 = int(x1/n_len)
            y1 = int(y1/n_len)

            r1 = x1+(mask+1) if r1&(mask+1) else mask - x1
            g1 = y1+(mask+1) if g1&(mask+1) else mask - y1

        # store the normalized colors
        c_0[1] = r0; c_1[1] = r1
        c_0[2] = g0; c_1[2] = g1
        c_0[3] = b0; c_1[3] = b1

        # calculate the in-between colors
        c_2[1] = (c_0[1]*2 + c_1[1])//3
        c_2[2] = (c_0[2]*2 + c_1[2])//3
        c_2[3] = (c_0[3]*2 + c_1[3])//3

        c_3[1] = (c_0[1] + c_1[1]*2)//3
        c_3[2] = (c_0[2] + c_1[2]*2)//3
        c_3[3] = (c_0[3] + c_1[3]*2)//3

        for k in pixel_indices:
            color = colors[(idx >> (k*2))&3]
            off = k*ucc + pxl_i
            unpacked[off + chan1] = color[1]
            unpacked[off + chan2] = color[2]
            unpacked[off + chan3] = color[3]

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, False, ucc, width, height)

    return unpacked


def unpack_u8v8(self, bitmap_index, width, height, depth=1):
    packed = self.texture_block[bitmap_index]
        
    #create a new array to hold the pixels after we unpack them
    unpack_code = self._UNPACK_ARRAY_CODE
    ucc = self.unpacked_channel_count
    bpp = ab.PIXEL_ENCODING_SIZES[unpack_code]*ucc
    unpacked = ab.bitmap_io.make_array(unpack_code, width*height*bpp)
    
    try:
        chan1 = self.channel_mapping.index(1)
        chan2 = self.channel_mapping.index(2)
        chan3 = self.channel_mapping.index(3)
    except Exception:
        print("Cannot unpack U8V8 texture. Channel mapping must include " +
              "channels 1, 2, and 3, not %s" % self.channel_mapping)

    r_scale = self.channel_upscalers[chan1]
    g_scale = self.channel_upscalers[chan2]
    b_scale = self.channel_upscalers[chan3]

    for i in range(0, len(packed)):
        j = ucc*i
        r = packed[i]&255
        g = (packed[i]>>8)&255
        '''
        So an RGB normal map is [0, 255] and maps linearly to [-1, 1],
        and U8V8 is [-127, 127] and does NOT map linearly to [-1, 1].
        If read as unsigned, U8V8 maps [0, 127] to [-127, 0] and
        [128, 255] to [0, 127]. Because of this, we may need to
        subtract 255 from the r and g values. This is complicated
        even more by the fact that the packed array isnt signed in
        the form we are reading from it, so we need account for that.
        '''
        r = r-255 if r&128 else r
        g = g-255 if g&128 else g

        # we're normalizing the coordinates here, not just unpacking them
        d = 16129 - r**2 - g**2  # 16129 == 127**2
        if d > 0:
            b = int(sqrt(d))
        else:
            n_len = sqrt(16129 - d)/127
            r = int(r/n_len)
            g = int(g/n_len)
            b = 0

        unpacked[j + chan1] = r_scale[r+128]
        unpacked[j + chan2] = g_scale[g+128]
        unpacked[j + chan3] = b_scale[b+128]

    return unpacked


########################################
'''######## PACKING ROUTINES ########'''
########################################


def pack_dxt1(self, unpacked, width, height, depth=1):
    ucc, bpt = self.unpacked_channel_count, 8
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    pixels_per_texel = get_texel_pixel_count(width, height)
    channels_per_texel = ucc*pixels_per_texel
    can_have_alpha = self.color_key_transparency
    a_cutoff = self.one_bit_bias

    _, r_scale, g_scale, b_scale = self.channel_downscalers
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, ucc, width, height)

    if fast_dds_defs:
        dds_defs_ext.pack_dxt1(
            repacked, unpacked, r_scale, g_scale, b_scale,
            pixels_per_texel, can_have_alpha, a_cutoff)
        return repacked

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    pixel_indices = range(0, channels_per_texel, ucc)
    make_alpha = False
    c_2 = [0,0,0,0]
    c_3 = [0,0,0,0]

    #shorthand names
    rpa = repacked
    upa = unpacked

    #loop for each texel
    for txl_i in range(0, len(repacked), 2):
        dist0 = dist1 = c_0i = c_1i = idx = 0

        pxl_i = (txl_i//2)*channels_per_texel
        r_pxl_i, g_pxl_i, b_pxl_i = pxl_i+1, pxl_i+2, pxl_i+3

        # compare distance between all pixels and find the two furthest apart
        # (we are actually comparing the area of the distance as it's faster)
        for i in pixel_indices:
            r = upa[r_pxl_i+i]
            g = upa[g_pxl_i+i]
            b = upa[b_pxl_i+i]
            for j in pixel_indices:
                if i is j: continue
                dist1 = ((r-upa[r_pxl_i+j])**2+
                         (g-upa[g_pxl_i+j])**2+
                         (b-upa[b_pxl_i+j])**2)
                if dist1 > dist0:
                    dist0 = dist1
                    c_0i = i
                    c_1i = j

        # store furthest apart colors for use
        c_0 = upa[pxl_i+c_0i: 4+pxl_i+c_0i]
        c_1 = upa[pxl_i+c_1i: 4+pxl_i+c_1i]

        # quantize the colors down to 16 bit color and repack
        color0 = (r_scale[c_0[1]]<<11)+(g_scale[c_0[2]]<<5)+b_scale[c_0[3]]
        color1 = (r_scale[c_1[1]]<<11)+(g_scale[c_1[2]]<<5)+b_scale[c_1[3]]

        # figure out if we are using color key transparency for this pixel
        #by seeing if any of the alpha values are below the cutoff bias
        if can_have_alpha:
            make_alpha = False
            for i in pixel_indices:
                if upa[pxl_i+i] < a_cutoff:
                    make_alpha = True
                    break

        if color0 == color1 and not make_alpha:
            #do nothing except save one of the colors to the array
            rpa[txl_i] = color0
            continue

        # if the current color selection doesn't match what we want then
        # we reverse which color is which (if we are using transparency then
        # the first color as an integer must be smaller or equal to the second)
        if make_alpha == (color0 > color1):
            c_0, c_1 = c_1, c_0
            rpa[txl_i] = (color0<<16) + color1
        else:
            rpa[txl_i] = (color1<<16) + color0

        # calculate the intermediate colors
        """If the target format is DXT2/3/4/5 then no CK transparency is used.
        CK mode will only be selected if both colors are the same.
        If both colors are the same then it is fine to run non-CK
        calculation on it since it will default to index zero.
        That is why the DXT3/5 calculation is in this part only"""
        if rpa[txl_i]&65535 > rpa[txl_i]>>16:
            c_2[1] = (c_0[1]*2 + c_1[1])//3
            c_2[2] = (c_0[2]*2 + c_1[2])//3
            c_2[3] = (c_0[3]*2 + c_1[3])//3
            
            c_3[1] = (c_0[1] + c_1[1]*2)//3
            c_3[2] = (c_0[2] + c_1[2]*2)//3
            c_3[3] = (c_0[3] + c_1[3]*2)//3
        
            # calculate each pixel's closest match
            # and assign it the proper index
            for i in pixel_indices:
                r = upa[r_pxl_i+i]
                g = upa[g_pxl_i+i]
                b = upa[b_pxl_i+i]
                dists = ((r-c_0[1])**2 + (g-c_0[2])**2 + (b-c_0[3])**2,
                         (r-c_1[1])**2 + (g-c_1[2])**2 + (b-c_1[3])**2,
                         (r-c_2[1])**2 + (g-c_2[2])**2 + (b-c_2[3])**2,
                         (r-c_3[1])**2 + (g-c_3[2])**2 + (b-c_3[3])**2)

                idx += dists.index(min(dists))<<(i>>1)

            rpa[txl_i+1] = idx
            continue

        c_2[1] = (c_0[1]+c_1[1])//2
        c_2[2] = (c_0[2]+c_1[2])//2
        c_2[3] = (c_0[3]+c_1[3])//2
        #here, c_3 represents zero color and fully transparent
        
        #calculate each pixel's closest match and assign it the proper index
        for i in pixel_indices:
            if upa[pxl_i+i] < a_cutoff:
                idx += 3<<(i>>1)
                continue
            r = upa[r_pxl_i+i]
            g = upa[g_pxl_i+i]
            b = upa[b_pxl_i+i]
            dists = ((r-c_0[1])**2 + (g-c_0[2])**2 + (b-c_0[3])**2,
                     (r-c_1[1])**2 + (g-c_1[2])**2 + (b-c_1[3])**2,
                     (r-c_2[1])**2 + (g-c_2[2])**2 + (b-c_2[3])**2)

            idx += dists.index(min(dists))<<(i>>1)

        rpa[txl_i+1] = idx
            
    return repacked


def pack_dxt2_3(self, unpacked, width, height, depth=1):
    ucc, bpt = self.unpacked_channel_count, 16
    ucc = self.unpacked_channel_count
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    pixels_per_texel = get_texel_pixel_count(width, height)
    channels_per_texel = ucc*pixels_per_texel

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, ucc, width, height)

    if fast_dds_defs:
        dds_defs_ext.pack_dxt2_3(
            repacked, unpacked,
            a_scale, r_scale, g_scale, b_scale, pixels_per_texel)
        return repacked

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    pixel_indices = range(0, channels_per_texel, ucc)
    c_2 = [0,0,0,0]
    c_3 = [0,0,0,0]

    #shorthand names
    rpa = repacked
    upa = unpacked

    #loop for each texel
    for txl_i in range(0, len(repacked), 4):
        dist0 = dist1 = c_0i = c_1i = 0

        pxl_i = (txl_i//4)*channels_per_texel
        r_pxl_i, g_pxl_i, b_pxl_i = pxl_i+1, pxl_i+2, pxl_i+3

        '''CALCULATE THE ALPHA'''
        # calculate alpha channel for DXT 2/3
        # coincidentally, the number of channels(4) matches the number of
        # bits in the alpha(4), so the shift is the same as the channel index
        alpha = sum(a_scale[upa[pxl_i+i]]<<i for i in pixel_indices)

        rpa[txl_i]   = alpha&0xFFffFFff
        rpa[txl_i+1] = alpha>>32

        '''CALCULATE THE COLORS'''
        # compare distance between all pixels and find the two furthest apart
        # (we are actually comparing the area of the distance as it's faster)
        for i in pixel_indices:
            for j in pixel_indices:
                if i is j: continue
                dist1 = ((upa[r_pxl_i+i]-upa[r_pxl_i+j])**2+
                         (upa[g_pxl_i+i]-upa[g_pxl_i+j])**2+
                         (upa[b_pxl_i+i]-upa[b_pxl_i+j])**2)
                if dist1 > dist0:
                    dist0 = dist1
                    c_0i = i
                    c_1i = j

        # store furthest apart colors for use
        c_0 = upa[pxl_i+c_0i: 4+pxl_i+c_0i]
        c_1 = upa[pxl_i+c_1i: 4+pxl_i+c_1i]

        # quantize the colors down to 16 bit color and repack
        color0 = (r_scale[c_0[1]]<<11)+(g_scale[c_0[2]]<<5)+b_scale[c_0[3]]
        color1 = (r_scale[c_1[1]]<<11)+(g_scale[c_1[2]]<<5)+b_scale[c_1[3]]

        if color0 == color1:
            # do nothing except save one of the colors to the array
            rpa[txl_i+2] = color0
        else:
            # if the current color selection doesn't match what
            # we want then we reverse which color is which
            if color0 < color1:
                c_0, c_1 = c_1, c_0
                color0, color1 = color1, color0

            idx = 0
            c_2[1] = (c_0[1]*2 + c_1[1])//3
            c_2[2] = (c_0[2]*2 + c_1[2])//3
            c_2[3] = (c_0[3]*2 + c_1[3])//3

            c_3[1] = (c_0[1] + c_1[1]*2)//3
            c_3[2] = (c_0[2] + c_1[2]*2)//3
            c_3[3] = (c_0[3] + c_1[3]*2)//3
        
            # calculate each pixel's closest match
            # and assign it the proper index
            for i in pixel_indices:
                r = upa[r_pxl_i+i]
                g = upa[g_pxl_i+i]
                b = upa[b_pxl_i+i]
                dists = ((r-c_0[1])**2 + (g-c_0[2])**2 + (b-c_0[3])**2,
                         (r-c_1[1])**2 + (g-c_1[2])**2 + (b-c_1[3])**2,
                         (r-c_2[1])**2 + (g-c_2[2])**2 + (b-c_2[3])**2,
                         (r-c_3[1])**2 + (g-c_3[2])**2 + (b-c_3[3])**2)

                idx += dists.index(min(dists))<<(i>>1)

            rpa[txl_i+2] = (color1<<16) + color0
            rpa[txl_i+3] = idx
            
    return repacked


def pack_dxt4_5(self, unpacked, width, height, depth=1):
    ucc, bpt = self.unpacked_channel_count, 16
    ucc = self.unpacked_channel_count
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
    pixels_per_texel = get_texel_pixel_count(width, height)
    channels_per_texel = ucc*pixels_per_texel

    a_scale, r_scale, g_scale, b_scale = self.channel_downscalers
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, ucc, width, height)

    if fast_dds_defs:
        dds_defs_ext.pack_dxt4_5(
            repacked, unpacked, a_scale, r_scale, g_scale, b_scale,
            pixels_per_texel)
        return repacked

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    pixel_indices = range(0, channels_per_texel, ucc)
    c_0 = [0,0,0,0]
    c_1 = [0,0,0,0]
    c_2 = [0,0,0,0]
    c_3 = [0,0,0,0]

    #shorthand names
    rpa = repacked
    upa = unpacked

    #loop for each texel
    for txl_i in range(0, len(repacked), 4):
        dist0 = dist1 = c_0i = c_1i = alpha_idx = 0
        
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//4)*channels_per_texel
        r_pxl_i, g_pxl_i, b_pxl_i = pxl_i+1, pxl_i+2, pxl_i+3

        '''CALCULATE THE ALPHA'''
        #find the most extreme values
        alpha0 = max(map(lambda i: a_scale[upa[pxl_i+i]], pixel_indices))
        alpha1 = min(map(lambda i: a_scale[upa[pxl_i+i]], pixel_indices))

        #if the most extreme values are NOT 0 and
        #255, use them as the interpolation values
        if alpha0 != 0 or alpha1 != 255:
            """In this mode, value_0 must be greater than value_1"""
            #if they are the same number then
            #the indexing can stay at all zero
            if alpha0 != alpha1:
                alpha_dif = alpha0-alpha1
                #calculate and store which interpolated
                #index each alpha value is closest to
                for i in pixel_indices:
                    #0 = c_0                 1 = c_1
                    #2 = (6*c_0 + c_1)//7    3 = (5*c_0 + 2*c_1)//7
                    #4 = (4*c_0 + 3*c_1)//7  5 = (3*c_0 + 4*c_1)//7
                    #6 = (2*c_0 + 5*c_1)//7  7 = (c_0 + 6*c_1)//7

                    #calculate how far between both colors
                    #that the value is as a 0 to 7 int
                    tmp = ((a_scale[upa[pxl_i+i]]-alpha1
                            )*7+alpha_dif//2)//alpha_dif
                    if tmp == 0:
                        alpha_idx += 1<<(i*3//ucc)
                    elif tmp < 7:
                        #Because the colors are stored in opposite
                        #order, we need to invert the index
                        alpha_idx += (8-tmp)<<(i*3//ucc)
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in pixel_indices:
                tmp = a_scale[upa[pxl_i+i]]
                #store if lowest int so far
                if alpha0 > tmp and tmp > 0: alpha0 = tmp
                #store if greatest int so far
                if alpha1 < tmp and tmp < 255: alpha1 = tmp

            #if they are the same number then
            #the indexing can stay at all zero
            if alpha0 != alpha1:
                #calculate and store which interpolated
                #index each alpha value is closest to

                alpha_dif = alpha1-alpha0
                for i in pixel_indices:
                    #there are 4 interpolated colors in this mode
                    #0 =  c_0                1 = c_1
                    #2 = (4*c_0 + c_1)//5    3 = (3*c_0 + 2*c_1)//5
                    #4 = (2*c_0 + 3*c_1)//5  5 = (c_0 + 4*c_1)//5
                    #6 =  0                  7 = 255
                    comp = a_scale[upa[pxl_i+i]]
                    if comp == 0:
                        #if the value is 0 we set it to index 6
                        alpha_idx += 6<<(i*3//ucc)
                    elif comp == 255:
                        #if the value is 255 we set it to index 7
                        alpha_idx += 7<<(i*3//ucc)
                    else:
                        #calculate how far between both colors
                        #that the value is as a 0 to 5 int
                        tmp = ((comp-alpha0)*5 + alpha_dif//2)//alpha_dif
                        if tmp == 5:
                            alpha_idx += 1<<(i*3//ucc)
                        elif tmp > 0:
                            alpha_idx += (tmp+1)<<(i*3//ucc)

        rpa[txl_i] = ((alpha_idx<<16) + (alpha1<<8) + alpha0)&0xFFffFFff
        rpa[txl_i+1] = alpha_idx>>16

        '''CALCULATE THE COLORS'''
        # compare distance between all pixels and find the two furthest apart
        # (we are actually comparing the area of the distance as it's faster)
        for i in pixel_indices:
            for j in pixel_indices:
                if i is j: continue
                dist1 = ((upa[r_pxl_i+i]-upa[r_pxl_i+j])**2+
                         (upa[g_pxl_i+i]-upa[g_pxl_i+j])**2+
                         (upa[b_pxl_i+i]-upa[b_pxl_i+j])**2)
                if dist1 > dist0:
                    dist0 = dist1
                    c_0i = i
                    c_1i = j

        # store furthest apart colors for use
        c_0 = upa[pxl_i+c_0i: 4+pxl_i+c_0i]
        c_1 = upa[pxl_i+c_1i: 4+pxl_i+c_1i]

        # quantize the colors down to 16 bit color and repack
        color0 = (r_scale[c_0[1]]<<11)+(g_scale[c_0[2]]<<5)+b_scale[c_0[3]]
        color1 = (r_scale[c_1[1]]<<11)+(g_scale[c_1[2]]<<5)+b_scale[c_1[3]]
            
        if color0 == color1:
            # do nothing except save one of the colors to the array
            rpa[txl_i+2] = color0
        else:
            # if the current color selection doesn't match what
            # we want then we reverse which color is which
            if color0 < color1:
                c_0, c_1 = c_1, c_0
                color0, color1 = color1, color0

            idx = 0
            c_2[1] = (c_0[1]*2 + c_1[1])//3
            c_2[2] = (c_0[2]*2 + c_1[2])//3
            c_2[3] = (c_0[3]*2 + c_1[3])//3

            c_3[1] = (c_0[1] + c_1[1]*2)//3
            c_3[2] = (c_0[2] + c_1[2]*2)//3
            c_3[3] = (c_0[3] + c_1[3]*2)//3
        
            # calculate each pixel's closest match
            # and assign it the proper index
            for i in pixel_indices:
                r = upa[r_pxl_i+i]
                g = upa[g_pxl_i+i]
                b = upa[b_pxl_i+i]
                dists = ((r-c_0[1])**2 + (g-c_0[2])**2 + (b-c_0[3])**2,
                         (r-c_1[1])**2 + (g-c_1[2])**2 + (b-c_1[3])**2,
                         (r-c_2[1])**2 + (g-c_2[2])**2 + (b-c_2[3])**2,
                         (r-c_3[1])**2 + (g-c_3[2])**2 + (b-c_3[3])**2)

                idx += dists.index(min(dists))<<(i>>1)

            rpa[txl_i+2] = (color1<<16) + color0
            rpa[txl_i+3] = idx

    return repacked


def pack_dxt5a(self, unpacked, width, height, depth=1):        
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    ucc = self.unpacked_channel_count
    assert self.target_channel_count == ucc
    bpt = ucc*8
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, ucc, width, height)

    #shorthand names
    rpa = repacked
    upa = unpacked

    scale = self.channel_downscalers[0]

    channels_per_texel = ucc*get_texel_pixel_count(width, height)
    pixel_indices = range(0, channels_per_texel, ucc)

    #loop for each texel
    for txl_i in range(0, len(repacked), 2):
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//(2*ucc))*channels_per_texel
        chan = (txl_i//2)%ucc
        val0 = idx = 0
        val1 = 255

        #find the most extreme vals
        for i in pixel_indices:
            val = upa[pxl_i+i+chan]
            val0 = max(val0, val)
            val1 = min(val1, val)

        # if the most extreme vals are NOT 0 and
        # 255, use them as the interpolation vals
        if val0 != 0 or val1 != 255:
            """In this mode, value_0 must be greater than value_1"""

            # if they are the same number then
            # the indexing can stay at all zero
            if val0 != val1:
                val_dif = val0-val1
                # calculate and store which interpolated
                # index each alpha value is closest to
                for i in pixel_indices:
                    tmp = ((upa[pxl_i+i+chan]-val1)*7 + val_dif//2)//val_dif
                    """Because the colors are stored in reverse
                    order, we need to invert the index"""
                    if tmp == 0:
                        idx += 1<<(i*3//ucc)
                    elif tmp < 7:
                        idx += (8-tmp)<<(i*3//ucc)
        else:
            """In this mode, val0 must be less than or equal to val1"""
            #if the most extreme vals ARE 0 and 255 though, then
            #we need to calculate the second most extreme vals
            for i in pixel_indices:
                comp = upa[pxl_i+i+chan]
                if val0 > comp and comp > 0: val0 = comp
                if val1 < comp and comp < 255: val1 = comp

            # if they are the same number then
            # the indexing can stay at all zero
            if val0 != val1:
                val_dif = val0-val1
                # calculate and store which interpolated
                # index each alpha value is closest to
                for i in pixel_indices:
                    comp = upa[pxl_i+i+chan]
                    if comp == 0:
                        idx += 6<<(i*3//ucc)
                    elif comp == 255:
                        idx += 7<<(i*3//ucc)
                    else:
                        tmp = ((comp-val0)*5 + val_dif//2)//val_dif
                        if tmp == 5:
                            idx += 1<<(i*3//ucc)
                        elif tmp > 0:
                            idx += (tmp+1)<<(i*3//ucc)

        rpa[txl_i] = ((idx<<16) + (val1<<8) + val0)&0xFFffFFff
        rpa[txl_i+1] = idx>>16
            
    return repacked


def pack_dxn(self, unpacked, width, height, depth=1):
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)
        
    #create a new array to hold the texels after we repack them
    bpt = 16
    ucc = self.unpacked_channel_count
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, ucc, width, height)

    #shorthand names
    rpa = repacked
    upa = unpacked

    scale = self.channel_downscalers[0]

    channels_per_texel = ucc*get_texel_pixel_count(width, height)
    pixel_indices = range(0, channels_per_texel, ucc)

    #loop for each texel
    for txl_i in range(0, len(repacked), 2):
        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i>>2)*channels_per_texel
        val0 = idx = 0
        val1 = 255

        # figure out if we're packing red or green(1=red, 2=green)
        chan = ((txl_i>>1)%2)+1

        #8: find the most extreme vals
        for i in pixel_indices:
            val = upa[pxl_i+i+chan]
            val0 = max(val0, val)
            val1 = min(val1, val)

        # if the most extreme vals are NOT 0 and
        # 255, use them as the interpolation vals
        if val0 != 0 or val1 != 255:
            """In this mode, value_0 must be greater than value_1"""

            #if they are the same number then
            #the indexing can stay at all zero
            if val0 != val1:
                val_dif = val0-val1
                # calculate and store which interpolated
                # index each alpha value is closest to
                for i in pixel_indices:
                    tmp = ((upa[pxl_i+i+chan]-val1)*7 + val_dif//2)//val_dif
                    """Because the colors are stored in reverse
                    order, we need to invert the index"""
                    if tmp == 0:
                        idx += 1<<(i*3//ucc)
                    elif tmp < 7:
                        idx += (8-tmp)<<(i*3//ucc)
                
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme vals ARE 0 and 255 though, then
            #we need to calculate the second most extreme vals
            for i in pixel_indices:
                comp = upa[pxl_i+i+chan]
                if val0 > comp and comp > 0: val0 = comp
                if val1 < comp and comp < 255: val1 = comp

            #if they are the same number then
            #the indexing can stay at all zero
            if val0 != val1:
                val_dif = val1-val0
                # calculate and store which interpolated
                # index each alpha value is closest to
                for i in pixel_indices:
                    comp = upa[pxl_i+i+chan]
                    if comp == 0:
                        idx += 6<<(i*3//ucc)
                    elif comp == 255:
                        idx += 7<<(i*3//ucc)
                    else:
                        tmp = ((comp-val0)*5 + (val_dif//2))//val_dif
                        if tmp == 5:
                            idx += 1<<(i*3//ucc)
                        elif tmp > 0:
                            idx += (tmp+1)<<(i*3//ucc)

        rpa[txl_i] = ((idx<<16) + (val1<<8) + val0)&0xFFffFFff
        rpa[txl_i+1] = idx>>16
            
    return repacked


def pack_ctx1(self, unpacked, width, height, depth=1):
    #this is how many texels wide/tall the texture is
    texel_width, texel_height, _ = ab.clip_dimensions(width//4, height//4)

    #create a new array to hold the texels after we repack them
    bpt = 8
    repacked = ab.bitmap_io.make_array("L", texel_width*texel_height*bpt)

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if texel_width > 1:
        dxt_swizzler = ab.swizzler.Swizzler(converter=self, mask_type="DXT")
        unpacked = dxt_swizzler.swizzle_single_array(
            unpacked, True, 4, width, height)

    #shorthand names
    rpa = repacked
    upa = unpacked

    _, r_scale, g_scale, __ = self.channel_downscalers
    channels_per_texel = 4*get_texel_pixel_count(width, height)

    pixel_indices = range(0, channels_per_texel, 4)

    #loop for each texel
    for txl_i in range(0, len(repacked), 2):
        dist0 = dist1 = c_0i = c_1i = 0
        xy_0 = [0,0,0,0]
        xy_1 = [0,0,0,0]
        xy_2 = [0,0,0,0]
        xy_3 = [0,0,0,0]

        #cache so it doesn't have to keep being calculated
        pxl_i = (txl_i//2)*channels_per_texel
        r_pxl_i, g_pxl_i = pxl_i+1, pxl_i+2

        # compare distance between all pixels and find the two furthest apart
        #(we are actually comparing the area of the distance as it's faster)
        for i in pixel_indices:
            for j in pixel_indices:
                dist1 = ((upa[r_pxl_i+i]-upa[r_pxl_i+j])**2+
                         (upa[g_pxl_i+i]-upa[g_pxl_i+j])**2)
                if dist1 > dist0:
                    dist0 = dist1
                    c_0i = i
                    c_1i = j

        # store furthest apart colors for use
        xy_0[0] = upa[pxl_i+1+c_0i]
        xy_0[1] = upa[pxl_i+2+c_0i]
        
        xy_1[0] = upa[pxl_i+1+c_1i]
        xy_1[1] = upa[pxl_i+2+c_1i]

        color0 = xy_0[0] + (xy_0[1]<<8)
        color1 = xy_1[0] + (xy_1[1]<<8)
            
        if color0 == color1:
            #do nothing except save one of the colors to the array
            rpa[txl_i] = color0
        else:
            rpa[txl_i] = color0 + (color1<<16)

            # calculate the intermediate colors
            xy_2[0] = (xy_0[0]*2+xy_1[0])//3
            xy_2[1] = (xy_0[1]*2+xy_1[1])//3
            
            xy_3[0] = (xy_0[0]+xy_1[0]*2)//3
            xy_3[1] = (xy_0[1]+xy_1[1]*2)//3
            
            # calculate each pixel's closest match
            # and assign it the proper index
            for i in pixel_indices:
                x = upa[r_pxl_i+i]
                y = upa[g_pxl_i+i]
                dist0 = (x-xy_0[0])**2 + (y-xy_0[1])**2
                dist1 = (x-xy_1[0])**2 + (y-xy_1[1])**2
                
                # add appropriate indexing value to array
                if dist0 <= dist1: #closer to color 0
                    if dist0 > (x-xy_2[0])**2 + (y-xy_2[1])**2:
                        #closest to color 2
                        rpa[txl_i+1] += 2<<(i//2)
                elif dist1 < (x-xy_3[0])**2 + (y-xy_3[1])**2:
                    #closest to color 1
                    rpa[txl_i+1] += 1<<(i//2)
                else: #closest to color 3
                    rpa[txl_i+1] += 3<<(i//2)
            
    return repacked


def pack_u8v8(self, unpacked, width, height, depth=1):
    ucc = self.unpacked_channel_count
    if ucc < 2:
        raise TypeError(
            "Cannot convert image with less than 2 channels to U8V8.")

    packed = ab.bitmap_io.make_array("H", 2*len(unpacked)//ucc)
    _, r_scale, g_scale, __ = self.channel_downscalers
    if ucc == 2:
        chan0, chan1 = 0, 1
    else:
        chan0, chan1 = 1, 2

    for i in range(0, len(unpacked), ucc):
        # packing channels 1 and 2
        r = r_scale[unpacked[i+chan0]]
        g = g_scale[unpacked[i+chan1]]
        '''
        So an RGB normal map is [0, 255] and maps linearly to [-1, 1],
        and U8V8 is [-127, 127] and does NOT map linearly to [-1, 1].
        '''
        r = r-128 if r&128 else r+128
        g = g-128 if g&128 else g+128
        packed[i//ucc] = (g<<8) + r

    return packed
