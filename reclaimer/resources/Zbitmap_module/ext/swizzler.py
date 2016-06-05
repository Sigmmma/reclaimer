from array import array
from math import ceil
from traceback import format_exc
import time

logs_of_2 = {}

for log in range(64):
    logs_of_2[2**log] = log

    
class Swizzler():
    '''THIS SWIZZLER PLUGS INTO THE BITMAP CONVERTOR
    AND EXPECTS IT TO CONTAIN CERTAIN VARIABLES.
    This module was split to make it easier to
    navigate the bitmap convertor and swizzler'''

    def __init__(self, **kwargs):
        if "texture_converter" in kwargs and "mask_type" in kwargs:
            self.converter = kwargs["texture_converter"]
            self.swizzler_mask = SwizzlerMask(**kwargs)
        else:
            self.converter = None


    def swizzle_texture(self, force_swizzle=False, delete_old_array=True):
        '''this is the function to call if you want to swizzle or
        unswizzle an entire texture, mipmaps, cube faces and all'''
        if self.converter is None:
            return False
        
        if self.converter.texture_block is not None:
            '''if we are forcing the texture to be swizzled or deswizzled then we set
            the swizzle mode to the inverse of whether or not it is swizzled'''
            if force_swizzle:
                swizzler_mode = not(self.converter.swizzled)
            else:
                swizzler_mode = self.converter.swizzler_mode

            #only run if the texture is swizzled and we want to unswizzle it or vice versa.
            #this prevents it from unswizzling a bitmap that's unswizzled and vice versa.
            #also check that that the bitmap is being saved to a format that supports swizzling
            if swizzler_mode != self.converter.swizzled:
                #this variable is used to keep track of which pixel array we are reading
                curr_b_index = 0

                #make the variables to hold the width, height, and depth as we iterate over the mipmaps
                width, height, depth = (self.converter.width,
                                        self.converter.height,
                                        self.converter.depth)

                for mipmap in range(self.converter.mipmap_count+1):
                    
                    for sub_bitmap in range(self.converter.sub_bitmap_count):
                        #get the pixel array to be swizzled/unswizzled
                        orig_pixel_array = self.converter.texture_block[curr_b_index]
                        swizzled_pixel_array = None
                        
                        #make the new array to place the swizzled data into
                        if isinstance(orig_pixel_array, array):
                            swizzled_pixel_array = array(orig_pixel_array.typecode,
                                                         orig_pixel_array)
                        elif isinstance(orig_pixel_array, bytearray):
                            swizzled_pixel_array = bytearray(orig_pixel_array)
                        
                        if swizzled_pixel_array is not None:
                            if self.converter.packed:
                                ucc = 1
                            else:
                                ucc = self.converter.unpacked_channel_count
                                
                            self._swizzle_block(swizzler_mode, orig_pixel_array,
                                                swizzled_pixel_array, ucc,
                                                width, height, depth)

                            #replace the old pixel array with the new swizzled one
                            self.converter.texture_block[curr_b_index] = swizzled_pixel_array

                            #delete the old pixel array
                            if delete_old_array:
                                #delete the old pixel array
                                del orig_pixel_array[:]
                        else:
                            raise TypeError('Pixel array is not the proper type.'+
                                            'Expected array.array or bytearray, got %s'
                                            % type(orig_pixel_array))
                            
                        curr_b_index += 1

                    #we're going to the next lowest mipmap level so we halve the resolution
                    width = int(ceil(width/2))
                    height = int(ceil(height/2))
                    depth = int(ceil(depth/2))
    
                #now that we're done (un)swizzling
                #the bitmap we invert the boolean
                self.converter.swizzled = not(self.converter.swizzled)
        else:
            print("ERROR: NO TEXTURE LOADED. CANNOT PREFORM "+
                  "SWIZZLE OPERATION WITHOUT A LOADED TEXTURE")
            return False
        
        #no errors occurred so we return a success
        return True



    def swizzle_single_array(self, orig_array, swizzler_mode,
                             channel_count, width, height, depth=1,
                             delete_old_array=True):
        '''this is the function to call if you just
        want to swizzle or unswizzle a single array
        swizzler_mode: True = Swizzle    False = Deswizzle'''
        try:
            swizzled_array = None
            
            #make the new array to place the swizzled data into
            if isinstance(orig_array, array):
                swizzled_array = array(orig_array.typecode, orig_array)
            elif isinstance(orig_array, bytearray):
                swizzled_array = bytearray(orig_array)
            
            if swizzled_array is not None:
                self._swizzle_block(swizzler_mode, orig_array, swizzled_array,
                                     channel_count, width, height, depth)
                
                if delete_old_array:
                    #delete the old pixel array
                    del orig_array[:]
                
                return swizzled_array
            else:
                raise TypeError('Array is not the proper type.'+
                                'Expected array.array or bytearray, got %s'
                                % type(orig_array))
        except:
            print("ERROR OCCURRED WHILE TRYING TO SWIZZLE ARRAY")
            print(format_exc())
            return False


    def _swizzle_block(self, swizzler_mode, orig_array, swizzled_array,
                        channels, width, height, depth):
        '''this function should only be called by one of the
        above two functions. this swizzler only works with
        entire pixels and can't swizzle individual channels'''

        #this is the number of bits per axis. We'll use it
        #when calculating how much to bitshift the offsets
        c_blocks, x_blocks, y_blocks, z_blocks = (logs_of_2[channels],
                                                  logs_of_2[width],
                                                  logs_of_2[height],
                                                  logs_of_2[depth])

        #these are the masks that will be used for calculating the swizzled offsets
        c_mask, x_mask, y_mask, z_mask = (array("B",[]), array("B",[]),
                                          array("B",[]), array("B",[]))
        
        #generate the mask for the swizzler pattern
        self.swizzler_mask.mask_set(c_blocks, x_blocks, y_blocks, z_blocks,
                                    c_mask,   x_mask,   y_mask,   z_mask)

        bit_swizzler = self._bit_swizzler

        #swizzle the bits of the offsets. supports up to 2^32 array elements(4GB if each element is 1 byte)
        c_block_offs = array("I", map(bit_swizzler, range(channels), (c_mask,)*channels))
        x_block_offs = array("I", map(bit_swizzler, range(width), (x_mask,)*width))
        y_block_offs = array("I", map(bit_swizzler, range(height), (y_mask,)*height))
        z_block_offs = array("I", map(bit_swizzler, range(depth), (z_mask,)*depth))
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        array_idx = 0
        #swizzler_mode: True = Swizzle    False = Deswizzle
        if swizzler_mode:
            if channels == 1:
                for z in z_block_offs:
                    for y in y_block_offs:
                        zy = z+y
                        for x in x_block_offs:
                            swizzled_array[zy+x] = orig_array[array_idx]
                            
                            array_idx += 1
            else:
                for z in z_block_offs:
                    for y in y_block_offs:
                        zy = z+y
                        for x in x_block_offs:
                            zyx = zy+x
                            for c in c_block_offs:
                                swizzled_array[zyx+c] = orig_array[array_idx]
                                
                                array_idx += 1
        else:
            if channels == 1:
                for z in z_block_offs:
                    for y in y_block_offs:
                        zy = z+y
                        for x in x_block_offs:
                            swizzled_array[array_idx] = orig_array[zy+x]
                            
                            array_idx += 1
            else:
                for z in z_block_offs:
                    for y in y_block_offs:
                        zy = z+y
                        for x in x_block_offs:
                            zyx = zy+x                       
                            for c in c_block_offs:
                                swizzled_array[array_idx] = orig_array[zyx+c]
                                
                                array_idx += 1
        
    
    def _bit_swizzler(self, axis_offset, axis_mask):
        '''axis_offset is the x, y, or z index who's bits we are swizzling
        axis_mask is an array which is the length of Log2(Dimension). Each index
        corrosponds to the equivelant bit in the dimension's binary form. The value
        of each index is how far left the bit should be shifted. if the value is
        negative then the bit will instead be shifted to the right by that amount.'''
        
        #this will be used to store the index after we swizzle it's bits
        swizzled_axis_offset = 0

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        #we loop through each of the bits in the axis_offset
        for bit_idx in range(len(axis_mask)):
            '''Mask off the value of the bit, shift it to the index it needs to be
            in, and add the result to the return value "swizzled_axis_offset" '''
            if axis_mask[bit_idx] < 0:
                swizzled_axis_offset += (axis_offset&(1<<bit_idx)) >> (-1*axis_mask[bit_idx])
            else:
                swizzled_axis_offset += (axis_offset&(1<<bit_idx)) << axis_mask[bit_idx]
        
        return swizzled_axis_offset
    


class SwizzlerMask():
    """This swizzler uses a z-order curve based swizzling routine, but the exact pattern is modifiable.
    Currently there is a Morton style nested z swizzle pattern, a pattern which will place pixels within
    a certain size square directly next to each other(for merging together), and a pattern that will
    place pixels within a 4x4 square directly next to each other(to aid in calculating DXT texels)"""

    def __init__(self, **kwargs):
        '''this is a list of functions to swizzle masks in different formats.
        unless more are added the default will be the only available one.
        Default is z-order curve, or morton order'''
        self.masks = {"DEFAULT":self._z_order_mask_set,
                      "MORTON":self._z_order_mask_set,
                      "DXT_CALC":self._dxt_calculation_mask_set,
                      "DOWNSAMPLER":self._pixel_merge_mask_set}
        
        self.swizzler_settings = kwargs
    
        if "mask_type" in kwargs and kwargs["mask_type"] in self.masks:
            self.mask_set = self.masks[kwargs["mask_type"]]
        else:
            print("ERROR: UNKNOWN SWIZZLER MASK TYPE.")


    def mask_set(self, *args, **kwargs):
        '''PLACEHOLDER'''
        pass


    def _z_order_mask_set(self, c_blocks, x_blocks, y_blocks, z_blocks,
                          c_mask,   x_mask,   y_mask,   z_mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF x, y, AND z OFFSETS
        TOGETHER IN z-ORDER STYLE. THE COLOR CHANNELS CAN ALSO BE SWIZZLED"""

        #do this separately and FIRST. its not likely that
        #we want swizzled channels so we do this separate
        c_mask.extend( [0] * c_blocks )
        current_bit = c_blocks
        
        #Loop for each of the bits in the largest dimension
        for BLOCK_SIZE in range(max(x_blocks, y_blocks, z_blocks)):
            """WE CHECK IF THERE ARE STILL ANY BITS FOR EACH AXIS"""
                
            if x_blocks > BLOCK_SIZE:
                x_mask.append(current_bit)
                current_bit += 1
                
            if y_blocks > BLOCK_SIZE:
                y_mask.append(current_bit)
                current_bit += 1
                
            if z_blocks > BLOCK_SIZE:
                z_mask.append(current_bit)
                current_bit += 1
                
            current_bit -= 1


    def _dxt_calculation_mask_set(self, log_c,  log_x,  log_y,  log_z,
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
        
        x_mask.extend([log_c+tmp_y+log_z]*(log_x-tmp_x) )

        y_mask.extend([log_c+log_x+log_z]*(log_y-tmp_y) )


    def _pixel_merge_mask_set(self, log_c,  log_w,  log_h,  log_d,
                              c_mask, x_mask, y_mask, z_mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF C, X, Y,
        AND Z OFFSETS IN SUCH A WAY THAT THE PIXELS BEING
        MERGED END UP DIRECTLY ADJACENT EACH OTHER"""
        current_bit = 0
        
        new_width, new_height, new_depth = (self.swizzler_settings["new_width"],
                                            self.swizzler_settings["new_height"],
                                            self.swizzler_settings["new_depth"])
        
        #these are how many blocks are being merged on eachs of the axis
        log_x_merge = log_w - logs_of_2[new_width]
        log_y_merge = log_h - logs_of_2[new_height]
        log_z_merge = log_d - logs_of_2[new_depth]

        """so we can properly swizzle each of the axis we need to know
        which one we are currently working on and ONLY increment that
        one. when we have reached the last bit for that axis this number
        is incremented. when this number reaches 4 it is reset to 0."""
        current_axis = 0
        current_axis_bit = 0
        bit_shift_amounts = [0,0,0,0]
        
        curr_x_bit = 0
        curr_y_bit = 0
        curr_z_bit = 0
        current_c_bit = 0
        
        #Loop for each of the bits in the integer (W*H*D*C)
        for current_bit in range(log_x_merge+log_y_merge+log_z_merge+log_c):
            selecting_axis = True

            while selecting_axis:
                selecting_axis = False
                
                if curr_x_bit >= log_w and current_axis == 0:
                    current_axis = 1
                    current_axis_bit = 0
                if curr_y_bit >= log_h and current_axis == 1:
                    current_axis = 2
                    current_axis_bit = 0
                if curr_z_bit >= log_d and current_axis == 2:
                    current_axis = 3
                    current_axis_bit = 0
                if current_c_bit >= log_c and current_axis == 3:
                    current_axis = -1
                    current_axis_bit = 0
                    
                
                if current_axis_bit >= log_x_merge and current_axis == 0:
                    current_axis = 1
                    current_axis_bit = 0
                    selecting_axis = True
                if current_axis_bit >= log_y_merge and current_axis == 1:
                    current_axis = 2
                    current_axis_bit = 0
                    selecting_axis = True
                if current_axis_bit >= log_z_merge and current_axis == 2:
                    current_axis = 3
                    current_axis_bit = 0
                    selecting_axis = True
                if current_axis_bit >= log_c and current_axis == 3:
                    current_axis = -1
                    current_axis_bit = 0
            
            if current_axis == 0:
                x_mask.append(bit_shift_amounts[0])
                bit_shift_amounts[0] -= 1
                curr_x_bit += 1
            elif current_axis == 1:
                y_mask.append(bit_shift_amounts[1])
                bit_shift_amounts[1] -= 1
                curr_y_bit += 1
            elif current_axis == 2:
                z_mask.append(bit_shift_amounts[2])
                bit_shift_amounts[2] -= 1
                curr_z_bit += 1
            elif current_axis == 3:
                c_mask.append(bit_shift_amounts[3])
                bit_shift_amounts[3] -= 1
                current_c_bit += 1
            
            bit_shift_amounts[0] += 1
            bit_shift_amounts[1] += 1
            bit_shift_amounts[2] += 1
            bit_shift_amounts[3] += 1
            current_axis_bit += 1
            
        x_remainder = log_w-log_x_merge
        y_remainder = log_h-log_y_merge
        z_remainder = log_d-log_z_merge

        shift_amount = (log_x_merge + log_y_merge + log_z_merge + log_c)
        
        x_mask.extend([shift_amount-len(x_mask)]*x_remainder)
        y_mask.extend([shift_amount+x_remainder-len(y_mask)]*y_remainder)
        z_mask.extend([shift_amount+x_remainder+y_remainder-len(z_mask)]*z_remainder)
