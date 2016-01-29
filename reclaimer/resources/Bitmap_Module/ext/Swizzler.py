from array import array
from math import ceil
from traceback import format_exc
import time

Logs_of_2 = {}

for Log in range(64):
    Logs_of_2[2**Log] = Log

    
class Swizzler():
    '''THIS SWIZZLER PLUGS INTO THE BITMAP CONVERTOR AND EXPECTS IT TO CONTAIN CERTAIN VARIABLES.
    This module was split to make it easier to navigate the bitmap convertor and swizzler'''

    def __init__(self, **kwargs):
        if "Texture_Convertor" in kwargs and "Mask_Type" in kwargs:
            self.Convertor = kwargs["Texture_Convertor"]
            self.Swizzler_Mask = Swizzler_Mask(**kwargs)
        else: self.Convertor = None


    def Swizzle_Texture(self, Force_Swizzle=False, Delete_Old_Array=True):
        '''this is the function to call if you want to swizzle or
        unswizzle an entire texture, mipmaps, cube faces and all'''
        if self.Convertor is None:
            return(False)
        
        if self.Convertor.Texture_Block is not None:
            '''if we are forcing the texture to be swizzled or deswizzled then we set
            the swizzle mode to the inverse of whether or not it is swizzled'''
            if Force_Swizzle:
                Swizzler_Mode = not(self.Convertor.Swizzled)
            else: Swizzler_Mode = self.Convertor.Swizzler_Mode

            #only run if the texture is swizzled and we want to unswizzle it or vice versa.
            #this prevents it from unswizzling a bitmap that's unswizzled and vice versa.
            #also check that that the bitmap is being saved to a format that supports swizzling
            if Swizzler_Mode != self.Convertor.Swizzled:
                #this variable is used to keep track of which pixel array we are reading
                Current_Block_Index = 0

                #make the variables to hold the width, height, and depth as we iterate over the mipmaps
                Width, Height, Depth = self.Convertor.Width, self.Convertor.Height, self.Convertor.Depth

                for Mipmap in range(self.Convertor.Mipmap_Count+1):
                    
                    for Sub_Bitmap in range(self.Convertor.Sub_Bitmap_Count):
                        #get the pixel array to be swizzled/unswizzled
                        Original_Pixel_Array = self.Convertor.Texture_Block[Current_Block_Index]
                        Swizzled_Pixel_Array = None
                        
                        #make the new array to place the swizzled data into
                        if isinstance(Original_Pixel_Array, array):
                            Swizzled_Pixel_Array = array(Original_Pixel_Array.typecode,
                                                         Original_Pixel_Array)
                        elif isinstance(Original_Pixel_Array, bytearray):
                            Swizzled_Pixel_Array = bytearray(Original_Pixel_Array)
                        
                        if Swizzled_Pixel_Array is not None:
                            if self.Convertor.Packed: UCC = 1
                            else: UCC = self.Convertor.Unpacked_Channel_Count
                                
                            self._Swizzle_Block_Function(Swizzler_Mode, Original_Pixel_Array,
                                                         Swizzled_Pixel_Array, UCC, Width, Height, Depth)

                            #replace the old pixel array with the new swizzled one
                            self.Convertor.Texture_Block[Current_Block_Index] = Swizzled_Pixel_Array

                            #delete the old pixel array
                            if Delete_Old_Array:
                                #delete the old pixel array
                                del Original_Pixel_Array[:]
                        else:
                            raise TypeError('Pixel array is not the proper type.'+
                                            'Expected array.array or bytearray, got %s'
                                            % type(Original_Pixel_Array))
                            
                        Current_Block_Index += 1

                    #we're going to the next lowest mipmap level so we halve the resolution
                    Width = int(ceil(Width/2))
                    Height = int(ceil(Height/2))
                    Depth = int(ceil(Depth/2))
    
                #now that we're done swizzling or unswizzling the bitmap we invert the booleans
                self.Convertor.Swizzled = not(self.Convertor.Swizzled)
        else:
            print("ERROR: NO TEXTURE LOADED. CANNOT PREFORM SWIZZLE OPERATION WITHOUT A LOADED TEXTURE")
            return(False)
        
        #no errors occurred so we return a success
        return(True)



    def Swizzle_Single_Array(self, Original_Array, Swizzler_Mode,
                             Channel_Count, Width, Height, Depth=1,
                             Delete_Old_Array=True):
        '''this is the function to call if you just
        want to swizzle or unswizzle a single array
        Swizzler_Mode: True = Swizzle    False = Deswizzle'''
        try:
            Swizzled_Array = None
            
            #make the new array to place the swizzled data into
            if isinstance(Original_Array, array):
                Swizzled_Array = array(Original_Array.typecode,
                                       Original_Array)
            elif isinstance(Original_Array, bytearray):
                Swizzled_Array = bytearray(Original_Array)
            
            if Swizzled_Array is not None:
                self._Swizzle_Block_Function(Swizzler_Mode, Original_Array, Swizzled_Array,
                                             Channel_Count, Width, Height, Depth)
                
                if Delete_Old_Array:
                    #delete the old pixel array
                    del Original_Array[:]
                
                return(Swizzled_Array)
            else:
                raise TypeError('Array is not the proper type.'+
                                'Expected array.array or bytearray, got %s'
                                % type(Original_Array))
        except:
            print("ERROR OCCURRED WHILE TRYING TO SWIZZLE ARRAY")
            print(format_exc())
            return(False)


    def _Swizzle_Block_Function(self, Swizzler_Mode, Original_Array, Swizzled_Array,
                                Channels, Width, Height, Depth):
        '''this function should only be called by one of the
        above two functions. this swizzler only works with
        entire pixels and can't swizzle individual channels'''

        #this is the number of bits per axis. We'll use it
        #when calculating how much to bitshift the offsets
        C_Blocks, X_Blocks, Y_Blocks, Z_Blocks = (Logs_of_2[Channels],
                                                  Logs_of_2[Width],
                                                  Logs_of_2[Height],
                                                  Logs_of_2[Depth])

        #these are the masks that will be used for calculating the swizzled offsets
        C_Mask, X_Mask, Y_Mask, Z_Mask = (array("B",[]), array("B",[]), array("B",[]), array("B",[]))
        
        #generate the mask for the swizzler pattern
        self.Swizzler_Mask.Mask_Set(C_Blocks, X_Blocks, Y_Blocks, Z_Blocks,
                                    C_Mask,   X_Mask,   Y_Mask,   Z_Mask)

        Bit_Swizzler = self._Bit_Swizzler

        #swizzle the bits of the offsets. supports up to 2^32 array elements(4GB if each element is 1 byte)
        C_Block_Offsets = array("I", map(Bit_Swizzler, range(Channels), (C_Mask,)*Channels))
        X_Block_Offsets = array("I", map(Bit_Swizzler, range(Width), (X_Mask,)*Width))
        Y_Block_Offsets = array("I", map(Bit_Swizzler, range(Height), (Y_Mask,)*Height))
        Z_Block_Offsets = array("I", map(Bit_Swizzler, range(Depth), (Z_Mask,)*Depth))
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        Array_Index = 0
        #Swizzler_Mode: True = Swizzle    False = Deswizzle
        if Swizzler_Mode:
            if Channels == 1:
                for Z in Z_Block_Offsets:
                    for Y in Y_Block_Offsets:
                        ZY = Z+Y
                        for X in X_Block_Offsets:
                            Swizzled_Array[ZY+X] = Original_Array[Array_Index]
                            
                            Array_Index += 1
            else:
                for Z in Z_Block_Offsets:
                    for Y in Y_Block_Offsets:
                        ZY = Z+Y
                        for X in X_Block_Offsets:
                            ZYX = ZY+X
                            for C in C_Block_Offsets:
                                Swizzled_Array[ZYX+C] = Original_Array[Array_Index]
                                
                                Array_Index += 1
        else:
            if Channels == 1:
                for Z in Z_Block_Offsets:
                    for Y in Y_Block_Offsets:
                        ZY = Z+Y
                        for X in X_Block_Offsets:
                            Swizzled_Array[Array_Index] = Original_Array[ZY+X]
                            
                            Array_Index += 1
            else:
                for Z in Z_Block_Offsets:
                    for Y in Y_Block_Offsets:
                        ZY = Z+Y
                        for X in X_Block_Offsets:
                            ZYX = ZY+X                       
                            for C in C_Block_Offsets:
                                Swizzled_Array[Array_Index] = Original_Array[ZYX+C]
                                
                                Array_Index += 1
        
    
    def _Bit_Swizzler(self, Axis_Offset, Axis_Mask):
        '''Axis_Offset is the X, Y, or Z index who's bits we are swizzling
        Axis_Mask is an array which is the length of Log2(Dimension). Each index
        corrosponds to the equivelant bit in the dimension's binary form. The value
        of each index is how far left the bit should be shifted. if the value is
        negative then the bit will instead be shifted to the right by that amount.'''
        
        #this will be used to store the index after we swizzle it's bits
        Swizzled_Axis_Offset = 0

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        #we loop through each of the bits in the Axis_Offset
        for Bit_Idx in range(len(Axis_Mask)):
            '''Mask off the value of the bit, shift it to the index it needs to be
            in, and add the result to the return value "Swizzled_Axis_Offset" '''
            if Axis_Mask[Bit_Idx] < 0:
                Swizzled_Axis_Offset += (Axis_Offset&(1<<Bit_Idx)) >> (-1*Axis_Mask[Bit_Idx])
            else:
                Swizzled_Axis_Offset += (Axis_Offset&(1<<Bit_Idx)) << Axis_Mask[Bit_Idx]
        
        return(Swizzled_Axis_Offset)
    


class Swizzler_Mask():
    """This swizzler uses a z-order curve based swizzling routine, but the exact pattern is modifiable.
    Currently there is a Morton style nested Z swizzle pattern, a pattern which will place pixels within
    a certain size square directly next to each other(for merging together), and a pattern that will
    place pixels within a 4x4 square directly next to each other(to aid in calculating DXT texels)"""

    def __init__(self, **kwargs):
        '''this is a list of functions to swizzle masks in different formats.
        unless more are added the default will be the only available one.
        Default is Z-order curve, or morton order'''
        self.Masks = {"DEFAULT":self._Z_Order_Mask_Set,
                      "MORTON":self._Z_Order_Mask_Set,
                      "DXT_CALC":self._DXT_Calculation_Mask_Set,
                      "DOWNSAMPLER":self._Pixel_Merge_Mask_Set}
        
        self.Swizzler_Settings = kwargs
    
        if "Mask_Type" in kwargs and kwargs["Mask_Type"] in self.Masks:
            self.Mask_Set = self.Masks[kwargs["Mask_Type"]]
        else: print("ERROR: UNKNOWN SWIZZLER MASK TYPE.")


    def Mask_Set(self, *args, **kwargs):
        '''PLACEHOLDER'''
        pass


    def _Z_Order_Mask_Set(self, C_Blocks, X_Blocks, Y_Blocks, Z_Blocks,
                                C_Mask,   X_Mask,   Y_Mask,   Z_Mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF X, Y, AND Z OFFSETS
        TOGETHER IN Z-ORDER STYLE. THE COLOR CHANNELS CAN ALSO BE SWIZZLED"""

        #do this separately and FIRST. its not likely that
        #we want swizzled channels so we do this separate
        C_Mask.extend( [0] * C_Blocks )
        Current_Bit = C_Blocks
        
        #Loop for each of the bits in the largest dimension
        for BLOCK_SIZE in range(max(X_Blocks, Y_Blocks, Z_Blocks)):
            """WE CHECK IF THERE ARE STILL ANY BITS FOR EACH AXIS"""
                
            if X_Blocks > BLOCK_SIZE:
                X_Mask.append(Current_Bit)
                Current_Bit += 1
                
            if Y_Blocks > BLOCK_SIZE:
                Y_Mask.append(Current_Bit)
                Current_Bit += 1
                
            if Z_Blocks > BLOCK_SIZE:
                Z_Mask.append(Current_Bit)
                Current_Bit += 1
                
            Current_Bit -= 1


    def _DXT_Calculation_Mask_Set(self, Log_C,  Log_X,  Log_Y,  Log_Z,
                                        C_Mask, X_Mask, Y_Mask, Z_Mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF X, Y, AND Z, AND CHANNEL OFFSETS
        TOGETHER SO THAT ALL PIXELS PER DXT TEXEL ARE ADJACENT EACH OTHER"""

        
        """MAKES IT SO THE FIRST BITS ARE THE CHANNEL AXIS, NEXT TWO BITS ARE THE
        X AXIS, AND THE NEXT 2 BITS ARE THE Y AXIS. THE REMAINDER OF THE X BITS ARE NEXT,
        FOLLOWED BY THE REMAINDER OF THE Y BITS, FOLLOWED BY THE REMAINDER OF THE Z BITS"""

        Tmp_X = Log_X
        Tmp_Y = Log_Y
        if Tmp_X > 2: Tmp_X = 2
        if Tmp_Y > 2: Tmp_Y = 2

        C_Mask.extend([0]*Log_C)
        X_Mask.extend([Log_C]*Tmp_X)
        Y_Mask.extend([Log_C+Tmp_X]*Tmp_Y)
        
        Z_Mask.extend([Log_C+Tmp_X+Tmp_Y]*Log_Z)
        
        X_Mask.extend([Log_C+Tmp_Y+Log_Z]*(Log_X-Tmp_X) )

        Y_Mask.extend([Log_C+Log_X+Log_Z]*(Log_Y-Tmp_Y) )


    def _Pixel_Merge_Mask_Set(self, Log_C,  Log_W,  Log_H,  Log_D,
                                    C_Mask, X_Mask, Y_Mask, Z_Mask):
        """THIS FUNCTION WILL SWIZZLE AN ARRAY OF C, X, Y, AND Z OFFSETS IN SUCH
        A WAY THAT THE PIXELS BEING MERGED END UP DIRECTLY ADJACENT EACH OTHER"""
        Current_Bit = 0
        
        New_Width, New_Height, New_Depth = (self.Swizzler_Settings["New_Width"],
                                            self.Swizzler_Settings["New_Height"],
                                            self.Swizzler_Settings["New_Depth"])
        
        #these are how many blocks are being merged on eachs of the axis
        Log_X_Merge = Log_W - Logs_of_2[New_Width]
        Log_Y_Merge = Log_H - Logs_of_2[New_Height]
        Log_Z_Merge = Log_D - Logs_of_2[New_Depth]

        """so we can properly swizzle each of the axis we need to know
        which one we are currently working on and ONLY increment that
        one. when we have reached the last bit for that axis this number
        is incremented. when this number reaches 4 it is reset to 0."""
        Current_Axis = 0
        Current_Axis_Bit = 0
        Bit_Shift_Amounts = [0,0,0,0]
        
        Current_X_Bit = 0
        Current_Y_Bit = 0
        Current_Z_Bit = 0
        Current_C_Bit = 0
        
        #Loop for each of the bits in the integer (W*H*D*C)
        for Current_Bit in range(Log_X_Merge + Log_Y_Merge + Log_Z_Merge + Log_C):
            Selecting_Axis = True

            while Selecting_Axis:
                Selecting_Axis = False
                
                if Current_X_Bit >= Log_W and Current_Axis == 0:
                    Current_Axis = 1
                    Current_Axis_Bit = 0
                if Current_Y_Bit >= Log_H and Current_Axis == 1:
                    Current_Axis = 2
                    Current_Axis_Bit = 0
                if Current_Z_Bit >= Log_D and Current_Axis == 2:
                    Current_Axis = 3
                    Current_Axis_Bit = 0
                if Current_C_Bit >= Log_C and Current_Axis == 3:
                    Current_Axis = -1
                    Current_Axis_Bit = 0
                    
                
                if Current_Axis_Bit >= Log_X_Merge and Current_Axis == 0:
                    Current_Axis = 1
                    Current_Axis_Bit = 0
                    Selecting_Axis = True
                if Current_Axis_Bit >= Log_Y_Merge and Current_Axis == 1:
                    Current_Axis = 2
                    Current_Axis_Bit = 0
                    Selecting_Axis = True
                if Current_Axis_Bit >= Log_Z_Merge and Current_Axis == 2:
                    Current_Axis = 3
                    Current_Axis_Bit = 0
                    Selecting_Axis = True
                if Current_Axis_Bit >= Log_C and Current_Axis == 3:
                    Current_Axis = -1
                    Current_Axis_Bit = 0
            
            if Current_Axis == 0:
                X_Mask.append(Bit_Shift_Amounts[0])
                Bit_Shift_Amounts[0] -= 1
                Current_X_Bit += 1
            elif Current_Axis == 1:
                Y_Mask.append(Bit_Shift_Amounts[1])
                Bit_Shift_Amounts[1] -= 1
                Current_Y_Bit += 1
            elif Current_Axis == 2:
                Z_Mask.append(Bit_Shift_Amounts[2])
                Bit_Shift_Amounts[2] -= 1
                Current_Z_Bit += 1
            elif Current_Axis == 3:
                C_Mask.append(Bit_Shift_Amounts[3])
                Bit_Shift_Amounts[3] -= 1
                Current_C_Bit += 1
            
            Bit_Shift_Amounts[0] += 1
            Bit_Shift_Amounts[1] += 1
            Bit_Shift_Amounts[2] += 1
            Bit_Shift_Amounts[3] += 1
            Current_Axis_Bit += 1
            
        X_Remainder = Log_W-Log_X_Merge
        Y_Remainder = Log_H-Log_Y_Merge
        Z_Remainder = Log_D-Log_Z_Merge

        Shift_Amount = (Log_X_Merge + Log_Y_Merge + Log_Z_Merge + Log_C)
        
        X_Mask.extend([Shift_Amount-len(X_Mask)]*X_Remainder)
        Y_Mask.extend([Shift_Amount+X_Remainder-len(Y_Mask)]*Y_Remainder)
        Z_Mask.extend([Shift_Amount+X_Remainder+Y_Remainder-len(Z_Mask)]*Z_Remainder)
