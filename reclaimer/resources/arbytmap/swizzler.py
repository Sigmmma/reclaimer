from array import array
from math import ceil, log
from traceback import format_exc
import time

try:
    try:
        from .ext import swizzler_ext
    except Exception:
        from ext import swizzler_ext
    fast_swizzler = True
except Exception:
    fast_swizzler = False

    
class Swizzler():
    '''THIS SWIZZLER PLUGS INTO THE BITMAP CONVERTOR
    AND EXPECTS IT TO CONTAIN CERTAIN VARIABLES.
    This module was split to make it easier to
    navigate the bitmap convertor and swizzler'''
    converter = None

    def __init__(self, **kwargs):
        if "converter" not in kwargs or "mask_type" not in kwargs:
            return

        self.converter = kwargs["converter"]
        self.swizzler_mask = SwizzlerMask(**kwargs)

    def swizzle_texture(self, force=False, delete_old=True):
        '''this is the function to call if you want to swizzle or
        unswizzle an entire texture, mipmaps, cube faces and all'''
        conv = self.converter
        if conv is None:
            return False

        tex_block = conv.texture_block
        
        if tex_block is None:
            print("ERROR: NO TEXTURE LOADED. CANNOT PREFORM " +
                  "SWIZZLE OPERATION WITHOUT A LOADED TEXTURE")
            return False

        '''if we are forcing the texture to be swizzled or
        deswizzled then we set the swizzle mode to the
        inverse of whether or not it is swizzled'''
        mode = conv.swizzle_mode
        if force:
            mode = not(conv.swizzled)

        #only run if the texture is swizzled and we want to
        #unswizzle it or vice versa. this prevents it from
        #unswizzling a bitmap that's unswizzled and vice versa.
        #also check that that the bitmap is being saved to
        #a format that supports swizzling.
        if mode == conv.swizzled:
            return True

        #used to keep track of which pixel array we are reading
        i = 0
        width, height, depth = (conv.width, conv.height, conv.depth)
        ucc = 1
        if not conv.packed:
            ucc = conv.unpacked_channel_count

        for m in range(conv.mipmap_count + 1):
            for s in range(conv.sub_bitmap_count):
                #get the pixel array to be swizzled/unswizzled
                pixels = tex_block[i]
                
                #make the new array to place the swizzled data into
                if isinstance(pixels, array):
                    swizzled = array(pixels.typecode, pixels)
                elif isinstance(pixels, bytearray):
                    swizzled = bytearray(len(pixels))
                else:
                    raise TypeError(
                        'Pixel array is not the proper type. Expected ' +
                        'array.array or bytearray, got %s' % type(pixels))

                self._swizzle_block(mode, pixels, swizzled, ucc,
                                    width, height, depth)

                #replace the old pixels with the new swizzled one
                tex_block[i] = swizzled

                #delete the old pixel array
                if delete_old:
                    #delete the old pixel array
                    del pixels[:]
                    
                i += 1

            #we're going to the next lowest mipmap
            #level so we halve the resolution
            width  = int(ceil(width/2))
            height = int(ceil(height/2))
            depth  = int(ceil(depth/2))

        #now that we're done (un)swizzling
        #the bitmap we invert the boolean
        conv.swizzled = not(conv.swizzled)
        
        #no errors occurred so we return a success
        return True

    def swizzle_single_array(self, pixels, mode, channels,
                             width, height, depth=1, delete_old=True):
        '''this is the function to call if you just
        want to swizzle or unswizzle a single array
        mode: True = Swizzle    False = Deswizzle'''
        try:
            #make the new array to place the swizzled data into
            if isinstance(pixels, array):
                swizzled = array(pixels.typecode, pixels)
            elif isinstance(pixels, bytearray):
                swizzled = bytearray(len(pixels))
            else:
                raise TypeError('Array is not the proper type. ' +
                                'Expected array.array or bytearray, got %s'
                                % type(pixels))

            self._swizzle_block(mode, pixels, swizzled, channels,
                                width, height, depth)

            if delete_old:
                #delete the old pixel array
                del pixels[:]

            return swizzled
        except Exception:
            print("ERROR OCCURRED WHILE TRYING TO SWIZZLE ARRAY")
            print(format_exc())
            return False

    def _swizzle_block(self, mode, pixels, swizzled,
                       channels, width, height, depth):
        '''this function should only be called by one of the
        above two functions. this swizzler only works with
        entire pixels and can't swizzle individual channels'''

        #this is the number of bits per axis. We'll use it
        #when calculating how much to bitshift the offsets
        c_blocks, x_blocks, y_blocks, z_blocks = (
            int(log(channels, 2)), int(log(width, 2)),
            int(log(height, 2)), int(log(depth, 2)))

        #these are the masks that will be used
        #for calculating the swizzled offsets.
        c_mask, x_mask, y_mask, z_mask = (
            array("B"), array("B"), array("B"), array("B"))
        
        #generate the mask for the swizzler pattern
        self.swizzler_mask.mask_set(c_blocks, x_blocks, y_blocks, z_blocks,
                                    c_mask,   x_mask,   y_mask,   z_mask)

        bs = self._bit_swizzler

        #swizzle the bits of the offsets. supports up to
        #2^32 array elements(4GB if each element is 1 byte)
        c_block_offs = array("L", map(bs, range(channels), (c_mask,)*channels))
        x_block_offs = array("L", map(bs, range(width), (x_mask,)*width))
        y_block_offs = array("L", map(bs, range(height), (y_mask,)*height))
        z_block_offs = array("L", map(bs, range(depth), (z_mask,)*depth))
        
        if fast_swizzler:
            if mode:
                swizzler_ext.swizzle_array(
                    c_block_offs, x_block_offs, y_block_offs, z_block_offs,
                    swizzled, pixels)
            else:
                swizzler_ext.unswizzle_array(
                    c_block_offs, x_block_offs, y_block_offs, z_block_offs,
                    swizzled, pixels)

            return

        i = 0
        #mode: True = Swizzle    False = Deswizzle
        if mode and channels == 1:
            for z in z_block_offs:
                for y in y_block_offs:
                    zy = z+y
                    for x in x_block_offs:
                        swizzled[zy+x] = pixels[i]
                        i += 1
        elif mode:
            for z in z_block_offs:
                for y in y_block_offs:
                    zy = z+y
                    for x in x_block_offs:
                        zyx = zy+x
                        for c in c_block_offs:
                            swizzled[zyx+c] = pixels[i]
                            i += 1
        elif channels == 1:
            for z in z_block_offs:
                for y in y_block_offs:
                    zy = z+y
                    for x in x_block_offs:
                        swizzled[i] = pixels[zy+x]
                        i += 1
        else:
            for z in z_block_offs:
                for y in y_block_offs:
                    zy = z+y
                    for x in x_block_offs:
                        zyx = zy+x                       
                        for c in c_block_offs:
                            swizzled[i] = pixels[zyx+c]
                            i += 1
    
    def _bit_swizzler(self, axis_offset, axis_mask):
        '''axis_offset is the x, y, or z index who's bits we are swizzling
        axis_mask is an array which is the length of Log2(Dimension).
        Each index corrosponds to the equivelant bit in the dimension's
        binary form. The value of each index is how far left the bit should
        be shifted. if the value is negative then the bit will instead be
        shifted to the right by that amount.'''
        
        #this will be used to store the index after we swizzle it's bits
        swizzled_axis_offset = 0
        
        #we loop through each of the bits in the axis_offset
        for i in range(len(axis_mask)):
            '''Mask off the value of the bit, shift it to
            the index it needs to be in, and add the result
            to the return value "swizzled_axis_offset" '''
            mask = axis_mask[i]
            if mask < 0:
                swizzled_axis_offset += (axis_offset&(1<<i)) >> (-1*mask)
            else:
                swizzled_axis_offset += (axis_offset&(1<<i)) << mask
        
        return swizzled_axis_offset


class SwizzlerMask():
    """This swizzler uses a z-order curve based swizzling
    routine, but the exact pattern is modifiable.
    Currently there is a Morton style nested z swizzle
    pattern, a pattern which will place pixels within
    a certain size square directly next to each other(for
    merging together), and a pattern that will place pixels
    within a 4x4 square directly next to each other(to aid
    in calculating DXT texels)"""

    def __init__(self, **kwargs):
        '''this is a list of functions to swizzle masks in different formats.
        unless more are added the default will be the only available one.
        Default is z-order curve, or morton order'''
        self.masks = {"DEFAULT": self._z_order_mask_set,
                      "MORTON": self._z_order_mask_set,
                      "DXT": self._dxt_mask_set,
                      "DOWNSAMPLER": self._pixel_merge_mask_set}
        
        self.swizzler_settings = kwargs
    
        if kwargs.get("mask_type") not in self.masks:
            raise TypeError("Unknown swizzler mask type")

        self.mask_set = self.masks[kwargs.get("mask_type")]

    def mask_set(self, *args, **kwargs):
        raise NotImplementedError

    def _z_order_mask_set(self, c_blocks, x_blocks, y_blocks, z_blocks,
                          c_mask,   x_mask,   y_mask,   z_mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF x, y, AND z OFFSETS
        TOGETHER IN z-ORDER STYLE. THE COLOR CHANNELS CAN ALSO BE SWIZZLED"""

        #do this separately and FIRST. its not likely that
        #we want swizzled channels so we do this separate
        c_mask.extend([0]*c_blocks)
        i = c_blocks
        
        #Loop for each of the bits in the largest dimension
        for size in range(max(x_blocks, y_blocks, z_blocks)):
            """WE CHECK IF THERE ARE STILL ANY BITS FOR EACH AXIS"""
            if x_blocks > size:
                x_mask.append(i)
                i += 1
            if y_blocks > size:
                y_mask.append(i)
                i += 1
            if z_blocks > size:
                z_mask.append(i)
                i += 1
            i -= 1

    def _dxt_mask_set(self, log_c,  log_x,  log_y,  log_z,
                      c_mask, x_mask, y_mask, z_mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF X,
        Y, Z, AND CHANNEL OFFSETS TOGETHER SO THAT
        ALL PIXELS PER DXT TEXEL ARE ADJACENT.

        MAKES IT SO THE FIRST BITS ARE THE CHANNEL AXIS,
        NEXT TWO BITS ARE THE X AXIS, AND THE NEXT 2 BITS
        ARE THE Y AXIS. THE REMAINDER OF THE X BITS ARE NEXT,
        FOLLOWED BY THE REMAINDER OF THE Y BITS, FOLLOWED BY
        THE REMAINDER OF THE Z BITS"""

        tmp_x = log_x
        tmp_y = log_y
        if tmp_x > 2: tmp_x = 2
        if tmp_y > 2: tmp_y = 2

        c_mask.extend([0]*log_c)
        x_mask.extend([log_c]*tmp_x)
        y_mask.extend([log_c+tmp_x]*tmp_y)
        
        z_mask.extend([log_c+tmp_x+tmp_y]*log_z)
        x_mask.extend([log_c+tmp_y+log_z]*(log_x-tmp_x))
        y_mask.extend([log_c+log_x+log_z]*(log_y-tmp_y))


    def _pixel_merge_mask_set(self, log_c,  log_w,  log_h,  log_d,
                              c_mask, x_mask, y_mask, z_mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF C, X, Y,
        AND Z OFFSETS IN SUCH A WAY THAT THE PIXELS BEING
        MERGED END UP DIRECTLY ADJACENT EACH OTHER"""
        config = self.swizzler_settings
        new_width, new_height, new_depth = (
            config["new_width"], config["new_height"], config["new_depth"])
        
        #these are how many blocks are being merged on eachs of the axis
        x_merge = log_w - int(log(new_width, 2))
        y_merge = log_h - int(log(new_height, 2))
        z_merge = log_d - int(log(new_depth, 2))

        """so we can properly swizzle each of the axis we need to know
        which one we are currently working on and ONLY increment that
        one. when we have reached the last bit for that axis this number
        is incremented. when this number reaches 4 it is reset to 0."""
        axis = 0
        axis_bit = 0
        bit_shifts = [0, 0, 0, 0]
        
        x_bit = y_bit = z_bit = c_bit = i = 0
        
        #Loop for each of the bits in the integer (W*H*D*C)
        for i in range(x_merge + y_merge + z_merge + log_c):
            choosing_axis = True

            while choosing_axis:
                choosing_axis = False

                if x_bit >= log_w and axis == 0:
                    axis = 1
                    axis_bit = 0
                if y_bit >= log_h and axis == 1:
                    axis = 2
                    axis_bit = 0
                if z_bit >= log_d and axis == 2:
                    axis = 3
                    axis_bit = 0
                if c_bit >= log_c and axis == 3:
                    axis = -1
                    axis_bit = 0

                if axis_bit >= x_merge and axis == 0:
                    axis = 1
                    axis_bit = 0
                    choosing_axis = True
                if axis_bit >= y_merge and axis == 1:
                    axis = 2
                    axis_bit = 0
                    choosing_axis = True
                if axis_bit >= z_merge and axis == 2:
                    axis = 3
                    axis_bit = 0
                    choosing_axis = True
                if axis_bit >= log_c and axis == 3:
                    axis = -1
                    axis_bit = 0

            if axis == 0:
                x_mask.append(bit_shifts[0])
                bit_shifts[0] -= 1
                x_bit += 1
            elif axis == 1:
                y_mask.append(bit_shifts[1])
                bit_shifts[1] -= 1
                y_bit += 1
            elif axis == 2:
                z_mask.append(bit_shifts[2])
                bit_shifts[2] -= 1
                z_bit += 1
            elif axis == 3:
                c_mask.append(bit_shifts[3])
                bit_shifts[3] -= 1
                c_bit += 1

            bit_shifts[0] += 1
            bit_shifts[1] += 1
            bit_shifts[2] += 1
            bit_shifts[3] += 1
            axis_bit += 1

        x_rem = log_w - x_merge
        y_rem = log_h - y_merge
        z_rem = log_d - z_merge

        shift = (x_merge + y_merge + z_merge + log_c)

        x_mask.extend([shift - len(x_mask)]*x_rem)
        y_mask.extend([shift + x_rem - len(y_mask)]*y_rem)
        z_mask.extend([shift + x_rem + y_rem - len(z_mask)]*z_rem)
