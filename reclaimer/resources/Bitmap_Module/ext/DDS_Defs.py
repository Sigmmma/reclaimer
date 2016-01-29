
from array import array
from math import sqrt

#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
BC = None

def Combine(Main_Dict, *Dicts):        
    for Dict in Dicts:
        for key in Dict:
            if key in Main_Dict:
                if (isinstance(Dict[key], dict) and
                    isinstance(Main_Dict[key], dict)):
                    Combine(Main_Dict[key], Dict[key])
            else:
                Main_Dict[key] = Dict[key]
    return(Main_Dict)


def Initialize():
    """FOR DXT FORMATS, ALPHA CHANNELS ARE TREATED SPECIALLY, BUT ARE EXPLICITELY
    PLACED HERE TO MAKE SURE THEY DONT CAUSE THE CHANNEL MAP SWAPPING PROBLEMS"""
    
    BC.FORMAT_DXT1 = "DXT1"
    BC.FORMAT_DXT2 = "DXT2"
    BC.FORMAT_DXT3 = "DXT3"
    BC.FORMAT_DXT4 = "DXT4"
    BC.FORMAT_DXT5 = "DXT5"

    BC.FORMAT_DXT3A = "DXT3A"           #NOT YET IMPLEMENTED
    BC.FORMAT_DXT3A1111 = "DXT3A1111"   #NOT YET IMPLEMENTED
    
    BC.FORMAT_DXT5NM = "DXT5NM"         #NOT YET IMPLEMENTED
    BC.FORMAT_DXN = "DXN"
    BC.FORMAT_DXT5A = "DXT5A"           #NOT YET IMPLEMENTED
    BC.FORMAT_DXT5Y = "DXT5Y"           #NOT YET IMPLEMENTED
    BC.FORMAT_DXT5AY = "DXT5AY"         #NOT YET IMPLEMENTED
    
    BC.FORMAT_CXT1 = "CXT1"             #NOT YET IMPLEMENTED
    BC.FORMAT_U8V8 = "U8V8"             #NOT YET IMPLEMENTED

    DXT_Specifications = {'Compressed':True, 'DDS_Format':True,
                          'Min_Width':4, 'Min_Height':4,
                          'Data_Size':'I', 'Channel_Count':4,
                          'Channel_Offsets':(0,11,5,0),
                          'Channel_Masks':(0,63488,2016,31)}


    BC.Define_Format(**Combine({'Format_ID':BC.FORMAT_DXT1, 'BPP':4,
                                'Channel_Depths':(1,5,6,5),
                                'Unpacker':Unpack_DXT1, 'Packer':Pack_DXT1},
                               DXT_Specifications) )
    
    for FORMAT in (BC.FORMAT_DXT2, BC.FORMAT_DXT3):
        BC.Define_Format(**Combine({'Format_ID':FORMAT, 'BPP':8,
                                    'Channel_Depths':(4,5,6,5),
                                    'Unpacker':Unpack_DXT2_3, 'Packer':Pack_DXT2_3},
                                   DXT_Specifications) )
        
    for FORMAT in (BC.FORMAT_DXT4, BC.FORMAT_DXT5):
        BC.Define_Format(**Combine({'Format_ID':FORMAT, 'BPP':8,
                                    'Channel_Depths':(8,5,6,5),
                                    'Unpacker':Unpack_DXT4_5, 'Packer':Pack_DXT4_5},
                                   DXT_Specifications) )
        
    BC.Define_Format(**Combine({'Format_ID':BC.FORMAT_DXN, 'BPP':8,
                                'Channel_Depths':(0,8,8,8),
                                'Unpacker':Unpack_DXN, 'Packer':Pack_DXN,
                                'Channel_Offsets':(0,16,8,0), 'Three_Channels':True,
                                'Channel_Masks':(0,16711680,65280,255)},
                               DXT_Specifications) )
    
    BC.Define_Format(Format_ID=BC.FORMAT_U8V8, BPP=16, Channel_Count=4,
                     Unpacker=Unpack_U8V8, Packer=Pack_U8V8,
                     Channel_Depths=(0,8,8,8), DDS_Format=True,
                     Channel_Offsets=(0,0,8,0), Channel_Masks=(0,255,65280,0))


#used to make dxt1 deciphering faster
DXT1_Indexing_Masks = array("I", [])
DXT1_Indexing_Bit_Shifts = range(0, 32, 2)

#used to make dxt3 deciphering faster
DXT3_Alpha_Masks = array("Q", [])
DXT3_Alpha_Bit_Shifts = range(0, 64, 4)

#used to make dxt5 deciphering faster
DXT5_Alpha_Masks = array("Q", [])
DXT5_Alpha_Bit_Shifts = range(0, 48, 3)

#used to scale DXT pixel values up to 8-bit
DXT_R_Scale = array("B", [])
DXT_G_Scale = array("B", [])
DXT_B_Scale = array("B", [])

Range_16 = range(16)


for i in Range_16:
    DXT1_Indexing_Masks.append(3<<(i*2))
    DXT3_Alpha_Masks.append(15<<(i*4))
    DXT5_Alpha_Masks.append(7<<(i*3))


for Value in range(32):
    DXT_R_Scale.append(int(round( Value * (255/31) )))
    DXT_B_Scale.append(int(round( Value * (255/31) )))
for Value in range(64):
    DXT_G_Scale.append(int(round( Value * (255/63) )))



def Unpack_DXT1(self, Bitmap_Index, Width, Height, Depth=1):
    '''this function takes the loaded DXT1 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Packed_Pixel_Array = self.Texture_Block[Bitmap_Index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    Unpacked_Pixel_Array = array(self._UNPACK_ARRAY_CODE,
                                 [0]*Width*Height*self.Unpacked_Channel_Count )
    UPA = Unpacked_Pixel_Array

    #create the arrays to hold the color channel data
    Color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    Colors = [Color_0, Color_1, Color_2, Color_3]

    ################################################
    """CURRENTLY THE DXT UNPACKING ROUTINES DO NOT
    SUPPORT DROPPING CHANNELS WHILE UNPACKING. I SEE NO
    REASON TO IMPLEMENT IT AS IT WOULD BE VERY SLOW."""
    ################################################

    R_Scale = DXT_R_Scale
    G_Scale = DXT_G_Scale
    B_Scale = DXT_B_Scale
    
    Channel_0 = self.Channel_Mapping.index(0)
    Channel_1 = self.Channel_Mapping.index(1)
    Channel_2 = self.Channel_Mapping.index(2)
    Channel_3 = self.Channel_Mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    Texel_Pixel_Mapping = Get_Texel_Mapping(Width, Height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    Texel_X_Pixel_Offsets = range(0, Texel_Width*16, 16)
    Texel_Y_Pixel_Offsets = range(0, Texel_Height*16*Width, 16*Width)
    
    #loop through each texel
    for Current_Index in range(len(Packed_Pixel_Array)//2):

        #get the offset to use
        Texel_Offset = (Texel_X_Pixel_Offsets[Current_Index%Texel_Width] +
                        Texel_Y_Pixel_Offsets[Current_Index//Texel_Width])
        
        """if the format DXT1 then the two entries in the array
        are the colors and the color indexing in that order."""
        COLOR_0 = Packed_Pixel_Array[Current_Index*2] & 65535
        COLOR_1 = (Packed_Pixel_Array[Current_Index*2] & 4294901760) >> 16
        INDEXING = Packed_Pixel_Array[Current_Index*2+1]

        """unpack the colors"""
        Color_0[1] = R_Scale[(COLOR_0 & 63488) >> 11]
        Color_0[2] = G_Scale[(COLOR_0 & 2016) >> 5]
        Color_0[3] = B_Scale[COLOR_0 & 31]
        
        Color_1[1] = R_Scale[(COLOR_1 & 63488) >> 11]
        Color_1[2] = G_Scale[(COLOR_1 & 2016) >> 5]
        Color_1[3] = B_Scale[COLOR_1 & 31]

        #if the first color is a larger integer then color key transparency is NOT used
        if COLOR_0 > COLOR_1:
            Color_2[1] = (Color_0[1]*2 + Color_1[1])//3
            Color_2[2] = (Color_0[2]*2 + Color_1[2])//3
            Color_2[3] = (Color_0[3]*2 + Color_1[3])//3
            Colors[3] = [255,(Color_0[1] + 2*Color_1[1])//3,
                         (Color_0[2] + 2*Color_1[2])//3,
                         (Color_0[3] + 2*Color_1[3])//3]
        else:
            Color_2[1] = (Color_0[1]+Color_1[1])//2
            Color_2[2] = (Color_0[2]+Color_1[2])//2
            Color_2[3] = (Color_0[3]+Color_1[3])//2
            Colors[3] = [0,0,0,0]
            
        for i in Range_16:
            Color = Colors[(INDEXING & DXT1_Indexing_Masks[i]) >> DXT1_Indexing_Bit_Shifts[i]]
            
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_0] = Color[0]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_1] = Color[1]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_2] = Color[2]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_3] = Color[3]

    return(Unpacked_Pixel_Array)


def Unpack_DXT2_3(self, Bitmap_Index, Width, Height, Depth=1):
    '''this function takes the loaded DXT2/3 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Packed_Pixel_Array = self.Texture_Block[Bitmap_Index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    Unpacked_Pixel_Array = array(self._UNPACK_ARRAY_CODE, [0]*Width*Height*self.Unpacked_Channel_Count )
    UPA = Unpacked_Pixel_Array

    #create the arrays to hold the color channel data
    Color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    Colors = [Color_0, Color_1, Color_2, Color_3]

    Alpha_Masks, Alpha_Bit_Shifts, Alpha_Lookup = DXT3_Alpha_Masks, DXT3_Alpha_Bit_Shifts, self.Channel_Upscalers[0]

    R_Scale = DXT_R_Scale
    G_Scale = DXT_G_Scale
    B_Scale = DXT_B_Scale
    
    Channel_0 = self.Channel_Mapping.index(0)
    Channel_1 = self.Channel_Mapping.index(1)
    Channel_2 = self.Channel_Mapping.index(2)
    Channel_3 = self.Channel_Mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    Texel_Pixel_Mapping = Get_Texel_Mapping(Width, Height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    Texel_X_Pixel_Offsets = range(0, Texel_Width*16, 16)
    Texel_Y_Pixel_Offsets = range(0, Texel_Height*16*Width, 16*Width)
    
    #loop through each texel
    for Current_Index in range(len(Packed_Pixel_Array)//4):

        #get the offset to use
        Texel_Offset = (Texel_X_Pixel_Offsets[Current_Index%Texel_Width] +
                        Texel_Y_Pixel_Offsets[Current_Index//Texel_Width])
        
        #DXT2/3 is much simpler
        ALPHA = (Packed_Pixel_Array[Current_Index*4+1]<<32) + Packed_Pixel_Array[Current_Index*4]
        COLOR_0 = Packed_Pixel_Array[Current_Index*4+2] & 65535
        COLOR_1 = (Packed_Pixel_Array[Current_Index*4+2] & 4294901760) >> 16
        INDEXING = Packed_Pixel_Array[Current_Index*4+3]

        """unpack the colors"""
        Color_0[1] = R_Scale[(COLOR_0 & 63488) >> 11]
        Color_0[2] = G_Scale[(COLOR_0 & 2016) >> 5]
        Color_0[3] = B_Scale[COLOR_0 & 31]
        
        Color_1[1] = R_Scale[(COLOR_1 & 63488) >> 11]
        Color_1[2] = G_Scale[(COLOR_1 & 2016) >> 5]
        Color_1[3] = B_Scale[COLOR_1 & 31]

        Color_2[1] = (Color_0[1]*2 + Color_1[1])//3
        Color_2[2] = (Color_0[2]*2 + Color_1[2])//3
        Color_2[3] = (Color_0[3]*2 + Color_1[3])//3
        Colors[3] = [255,(Color_0[1] + 2*Color_1[1])//3,
                     (Color_0[2] + 2*Color_1[2])//3,
                     (Color_0[3] + 2*Color_1[3])//3]

        for i in Range_16:
            Color = Colors[(INDEXING & DXT1_Indexing_Masks[i]) >> DXT1_Indexing_Bit_Shifts[i]]
            UPA[Texel_Pixel_Mapping[i]+Texel_Offset+Channel_0] = Alpha_Lookup[(ALPHA & Alpha_Masks[i]) >>
                                                                              Alpha_Bit_Shifts[i]]
            UPA[Texel_Pixel_Mapping[i]+Texel_Offset+Channel_1] = Color[1]
            UPA[Texel_Pixel_Mapping[i]+Texel_Offset+Channel_2] = Color[2]
            UPA[Texel_Pixel_Mapping[i]+Texel_Offset+Channel_3] = Color[3]

    return(Unpacked_Pixel_Array)



def Unpack_DXT4_5(self, Bitmap_Index, Width, Height, Depth=1):
    '''this function takes the loaded DXT5 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Packed_Pixel_Array = self.Texture_Block[Bitmap_Index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    Unpacked_Pixel_Array = array(self._UNPACK_ARRAY_CODE, [0]*Width*Height*self.Unpacked_Channel_Count )
    UPA = Unpacked_Pixel_Array

    #create the arrays to hold the color channel data
    Color_0 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_1 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_2 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])
    Color_3 = array(self._UNPACK_ARRAY_CODE, [255,0,0,0])

    #stores the colors in a way we can easily access them
    Colors = [Color_0, Color_1, Color_2, Color_3]
    
    Alpha_Masks = DXT5_Alpha_Masks
    Alpha_Bit_Shifts = DXT5_Alpha_Bit_Shifts
    Alpha_Lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    R_Scale = DXT_R_Scale
    G_Scale = DXT_G_Scale
    B_Scale = DXT_B_Scale
    
    Channel_0 = self.Channel_Mapping.index(0)
    Channel_1 = self.Channel_Mapping.index(1)
    Channel_2 = self.Channel_Mapping.index(2)
    Channel_3 = self.Channel_Mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    Texel_Pixel_Mapping = Get_Texel_Mapping(Width, Height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    Texel_X_Pixel_Offsets = range(0, Texel_Width*16, 16)
    Texel_Y_Pixel_Offsets = range(0, Texel_Height*16*Width, 16*Width)
    
    #loop through each texel
    for Current_Index in range(len(Packed_Pixel_Array)//4):

        #get the offset to use
        Texel_Offset = (Texel_X_Pixel_Offsets[Current_Index%Texel_Width] +
                        Texel_Y_Pixel_Offsets[Current_Index//Texel_Width])

        Alpha_0 = Alpha_Lookup[0] = Packed_Pixel_Array[Current_Index*4]&255
        Alpha_1 = Alpha_Lookup[1] = (Packed_Pixel_Array[Current_Index*4]&65280)>>8

        """depending on which alpha value is larger the indexing is calculated differently"""
        if Alpha_0 > Alpha_1:
            Alpha_Lookup[2] = (Alpha_0*6 + Alpha_1)//7
            Alpha_Lookup[3] = (Alpha_0*5 + Alpha_1*2)//7
            Alpha_Lookup[4] = (Alpha_0*4 + Alpha_1*3)//7
            Alpha_Lookup[5] = (Alpha_0*3 + Alpha_1*4)//7
            Alpha_Lookup[6] = (Alpha_0*2 + Alpha_1*5)//7
            Alpha_Lookup[7] = (Alpha_0 + Alpha_1*6)//7
        else:
            Alpha_Lookup[2] = (Alpha_0*4 + Alpha_1)//5
            Alpha_Lookup[3] = (Alpha_0*3 + Alpha_1*2)//5
            Alpha_Lookup[4] = (Alpha_0*2 + Alpha_1*3)//5
            Alpha_Lookup[5] = (Alpha_0 + Alpha_1*4)//5
            Alpha_Lookup[6] = 0
            Alpha_Lookup[7] = 255
        
        #half of the first array entry in DXT4/5 format is both alpha values and the first third of the indexing
        ALPHA = ((Packed_Pixel_Array[Current_Index*4]&4294901760)>>16) + (Packed_Pixel_Array[Current_Index*4+1]<<16)
        COLOR_0 = Packed_Pixel_Array[Current_Index*4+2] & 65535
        COLOR_1 = (Packed_Pixel_Array[Current_Index*4+2] & 4294901760) >> 16
        INDEXING = Packed_Pixel_Array[Current_Index*4+3]

        """unpack the colors"""
        Color_0[1] = R_Scale[(COLOR_0 & 63488) >> 11]
        Color_0[2] = G_Scale[(COLOR_0 & 2016) >> 5]
        Color_0[3] = B_Scale[COLOR_0 & 31]
        
        Color_1[1] = R_Scale[(COLOR_1 & 63488) >> 11]
        Color_1[2] = G_Scale[(COLOR_1 & 2016) >> 5]
        Color_1[3] = B_Scale[COLOR_1 & 31]

        Color_2[1] = (Color_0[1]*2 + Color_1[1])//3
        Color_2[2] = (Color_0[2]*2 + Color_1[2])//3
        Color_2[3] = (Color_0[3]*2 + Color_1[3])//3
        Colors[3] = [255,(Color_0[1] + 2*Color_1[1])//3,
                     (Color_0[2] + 2*Color_1[2])//3,
                     (Color_0[3] + 2*Color_1[3])//3]
            
        for i in Range_16:
            Color = Colors[(INDEXING & DXT1_Indexing_Masks[i]) >> DXT1_Indexing_Bit_Shifts[i]]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_0] = Alpha_Lookup[(ALPHA & Alpha_Masks[i]) >>
                                                                                Alpha_Bit_Shifts[i]]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_1] = Color[1]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_2] = Color[2]
            UPA[Texel_Pixel_Mapping[i] + Texel_Offset+Channel_3] = Color[3]

    return(Unpacked_Pixel_Array)



def Unpack_DXN(self, Bitmap_Index, Width, Height, Depth=1):
    '''this function takes the loaded DXN texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Packed_Pixel_Array = self.Texture_Block[Bitmap_Index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    Unpacked_Pixel_Array = array(self._UNPACK_ARRAY_CODE, [0]*Width*Height*self.Unpacked_Channel_Count )
    UPA = Unpacked_Pixel_Array
    
    DXN_Masks = DXT5_Alpha_Masks
    DXN_Bit_Shifts = DXT5_Alpha_Bit_Shifts
    Red_Lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])
    Green_Lookup = array(self._UNPACK_ARRAY_CODE, [0,0,0,0, 0,0,0,0])

    R_Scale = DXT_R_Scale
    G_Scale = DXT_G_Scale
    B_Scale = DXT_B_Scale
    
    Channel_0 = self.Channel_Mapping.index(0)
    Channel_1 = self.Channel_Mapping.index(1)
    Channel_2 = self.Channel_Mapping.index(2)
    Channel_3 = self.Channel_Mapping.index(3)
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)

    #used to know where each pixel from the 4x4 texel should be placed into the unpacked pixel array
    Texel_Pixel_Mapping = Get_Texel_Mapping(Width, Height)

    #these are used to know how many pixels in that each pixel
    #within a texel is when unpacked into a linear array
    Texel_X_Pixel_Offsets = range(0, Texel_Width*16, 16)
    Texel_Y_Pixel_Offsets = range(0, Texel_Height*16*Width, 16*Width)
    
    #loop through each texel
    for Current_Index in range(len(Packed_Pixel_Array)//4):

        #get the offset to use
        Texel_Offset = (Texel_X_Pixel_Offsets[Current_Index%Texel_Width] +
                        Texel_Y_Pixel_Offsets[Current_Index//Texel_Width])

        R_Index = Texel_Offset + Channel_1
        G_Index = Texel_Offset + Channel_2
        B_Index = Texel_Offset + Channel_3

        Red_0 = Red_Lookup[0] = Packed_Pixel_Array[Current_Index*4]&255
        Red_1 = Red_Lookup[1] = (Packed_Pixel_Array[Current_Index*4]&65280)>>8
        Red_Indexing = (((Packed_Pixel_Array[Current_Index*4]&4294901760)>>16) +
                        (Packed_Pixel_Array[Current_Index*4+1]<<16))
        
        Green_0 = Green_Lookup[0] = Packed_Pixel_Array[Current_Index*4+2]&255
        Green_1 = Green_Lookup[1] = (Packed_Pixel_Array[Current_Index*4+2]&65280)>>8
        Green_Indexing = (((Packed_Pixel_Array[Current_Index*4+2]&4294901760)>>16) +
                          (Packed_Pixel_Array[Current_Index*4+3]<<16))

        """depending on which alpha value is larger the indexing is calculated differently"""
        if Red_0 > Red_1:
            Red_Lookup[2] = (Red_0*6 + Red_1)//7
            Red_Lookup[3] = (Red_0*5 + Red_1*2)//7
            Red_Lookup[4] = (Red_0*4 + Red_1*3)//7
            Red_Lookup[5] = (Red_0*3 + Red_1*4)//7
            Red_Lookup[6] = (Red_0*2 + Red_1*5)//7
            Red_Lookup[7] = (Red_0 + Red_1*6)//7
        else:
            Red_Lookup[2] = (Red_0*4 + Red_1)//5
            Red_Lookup[3] = (Red_0*3 + Red_1*2)//5
            Red_Lookup[4] = (Red_0*2 + Red_1*3)//5
            Red_Lookup[5] = (Red_0 + Red_1*4)//5
            Red_Lookup[6] = 0
            Red_Lookup[7] = 255
            
        if Green_0 > Green_1:
            Green_Lookup[2] = (Green_0*6 + Green_1)//7
            Green_Lookup[3] = (Green_0*5 + Green_1*2)//7
            Green_Lookup[4] = (Green_0*4 + Green_1*3)//7
            Green_Lookup[5] = (Green_0*3 + Green_1*4)//7
            Green_Lookup[6] = (Green_0*2 + Green_1*5)//7
            Green_Lookup[7] = (Green_0 + Green_1*6)//7
        else:
            Green_Lookup[2] = (Green_0*4 + Green_1)//5
            Green_Lookup[3] = (Green_0*3 + Green_1*2)//5
            Green_Lookup[4] = (Green_0*2 + Green_1*3)//5
            Green_Lookup[5] = (Green_0 + Green_1*4)//5
            Green_Lookup[6] = 0
            Green_Lookup[7] = 255
        
        for i in Range_16:
            UPA[Texel_Pixel_Mapping[i]+R_Index] = Red_Lookup[(Red_Indexing & DXN_Masks[i]) >> DXN_Bit_Shifts[i]]
            UPA[Texel_Pixel_Mapping[i]+G_Index] = Green_Lookup[(Green_Indexing & DXN_Masks[i]) >> DXN_Bit_Shifts[i]]
            Blue = (16129 - (127-UPA[Texel_Pixel_Mapping[i]+R_Index])**2
                          - (127-UPA[Texel_Pixel_Mapping[i]+G_Index])**2)
            
            if Blue >= 16129:
                UPA[Texel_Pixel_Mapping[i]+B_Index] = 255
            elif Blue == 0:
                UPA[Texel_Pixel_Mapping[i]+B_Index] = 128
            elif Blue <= -16129:
                UPA[Texel_Pixel_Mapping[i]+B_Index] = 0
            elif Blue < 0:
                UPA[Texel_Pixel_Mapping[i]+B_Index] = 127-int(sqrt(Blue*-1))
            else:
                UPA[Texel_Pixel_Mapping[i]+B_Index] = 127+int(sqrt(Blue))
            
    return(Unpacked_Pixel_Array)




def Unpack_U8V8(self, Bitmap_Index, Width, Height, Depth=1):
    '''this function takes the loaded U8V8 texture and unpacks it'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    Packed_Pixel_Array = self.Texture_Block[Bitmap_Index]
        
    #create a new array to hold the pixels after we unpack them
    """there are 16 pixels per texel. divide this by how many array entries make up 1 texel"""
    Unpacked_Pixel_Array = array(self._UNPACK_ARRAY_CODE, [0]*Width*Height*self.Unpacked_Channel_Count )
    UPA = Unpacked_Pixel_Array
    
    R_Scale = self.Channel_Upscalers[1]
    G_Scale = self.Channel_Upscalers[2]
    B_Scale = self.Channel_Upscalers[3]
    
    Red_I = self.Channel_Mapping.index(1)
    Green_I = self.Channel_Mapping.index(2)
    Blue_I = self.Channel_Mapping.index(3)

    R_Max = R_Scale[len(R_Scale)-1]
    G_Max = G_Scale[len(G_Scale)-1]

    for i in range(0, len(Packed_Pixel_Array)*4, 4):
        UPA[i+Red_I] = (R_Scale[Packed_Pixel_Array[i//4]&255])*2&R_Max
        UPA[i+Green_I] = (G_Scale[(Packed_Pixel_Array[i//4]&65280)>>8])*2&G_Max
        Blue = 16129 - (127-UPA[i+Red_I])**2 - (127-UPA[i+Green_I])**2
        
        if Blue >= 16129:
            UPA[i+Blue_I] = B_Scale[255]
        elif Blue == 0:
            UPA[i+Blue_I] = B_Scale[128]
        elif Blue <= -16129:
            UPA[i+Blue_I] = 0
        elif Blue < 0:
            UPA[i+Blue_I] = B_Scale[127-int(sqrt(Blue*-1))]
        else:
            UPA[i+Blue_I] = B_Scale[127+int(sqrt(Blue))]


    return(Unpacked_Pixel_Array)
    



########################################
'''######## PACKING ROUTINES ########'''
########################################




def Pack_DXT1(self, Unpacked_Pixel_Array, Width, Height, Depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == BC.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT1 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
    
    DXT1_Transparency = self.Color_Key_Transparency
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    Repacked_Pixel_Array = array("I", [0]*Texel_Width*Texel_Height*2 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    if Texel_Width > 1:
        DXT_Swizzler = BC.Swizzler.Swizzler(Texture_Convertor = self, Mask_Type = "DXT_CALC")
        Unpacked_Pixel_Array = DXT_Swizzler.Swizzle_Single_Array(Unpacked_Pixel_Array, True, 4, Width, Height)

    #shorthand names
    RPA = Repacked_Pixel_Array
    UPA = Unpacked_Pixel_Array

    A_Scale, R_Scale, G_Scale, B_Scale = self.Channel_Downscalers

    #calculate for the unpacked channels
    Texel_Pixel_Channel_Count = 4*Get_Texel_Pixel_Count(Width, Height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    Furthest_Colors = array("B", [0,0])
    Distances = array("i", [0,0,0,0])

    Color_0 = array("B", [0,0,0,0])
    Color_1 = array("B", [0,0,0,0])
    Color_2 = array("B", [0,0,0,0])
    Color_3 = array("B", [0,0,0,0])

    Include_Transparency = False
    Alpha_Cutoff = self.One_Bit_Bias

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    Range_Pixels = range(0, Texel_Pixel_Channel_Count, 4)

    Pixel_Comparison_Slices = list(map(lambda x: Range_Pixels[x//4+1:], Range_Pixels))
    
    #loop for each texel
    for TXL_I in range(0, len(Repacked_Pixel_Array), 2):
        Furthest_Colors[0] = 0
        Furthest_Colors[1] = 0
        Distances[0] = -1
        
        #cache so it doesn't have to keep being calculated
        PXL_I = (TXL_I//2)*Texel_Pixel_Channel_Count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in Range_Pixels:
            for j in Pixel_Comparison_Slices[i//4]:
                Distances[1] = (((UPA[PXL_I+1+i]-UPA[PXL_I+1+j])**2)+
                                ((UPA[PXL_I+2+i]-UPA[PXL_I+2+j])**2)+
                                ((UPA[PXL_I+3+i]-UPA[PXL_I+3+j])**2))
                if Distances[1] > Distances[0]:
                    Distances[0] = Distances[1]
                    Furthest_Colors[0] = i
                    Furthest_Colors[1] = j

        #2: store furthest apart colors for use
        Color_0[1] = UPA[PXL_I+1+Furthest_Colors[0]]
        Color_0[2] = UPA[PXL_I+2+Furthest_Colors[0]]
        Color_0[3] = UPA[PXL_I+3+Furthest_Colors[0]]
        
        Color_1[1] = UPA[PXL_I+1+Furthest_Colors[1]]
        Color_1[2] = UPA[PXL_I+2+Furthest_Colors[1]]
        Color_1[3] = UPA[PXL_I+3+Furthest_Colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (R_Scale[Color_0[1]]<<11)+(G_Scale[Color_0[2]]<<5)+B_Scale[Color_0[3]]
        COLOR_1 = (R_Scale[Color_1[1]]<<11)+(G_Scale[Color_1[2]]<<5)+B_Scale[Color_1[3]]

        #4: figure out if we are using color key transparency for this pixel
        #by seeing if any of the alpha values are below the cutoff bias
        if DXT1_Transparency:
            Include_Transparency = False
            for i in Range_Pixels:
                if UPA[PXL_I+i] < Alpha_Cutoff:
                    Include_Transparency = True
                    break
            
        if COLOR_0 == COLOR_1 and not Include_Transparency:
            #do nothing except save one of the colors to the array
            RPA[TXL_I] = COLOR_0
        else:
            #5: if the current color selection doesn't match what we want then
            #we reverse which color is which (if we are using transparency then
            #the first color as an integer must be smaller or equal to the second)
            if Include_Transparency == (COLOR_0 > COLOR_1):
                Color_0, Color_1 = Color_1, Color_0
                RPA[TXL_I] = (COLOR_0<<16) + COLOR_1
            else: RPA[TXL_I] = (COLOR_1<<16) + COLOR_0
        
            #6: calculate the intermediate colors
            """If the target format is DXT2/3/4/5 then no CK transparency will be used.
            CK mode will only be selected if both colors are the same. If both colors
            are the same then it is fine to run non-CK calculation on it since it will
            default to index zero. That is why the DXT3/5 calculation is in this part only"""
            if (RPA[TXL_I]&65535 > RPA[TXL_I]>>16):
                Color_2[1] = (Color_0[1]*2+Color_1[1])//3
                Color_2[2] = (Color_0[2]*2+Color_1[2])//3
                Color_2[3] = (Color_0[3]*2+Color_1[3])//3
                
                Color_3[1] = (Color_0[1]+Color_1[1]*2)//3
                Color_3[2] = (Color_0[2]+Color_1[2]*2)//3
                Color_3[3] = (Color_0[3]+Color_1[3]*2)//3
                
                #7: calculate each pixel's closest match and assign it the proper index
                for i in Range_Pixels:
                    Distances[0] = (((UPA[PXL_I+1+i]-Color_0[1])**2)+
                                    ((UPA[PXL_I+2+i]-Color_0[2])**2)+
                                    ((UPA[PXL_I+3+i]-Color_0[3])**2))
                    Distances[1] = (((UPA[PXL_I+1+i]-Color_1[1])**2)+
                                    ((UPA[PXL_I+2+i]-Color_1[2])**2)+
                                    ((UPA[PXL_I+3+i]-Color_1[3])**2))
                    
                    #8: add appropriate indexing value to array
                    if Distances[0] <= Distances[1]: #closer to color 0
                        if (Distances[0] > (((UPA[PXL_I+1+i]-Color_2[1])**2)+
                                            ((UPA[PXL_I+2+i]-Color_2[2])**2)+
                                            ((UPA[PXL_I+3+i]-Color_2[3])**2))): #closest to color 2
                            RPA[TXL_I+1] += 2<<(i//2)
                    else: #closer to color 1
                        if (Distances[1] < (((UPA[PXL_I+1+i]-Color_3[1])**2)+
                                            ((UPA[PXL_I+2+i]-Color_3[2])**2)+
                                            ((UPA[PXL_I+3+i]-Color_3[3])**2))): #closest to color 1
                            RPA[TXL_I+1] += 1<<(i//2)
                        else: #closest to color 3
                            RPA[TXL_I+1] += 3<<(i//2)
            else:
                Color_2[1] = (Color_0[1]+Color_1[1])//2
                Color_2[2] = (Color_0[2]+Color_1[2])//2
                Color_2[3] = (Color_0[3]+Color_1[3])//2
                #here, Color_3 represents zero color and fully transparent
                
                #7: calculate each pixel's closest match and assign it the proper index
                for i in Range_Pixels:
                    if UPA[PXL_I+i] < Alpha_Cutoff:
                        RPA[TXL_I+1] += 3<<(i//2)
                    else:
                        Distances[0] = ((UPA[PXL_I+1+i]-Color_0[1])**2+
                                        (UPA[PXL_I+2+i]-Color_0[2])**2+
                                        (UPA[PXL_I+3+i]-Color_0[3])**2)
                        Distances[1] = ((UPA[PXL_I+1+i]-Color_1[1])**2+
                                        (UPA[PXL_I+2+i]-Color_1[2])**2+
                                        (UPA[PXL_I+3+i]-Color_1[3])**2)

                        #8: add appropriate indexing value to array
                        if (Distances[1] < Distances[0] and
                           (Distances[1] < ((UPA[PXL_I+1+i]-Color_2[1])**2+
                                            (UPA[PXL_I+2+i]-Color_2[2])**2+
                                            (UPA[PXL_I+3+i]-Color_2[3])**2))):#closest to color 1
                                RPA[TXL_I+1] += 1<<(i//2)
                        else: #closer to color 2
                            if (Distances[2] < Distances[0] and
                               (Distances[1] >= ((UPA[PXL_I+1+i]-Color_2[1])**2+
                                                 (UPA[PXL_I+2+i]-Color_2[2])**2+
                                                 (UPA[PXL_I+3+i]-Color_2[3])**2))):#closest to color 2
                                RPA[TXL_I+1] += 2<<(i//2)
            
    return(Repacked_Pixel_Array)




def Pack_DXT2_3(self, Unpacked_Pixel_Array, Width, Height, Depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == BC.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT2/3 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    Repacked_Pixel_Array = array("I", [0]*Texel_Width*Texel_Height*4 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if Texel_Width > 1:
        DXT_Swizzler = BC.Swizzler.Swizzler(Texture_Convertor = self, Mask_Type = "DXT_CALC")
        Unpacked_Pixel_Array = DXT_Swizzler.Swizzle_Single_Array(Unpacked_Pixel_Array, True, 4, Width, Height)

    #shorthand names
    RPA = Repacked_Pixel_Array
    UPA = Unpacked_Pixel_Array

    A_Scale, R_Scale, G_Scale, B_Scale = self.Channel_Downscalers

    #calculate for the unpacked channels
    Texel_Pixel_Channel_Count = 4*Get_Texel_Pixel_Count(Width, Height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    Furthest_Colors = array("B", [0,0])
    Distances = array("i", [0,0,0,0])

    Color_0 = array("B", [0,0,0,0])
    Color_1 = array("B", [0,0,0,0])
    Color_2 = array("B", [0,0,0,0])
    Color_3 = array("B", [0,0,0,0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    Range_Pixels = range(0, Texel_Pixel_Channel_Count, 4)

    #these are split apart since the alpha for DXT3 is split into 2, 4byte ints in the array
    DXT3_Range_Pixels_0 = array("B", Range_Pixels[:8])
    DXT3_Range_Pixels_1 = array("B", Range_Pixels[8:])

    Pixel_Comparison_Slices = list(map(lambda x: Range_Pixels[x//4+1:], Range_Pixels))
    
    #loop for each texel
    for TXL_I in range(0, len(Repacked_Pixel_Array), 4):
        Furthest_Colors[0] = 0
        Furthest_Colors[1] = 0
        Distances[0] = -1
        
        #cache so it doesn't have to keep being calculated
        PXL_I = (TXL_I//4)*Texel_Pixel_Channel_Count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in Range_Pixels:
            for j in Pixel_Comparison_Slices[i//4]:
                Distances[1] = (((UPA[PXL_I+1+i]-UPA[PXL_I+1+j])**2)+
                                ((UPA[PXL_I+2+i]-UPA[PXL_I+2+j])**2)+
                                ((UPA[PXL_I+3+i]-UPA[PXL_I+3+j])**2))
                if Distances[1] > Distances[0]:
                    Distances[0] = Distances[1]
                    Furthest_Colors[0] = i
                    Furthest_Colors[1] = j

        #2: store furthest apart colors for use
        Color_0[1] = UPA[PXL_I+1+Furthest_Colors[0]]
        Color_0[2] = UPA[PXL_I+2+Furthest_Colors[0]]
        Color_0[3] = UPA[PXL_I+3+Furthest_Colors[0]]
        
        Color_1[1] = UPA[PXL_I+1+Furthest_Colors[1]]
        Color_1[2] = UPA[PXL_I+2+Furthest_Colors[1]]
        Color_1[3] = UPA[PXL_I+3+Furthest_Colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (R_Scale[Color_0[1]]<<11)+(G_Scale[Color_0[2]]<<5)+B_Scale[Color_0[3]]
        COLOR_1 = (R_Scale[Color_1[1]]<<11)+(G_Scale[Color_1[2]]<<5)+B_Scale[Color_1[3]]
        
        if COLOR_0 == COLOR_1:
            #do nothing except save one of the colors to the array
            RPA[TXL_I+2] = COLOR_0
        else:
            #4: make sure the colors are properly ordered
            if COLOR_0 < COLOR_1:
                Color_0, Color_1 = Color_1, Color_0
                RPA[TXL_I+2] = (COLOR_0<<16) + COLOR_1
            else: RPA[TXL_I+2] = (COLOR_1<<16) + COLOR_0
        
            #5: calculate the intermediate colors
            Color_2[1] = (Color_0[1]*2+Color_1[1])//3
            Color_2[2] = (Color_0[2]*2+Color_1[2])//3
            Color_2[3] = (Color_0[3]*2+Color_1[3])//3
            
            Color_3[1] = (Color_0[1]+Color_1[1]*2)//3
            Color_3[2] = (Color_0[2]+Color_1[2]*2)//3
            Color_3[3] = (Color_0[3]+Color_1[3]*2)//3
            
            #6: calculate each pixel's closest match and assign it the proper index
            for i in Range_Pixels:
                Distances[0] = (((UPA[PXL_I+1+i]-Color_0[1])**2)+
                                ((UPA[PXL_I+2+i]-Color_0[2])**2)+
                                ((UPA[PXL_I+3+i]-Color_0[3])**2))
                Distances[1] = (((UPA[PXL_I+1+i]-Color_1[1])**2)+
                                ((UPA[PXL_I+2+i]-Color_1[2])**2)+
                                ((UPA[PXL_I+3+i]-Color_1[3])**2))
                
                #7: add appropriate indexing value to array
                if Distances[0] <= Distances[1]: #closer to color 0
                    if (Distances[0] > (((UPA[PXL_I+1+i]-Color_2[1])**2)+
                                        ((UPA[PXL_I+2+i]-Color_2[2])**2)+
                                        ((UPA[PXL_I+3+i]-Color_2[3])**2))): #closest to color 2
                        RPA[TXL_I+3] += 2<<(i//2)
                else: #closer to color 1
                    if (Distances[1] < (((UPA[PXL_I+1+i]-Color_3[1])**2)+
                                        ((UPA[PXL_I+2+i]-Color_3[2])**2)+
                                        ((UPA[PXL_I+3+i]-Color_3[3])**2))): #closest to color 1
                        RPA[TXL_I+3] += 1<<(i//2)
                    else: #closest to color 3
                        RPA[TXL_I+3] += 3<<(i//2)

        #8: calculate alpha channel for DXT 2/3/4/5
        for i in DXT3_Range_Pixels_0:
            RPA[TXL_I] += A_Scale[UPA[PXL_I+i]]<<i
        for i in DXT3_Range_Pixels_1:
            RPA[TXL_I+1] += A_Scale[UPA[PXL_I+i]]<<(i-32)
            
    return(Repacked_Pixel_Array)





def Pack_DXT4_5(self, Unpacked_Pixel_Array, Width, Height, Depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if not self._UNPACK_FORMAT == BC.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXT4/5 THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)
        
    #create a new array to hold the texels after we repack them
    """there are 16 pixels per texel. multiply the
    number of texels by the number of entries per texel"""
    Repacked_Pixel_Array = array("I", [0]*Texel_Width*Texel_Height*4 )

    """If the texture is more than 1 texel wide we need to have the swizzler
    rearrange the pixels so that each texel's pixels are adjacent each other.
    This will allow us to easily group each texel's pixels nicely together."""
    
    if Texel_Width > 1:
        DXT_Swizzler = BC.Swizzler.Swizzler(Texture_Convertor = self, Mask_Type = "DXT_CALC")
        Unpacked_Pixel_Array = DXT_Swizzler.Swizzle_Single_Array(Unpacked_Pixel_Array, True, 4, Width, Height)

    #shorthand names
    RPA = Repacked_Pixel_Array
    UPA = Unpacked_Pixel_Array

    A_Scale, R_Scale, G_Scale, B_Scale = self.Channel_Downscalers

    #calculate for the unpacked channels
    Texel_Pixel_Channel_Count = 4*Get_Texel_Pixel_Count(Width, Height)

    #arrays are faster for assignment since they're C based
    #and don't require new objects to be created on assignment
    Furthest_Colors = array("B", [0,0])
    Distances = array("i", [0,0,0,0])

    Color_0 = array("B", [0,0,0,0])
    Color_1 = array("B", [0,0,0,0])
    Color_2 = array("B", [0,0,0,0])
    Color_3 = array("B", [0,0,0,0])
    
    DXT5_Values = array("B", [0,0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    Range_Pixels = range(0, Texel_Pixel_Channel_Count, 4)

    Pixel_Comparison_Slices = list(map(lambda x: Range_Pixels[x//4+1:], Range_Pixels))
    
    #loop for each texel
    for TXL_I in range(0, len(Repacked_Pixel_Array), 4):
        Furthest_Colors[0] = 0
        Furthest_Colors[1] = 0
        Distances[0] = -1
        
        #cache so it doesn't have to keep being calculated
        PXL_I = (TXL_I//4)*Texel_Pixel_Channel_Count
        
        #1: compare distance between all pixels and find the two furthest apart
        #(we are actually only comparing the area of the distance as it's faster)
        for i in Range_Pixels:
            for j in Pixel_Comparison_Slices[i//4]:
                Distances[1] = (((UPA[PXL_I+1+i]-UPA[PXL_I+1+j])**2)+
                                ((UPA[PXL_I+2+i]-UPA[PXL_I+2+j])**2)+
                                ((UPA[PXL_I+3+i]-UPA[PXL_I+3+j])**2))
                if Distances[1] > Distances[0]:
                    Distances[0] = Distances[1]
                    Furthest_Colors[0] = i
                    Furthest_Colors[1] = j

        #2: store furthest apart colors for use
        Color_0[1] = UPA[PXL_I+1+Furthest_Colors[0]]
        Color_0[2] = UPA[PXL_I+2+Furthest_Colors[0]]
        Color_0[3] = UPA[PXL_I+3+Furthest_Colors[0]]
        
        Color_1[1] = UPA[PXL_I+1+Furthest_Colors[1]]
        Color_1[2] = UPA[PXL_I+2+Furthest_Colors[1]]
        Color_1[3] = UPA[PXL_I+3+Furthest_Colors[1]]

        #3: quantize the colors down to 16 bit color and repack
        COLOR_0 = (R_Scale[Color_0[1]]<<11)+(G_Scale[Color_0[2]]<<5)+B_Scale[Color_0[3]]
        COLOR_1 = (R_Scale[Color_1[1]]<<11)+(G_Scale[Color_1[2]]<<5)+B_Scale[Color_1[3]]
            
        if COLOR_0 == COLOR_1:
            #do nothing except save one of the colors to the array
            RPA[TXL_I+2] = COLOR_0
        else:
            #4: make sure the colors are properly ordered
            if COLOR_0 < COLOR_1:
                Color_0, Color_1 = Color_1, Color_0
                RPA[TXL_I+2] = (COLOR_0<<16) + COLOR_1
            else: RPA[TXL_I+2] = (COLOR_1<<16) + COLOR_0
            
            #5: calculate the intermediate colors
            Color_2[1] = (Color_0[1]*2+Color_1[1])//3
            Color_2[2] = (Color_0[2]*2+Color_1[2])//3
            Color_2[3] = (Color_0[3]*2+Color_1[3])//3
            
            Color_3[1] = (Color_0[1]+Color_1[1]*2)//3
            Color_3[2] = (Color_0[2]+Color_1[2]*2)//3
            Color_3[3] = (Color_0[3]+Color_1[3]*2)//3
        
            #6: calculate each pixel's closest match and assign it the proper index
            for i in Range_Pixels:
                Distances[0] = (((UPA[PXL_I+1+i]-Color_0[1])**2)+
                                ((UPA[PXL_I+2+i]-Color_0[2])**2)+
                                ((UPA[PXL_I+3+i]-Color_0[3])**2))
                Distances[1] = (((UPA[PXL_I+1+i]-Color_1[1])**2)+
                                ((UPA[PXL_I+2+i]-Color_1[2])**2)+
                                ((UPA[PXL_I+3+i]-Color_1[3])**2))
                
                #7: add appropriate indexing value to array
                if Distances[0] <= Distances[1]: #closer to color 0
                    if (Distances[0] > (((UPA[PXL_I+1+i]-Color_2[1])**2)+
                                        ((UPA[PXL_I+2+i]-Color_2[2])**2)+
                                        ((UPA[PXL_I+3+i]-Color_2[3])**2))): #closest to color 2
                        RPA[TXL_I+3] += 2<<(i//2)
                else: #closer to color 1
                    if (Distances[1] < (((UPA[PXL_I+1+i]-Color_3[1])**2)+
                                        ((UPA[PXL_I+2+i]-Color_3[2])**2)+
                                        ((UPA[PXL_I+3+i]-Color_3[3])**2))): #closest to color 1
                        RPA[TXL_I+3] += 1<<(i//2)
                    else: #closest to color 3
                        RPA[TXL_I+3] += 3<<(i//2)

        #8: find the most extreme values
        DXT5_Values[0] = max(map(lambda i: UPA[PXL_I+i], Range_Pixels))
        DXT5_Values[1] = min(map(lambda i: UPA[PXL_I+i], Range_Pixels))

        #reset the alpha data temp value
        DXT5_Alpha_Data = 0
        #9: if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if DXT5_Values[0] != 0 or DXT5_Values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""

            #if they are the same number then the indexing can stay at all zero
            if DXT5_Values[0] != DXT5_Values[1]:
                #10: calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    #0 = color_0                    1 = color_1
                    #2 = (6*color_0 + color_1)/7    3 = (5*color_0 + 2*color_1)/7
                    #4 = (4*color_0 + 3*color_1)/7  5 = (3*color_0 + 4*color_1)/7
                    #6 = (2*color_0 + 5*color_1)/7  7 = (color_0 + 6*color_1)/7

                    #calculate how far between both colors that the value is as a 0 to 7 int
                    DXT5_Temp_Value = ( ((UPA[PXL_I+i]-DXT5_Values[1])*7 +
                                         ((DXT5_Values[0]-DXT5_Values[1])//2) )//
                                        (DXT5_Values[0]-DXT5_Values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if DXT5_Temp_Value == 0:
                        DXT5_Alpha_Data += 1<<((i//4)*3 + 16)
                    elif DXT5_Temp_Value < 7:
                        DXT5_Alpha_Data += (8-DXT5_Temp_Value)<<((i//4)*3 + 16)
                
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
           
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in Range_Pixels:
                #store if lowest int so far
                if DXT5_Values[0] > UPA[PXL_I+i] and UPA[PXL_I+i] > 0:
                    DXT5_Values[0] = UPA[PXL_I+i]
                    
                #store if greatest int so far
                if DXT5_Values[1] < UPA[PXL_I+i] and UPA[PXL_I+i] < 255:
                    DXT5_Values[1] = UPA[PXL_I+i]

            #if they are the same number then the indexing can stay at all zero
            if DXT5_Values[0] != DXT5_Values[1]:
                #10: calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    #there are 4 interpolated colors in this mode
                    #0 =  color_0                   1 = color_1
                    #2 = (4*color_0 + color_1)/5    3 = (3*color_0 + 2*color_1)/5
                    #4 = (2*color_0 + 3*color_1)/5  5 = (color_0 + 4*color_1)/5
                    #6 =  0                         7 = 255

                    if UPA[PXL_I+i] == 0:
                        #if the value is 0 we set it to index 6
                        DXT5_Alpha_Data += 6<<((i//4)*3 + 16)
                    elif UPA[PXL_I+i] == 255:
                        #if the value is 255 we set it to index 7
                        DXT5_Alpha_Data += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        DXT5_Temp_Value = ( ((UPA[PXL_I+i]-DXT5_Values[0])*5 +
                                             ((DXT5_Values[1]-DXT5_Values[0])//2) )//
                                            (DXT5_Values[1]-DXT5_Values[0])  )
                        if DXT5_Temp_Value == 5:
                            DXT5_Alpha_Data += 1<<((i//4)*3 + 16)
                        elif DXT5_Temp_Value > 0:
                            DXT5_Alpha_Data += (DXT5_Temp_Value+1)<<((i//4)*3 + 16)
                      
        #11: store the calculated alpha data to the pixel array
        '''alpha indexing is pre-shifted left by 2 bytes and as such
        just needs to be masked and summed with the alpha values'''
        RPA[TXL_I] = (DXT5_Alpha_Data&4294967295) + (DXT5_Values[1]<<8) + DXT5_Values[0]
        RPA[TXL_I+1] = DXT5_Alpha_Data>>32
            
    return(Repacked_Pixel_Array)




def Pack_DXN(self, Unpacked_Pixel_Array, Width, Height, Depth=1):
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    if not self._UNPACK_FORMAT == BC.FORMAT_A8R8G8B8:
        print("ERROR: TO CONVERT TO DXN THE UNPACK FORMAT MUST BE A8R8G8B8")
        return
        
    #this is how many texels wide/tall the texture is
    Texel_Width, Texel_Height, _ = BC.Dimension_Lower_Bound_Check(Width//4, Height//4)
    
    Repacked_Pixel_Array = array("I", [0]*Texel_Width*Texel_Height*4 )
    
    if Texel_Width > 1:
        DXT_Swizzler = BC.Swizzler.Swizzler(Texture_Convertor = self, Mask_Type = "DXT_CALC")
        Unpacked_Pixel_Array = DXT_Swizzler.Swizzle_Single_Array(Unpacked_Pixel_Array, True, 4, Width, Height)

    #shorthand names
    RPA = Repacked_Pixel_Array
    UPA = Unpacked_Pixel_Array

    #calculate for the unpacked channels
    Texel_Pixel_Channel_Count = 4*Get_Texel_Pixel_Count(Width, Height)
    
    Green_Values = array("B", [0,0])
    Green_Temp_Value = array("B", [0])
    
    Red_Values = array("B", [0,0])
    Red_Temp_Value = array("B", [0])

    #this is the indexing for each pixel in each texel
    #values are multiplied by 4 to account for the channels
    Range_Pixels = range(0, Texel_Pixel_Channel_Count, 4)

    #loop for each texel
    for TXL_I in range(0, len(Repacked_Pixel_Array), 4):
        #cache so it doesn't have to keep being calculated
        PXL_I = (TXL_I//4)*Texel_Pixel_Channel_Count
        
        #8: find the most extreme values
        Red_Values[0] = max(map(lambda i: UPA[PXL_I+1+i], Range_Pixels))
        Red_Values[1] = min(map(lambda i: UPA[PXL_I+1+i], Range_Pixels))
        
        Green_Values[0] = max(map(lambda i: UPA[PXL_I+2+i], Range_Pixels))
        Green_Values[1] = min(map(lambda i: UPA[PXL_I+2+i], Range_Pixels))

        Red_Indexing = Green_Indexing = 0
        
        #if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if Red_Values[0] != 0 or Red_Values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""
            #if they are the same number then the indexing can stay at all zero
            if Red_Values[0] != Red_Values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    #calculate how far between both colors that the value is as a 0 to 7 int
                    Temp = ( ((UPA[PXL_I+1+i]-Red_Values[1])*7 +
                              ((Red_Values[0]-Red_Values[1])//2) )//
                             (Red_Values[0]-Red_Values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if Temp == 0:  Red_Indexing += 1<<((i//4)*3 + 16)
                    elif Temp < 7: Red_Indexing += (8-Temp)<<((i//4)*3 + 16)
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in Range_Pixels:
                #store if lowest int so far
                if Red_Values[0] > UPA[PXL_I+1+i] and UPA[PXL_I+1+i] > 0:
                    Red_Values[0] = UPA[PXL_I+1+i]
                #store if greatest int so far
                if Red_Values[1] < UPA[PXL_I+1+i] and UPA[PXL_I+1+i] < 255:
                    Red_Values[1] = UPA[PXL_I+1+i]

            #if they are the same number then the indexing can stay at all zero
            if Red_Values[0] != Red_Values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    
                    if UPA[PXL_I+1+i] == 0: Red_Indexing += 6<<((i//4)*3 + 16)
                    elif UPA[PXL_I+1+i] == 255: Red_Indexing += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        Temp = ( ((UPA[PXL_I+1+i]-Red_Values[0])*5 +
                                  ((Red_Values[1]-Red_Values[0])//2) )//
                                 (Red_Values[1]-Red_Values[0])  )
                        if Temp == 5: Red_Indexing += 1<<((i//4)*3 + 16)
                        elif Temp > 0: Red_Indexing += (Temp+1)<<((i//4)*3 + 16)

        
        #if the most extreme values are NOT 0 and 255, use them as the interpolation values
        if Green_Values[0] != 0 or Green_Values[1] != 255:
            """In this mode, value_0 must be greater than value_1"""
            #if they are the same number then the indexing can stay at all zero
            if Green_Values[0] != Green_Values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    #calculate how far between both colors that the value is as a 0 to 7 int
                    Temp = ( ((UPA[PXL_I+2+i]-Green_Values[1])*7 +
                              ((Green_Values[0]-Green_Values[1])//2) )//
                             (Green_Values[0]-Green_Values[1])  )
                    """Because the colors are stored in opposite order, we need to invert the index"""
                    if Temp == 0:  Green_Indexing += 1<<((i//4)*3 + 16)
                    elif Temp < 7: Green_Indexing += (8-Temp)<<((i//4)*3 + 16)
        else:
            """In this mode, value_0 must be less than or equal to value_1"""
            #if the most extreme values ARE 0 and 255 though, then
            #we need to calculate the second most extreme values
            for i in Range_Pixels:
                #store if lowest int so far
                if Green_Values[0] > UPA[PXL_I+2+i] and UPA[PXL_I+2+i] > 0:
                    Green_Values[0] = UPA[PXL_I+2+i]
                #store if greatest int so far
                if Green_Values[1] < UPA[PXL_I+2+i] and UPA[PXL_I+2+i] < 255:
                    Green_Values[1] = UPA[PXL_I+2+i]

            #if they are the same number then the indexing can stay at all zero
            if Green_Values[0] != Green_Values[1]:
                #calculate and store which interpolated index each alpha value is closest to
                for i in Range_Pixels:
                    
                    if UPA[PXL_I+2+i] == 0: Green_Indexing += 6<<((i//4)*3 + 16)
                    elif UPA[PXL_I+2+i] == 255: Green_Indexing += 7<<((i//4)*3 + 16)
                    else:
                        #calculate how far between both colors that the value is as a 0 to 5 int
                        Temp = ( ((UPA[PXL_I+2+i]-Green_Values[0])*5 +
                                  ((Green_Values[1]-Green_Values[0])//2) )//
                                 (Green_Values[1]-Green_Values[0])  )
                        if Temp == 5: Green_Indexing += 1<<((i//4)*3 + 16)
                        elif Temp > 0: Green_Indexing += (Temp+1)<<((i//4)*3 + 16)
                      
        '''indexing is pre-shifted left by 2 bytes and as such
        just needs to be masked and summed with the channel values'''
        RPA[TXL_I] = (Red_Indexing&4294967295) + (Red_Values[1]<<8) + Red_Values[0]
        RPA[TXL_I+1] = Red_Indexing>>32
        RPA[TXL_I+2] = (Green_Indexing&4294967295) + (Green_Values[1]<<8) + Green_Values[0]
        RPA[TXL_I+3] = Green_Indexing>>32
            
    return(Repacked_Pixel_Array)



def Pack_U8V8(self, Unpacked_Pixel_Array, Width, Height, Depth=1):
    '''this function takes an unpacked texture and packs it to U8V8'''
    ######################
    '''NEEDS MORE SPEED'''
    ######################

    if self.Unpacked_Channel_Count < 1:
        print("ERROR: CANNOT CONVERT IMAGE WITHOUT RGB CHANNELS TO U8V8")
        return

    if self.Unpacked_Channel_Count == 2:
        Packed_Array = array("H", bytes(Unpacked_Pixel_Array))
    else:
        Packed_Array = array("H", [0]*(len(Unpacked_Pixel_Array)//4))
        Red_Index = self.Channel_Order.index("R")
        Green_Index = self.Channel_Order.index("G")
        
        for i in range(0, len(Unpacked_Pixel_Array), 4):
            Packed_Array[i//4] = ( Unpacked_Pixel_Array[i+Red_Index]+
                                  (Unpacked_Pixel_Array[i+Green_Index]<<8))

    return(Packed_Array)



def Get_Texel_Mapping(W, H):
    """when we are uncompressing a texture we need to make sure that
    we only read the number of pixels that the width*height SHOULD
    be. Texels are a minimum of 4x4 pixels, but if one is representing
    a 4x2, 4x1, 2x2, 2x1, or 1x1 then we need to restrict our reading
    of the texel to the dimensions it actually represents"""
    if H > 2:
        if W > 2:
            List =(array("H", (0,   1,     2,     3,
                               W*1, 1+W*1, 2+W*1, 3+W*1,
                               W*2, 1+W*2, 2+W*2, 3+W*2,
                               W*3, 1+W*3, 2+W*3, 3+W*3) ))
        elif W == 2:
            List =(array("B", (0,1,
                               2,3,
                               4,5,
                               6,7) ))
        elif W == 1:
            List =(array("B", (0,
                               1,
                               2,
                               3) ))
    elif W > 2:
        if H == 2:
            List =(array("H", (0, 1,   2,   3,
                               W, 1+W, 2+W, 3+W) ))
        elif H == 1:
            List =(array("B", (0,1,2,3) ))
            
    elif W == 2 and H == 2:
        List =(array("B", (0,1,
                           2,3) ))
    else:
        List =(array("B", (0,) ))

    #because there are 4 channels per pixel we can speed things up a little by adjusting for that in here
    List = array(List.typecode, map(lambda x: x*4, List))

    #the list needs to be 16 elements long, so however many are missing we append a
    #list of the array's last index value to it which is the length of 16-(list length)
    List.extend( [List[len(List)-1]]*(16-len(List)) )
        
    return(List)


def Get_Texel_Pixel_Count(Width, Height):
    if Width > 2:
        Texel_Pixel_Count = 4
    else:
        Texel_Pixel_Count = Width
    if Height > 2:
        Texel_Pixel_Count *= 4
    else:
        Texel_Pixel_Count *= Height
    
    return(Texel_Pixel_Count)
