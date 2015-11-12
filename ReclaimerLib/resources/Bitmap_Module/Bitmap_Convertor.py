



"""DONT FORGET TO INCLUDE A GNU PUBLIC LICENSE
   ON EVERY MODULE ONCE THE PROGRAM IS DONE"""




"""There is a lot of code that SHOULD be executed in C++ because
of how number intensive it is, but until I can write the C
extensions, these will have to do. Even after they are written
these slow pure python functions will still be included as
something to fall back on in case the C++ code can't run."""


import time
import sys


this_module = sys.modules[__name__]

    
from traceback import format_exc
from array import array
from math import ceil
from os import path
from copy import deepcopy
from decimal import Decimal

from .ext.Format_Defs import *

try:
    from .ext import Swizzler
except:
    print("ERROR: COULDNT IMPORT Swizzler MODULE")
    print(format_exc())
    Swizzler = None

try:
    from .ext import Bitmap_IO
    Bitmap_IO.BC = this_module
except:
    print("ERROR: COULDNT IMPORT Bitmap_IO MODULE")
    print(format_exc())
    Bitmap_IO = None

try:
    from .ext import DDS_Defs
    DDS_Defs.BC = this_module
    DDS_Defs.Initialize()
except:
    print("ERROR: COULDNT IMPORT DDS_Defs MODULE")
    print(format_exc())
    DDS_Defs = None


#speed things up by caching these so we don't have to
#calculate them on the fly or constantly remake them
Range_16 = range(16)
Logs_of_2 = {}
        
#used for swizzling and deswizzling
for Logarithm in range(len(Powers_of_2)):
    Logs_of_2[Powers_of_2[Logarithm]] = Logarithm


'''when constructing this class you must provide the block containing the textures and
a dictionary which contains the texture's height, width, type, and format.'''
#The format must be able to be found in the appropriate dictionaries in:
#ReclaimerLib.Tag_Specific_Functions.bitm  as well as the above dictionaries.
'''    Optional parameters include the depth, mipmap count, sub-texture count(cubemaps are
composed of 6 2D subtextures for example), the format to convert the pixels to, whether to/what
order to swap channels around, which channels should be merged/removed/cloned when converting
to a format with a different number of channels, 0-255 cutoff when compressing a channel to 1-bit,
the numebr of times to cut the resolution in half, and the power to use for merging pixels
while taking gamma into account.'''
class Bitmap_Manipulator():
    
    def __init__(self, **kwargs):
        self.Default_Palette_Picker = self._Palette_Picker
        self.Set_Deep_Color_Mode()

        self.Texture_Block = self.Texture_Info = None

        '''set this to true to force routines to make
           exported data compatible with Photoshop.'''
        self.Photoshop_Compatibility = True
        
        #initialize the bitmap description variables
        self.Sub_Bitmap_Count = self.Mipmap_Count = 0
        self.Swizzled = self.Packed = self.Palette_Packed = False
        self.Filepath = None
        self.Indexing_Size = 0
        self.Width = self.Height = self.Depth = 0
        self.Format = self.Texture_Type = ""
        self.Channel_Order = C_ORDER_DEFAULT

        #Palette stuff
        self.Palette = None
        self.Palettized_Unpacker = None
        self.Palettized_Packer = None
        self.Palette_Unpacker = None
        self.Palette_Packer = None
        self.Indexing_Unpacker = None
        self.Indexing_Packer = None
        
        #initialize the conversion variables
        self.Target_Format = ""
        self.One_Bit_Bias = 127
        self.Downres_Amount = 0
        self.Generate_Mipmaps = self.Swizzler_Mode = False
        self.Gamma = [1.0]*4#this is only meant to ever handle up to 4 channels
        self.Color_Key_Transparency = False
        self.Reswizzler = self.Deswizzler = None
        self.Palette_Picker = self.Default_Palette_Picker
        self.Palettize = False
        self.Channel_Mapping = self.Channel_Merge_Mapping = None
        self.Repack = True
        self.Target_Indexing_Size = DEFAULT_INDEXING_SIZE
        

        #initialize the variables created in the below functions
        self.Source_Depths = None
        self.Unpacked_Depths = None
        self.Target_Depths = None

        self.Source_Channel_Count = 0
        self.Unpacked_Channel_Count = 0
        self.Target_Channel_Count = 0
        
        self.Swapping_Channels = False
        self.Channel_Masks = None
        self.Channel_Offsets = None
        self.Channel_Depths = None
        self.Channel_Merge_Divisors = None
        self.Channel_Upscalers = None
        self.Channel_Downscalers = None
        

        #if a texture block is provided in the kwargs then we load the texture as we build the class
        if "Texture_Block" in kwargs:
            #create/set this class's variables to those in the texture block
            self.Load_New_Texture(**kwargs)
            

    def Set_Deep_Color_Mode(self, Deep_State=None):
        """Allows changing the unpacking mode of this module from "true color"(32BPP)
           to "deep color"(64BPP). If the argument is None, the mode will be the
           default one set in Format_Defs, if False the unpack format will be
           Format_A8R8G8B8, and if True the format will be FORMAT_A16R16G16B16."""
        if Deep_State is None:
            self._UNPACK_FORMAT = DEFAULT_UNPACK_FORMAT
            self._UNPACK_ARRAY_CODE = INVERSE_PIXEL_ENCODING_SIZES[max(FORMAT_CHANNEL_DEPTHS[self._UNPACK_FORMAT])//8]
        else:
            if Deep_State:
                self._UNPACK_FORMAT = FORMAT_A16R16G16B16
                self._UNPACK_ARRAY_CODE = "H"
            else:
                self._UNPACK_FORMAT = FORMAT_A8R8G8B8
                self._UNPACK_ARRAY_CODE = "B"


    #call this when providing the convertor with a new list of pixel arrays
    def Load_New_Texture(self, **kwargs):
        
        try:
            if "Texture_Block" not in kwargs:
                print("ERROR: NO BITMAP BLOCK SUPPLIED.\n",
                      "CANNOT LOAD BITMAP WITHOUT A SUPPLIED BITMAP BLOCK")
                self.Texture_Block = None
                return
            else: Texture_Block = kwargs["Texture_Block"]
            
            if "Texture_Info" not in kwargs:
                print("ERROR: BITMAP BLOCK SUPPLIED HAS NO TEXTURE INFO.\n",
                      "CANNOT LOAD BITMAP WITHOUT A DESCRIPTION OF THE BITMAP")
                self.Texture_Block = None
                return
            else: Texture_Info = kwargs["Texture_Info"]
            
            if "Format" not in Texture_Info:
                print("ERROR: THE SUPPLIED BITMAP'S INFO BLOCK HAS NO FORMAT ENTRY!\n",
                      "CAN NOT LOAD BITMAP WITHOUT KNOWING THE BITMAP'S FORMAT.")
                self.Texture_Block = None
                return
            
            if Texture_Info["Format"] not in VALID_FORMATS:
                print("ERROR: THE SUPPLIED BITMAP IS IN AN UNKNOWN FORMAT!\n",
                      "IF YOU WISH TO USE THIS FORMAT YOU MUST INCOROPRATE IT YOURSELF.")
                self.Texture_Block = None
                return

            #if provided with just a pixel data array we will need to put it inside a list
            if isinstance(Texture_Block, array):
                Texture_Block = [Texture_Block]
            
            #initialize the optional bitmap DESCRIPTION variables
            self.Depth = 1
            self.Sub_Bitmap_Count = 1
            self.Mipmap_Count = 0
            self.Swizzled = False
            self.Filepath = None
            self.Palette = None
            self.Palettized_Unpacker = None
            self.Palettized_Packer = None
            self.Palette_Unpacker = None
            self.Palette_Packer = None
            self.Indexing_Unpacker = None
            self.Indexing_Packer = None
            self.Indexing_Size = DEFAULT_INDEXING_SIZE
            
            
            #get the bitmap's info from the texture block's info dictionary
            self.Width = Texture_Info["Width"]
            self.Height = Texture_Info["Height"]
            self.Format = Texture_Info["Format"]
            self.Texture_Type = TYPE_2D
            self.Packed = self.Palette_Packed = True
            self.Channel_Order = C_ORDER_DEFAULT
            
            if "Depth" in Texture_Info:
                self.Depth = Texture_Info["Depth"]
            
            if "Swizzled" in Texture_Info:
                self.Swizzled = Texture_Info["Swizzled"]
            
            if "Sub_Bitmap_Count" in Texture_Info and Texture_Info["Sub_Bitmap_Count"] > 0:
                self.Sub_Bitmap_Count = Texture_Info["Sub_Bitmap_Count"]
            
            if "Mipmap_Count" in Texture_Info:
                self.Mipmap_Count = Texture_Info["Mipmap_Count"]
            
            if "Packed" in Texture_Info:
                self.Packed = Texture_Info["Packed"]

            if "Deswizzler" in Texture_Info:
                if Swizzler is not None:
                    self.Deswizzler = Swizzler.Swizzler(Texture_Convertor = self,
                                                        Mask_Type = Texture_Info["Deswizzler"])
                else:
                    print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")
            else:
                if Swizzler is not None:
                    self.Deswizzler = Swizzler.Swizzler(Texture_Convertor = self, Mask_Type = "DEFAULT")

            if "Texture_Type" in Texture_Info:
                self.Texture_Type = Texture_Info["Texture_Type"]
                
            if "Channel_Order" in Texture_Info:
                self.Channel_Order = Texture_Info["Channel_Order"]
                
            if "Filepath" in Texture_Info:
                self.Filepath = Texture_Info["Filepath"]
                
            if "Palette" in Texture_Info and Texture_Info["Palette"] is not None:
                if "Indexing_Size" in Texture_Info and Texture_Info["Indexing_Size"] not in (0, None):
                    self.Palette = Texture_Info["Palette"]
                    self.Indexing_Size = Texture_Info["Indexing_Size"]
                    self.Palettize = True
                    
                    if "Palette_Packed" in Texture_Info:
                        self.Palette_Packed = Texture_Info["Palette_Packed"]
                else:
                    print("ERROR: PALETTE WAS SUPPLIED, BUT BIT-SIZE OF INDEXING WAS NOT.")
                    return

            if "Palettized_Unpacker" in Texture_Info:
                  self.Palettized_Unpacker = Texture_Info["Palettized_Unpacker"]
            else: self.Palettized_Unpacker = self._Unpack_Palettized

            if "Palettized_Packer" in Texture_Info:
                  self.Palettized_Packer = Texture_Info["Palettized_Packer"]
            else: self.Palettized_Packer = self._Pack_Palettized

            if "Palette_Unpacker" in Texture_Info:
                  self.Palette_Unpacker = Texture_Info["Palette_Unpacker"]
            else: self.Palette_Unpacker = self._Unpack_Palette

            if "Indexing_Unpacker" in Texture_Info:
                  self.Indexing_Unpacker = Texture_Info["Indexing_Unpacker"]
            else: self.Indexing_Unpacker = self._Unpack_Indexing

            if "Palette_Packer" in Texture_Info:
                  self.Palette_Packer = Texture_Info["Palette_Packer"]
            else: self.Palette_Packer = self._Pack_Palette

            if "Indexing_Packer" in Texture_Info:
                  self.Indexing_Packer = Texture_Info["Pack_Indexing"]
            else: self.Indexing_Packer = self._Pack_Indexing


            #we may have been provided with conversion settings at the same time we were given the texture
            self.Load_New_Conversion_Settings(**kwargs)
                
            self.Texture_Block = Texture_Block
            self.Texture_Info = Texture_Info
        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD TEXTURE INTO BITMAP CONVERTOR")
            print(format_exc())


    def Load_New_Conversion_Settings(self, **kwargs):
        #only run if there is a valid texture block loaded
        if (self.Texture_Info is None and
            ("Texture_Info" not in kwargs or kwargs["Texture_Info"] is None)):
            print("ERROR: CANNOT LOAD CONVERSION SETTINGS WITHOUT A LOADED TEXTURE.")
            return

        """RESETTING THE CONVERSION VARIABLES EACH TIME IS INTENTIONAL
        TO PREVENT ACCIDENTALLY LEAVING INCOMPATIBLE ONES SET"""
        try:
            #initialize the bitmap CONVERSION variables
            self.Target_Format = self.Format
            self.One_Bit_Bias = 127
            self.Downres_Amount = 0
            self.Generate_Mipmaps = False
            self.Swizzler_Mode = self.Swizzled
            self.Gamma = 1.0
            self.Color_Key_Transparency = False
            self.Reswizzler = self.Deswizzler
            self.Palette_Picker = self.Default_Palette_Picker
            self.Palettize = self.Is_Palettized()
            self.Target_Indexing_Size = self.Indexing_Size
            self.Channel_Mapping = None
            self.Channel_Merge_Mapping = None
            self.Repack = True
            
            if "Target_Format" in kwargs and kwargs["Target_Format"] in VALID_FORMATS:
                self.Target_Format = kwargs["Target_Format"]
            
            if self.Target_Format in DDS_FORMATS and Swizzler is None:
                print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT COMPRESS TO DXT WITHOUT SWIZZLER. SWITCHING TO A8R8G8B8.")
                self.Target_Format = self._UNPACK_FORMAT
                
            if "One_Bit_Bias" in kwargs:
                self.One_Bit_Bias = kwargs["One_Bit_Bias"]
                
            if "Downres_Amount" in kwargs and kwargs["Downres_Amount"] > 0:
                #we only want whole number times to cut the resolution in half
                self.Downres_Amount = int(kwargs["Downres_Amount"])
                
            if "Generate_Mipmaps" in kwargs and kwargs["Generate_Mipmaps"]:
                #if we are being told to create more mipmaps this is how many more to make
                self.Generate_Mipmaps = kwargs["Generate_Mipmaps"]
                
            if "Swizzler_Mode" in kwargs:
                #whether to swizzle or deswizzle the bitmap when the swizzler is called
                '''False = Deswizzle the bitmap    True = Swizzle the bitmap'''
                self.Swizzler_Mode = kwargs["Swizzler_Mode"]
                
            if "Gamma" in kwargs:
                self.Gamma = kwargs["Gamma"]
                
            if "Repack" in kwargs:
                self.Repack = kwargs["Repack"]
                
            if "Color_Key_Transparency" in kwargs:
                self.Color_Key_Transparency = kwargs["Color_Key_Transparency"]

            if "Reswizzler" in kwargs:
                if Swizzler is not None:
                    self.Reswizzler = Swizzler.Swizzler(Texture_Convertor = self,
                                                        Mask_Type=kwargs["Reswizzler"])
                else:
                    print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")
                
            if "Palette_Picker" in kwargs:
                self.Palette_Picker = kwargs["Palette_Picker"]
                
            if "Palettize" in kwargs:
                self.Palettize = kwargs["Palettize"]

            if "Target_Indexing_Size" in kwargs:
                self.Target_Indexing_Size = kwargs["Target_Indexing_Size"]
            
            #set up all the channel mappings and such
            self._Set_All_Channel_Mappings(**kwargs)

        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD CONVERSION SETTINGS INTO BITMAP CONVERTOR.\n"
                  "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
            print(format_exc())
            self.Texture_Block = None


    def Print_Info(self, Print_Texture_Info=True, Print_Conversion_Settings=False,
                   Print_Channel_Mappings=False, Print_Methods=False, Print_Scalers=False):
        if Print_Texture_Info:
            print("Texture Info:")
            print("   Filepath:", self.Filepath)
            print("   Type:", self.Texture_Type)
            print("   Format:", self.Format)
            print("   Width:", self.Width)
            print("   Height:", self.Height)
            print("   Depth:", self.Depth)
            print()
            print("   Sub_Bitmap_Count:", self.Sub_Bitmap_Count)
            print("   Mipmap_Count:", self.Mipmap_Count)
            print("   Swizzled:", self.Swizzled)
            print()
            print("   Currently_Packed:", self.Packed)
            print("   Is_Palettized:", self.Is_Palettized())
            if self.Is_Palettized():
                print()
                print("   Palette_Currently_Packed:", self.Palette_Packed)
                print("   Indexing_Size:", self.Indexing_Size)
            print()
            
        if Print_Conversion_Settings:
            print("Conversion Settings:")
            print("   Photoshop_Compatibility:", self.Photoshop_Compatibility)
            print("   Target_Format:", self.Target_Format)
            print("   Target_Indexing_Size:", self.Target_Indexing_Size)
            print()
            print("   One_Bit_Bias:", self.One_Bit_Bias)
            print("   Gamma:", self.Gamma)
            print("   Swizzler_Mode:", self.Swizzler_Mode)
            print("   Downres_Amount:", self.Downres_Amount)
            print("   Generate_Mipmaps:", self.Generate_Mipmaps)
            print()
            print("   Color_Key_Transparency:", self.Color_Key_Transparency)
            print("   Make\\Keep_Palettized:", self.Palettize)
            print("   Repack:", self.Repack)
            print("   Channel_Mapping:", self.Channel_Mapping)
            print("   Channel_Merge_Mapping:", self.Channel_Merge_Mapping)
            print()
            print("   Unpack_Format:", self._UNPACK_FORMAT)
            print("   Unpack_Array_Code:", self._UNPACK_ARRAY_CODE)
            print("   Channel_Order:", self.Channel_Order)
            print()
            
        if Print_Channel_Mappings:
            print("Channel Mapping Variables:")
            print("   Source_Depths:", self.Source_Depths)
            print("   Unpacked_Depths:", self.Unpacked_Depths)
            print("   Target_Depths:", self.Target_Depths)
            print()
            print("   Source_Channel_Count:", self.Source_Channel_Count)
            print("   Unpacked_Channel_Count:", self.Unpacked_Channel_Count)
            print("   Target_Channel_Count:", self.Target_Channel_Count)
            print()
            print("   Swapping_Channels:", self.Swapping_Channels)
            print()
            print("   Channel_Mapping:", self.Channel_Mapping)
            print("   Channel_Merge_Mapping:", self.Channel_Merge_Mapping)
            print()
            print("   Channel_Offsets:", self.Channel_Offsets)
            print("   Channel_Depths:", self.Channel_Depths)
            print("   Channel_Merge_Divisors:", self.Channel_Merge_Divisors)
            print()

        if Print_Methods:
            print("Bound Methods:")
            print("   Palettized_Unpacker:", self.Palettized_Unpacker)
            print("   Palettized_Packer:", self.Palettized_Packer)
            print()
            print("   Palette_Unpacker:", self.Palette_Unpacker)
            print("   Palette_Packer:", self.Palette_Packer)
            print()
            print("   Indexing_Unpacker:", self.Indexing_Unpacker)
            print("   Indexing_Packer:", self.Indexing_Packer)
            print()
            print("   Reswizzler:", self.Reswizzler)
            print("   Deswizzler:", self.Deswizzler)
            print("   Palette_Picker:", self.Palette_Picker)
            print("   Default_Palette_Picker:", self.Default_Palette_Picker)

        if Print_Scalers:
            print("Scaler Arrays:")
            print("   Channel_Upscalers:", self.Channel_Upscalers)
            print("   Channel_Downscalers:", self.Channel_Downscalers)
            print("   Gamma_Scaler:", self.Gamma_Scaler)
            print()


    def _Set_All_Channel_Mappings(self, **kwargs):
        """Sets(or defaults) all the different channel mappings"""
        try:
            self.Source_Channel_Count = FORMAT_CHANNEL_COUNTS[self.Format]
            self.Unpacked_Channel_Count = FORMAT_CHANNEL_COUNTS[self.Format]
            self.Target_Channel_Count = FORMAT_CHANNEL_COUNTS[self.Target_Format]

            """CREATE THE CHANNEL LOAD MAPPING"""
            self._Set_Channel_Load_Mapping(**kwargs)
            
            #If the format is DXT then the merge mapping will have JUST BEEN padded and set
            if self.Channel_Merge_Mapping is not None:
                kwargs["Channel_Merge_Mapping"] = self.Channel_Merge_Mapping

            """CREATE THE CHANNEL MERGE MAPPING"""
            self._Set_Channel_Merge_Mapping(**kwargs)

            """CREATE THE CHANNEL UP AND DOWN SCALER LISTS"""
            self._Set_Upscalers_and_Downscalers(**kwargs)
            
            """CREATE THE CHANNEL GAMMA SCALER LISTS"""
            self._Set_Gamma_Scaler(**kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO CREATE CHANNEL MAPPINGS AND SCALERS")
            print(format_exc())


        
    def Is_Palettized(self, Palette_Index=0):
        '''returns whether or not there is a valid palette for the bitmap at the index provided'''
        return( self.Palette is not None and
                ( (hasattr(self.Palette, '__iter__') and len(self.Palette) > Palette_Index)
                  and self.Palette[Palette_Index] is not None) )

    
    def _Set_Gamma_Scaler(self, **kwargs):
        '''creates the list per channel for the gamma scaling'''
        if isinstance(self.Gamma,(int,float)):
            self.Gamma = [self.Gamma]*self.Unpacked_Channel_Count
        elif len(self.Gamma) < self.Unpacked_Channel_Count:
            #if there aren't enough indexes in the gamma scalar we repeat
            #the last element in the scalar list for each missign channel
            Old_Gamma_Len = len(self.Gamma)
            for i in range(self.Unpacked_Channel_Count-Old_Gamma_Len):
                self.Gamma.append(self.Gamma[Old_Gamma_Len-1])
        
        self.Gamma_Scaler = [0]*self.Unpacked_Channel_Count
        #this array will be used to quickly convert a color
        #channel value from a linear value to a gamma scaled value
        for Channel in range(self.Unpacked_Channel_Count):
            self.Gamma_Scaler[Channel] = array("f",[0.0]*self.Unpacked_Channel_Count)
            for Value in range(256):
                self.Gamma_Scaler[Channel].append(( (float(Value)/255)**self.Gamma[Channel])*255)


    def _Set_Upscalers_and_Downscalers(self, **kwargs):
        '''NEED TO ADD A DESCRIPTION'''
        
        #specifies what depth we want to unpack each channel from
        self.Source_Depths = FORMAT_CHANNEL_DEPTHS[self.Format][:]
        #specifies what depth we want to unpack each channel to
        self.Unpacked_Depths = FORMAT_CHANNEL_DEPTHS[self._UNPACK_FORMAT][:self.Unpacked_Channel_Count]
        #specifies what depth we want to repack each channel to
        self.Target_Depths = FORMAT_CHANNEL_DEPTHS[self.Target_Format][:]
        
        #each index is a list to upscale the source depth to the unpacked depth
        self.Channel_Upscalers = []
        self.Channel_Downscalers = []

        if self.Channel_Merge_Mapping is not None:
            self.Target_Depths = []
            for i in range(len(self.Unpacked_Depths)):
                self.Target_Depths.append(FORMAT_CHANNEL_DEPTHS[self.Target_Format]
                                          [self.Channel_Merge_Mapping[i]])

        
        """BUILD THE UPSCALER ARRAYS"""
        for i in range(len(self.Unpacked_Depths)):
            #figure out how large the entries in the arrays need to be
            Array_Encoding = INVERSE_PIXEL_ENCODING_SIZES[int(ceil(self.Unpacked_Depths[self.Channel_Mapping[i]]/8.0))]
            #make a new array to map the source values to their upscaled values
            self.Channel_Upscalers.append(array(Array_Encoding, []))

            #this is the amount the values will be scaled to and from depths
            if self.Source_Depths[self.Channel_Mapping[i]] == 0: Scale = 0.0000000001
            else: Scale = (2**self.Unpacked_Depths[i]-1) / (2**self.Source_Depths[self.Channel_Mapping[i]]-1)
            
            for Value in range(2**self.Source_Depths[self.Channel_Mapping[i]]):
                self.Channel_Upscalers[i].append(int(round( Value * Scale )))


        """BUILD THE DOWNSCALER ARRAYS"""
        for i in range(len(self.Target_Depths)):
            #figure out how large the entries in the arrays need to be
            Array_Encoding = INVERSE_PIXEL_ENCODING_SIZES[int(ceil(self.Unpacked_Depths[i]/8.0))]
            #make a new array to map the target values to their downscaled values
            self.Channel_Downscalers.append(array(Array_Encoding, []))
            
            if self.Target_Depths[i] == 1:
                #if the source depth is 1 bit we use a bias to determine what is white and black
                for Value in range(2**self.Unpacked_Depths[i]):
                    self.Channel_Downscalers[i].append(int(Value >= self.One_Bit_Bias))
            else:
                #this is the amount the values will be scaled to and from depths
                if self.Unpacked_Depths[i] == 0: Scale = 0.0000000001
                else: Scale = (2**self.Target_Depths[i]-1) / (2**self.Unpacked_Depths[i]-1)
                
                for Value in range(2**self.Unpacked_Depths[i]):
                    self.Channel_Downscalers[i].append(int(round( Value * Scale )))


    def _Set_Channel_Load_Mapping(self, **kwargs):
        """THIS FUNCTION CREATES MAPPINGS THAT ALLOW US TO
        SWAP CHANNELS AROUND PER PIXEL AS THEY ARE UNPACKED"""
        
        if "Channel_Mapping" in kwargs:
            self.Channel_Mapping = array("b",kwargs["Channel_Mapping"])
            self.Swapping_Channels = True
        else:
            self.Channel_Mapping = array("b",range(self.Source_Channel_Count))
            self.Swapping_Channels = False

        
        """ONLY RUN IF WE CAN FIND THE FORMAT WE ARE LOADING IN THE CHANNEL MASKS"""
        #it is possible to have a valid format that doesn't have channel masks.
        #if the format is compressed or palettized it wont work with this method
        if self.Format in FORMAT_CHANNEL_MASKS:
            
            #create the default offset, mask, and depth arrays
            self.Channel_Masks = array("Q", FORMAT_CHANNEL_MASKS[self.Format])
            self.Channel_Offsets = array("B", FORMAT_CHANNEL_OFFSETS[self.Format])
            self.Channel_Depths = array("B", FORMAT_CHANNEL_DEPTHS[self.Format])

            if "Channel_Mapping" in kwargs:
                #set the number of channels to how many are in the channel mapping
                self.Unpacked_Channel_Count = len(kwargs["Channel_Mapping"])
                self.Channel_Masks = array("I", [])
                self.Channel_Offsets = array("B", [])
                self.Channel_Depths = array("B", [])
                """THE BELOW CODE WILL SWAP AROUND THE OFFSETS, MASKS, AND CHANNEL DEPTHS PER CHANNEL.
                THIS WILL ALLOW US TO SWITCH CHANNELS WITH EACH OTHER BY CHANGING THE ORDER WE UNPACK THEM."""
                for i in range(len(self.Channel_Mapping)):
                    Channel = self.Channel_Mapping[i]
                    
                    if Channel < 0 or Channel >= self.Source_Channel_Count:
                        """if the channel index provided is outside the number
                        of channels we have, it means to make a blank channel.
                        this will be used for things like A8 to self._UNPACK_FORMAT"""
                        self.Channel_Masks.append(0)
                        self.Channel_Offsets.append(0)
                        
                        #we preserve the alpha channel depth so we can set it to full white
                        if i == 0: self.Channel_Depths.append(FORMAT_CHANNEL_DEPTHS[self.Format][0])
                        else: self.Channel_Depths.append(0)
                    else:
                        """otherwise build the channel masks/offsets/depths from
                        the approporate template arrays for the channel specified"""
                        self.Channel_Masks.append(FORMAT_CHANNEL_MASKS[self.Format][Channel])
                        self.Channel_Offsets.append(FORMAT_CHANNEL_OFFSETS[self.Format][Channel])
                        self.Channel_Depths.append(FORMAT_CHANNEL_DEPTHS[self.Format][Channel])


            '''if this is a DDS format we need to unpack it to 4 channels no matter what. in
            order for that to work we need to pad the channel mapping and the merge mapping'''
            if self.Format in DDS_FORMATS and self.Unpacked_Channel_Count < 4:
                #pad the channel mapping
                for i in range(self.Unpacked_Channel_Count, 4):
                    self.Channel_Mapping.append(i)
                    
                #check if there is a merge mapping
                if "Channel_Merge_Mapping" in kwargs:
                    #pad the merge mapping
                    self.Channel_Merge_Mapping = array("b", kwargs["Channel_Merge_Mapping"])
                    
                    for i in range(self.Unpacked_Channel_Count, 4):
                        self.Channel_Merge_Mapping.append(-1)
                else:
                    #create a merge mapping if none exists
                    self.Channel_Merge_Mapping = array("b", [0,1,2,3])
                    for i in range(4):
                        if self.Channel_Mapping[i] == -1 or self.Channel_Mapping[i] >= self.Target_Channel_Count:
                            self.Channel_Merge_Mapping[i] = -1
                            
                self.Unpacked_Channel_Count = 4


    def _Set_Channel_Merge_Mapping(self, **kwargs):
        """THIS FUNCTION ALLOWS US TO SPECIFY HOW CHANNELS
        ARE MERGED WHEN CONVERTING TO A DIFFERENT FORMAT"""
        
        """
        Channel_Merge_Mapping:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE ORIGINAL FORMAT. EACH
        INDEX WILL BE THE CHANNEL OF THE TARGET FORMAT TO ADD THE CHANNEL INTO.

        Channel_Merge_Divisors:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE TARGET FORMAT. EACH
        INDEX WILL STORE AN INTEGER. THIS INTEGER WILL BE THE NUMBER OF CHANNELS
        THAT HAVE BEEN ADDED TOGETHER FROM THE ORIGINAL FORMAT INTO THIS CHANNEL.
        THE PURPOSE OF THIS ARRAY WILL BE TO QUICKLY DIVIDE THE ADDED TOGETHER
        CHANNELS TO GET A RANGE WITHIN THE CHANNEL'S DEPTH
        """
        
        #if the unpacked number of channels is more than the target format then we need to merge some
        if self.Unpacked_Channel_Count > self.Target_Channel_Count:
            if "Channel_Merge_Mapping" in kwargs:

                #only use the mapping provided if it is the same length as the unpacked channel count
                if len(kwargs["Channel_Merge_Mapping"]) == self.Unpacked_Channel_Count:
                    if self.Channel_Merge_Mapping is None:
                        self.Channel_Merge_Mapping = array("b",kwargs["Channel_Merge_Mapping"])
                else:
                    print("ERROR: INVALID NUMBER OF CHANNELS IN CHANNEL MERGE MAPPING.\nEXPECTED",
                          self.Unpacked_Channel_Count, "CHANNELS BUT GOT", len(kwargs["Channel_Merge_Mapping"]), ".\n",
                          "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
                    self.Texture_Block = None

                self.Channel_Merge_Divisors = array("q",[0]*self.Target_Channel_Count)
                
                #loop through the length of the convert channel mapping
                for i in self.Channel_Merge_Mapping:
                    """WHAT WE ARE DOING HERE IS ADDING 1 TO EACH CHANNEL'S DIVISOR IN THE
                    TARGET FORMAT FOR EVERY CHANNEL FROM THE ORIGINAL FORMAT BEING MERGED IN"""
                    if i >= 0:
                        self.Channel_Merge_Divisors[i] += 1
                
            else:
                print("ERROR: CONVERTING FROM FORMAT WITH", self.Source_Channel_Count,
                      "CHANNELS TO FORMAT WITH", self.Target_Channel_Count, "CHANNELS.\n",
                      "A MAPPING IS NEEDED TO SPECIFY WHAT SHOULD BE MERGED WITH WHAT.\n",
                      "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
                self.Texture_Block = None
        else:
            self.Channel_Merge_Mapping = None

        #because the merge mapping will reference index -1 it will be the last index.
        #because we are appending an additional divisor of 256 it will be erased when packed
        if self.Channel_Merge_Mapping is not None and -1 in self.Channel_Merge_Mapping:
            self.Channel_Merge_Divisors.append(CHANNEL_ERASE_DIVISOR)



    def Save_to_File(self, **kwargs):
        try:
            """saves the loaded bitmap to a file"""
            
            if "Output_Path" in kwargs:
                Output_Path = kwargs["Output_Path"]
                del(kwargs["Output_Path"])
            else:
                if self.Filepath is None:
                    print("BITMAP SAVE ERROR: MISSING OUTPUT PATH.")
                    return
                else:
                    Output_Path = self.Filepath
            
            if self.Texture_Block is None:
                print("BITMAP SAVE ERROR: NO TEXTURE LOADED.")
                return
                
            if Bitmap_IO is None:
                print("BITMAP SAVE ERROR: BITMAP IO MODULE NOT LOADED.")
                return

            #if the extension isnt provided in the kwargs we try to get it from the filepath
            if "Ext" in kwargs:
                Format_Ext = kwargs["Ext"]
            else:
                SplitPath = path.splitext(Output_Path)
                Output_Path = SplitPath[0]
                Format_Ext = SplitPath[1][1:]

            if Format_Ext.lower() not in Bitmap_IO.File_Writers:
                print("BITMAP SAVE ERROR: UNKNOWN BITMAP FILE EXPORT FORMAT: ", Format_Ext.lower())
                return
            Bitmap_IO.File_Writers[Format_Ext.lower()](self, Format_Ext, Output_Path, **kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO SAVE BITMAP TO FILE.")
            print(format_exc())


    def Load_from_File(self, **kwargs):
        try:
            """loads the current bitmap from a file"""
            
            if "Input_Path" in kwargs:
                Input_Path = kwargs["Input_Path"]
                del(kwargs["Input_Path"])
            else:
                if self.Filepath is None:
                    print("BITMAP LOAD ERROR: MISSING INPUT PATH.")
                    return
                else:
                    Input_Path = self.Filepath
                    
            if Bitmap_IO is None:
                print("BITMAP LOAD ERROR: BITMAP IO MODULE NOT LOADED.")
                return

            #if the extension isnt provided in the kwargs we try to get it from the filepath
            if "Ext" in kwargs:
                Format_Ext = kwargs["Ext"]
            else:
                SplitPath = path.splitext(Input_Path)
                Input_Path = SplitPath[0]
                Format_Ext = SplitPath[1][1:]
            
            if Format_Ext.lower() not in Bitmap_IO.File_Readers:
                print("BITMAP LOAD ERROR: UNKNOWN BITMAP FILE IMPORT FORMAT: ", Format_Ext.lower())
                return
            
            Bitmap_IO.File_Readers[Format_Ext.lower()](self, Format_Ext, Input_Path, **kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO LOAD BITMAP FROM FILE.")
            print(format_exc())
        


    def Convert_Texture(self):
        """Runs all the conversions routines for the parameters specified"""

        #only run if there is a valid texture block loaded
        if self.Texture_Block is not None:
            try:
                Format = self.Format
                Target_Format = self.Target_Format
            
                '''if we want to reduce the resolution, but we have mipmaps, we can quickly
                reduce it by removing the larger bitmaps and using the mipmaps instead'''
                while self.Mipmap_Count > 0 and self.Downres_Amount > 0:
                    if (self.Width  in Powers_of_2 and
                        self.Height in Powers_of_2 and
                        self.Depth  in Powers_of_2):
                        #remove one mipmap level for each sub-bitmap
                        for Sub_Bitmap_Index in range(self.Sub_Bitmap_Count):
                            self.Texture_Block.pop(0)

                        #divide the dimensions in half and make sure they don't go below the minimum
                        self.Width, self.Height, self.Depth = Dimension_Lower_Bound_Check(self.Width//2,
                                                                                          self.Height//2,
                                                                                          self.Depth//2,
                                                                                          Format)
                        self.Downres_Amount -= 1
                        self.Mipmap_Count -= 1
                        self.Texture_Info["Width"] = self.Width
                        self.Texture_Info["Height"] = self.Height
                        self.Texture_Info["Depth"] = self.Depth
                        self.Texture_Info["Mipmap_Count"] = self.Mipmap_Count
                    else:
                        print("ERROR: CANNOT DOWNSCALE NON-POWER-OF-2 BITMAPS.")
                        self.Downres_Amount = 0
                    
                
                '''only run this section if we are doing at least one of these things:'''
                #Converting to a different format
                #Downsampling the bitmap
                #Generating mipmaps
                #Swapping the bitmap's channels.
                if (Format != Target_Format or self.Downres_Amount > 0 or
                    self.Swapping_Channels or self.Generate_Mipmaps):
                    
                    '''if the texture is swizzled then need to unswizzle it before we
                    can do certain conversions with it. We can't downsample it while
                    swizzled nor convert to a compressed format(swizzling unsupported)'''
                    if self.Swizzled and (self.Downres_Amount > 0 or self.Generate_Mipmaps or
                                          Target_Format in COMPRESSED_FORMATS):
                        if Swizzler is not None:
                            self.Deswizzler.Swizzle_Texture(True)
                        else:
                            print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

                    '''figure out if we need to depalettize. some formats wont
                    support palettes, like DXT1-5, and downressing and other
                    operations will require pixels to be explicitely defined'''
                    if (Target_Format in COMPRESSED_FORMATS or self.Downres_Amount > 0) and self.Is_Palettized():
                        self.Palettize = False

                    
                    """CONVERT PACKED PIXELS INTO UNPACKED CHANNEL VALUES.
                    CHANNEL SWAPPING IS INTEGRATED INTO UNPACKING THE PIXELS"""
                    if self.Packed:
                        #store the dimensions to local variables so we can change them
                        Width, Height, Depth = self.Width, self.Height, self.Depth
                        
                        for Mipmap_Index in range(self.Mipmap_Count+1):
                            
                            for Sub_Bitmap in range(self.Sub_Bitmap_Count):
                                #get the index of the bitmap we'll be working with
                                Bitmap_Index = Sub_Bitmap + (Mipmap_Index*self.Sub_Bitmap_Count)
                                
                                if self.Is_Palettized(Bitmap_Index):
                                    #unpack the bitmap's palette and indexing
                                    Unpacked_Palette, Unpacked_Pixels = self.Palettized_Unpacker(self.Palette[Bitmap_Index],
                                                                                                 self.Texture_Block[Bitmap_Index])
                                    if not Unpacked_Pixels:
                                        return(False)
                                    
                                    '''replace the packed palette with the unpacked one'''
                                    self.Palette[Bitmap_Index] = Unpacked_Palette
                                else:
                                    Unpacked_Pixels = self.Unpack(Bitmap_Index, Width, Height, Depth)
                                    if Unpacked_Pixels is None:
                                        print("ERROR: UNABLE TO UNPACK IMAGE DATA. CONVERSION CANCELLED.")
                                        return(False)
                                    
                                #now that we are done unpacking the pixel data we
                                #replace the packed array with the unpacked one
                                self.Texture_Block[Bitmap_Index] = Unpacked_Pixels

                            #calculate the dimensions for the next mipmap
                            Width, Height, Depth = Dimension_Lower_Bound_Check(Width//2,Height//2,Depth//2)
                            
                        self.Packed = False
                        self.Palette_Packed = False


                    
                    '''DOWNRES BITMAP TO A LOWER RESOLUTION IF STILL NEEDING TO'''
                    #only run if there aren't any mipmaps and
                    #this bitmap still needs to be downressed
                    if self.Mipmap_Count == 0 and self.Downres_Amount > 0:
                        if Swizzler is not None:
                            for Sub_Bitmap in range(self.Sub_Bitmap_Count):
                                Downressed_Pixel_Array, Width, Height, Depth = self._Downsample_Bitmap(self.Texture_Block[Sub_Bitmap],
                                                                                                       self.Downres_Amount, self.Width,
                                                                                                       self.Height, self.Depth, True)
                                
                                #now that we are done repacking the pixel data we replace the old pixel array with the new one
                                self.Texture_Block[Sub_Bitmap] = Downressed_Pixel_Array
                                
                            self.Downres_Amount = 0
                            self.Texture_Info["Width"] = self.Width = Width
                            self.Texture_Info["Height"] = self.Height = Height
                            self.Texture_Info["Depth"] = self.Depth = Depth
                        else:
                            self.Downres_Amount = 0
                            print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT DOWNRES WITHOUT SWIZZLER.")



                    '''GENERATE MIPMAPS FOR BITMAP'''
                    if self.Generate_Mipmaps:
                        if Swizzler is not None:
                            New_Mipmap_Count = Logs_of_2[max(self.Width, self.Height, self.Depth)]
                            Mipmaps_to_Make = New_Mipmap_Count - self.Mipmap_Count
                            
                            if Mipmaps_to_Make:
                                
                                #get the current smallest dimensions so we can change them
                                Mip_Width, Mip_Height, Mip_Depth = Dimension_Lower_Bound_Check(self.Width//(2**self.Mipmap_Count),
                                                                                               self.Height//(2**self.Mipmap_Count),
                                                                                               self.Depth//(2**self.Mipmap_Count))
                                #Loop for each mipmap we need to make
                                for Mipmap in range(self.Mipmap_Count, New_Mipmap_Count):
                                    for Sub_Bitmap in range(self.Sub_Bitmap_Count):
                                        
                                        if self.Is_Palettized(Bitmap_Index):
                                            #################################################################################
                                            """############ NEED TO WRITE ROUTINE FOR MAKING PALETTIZED MIPS #############"""
                                            #################################################################################

                                            #FOR NOW WE'LL PREVENT MIPS FROM BEING CREATED BY RESETTING THE MIPMAP COUNT
                                            New_Mipmap_Count = self.Mipmap_Count
                                        else:
                                            #get the array of packed pixels we'll be working with
                                            Mipmap_Pixel_Array = self.Texture_Block[Mipmap*self.Sub_Bitmap_Count + Sub_Bitmap]
                                            
                                            Mipmap_Pixel_Array, _, __, ___ = self._Downsample_Bitmap(Mipmap_Pixel_Array, 1,
                                                                                                     Mip_Width, Mip_Height, Mip_Depth)
                                            self.Texture_Block.append(Mipmap_Pixel_Array)
                                    
                                    #calculate the dimensions for the next mipmap
                                    Mip_Width, Mip_Height, Mip_Depth = Dimension_Lower_Bound_Check(Mip_Width//2,
                                                                                                   Mip_Height//2,
                                                                                                   Mip_Depth//2)
                                #change the mipmap count in the settings
                                self.Texture_Info["Mipmap_Count"] = self.Mipmap_Count = New_Mipmap_Count
                        else:
                            print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT GENERATE MIPMAPS WITHOUT SWIZZLER.")



                    '''REPACK THE PIXEL DATA TO THE TARGET FORMAT'''
                    if self.Repack:
                        #store the dimensions to local variables so we can change them
                        Width, Height, Depth = self.Width, self.Height, self.Depth

                        #if we are palettizing a non-palettized bitmap, we need new palette
                        if self.Palettize and not self.Is_Palettized():
                            self.Palette = [None]*(self.Mipmap_Count+1)*self.Sub_Bitmap_Count

                        for Mipmap_Index in range(self.Mipmap_Count+1):
                            for Sub_Bitmap in range(self.Sub_Bitmap_Count):
                                #get the index of the bitmap we'll be working with
                                Bitmap_Index = Sub_Bitmap + (Mipmap_Index*self.Sub_Bitmap_Count)

                                if self.Palettize:
                                    if self.Is_Palettized(Bitmap_Index):
                                        #get the unpacked palette and indexing we'll be working with
                                        Unpacked_Palette = self.Palette[Bitmap_Index]
                                        Unpacked_Indexing = self.Texture_Block[Bitmap_Index]
                                    else:
                                        #pass the pixels over to the function to create a color palette and indexing from it
                                        Unpacked_Palette, Unpacked_Indexing = self.Palette_Picker(self.Texture_Block[Bitmap_Index])

                                    Packed_Palette, Packed_Indexing = self.Palettized_Packer(Unpacked_Palette,
                                                                                             Unpacked_Indexing)
                                    self.Palette[Bitmap_Index] = Packed_Palette
                                    self.Texture_Block[Bitmap_Index] = Packed_Indexing
                                else:
                                    Repacked_Pixel_Array = self.Pack(self.Texture_Block[Bitmap_Index],
                                                                     Width, Height, Depth)
                                    if Repacked_Pixel_Array is None:
                                        print("ERROR: UNABLE TO PACK IMAGE DATA. CONVERSION CANCELLED.")
                                        return(False)
                                    
                                    #now that we are done repacking the pixel data we replace the old pixel array with the new one
                                    self.Texture_Block[Bitmap_Index] = Repacked_Pixel_Array

                            #calculate the dimensions for the next mipmap
                            Width, Height, Depth = Dimension_Lower_Bound_Check(Width//2,Height//2,Depth//2)
                            
                        self.Packed = True
                        self.Palette_Packed = True
                        self.Indexing_Size = self.Target_Indexing_Size

                """SWIZZLE THE TEXTURE IF POSSIBLE AND THE TARGET SWIZZLE MODE ISNT THE CURRENT SWIZZLE MODE"""
                if not(self.Target_Format in COMPRESSED_FORMATS):
                    if Swizzler is not None:
                        self.Reswizzler.Swizzle_Texture()
                    else:
                        print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

                #now that we have thoroughly messed with the bitmap, we need
                #to change the format and default all the channel mappings
                self.Format = Target_Format
                self._Set_All_Channel_Mappings()
                
                #return that the conversion was successful
                return(True)
            except:
                print("Error occurred while attempting to convert texture.")
                print(format_exc())
        else:
            print("ERROR: NO TEXTURE LOADED. CANNOT PREFORM BITMAP CONVERSION WITHOUT A LOADED TEXTURE")




    def Depalettize_Bitmap(self, Unpacked_Palette, Unpacked_Indexing):
        """Converts a palettized bitmap into an 8BPP unpalettized version and
        returns it. Palette and indexing provided must be in an unpacked format"""
        UCC = self.Unpacked_Channel_Count
        
        Depalettized_Bitmap = array(self._UNPACK_ARRAY_CODE, [0]*(UCC*len(Unpacked_Indexing)))

        i = 0

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if UCC == 4:
            for Index in Unpacked_Indexing:
                Depalettized_Bitmap[i] = Unpacked_Palette[Index*4]
                Depalettized_Bitmap[i+1] = Unpacked_Palette[Index*4+1]
                Depalettized_Bitmap[i+2] = Unpacked_Palette[Index*4+2]
                Depalettized_Bitmap[i+3] = Unpacked_Palette[Index*4+3]
                i += 4
        elif UCC == 2:
            for Index in Unpacked_Indexing:
                Depalettized_Bitmap[i] = Unpacked_Palette[Index*2]
                Depalettized_Bitmap[i+1] = Unpacked_Palette[Index*2+1]
                i += 2
        elif UCC == 1:
            for Index in Unpacked_Indexing:
                Depalettized_Bitmap[i] = Unpacked_Palette[Index]
                i += 1
        
        return(Depalettized_Bitmap)



    def _Downsample_Bitmap(self, Unsampled_Bitmap, Sample_Size,
                           Width, Height, Depth, Delete_Original=False):
        '''this function will halve a bitmap's resolution X number of times. X = self.Downres_Amount'''
        UCC = self.Unpacked_Channel_Count
        
        Gamma = self.Gamma
        No_Gamma_Scale = True

        if max(Gamma) != 1.0 or min(Gamma) != 1.0:
            No_Gamma_Scale = False
            
        #calculate the new dimensions of the bitmap
        New_Width, New_Height, New_Depth = Dimension_Lower_Bound_Check(Width // Powers_of_2[Sample_Size],
                                                                       Height // Powers_of_2[Sample_Size],
                                                                       Depth // Powers_of_2[Sample_Size])
        
        """These next three variables are the log of each dimension"""
        Log_W, Log_H, Log_D = (Logs_of_2[Width],
                               Logs_of_2[Height],
                               Logs_of_2[Depth])

        """These next three variables are the log of each new dimension"""
        Log_New_W, Log_New_H, Log_New_D = (Logs_of_2[New_Width],
                                           Logs_of_2[New_Height],
                                           Logs_of_2[New_Depth])

        """These next three variables are how many pixels to merge on each axis"""
        Merge_X, Merge_Y, Merge_Z = (Powers_of_2[Log_W-Log_New_W],
                                     Powers_of_2[Log_H-Log_New_H],
                                     Powers_of_2[Log_D-Log_New_D])

        #make the new array to place the downsampled pixels into
        Downsampled_Bitmap = array(self._UNPACK_ARRAY_CODE, [0]*(New_Width*New_Height*New_Depth*UCC) )
        
        #this is how many pixels from are being merged into one
        PMIO = Merge_X * Merge_Y * Merge_Z

        #this is used in the gamma based merging to scale the 0-255 value to a 0-1 value
        PMD = PMIO * 255.0
        
        """THIS PART IS ABSOLUTELY CRUCIAL. In order to easily merge all
        the pixels together we will swizzle them around so that all the
        pixels that will be merged into one are directly next to each
        other, but separated by color channel. so it will look like this:
        
        px1A|px2A|px3A|px4A
        px1R|px2R|px3R|px4R
        px1G|px2G|px3G|px4G
        px1B|px2B|px3B|px4B
        """
        Pixel_Merge_Swizzler = Swizzler.Swizzler(Texture_Convertor = self,
                                                 Mask_Type = "DOWNSAMPLER",
                                                 New_Width=New_Width,
                                                 New_Height=New_Height,
                                                 New_Depth=New_Depth)

        #we provide Delete_Original as the last argument since we don't necessarily want to delete the original image        
        Swizzled_Bitmap = Pixel_Merge_Swizzler.Swizzle_Single_Array(Unsampled_Bitmap, True,
                                                                    UCC, Width, Height, Depth,
                                                                    Delete_Original)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if No_Gamma_Scale:
            """merge pixels linearly"""
            if UCC == 4:
                for i in range(0, New_Width*New_Height*New_Depth*4, 4):
                    Downsampled_Bitmap[i] = (sum( Swizzled_Bitmap[i*PMIO:PMIO*(i+1)] )//PMIO)
                    Downsampled_Bitmap[i+1] = (sum( Swizzled_Bitmap[PMIO*(i+1):PMIO*(i+2)] )//PMIO)
                    Downsampled_Bitmap[i+2] = (sum( Swizzled_Bitmap[PMIO*(i+2):PMIO*(i+3)] )//PMIO)
                    Downsampled_Bitmap[i+3] = (sum( Swizzled_Bitmap[PMIO*(i+3):PMIO*(i+4)] )//PMIO)
            elif UCC == 2:
                for i in range(0, New_Width*New_Height*New_Depth*2, 2):
                    Downsampled_Bitmap[i] = (sum( Swizzled_Bitmap[i*PMIO:PMIO*(i+1)] )//PMIO)
                    Downsampled_Bitmap[i+1] = (sum( Swizzled_Bitmap[PMIO*(i+1):PMIO*(i+2)] )//PMIO)
            else:
                for i in range(New_Width*New_Height*New_Depth):
                    Downsampled_Bitmap[i] = (sum( Swizzled_Bitmap[i*PMIO:PMIO*(i+1)] )//PMIO)
        else:
            """merge pixels with gamma correction"""
            #DO NOT USE GAMMA BASED MERGING IF THE BITMAP USES LINEAR GRADIENTS, LIKE METERS

            Gamma_0 = Gamma[0]
            Gamma_Exp_0 = 1.0/Gamma_0
            Gamma_Scaler_0 = self.Gamma_Scaler[0]
            
            if UCC > 0:
                Gamma_Exp_1 = 1.0/Gamma[1]
                Gamma_Scaler_1 = self.Gamma_Scaler[1]
                
            if UCC > 1:
                Gamma_Exp_2 = 1.0/Gamma[2]
                Gamma_Scaler_2 = self.Gamma_Scaler[2]
                
            if UCC > 2:
                Gamma_Exp_3 = 1.0/Gamma[3]
                Gamma_Scaler_3 = self.Gamma_Scaler[3]

            if UCC == 4:
                for i in range(0, New_Width*New_Height*New_Depth*4, 4):
                    Downsampled_Bitmap[i] = int(((sum(map(lambda Value: Gamma_Scaler_0[Value], Swizzled_Bitmap[i*PMIO:PMIO*(i+1)]))/PMD)**Gamma_Exp_0 )*255)
                    Downsampled_Bitmap[i+1] = int(((sum(map(lambda Value: Gamma_Scaler_1[Value], Swizzled_Bitmap[PMIO*(i+1):PMIO*(i+2)]))/PMD)**Gamma_Exp_1 )*255)
                    Downsampled_Bitmap[i+2] = int(((sum(map(lambda Value: Gamma_Scaler_2[Value], Swizzled_Bitmap[PMIO*(i+2):PMIO*(i+3)]))/PMD)**Gamma_Exp_2 )*255)
                    Downsampled_Bitmap[i+3] = int(((sum(map(lambda Value: Gamma_Scaler_3[Value], Swizzled_Bitmap[PMIO*(i+3):PMIO*(i+4)]))/PMD)**Gamma_Exp_3 )*255)
            elif UCC == 2:
                for i in range(0, New_Width*New_Height*New_Depth*2, 2):
                    Downsampled_Bitmap[i] = int(((sum(map(lambda Value: Gamma_Scaler_0[Value], Swizzled_Bitmap[i*PMIO:PMIO*(i+1)]))/PMD)**Gamma_Exp_0 )*255)
                    Downsampled_Bitmap[i+1] = int(((sum(map(lambda Value: Gamma_Scaler_1[Value], Swizzled_Bitmap[PMIO*(i+1):PMIO*(i+2)]))/PMD)**Gamma_Exp_1 )*255)
            else:
                for i in range(New_Width*New_Height*New_Depth):
                    Downsampled_Bitmap[i] = int(((sum(map(lambda Value: Gamma_Scaler_0[Value], Swizzled_Bitmap[i*PMIO:PMIO*(i+1)]))/PMD)**Gamma_Exp_0 )*255)
                    
        return(Downsampled_Bitmap, New_Width, New_Height, New_Depth)


    def _Unpack_Palettized(self, Packed_Palette, Packed_Indexing):
        '''When supplied with a packed palette and indexing,
        this function will return them in an unpacked form'''
        
        """UNPACK THE PALETTE"""
        if self.Packed:
              Unpacked_Palette = self.Palette_Unpacker(Packed_Palette)
        else: Unpacked_Palette = Packed_Palette
        
        """UNPACK THE INDEXING"""
        if self.Packed:
              Unpacked_Indexing = self.Indexing_Unpacker(Packed_Indexing)
        else: Unpacked_Indexing = Packed_Indexing
        
        if self.Palettize:
            return(Unpacked_Palette, Unpacked_Indexing)
        
        #if the bitmap isn't going to stay palettized, we depalettize it
        return(None, self.Depalettize_Bitmap(Unpacked_Palette, Unpacked_Indexing))


    def _Unpack_Palette(self, Packed_Palette):
        """Just a redirect to the _Unpack_Raw function"""
        if not self.Palette_Packed:
            return(Packed_Palette)
        else:
            return(self.Unpack_Raw(Packed_Palette))


    def _Unpack_Indexing(self, Packed_Indexing):
        if self.Indexing_Size not in (1,2,4,8):
            print("ERROR: PALETTIZED BITMAP INDEXING BIT COUNT MUST BE A POWER OF 2")
            return(None)
        
        if self.Indexing_Size == 8:
            #if the indexing is 8 bits then we can 
            #just copy it directly into a new array
            Unpacked_Indexing = array("B", Packed_Indexing)
        else:
            Pixel_Count = int(( Decimal(len(Packed_Indexing)) /
                                Decimal(self.Indexing_Size)) * Decimal(8) )
            BPP = int(ceil(self.Indexing_Size/8.0))
            Unpacked_Indexing = array(INVERSE_PIXEL_ENCODING_SIZES[BPP], [0]*Pixel_Count)
        
            i = 0
            
            ######################
            '''NEEDS MORE SPEED'''
            ######################
            
            """The indexing will be unpacked in little endian mode"""
            if self.Indexing_Size == 1:
                for Indexing_Chunk in Packed_Indexing:
                    Unpacked_Indexing[i] = Indexing_Chunk&1
                    Unpacked_Indexing[i+1] = (Indexing_Chunk&2)>>1
                    Unpacked_Indexing[i+2] = (Indexing_Chunk&4)>>2
                    Unpacked_Indexing[i+3] = (Indexing_Chunk&8)>>3
                    Unpacked_Indexing[i+4] = (Indexing_Chunk&16)>>4
                    Unpacked_Indexing[i+5] = (Indexing_Chunk&32)>>5
                    Unpacked_Indexing[i+6] = (Indexing_Chunk&64)>>6
                    Unpacked_Indexing[i+7] = (Indexing_Chunk&128)>>7
                    i += 8
            elif self.Indexing_Size == 2:
                for Indexing_Chunk in Packed_Indexing:
                    Unpacked_Indexing[i] = Indexing_Chunk&3
                    Unpacked_Indexing[i+1] = (Indexing_Chunk&12)>>2
                    Unpacked_Indexing[i+2] = (Indexing_Chunk&48)>>4
                    Unpacked_Indexing[i+3] = (Indexing_Chunk&192)>>6
                    i += 4
            elif self.Indexing_Size == 4:
                for Indexing_Chunk in Packed_Indexing:
                    Unpacked_Indexing[i] = Indexing_Chunk&15
                    Unpacked_Indexing[i+1] = (Indexing_Chunk&240)>>4
                    i += 2

        return(Unpacked_Indexing)


    def Unpack(self, Bitmap_Index, Width, Height, Depth):
        """Used for unpacking non-palettized formats"""
        if self.Format in FORMAT_UNPACKERS:
            Unpacked_Pixels = FORMAT_UNPACKERS[self.Format](self, Bitmap_Index,
                                                            Width, Height, Depth)
        elif self.Format in RAW_FORMATS:
            if (self.Unpacked_Channel_Count == 1 and
                self.Source_Channel_Count == 1 and sum(self.Unpacked_Depths) == 8):
                #if there is only 1 channel in the source file and we
                #are unpacking to only 1 channel then we don't need to
                #unpack the channels and we can use the array as it is
                Unpacked_Pixels = array("B", self.Texture_Block[Bitmap_Index])
            else:
                Unpacked_Pixels = self.Unpack_Raw(self.Texture_Block[Bitmap_Index])
        else:
            print("ERROR: CANNOT FIND FORMAT UNPACK METHOD.")
            return(None)
        
        return(Unpacked_Pixels)
        

    def Unpack_Raw(self, Packed_Array):
        '''this function takes the loaded raw pixel data texture and unpacks it'''
        Offsets = self.Channel_Offsets
        Masks = self.Channel_Masks
        UpScale = self.Channel_Upscalers
        Fill_Value = 0

        if BITS_PER_PIXEL[self.Format] in (8, 16, 24, 32, 48, 64):
            #this is a little hack to set the alpha channel value to white if we are erasing it
            if Masks[0] == 0:
                Fill_Value = Powers_of_2[self.Channel_Depths[0]] - 1

            if self.Unpacked_Channel_Count == 4:
                Unpacked_Array = self._Unpack_Raw_4_Channel(Packed_Array, Offsets,
                                                            Masks, UpScale, Fill_Value)
            elif self.Unpacked_Channel_Count == 2:
                Unpacked_Array = self._Unpack_Raw_2_Channel(Packed_Array, Offsets,
                                                            Masks, UpScale, Fill_Value)
            elif self.Unpacked_Channel_Count == 1:
                Unpacked_Array = self._Unpack_Raw_1_Channel(Packed_Array, Offsets,
                                                            Masks, UpScale, Fill_Value)
        else:
            #if each pixel doesn't take up a bytesized amount of
            #space, then there will need to be a function to handle
            #them carefully. there isn't one written yet, so crash
            print("ERROR: CANNOT WORK WITH PIXELS THAT AREN'T EITHER 8, 16, 24, OR 32 BYTES.")
            crash

        return(Unpacked_Array)
    
    

    def _Unpack_Raw_4_Channel(self, Packed_Array, Offsets, Masks, UpScale, Fill_Value=0):
        A_Shift, R_Shift, G_Shift, B_Shift = Offsets[0], Offsets[1], Offsets[2], Offsets[3]
        A_Mask,  R_Mask,  G_Mask,  B_Mask =  Masks[0],   Masks[1],   Masks[2],   Masks[3]
        A_Scale, R_Scale, G_Scale, B_Scale = UpScale[0], UpScale[1], UpScale[2], UpScale[3]
        
        Current_Index = 0
        #create a new array to hold the pixels after we unpack them
        Unpacked_Array = array(self._UNPACK_ARRAY_CODE, [Fill_Value]*len(Packed_Array)*self.Unpacked_Channel_Count )
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for Pixel in Packed_Array:
            Unpacked_Array[Current_Index] = A_Scale[(Pixel&A_Mask)>>A_Shift]
            Unpacked_Array[Current_Index+1] = R_Scale[(Pixel&R_Mask)>>R_Shift]
            Unpacked_Array[Current_Index+2] = G_Scale[(Pixel&G_Mask)>>G_Shift]
            Unpacked_Array[Current_Index+3] = B_Scale[(Pixel&B_Mask)>>B_Shift]
            Current_Index += 4

        return(Unpacked_Array)



    def _Unpack_Raw_2_Channel(self, Packed_Array, Offsets, Masks, UpScale, Fill_Value=0):
        A_Shift, I_Shift = Offsets[0], Offsets[1]
        A_Mask, I_Mask = Masks[0], Masks[1]
        A_Scale, I_Scale = UpScale[0], UpScale[1]
        
        Current_Index = 0
            
        #create a new array to hold the pixels after we unpack them
        Unpacked_Array = array(self._UNPACK_ARRAY_CODE, [Fill_Value]*len(Packed_Array)*self.Unpacked_Channel_Count )
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for Pixel in Packed_Array:
            Unpacked_Array[Current_Index] = A_Scale[(Pixel&A_Mask)>>A_Shift]
            Unpacked_Array[Current_Index+1] = I_Scale[(Pixel&I_Mask)>>I_Shift]
            Current_Index += 2
                
        return(Unpacked_Array)



    def _Unpack_Raw_1_Channel(self, Packed_Array, Offsets, Masks, UpScale, Fill_Value=0):
        Shift, Mask, Scale = Offsets[0], Masks[0], UpScale[0]        
        Current_Index = 0
            
        #create a new array to hold the pixels after we unpack them
        Unpacked_Array = array(self._UNPACK_ARRAY_CODE, [Fill_Value]*len(Packed_Array)*self.Unpacked_Channel_Count)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for Pixel in Packed_Array:
            Unpacked_Array[Current_Index] = Scale[(Pixel&Mask)>>Shift]
            Current_Index += 1
                
        return(Unpacked_Array)


    def _Pack_Palettized(self, Unpacked_Palette, Unpacked_Indexing):
        """Used for turning a palette and indexing into arrays
        suitable for being written to a file in little endian format"""
        
        """PACK THE PALETTE"""
        Packed_Palette = self.Palette_Packer(Unpacked_Palette)

        """PACK THE INDEXING"""
        Packed_Indexing = self.Indexing_Packer(Unpacked_Indexing)
            
        return(Packed_Palette, Packed_Indexing)


    def _Pack_Palette(self, Unpacked_Palette):
        if BITS_PER_PIXEL[self.Target_Format] == 24:
            #because we can't store 3 byte integers in an array, the
            #best we can do is remove the padded alpha channel
            Packed_Palette = Bitmap_IO.Unpad_24Bit_Array(Unpacked_Palette)
        else:
            Packed_Palette = self.Pack_Raw(Unpacked_Palette)

        return(Packed_Palette)


    def _Pack_Indexing(self, Unpacked_Indexing):
        if self.Indexing_Size not in (1,2,4,8):
            print("ERROR: PALETTIZED BITMAP INDEXING BIT COUNT MUST BE A POWER OF 2")
            return(None)
        
        Largest_Indexing_Value = max(Unpacked_Indexing)
        
        if Largest_Indexing_Value >= 2**self.Target_Indexing_Size:
            print("ERROR: PALETTE INDEXING CONTAINS TOO LARGE AN ENTRY TO FIT.")
            print("FOUND INDEXING VALUE: ", Largest_Indexing_Value)
            print("LARGEST ALLOWED INDEXING VALUE IS: ", 2**self.Target_Indexing_Size-1)
            return(None)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if self.Target_Indexing_Size == 8:
            #if the indexing is 8 bits then we can
            #just copy it directly into a new array
            Packed_Indexing = array("B", Unpacked_Indexing)
        else:
            UPI = Unpacked_Indexing
            Packed_Count = int( (Decimal(len(UPI)) / Decimal(8))
                                * Decimal(self.Target_Indexing_Size)  )
            Packed_Indexing = array("B", [0]*Packed_Count)
            
            """The indexing will be packed in little endian mode"""
            if self.Target_Indexing_Size == 1:
                for i in range(0, len(Packed_Indexing)*8, 8):
                    Packed_Indexing[i//8] = ( UPI[i]+        (UPI[i+1]<<1) +
                                             (UPI[i+2]<<2) + (UPI[i+3]<<3) +
                                             (UPI[i+4]<<4) + (UPI[i+5]<<5) +
                                             (UPI[i+6]<<6) + (UPI[i+7]<<7) )                    
            elif self.Target_Indexing_Size == 2:
                for i in range(0, len(Packed_Indexing)*4, 4):
                    Packed_Indexing[i//4] = ( UPI[i]       + (UPI[i+1]<<2) +
                                             (UPI[i+2]<<4) + (UPI[i+3]<<6)) 
            elif self.Target_Indexing_Size == 4:
                for i in range(0, len(Packed_Indexing)*2, 2):
                    Packed_Indexing[i//2] = UPI[i]+ (UPI[i+1]<<4)

        return(Packed_Indexing)


    def Pack(self, Unpacked_Pixel_Array, Width, Height, Depth):        
        """Used for packing non-palettized formats"""
        if self.Target_Format in FORMAT_PACKERS:
            Repacked_Pixel_Array = FORMAT_PACKERS[self.Target_Format](self, Unpacked_Pixel_Array,
                                                                      Width, Height, Depth)
        elif self.Target_Format in RAW_FORMATS:
            Repacked_Pixel_Array = self.Pack_Raw(Unpacked_Pixel_Array)
        else:
            print("ERROR: CANNOT FIND TARGET FORMAT PACK METHOD.")
            return(None)
        
        return(Repacked_Pixel_Array)
    


    def Pack_Raw(self, Unpacked_Array):
        '''this function packs the 8-bit pixel array that's been created by the unpacking process'''
        Downscale = self.Channel_Downscalers
        UCC = self.Unpacked_Channel_Count
        
        if BITS_PER_PIXEL[self.Target_Format] in (8, 16, 24, 32, 48, 64):
            """If the nubmer of unpacked channels is just 1 it
            means we can just use the original array as it is."""
            if UCC == 1 and self.Target_Channel_Count == 1:
                """We also need to check that the pixel is 8 bits, otherwise
                we'll need to put multiple pixels into one array index"""
                if BITS_PER_PIXEL[self.Target_Format] == 8:
                    Packed_Array = Unpacked_Array
                else:
                    Packed_Array = self._Pack_Raw_1_Channel(Unpacked_Array, Downscale, UCC)
            else:
                OFF = FORMAT_CHANNEL_OFFSETS[self.Target_Format]
                
                """if we need to merge channels to get the target channel count"""
                #we split here to save time on conversions that don't require merging
                if self.Channel_Merge_Mapping is not None:
                    CMM = self.Channel_Merge_Mapping
                    CMD = self.Channel_Merge_Divisors
                    
                    if UCC == 4:
                        Packed_Array = self._Pack_Raw_4_Channel_Merge(Unpacked_Array, Downscale,
                                                                      UCC, CMM, OFF, CMD)
                    elif UCC == 2:
                        Packed_Array = self._Pack_Raw_2_Channel_Merge(Unpacked_Array, Downscale,
                                                                      UCC, CMM, OFF, CMD)
                else:
                    if UCC == 4:
                        Packed_Array = self._Pack_Raw_4_Channel(Unpacked_Array, Downscale, UCC, OFF)
                    elif UCC == 2:
                        Packed_Array = self._Pack_Raw_2_Channel(Unpacked_Array, Downscale, UCC, OFF)
                        
        else:
            #if each pixel doesn't take up a bytesized amount of
            #space, then there will need to be a function to handle
            #them carefully. there isn't one written yet, so crash
            print("ERROR: CANNOT WORK WITH PIXELS THAT AREN'T EITHER 8, 16, 24, OR 32 BYTES.")
            crash

        return(Packed_Array)


    def _Pack_Raw_4_Channel(self, UPA, Downscale, UCC, OFF):        
        #create the array to hold the pixel data after it's been repacked in the target format
        Packed_Array = array(FORMAT_DATA_SIZES[self.Target_Format], [0]*(len(UPA)//UCC))
        
        A_Shift, R_Shift, G_Shift, B_Shift = OFF[0], OFF[1], OFF[2], OFF[3]
        A_Scale, R_Scale, G_Scale, B_Scale = Downscale[0], Downscale[1], Downscale[2], Downscale[3]

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(Packed_Array)*4, 4):
            Packed_Array[i//4] = ( (A_Scale[UPA[i]]<<A_Shift) +
                                   (R_Scale[UPA[i+1]]<<R_Shift) +
                                   (G_Scale[UPA[i+2]]<<G_Shift) +
                                   (B_Scale[UPA[i+3]]<<B_Shift) )

        return(Packed_Array)


    def _Pack_Raw_2_Channel(self, UPA, Downscale, UCC, OFF):
        #create the array to hold the pixel data after it's been repacked in the target format
        Packed_Array = array(FORMAT_DATA_SIZES[self.Target_Format], [0]*(len(UPA)//UCC))
            
        A_Shift, I_Shift = OFF[0], OFF[1]
        C1_Scale, C2_Scale = Downscale[0], Downscale[1]
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(Packed_Array)*2, 2):
            Packed_Array[i//2] = ( (C1_Scale[UPA[i]]<<A_Shift) +
                                   (C2_Scale[UPA[i+1]]<<I_Shift) )
        return(Packed_Array)


    def _Pack_Raw_1_Channel(self, UPA, Downscale, UCC, OFF=None):
        #create the array to hold the pixel data after it's been repacked in the target format
        Packed_Array = array(FORMAT_DATA_SIZES[self.Target_Format], [0]*(len(UPA)//UCC))
        
        Scale = Downscale[0]
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(len(Packed_Array)):
            Packed_Array[i] = Scale[UPA[i]]

        return(Packed_Array)


    def _Pack_Raw_4_Channel_Merge(self, UPA, Downscale, UCC, CMM, OFF, CMD):
        #create the array to hold the pixel data after it's been repacked in the target format
        Packed_Array = array(FORMAT_DATA_SIZES[self.Target_Format], [0]*(len(UPA)//UCC))
        
        A_T, R_T, G_T, B_T = CMM[0], CMM[1], CMM[2], CMM[3]
        A_Shift, R_Shift, G_Shift, B_Shift = OFF[A_T], OFF[R_T], OFF[G_T], OFF[B_T]
        A_Div, R_Div, G_Div, B_Div = CMD[A_T], CMD[R_T], CMD[G_T], CMD[B_T]
        A_Rnd, R_Rnd, G_Rnd, B_Rnd = A_Div//2, R_Div//2, G_Div//2, B_Div//2        
        A_Scale, R_Scale, G_Scale, B_Scale = Downscale[0], Downscale[1], Downscale[2], Downscale[3]
        
        #if the divisor is 256 it means we're removing the channel
        A_Rnd *= int(A_Div == CHANNEL_ERASE_DIVISOR)
        R_Rnd *= int(R_Div == CHANNEL_ERASE_DIVISOR)
        G_Rnd *= int(G_Div == CHANNEL_ERASE_DIVISOR)
        B_Rnd *= int(B_Div == CHANNEL_ERASE_DIVISOR)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(Packed_Array)*4, 4):
            Packed_Array[i//4] = ( (A_Scale[((UPA[i]+A_Rnd)//A_Div)]<<A_Shift) +
                                   (R_Scale[((UPA[i+1]+R_Rnd)//R_Div)]<<R_Shift) +
                                   (G_Scale[((UPA[i+2]+G_Rnd)//G_Div)]<<G_Shift) +
                                   (B_Scale[((UPA[i+3]+B_Rnd)//B_Div)]<<B_Shift) )
        return(Packed_Array)


    def _Pack_Raw_2_Channel_Merge(self, UPA, Downscale, UCC, CMM, OFF, CMD):
        #create the array to hold the pixel data after it's been repacked in the target format
        Packed_Array = array(FORMAT_DATA_SIZES[self.Target_Format], [0]*(len(UPA)//UCC))
        
        C1_Target, C2_Target = CMM[0], CMM[1]
        C1_Shift, C2_Shift = OFF[C1_Target], OFF[C2_Target]
        C1_Div, C2_Div = CMD[C1_Target], CMD[C2_Target]
        C1_Rnd, C2_Rnd = C1_Div//2, C2_Div//2
        C1_Scale, C2_Scale = Downscale[0], Downscale[1]

        #if the divisor is 256 it means we're removing the channel
        C1_Rnd *= int(C1_Div == CHANNEL_ERASE_DIVISOR)
        C2_Rnd *= int(C2_Div == CHANNEL_ERASE_DIVISOR)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(Packed_Array)*2, 2):
            Packed_Array[i//2] = ( (C1_Scale[((UPA[i]+C1_Rnd)//C1_Div)]<<C1_Shift) +
                                   (C2_Scale[((UPA[i+1]+C2_Rnd)//C2_Div)]<<C2_Shift) )

        return(Packed_Array)


    def _Palette_Picker(self, Unpacked_Pixels):
        """Converts a bitmap into and returns an unpacked palette and indexing"""
        crash
        return(Unpacked_Palette, Unpacked_Indexing)
