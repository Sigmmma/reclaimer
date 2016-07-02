"""DONT FORGET TO INCLUDE AN MIT PUBLIC LICENSE
   ON EVERY MODULE ONCE THE PROGRAM IS DONE

   There is a lot of code that SHOULD be executed in C++ because
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

from .ext.format_defs import *

try:
    from .ext import swizzler
except:
    print("ERROR: COULDNT IMPORT swizzler MODULE")
    print(format_exc())
    swizzler = None

try:
    from .ext import bitmap_io
    bitmap_io.bc = this_module
except:
    print("ERROR: COULDNT IMPORT bitmap_io MODULE")
    print(format_exc())
    bitmap_io = None

try:
    from .ext import dds_defs
    dds_defs.bc = this_module
    dds_defs.initialize()
except:
    print("ERROR: COULDNT IMPORT dds_defs MODULE")
    print(format_exc())
    dds_defs = None


#speed things up by caching these so we don't have to
#calculate them on the fly or constantly remake them
range_16 = range(16)
logs_of_2 = {}
        
#used for swizzling and deswizzling
for log2 in range(len(powers_of_2)):
    logs_of_2[powers_of_2[log2]] = log2


'''when constructing this class you must provide the block containing the textures and
a dictionary which contains the texture's height, width, type, and format.

    Optional parameters include the depth, mipmap count, sub-texture count(cubemaps are
composed of 6 2D subtextures for example), the format to convert the pixels to, whether to/what
order to swap channels around, which channels should be merged/removed/cloned when converting
to a format with a different number of channels, 0-255 cutoff when compressing a channel to 1-bit,
the numebr of times to cut the resolution in half, and the power to use for merging pixels
while taking gamma into account.'''
class BitmapManipulator():
    
    def __init__(self, **kwargs):
        self.default_palette_picker = self._palette_picker
        self.set_deep_color_mode()

        self.texture_block = self.texture_info = None

        '''set this to true to force routines to make
           exported data compatible with Photoshop.'''
        self.photoshop_compatability = True
        
        #initialize the bitmap description variables
        self.sub_bitmap_count = self.mipmap_count = 0
        self.swizzled = self.packed = self.palette_packed = False
        self.filepath = None
        self.indexing_size = 0
        self.width = self.height = self.depth = 0
        self.format = self.texture_type = ""
        self.channel_order = C_ORDER_DEFAULT

        #palette stuff
        self.palette = None
        self.palettized_unpacker = None
        self.palettized_packer = None
        self.palette_unpacker = None
        self.palette_packer = None
        self.indexing_unpacker = None
        self.indexing_packer = None
        
        #initialize the conversion variables
        self.target_format = ""
        self.one_bit_bias = 127
        self.downres_amount = 0
        self.generate_mipmaps = self.swizzler_mode = False
        self.gamma = [1.0]*4#this is only meant to ever handle up to 4 channels
        self.color_key_transparency = False
        self.reswizzler = self.deswizzler = None
        self.palette_picker = self.default_palette_picker
        self.palettize = False
        self.channel_mapping = self.channel_merge_mapping = None
        self.repack = True
        self.target_indexing_size = DEFAULT_INDEXING_SIZE
        

        #initialize the variables created in the below functions
        self.source_depths = None
        self.unpacked_depths = None
        self.target_depths = None

        self.source_channel_count = 0
        self.unpacked_channel_count = 0
        self.target_channel_count = 0
        
        self.swapping_channels = False
        self.channel_masks = None
        self.channel_offsets = None
        self.channel_depths = None
        self.channel_merge_divisors = None
        self.channel_upscalers = None
        self.channel_downscalers = None
        

        #if a texture block is provided in the kwargs
        #then we load the texture as we build the class
        if "texture_block" in kwargs:
            #create/set this class's variables to those in the texture block
            self.load_new_texture(**kwargs)
            

    def set_deep_color_mode(self, deep_state=None):
        """Allows changing the unpacking mode of this module from "true color"(32BPP)
           to "deep color"(64BPP). If the argument is None, the mode will be the
           default one set in Format_Defs, if False the unpack format will be
           Format_A8R8G8B8, and if True the format will be FORMAT_A16R16G16B16."""
        if deep_state is None:
            self._UNPACK_FORMAT = DEFAULT_UNPACK_FORMAT
            self._UNPACK_ARRAY_CODE = INVERSE_PIXEL_ENCODING_SIZES[max(FORMAT_CHANNEL_DEPTHS[self._UNPACK_FORMAT])//8]
        else:
            if deep_state:
                self._UNPACK_FORMAT = FORMAT_A16R16G16B16
                self._UNPACK_ARRAY_CODE = "H"
            else:
                self._UNPACK_FORMAT = FORMAT_A8R8G8B8
                self._UNPACK_ARRAY_CODE = "B"


    #call this when providing the convertor with a new list of pixel arrays
    def load_new_texture(self, **kwargs):
        
        try:
            texture_block = self.texture_block = kwargs.get("texture_block")
            texture_info = self.texture_info = kwargs.get("texture_info")
            
            if texture_block is None:
                print("ERROR: NO BITMAP BLOCK SUPPLIED.\n",
                      "CANNOT LOAD BITMAP WITHOUT A SUPPLIED BITMAP BLOCK")
                return
            
            if texture_info is None:
                print("ERROR: BITMAP BLOCK SUPPLIED HAS NO TEXTURE INFO.\n",
                      "CANNOT LOAD BITMAP WITHOUT A DESCRIPTION OF THE BITMAP")
                return
            
            if "format" not in texture_info:
                print("ERROR: THE SUPPLIED BITMAP'S INFO BLOCK HAS NO FORMAT ENTRY!\n",
                      "CAN NOT LOAD BITMAP WITHOUT KNOWING THE BITMAP'S FORMAT.")
                self.texture_block = None
                return
            
            if texture_info["format"] not in VALID_FORMATS:
                print("ERROR: THE SUPPLIED BITMAP IS IN AN UNKNOWN FORMAT!\n",
                      "IF YOU WISH TO USE THIS FORMAT YOU MUST INCOROPRATE IT YOURSELF.")
                self.texture_block = None
                return

            #if provided with just a pixel data array we will need to put it inside a list
            if isinstance(texture_block, array):
                texture_block = [texture_block]
            
            #initialize the optional bitmap description variables
            self.palette = None
            self.indexing_size = DEFAULT_INDEXING_SIZE
            
            
            #get the bitmap's info from the texture block's info dictionary
            self.width = texture_info.get("width", 1)
            self.height = texture_info.get("height", 1)
            self.depth = texture_info.get("depth", 1)
            self.format = texture_info["format"]
            
            self.swizzled = texture_info.get("swizzled", False)
            self.mipmap_count = texture_info.get("mipmap_count", 0)
            self.sub_bitmap_count = texture_info.get("sub_bitmap_count", 1)
            self.filepath = texture_info.get("filepath", None)
            
            self.packed = texture_info.get("packed", True)
            self.palette_packed = texture_info.get("palette_packed", True)

            if "deswizzler" in texture_info:
                if swizzler is not None:
                    self.deswizzler = swizzler.Swizzler(texture_converter = self,
                                                        mask_type = texture_info["deswizzler"])
                else:
                    print("ERROR: SWIZZLER MODULE NOT LOADED. "+
                          "CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")
            elif swizzler is not None:
                self.deswizzler = swizzler.Swizzler(texture_converter=self,
                                                    mask_type="DEFAULT")

            self.texture_type = texture_info.get("texture_type", TYPE_2D)
            self.channel_order = texture_info.get("channel_order",
                                                  C_ORDER_DEFAULT)
                
                
            if "palette" in texture_info and texture_info["palette"] is not None:
                if "indexing_size" in texture_info and texture_info["indexing_size"] not in (0, None):
                    self.palette = texture_info["palette"]
                    self.indexing_size = texture_info["indexing_size"]
                    self.palettize = True
                    
                    if "palette_packed" in texture_info:
                        self.palette_packed = texture_info["palette_packed"]
                else:
                    print("ERROR: PALETTE WAS SUPPLIED, BUT BIT-SIZE OF INDEXING WAS NOT.")
                    return

            self.palettized_packer = texture_info.get("palettized_packer",
                                                      self._pack_palettized)
            self.palettized_unpacker = texture_info.get("palettized_unpacker",
                                                        self._unpack_palettized)
            self.palette_packer = texture_info.get("palette_packer",
                                                     self._pack_palette)
            self.palette_unpacker = texture_info.get("palette_unpacker",
                                                     self._unpack_palette)
            self.indexing_packer = texture_info.get("indexing_packer",
                                                      self._pack_indexing)
            self.indexing_unpacker = texture_info.get("indexing_unpacker",
                                                      self._unpack_indexing)

            #we may have been provided with conversion settings at the same time we were given the texture
            self.load_new_conversion_settings(**kwargs)
                
            self.texture_block = texture_block
            self.texture_info = texture_info
        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD TEXTURE INTO BITMAP CONVERTOR")
            print(format_exc())


    def load_new_conversion_settings(self, **kwargs):
        #only run if there is a valid texture block loaded
        if (self.texture_info is None and
            ("texture_info" not in kwargs or kwargs["texture_info"] is None)):
            print("ERROR: CANNOT LOAD CONVERSION SETTINGS WITHOUT A LOADED TEXTURE.")
            return

        """RESETTING THE CONVERSION VARIABLES EACH TIME IS INTENTIONAL
        TO PREVENT ACCIDENTALLY LEAVING INCOMPATIBLE ONES SET"""
        try:
            #initialize the bitmap CONVERSION variables
            self.target_format = self.format
            self.one_bit_bias = 127
            self.downres_amount = 0
            self.generate_mipmaps = False
            self.swizzler_mode = self.swizzled
            self.gamma = 1.0
            self.color_key_transparency = False
            self.reswizzler = self.deswizzler
            self.palette_picker = self.default_palette_picker
            self.palettize = self.is_palettized()
            self.target_indexing_size = self.indexing_size
            self.channel_mapping = None
            self.channel_merge_mapping = None
            self.repack = True
            
            if "target_format" in kwargs and kwargs["target_format"] in VALID_FORMATS:
                self.target_format = kwargs["target_format"]
            
            if self.target_format in DDS_FORMATS and swizzler is None:
                print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT COMPRESS TO DXT WITHOUT SWIZZLER. SWITCHING TO A8R8G8B8.")
                self.target_format = self._UNPACK_FORMAT
                
            if "one_bit_bias" in kwargs:
                self.one_bit_bias = kwargs["one_bit_bias"]
                
            if "downres_amount" in kwargs and kwargs["downres_amount"] > 0:
                #we only want whole number times to cut the resolution in half
                self.downres_amount = int(kwargs["downres_amount"])
                
            if "generate_mipmaps" in kwargs and kwargs["generate_mipmaps"]:
                #if we are being told to create more mipmaps this is how many more to make
                self.generate_mipmaps = kwargs["generate_mipmaps"]
                
            if "swizzler_mode" in kwargs:
                #whether to swizzle or deswizzle the bitmap when the swizzler is called
                '''False = Deswizzle the bitmap    True = Swizzle the bitmap'''
                self.swizzler_mode = kwargs["swizzler_mode"]
                
            if "gamma" in kwargs:
                self.gamma = kwargs["gamma"]
                
            if "repack" in kwargs:
                self.repack = kwargs["repack"]
                
            if "color_key_transparency" in kwargs:
                self.color_key_transparency = kwargs["color_key_transparency"]

            if "reswizzler" in kwargs:
                if swizzler is not None:
                    self.reswizzler = swizzler.Swizzler(texture_converter = self,
                                                        mask_type=kwargs["reswizzler"])
                else:
                    print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")
                
            if "palette_picker" in kwargs:
                self.palette_picker = kwargs["palette_picker"]
                
            if "palettize" in kwargs:
                self.palettize = kwargs["palettize"]

            if "target_indexing_size" in kwargs:
                self.target_indexing_size = kwargs["target_indexing_size"]
            
            #set up all the channel mappings and such
            self._set_all_channel_mappings(**kwargs)

        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD CONVERSION SETTINGS INTO BITMAP CONVERTOR.\n"
                  "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
            print(format_exc())
            self.texture_block = None


    def print_info(self, print_texture_info=True, print_conversion_settings=False,
                   print_channel_mappings=False, print_methods=False, print_scalers=False):
        if print_texture_info:
            print("texture info:")
            print("   filepath:", self.filepath)
            print("   type:", self.texture_type)
            print("   format:", self.format)
            print("   width:", self.width)
            print("   height:", self.height)
            print("   depth:", self.depth)
            print()
            print("   sub_bitmap_count:", self.sub_bitmap_count)
            print("   mipmap_count:", self.mipmap_count)
            print("   swizzled:", self.swizzled)
            print()
            print("   currently_packed:", self.packed)
            print("   is_palettized:", self.is_palettized())
            if self.is_palettized():
                print()
                print("   palette_currently_packed:", self.palette_packed)
                print("   indexing_size:", self.indexing_size)
            print()
            
        if print_conversion_settings:
            print("conversion settings:")
            print("   photoshop_compatability:", self.photoshop_compatability)
            print("   target_format:", self.target_format)
            print("   target_indexing_size:", self.target_indexing_size)
            print()
            print("   one_bit_bias:", self.one_bit_bias)
            print("   gamma:", self.gamma)
            print("   swizzler_mode:", self.swizzler_mode)
            print("   downres_amount:", self.downres_amount)
            print("   generate_mipmaps:", self.generate_mipmaps)
            print()
            print("   color_key_transparency:", self.color_key_transparency)
            print("   make\\keep_palettized:", self.palettize)
            print("   repack:", self.repack)
            print("   channel_mapping:", self.channel_mapping)
            print("   channel_merge_mapping:", self.channel_merge_mapping)
            print()
            print("   unpack_format:", self._UNPACK_FORMAT)
            print("   unpack_array_code:", self._UNPACK_ARRAY_CODE)
            print("   channel_order:", self.channel_order)
            print()
            
        if print_channel_mappings:
            print("channel Mapping Variables:")
            print("   source_depths:", self.source_depths)
            print("   unpacked_depths:", self.unpacked_depths)
            print("   target_depths:", self.target_depths)
            print()
            print("   source_channel_count:", self.source_channel_count)
            print("   unpacked_channel_count:", self.unpacked_channel_count)
            print("   target_channel_count:", self.target_channel_count)
            print()
            print("   swapping_channels:", self.swapping_channels)
            print()
            print("   channel_mapping:", self.channel_mapping)
            print("   channel_merge_mapping:", self.channel_merge_mapping)
            print()
            print("   channel_offsets:", self.channel_offsets)
            print("   channel_depths:", self.channel_depths)
            print("   channel_merge_divisors:", self.channel_merge_divisors)
            print()

        if print_methods:
            print("Bound Methods:")
            print("   palettized_unpacker:", self.palettized_unpacker)
            print("   palettized_packer:", self.palettized_packer)
            print()
            print("   palette_unpacker:", self.palette_unpacker)
            print("   palette_packer:", self.palette_packer)
            print()
            print("   indexing_unpacker:", self.indexing_unpacker)
            print("   indexing_packer:", self.indexing_packer)
            print()
            print("   reswizzler:", self.reswizzler)
            print("   deswizzler:", self.deswizzler)
            print("   palette_picker:", self.palette_picker)
            print("   default_palette_picker:", self.default_palette_picker)

        if print_scalers:
            print("Scaler Arrays:")
            print("   channel_upscalers:", self.channel_upscalers)
            print("   channel_downscalers:", self.channel_downscalers)
            print("   gamma_scaler:", self.gamma_scaler)
            print()


    def _set_all_channel_mappings(self, **kwargs):
        """Sets(or defaults) all the different channel mappings"""
        try:
            self.source_channel_count = FORMAT_CHANNEL_COUNTS[self.format]
            self.unpacked_channel_count = FORMAT_CHANNEL_COUNTS[self.format]
            self.target_channel_count = FORMAT_CHANNEL_COUNTS[self.target_format]

            """CREATE THE CHANNEL LOAD MAPPING"""
            self._set_channel_load_mapping(**kwargs)
            
            #If the format is DXT then the merge mapping will have JUST BEEN padded and set
            if self.channel_merge_mapping is not None:
                kwargs["channel_merge_mapping"] = self.channel_merge_mapping

            """CREATE THE CHANNEL MERGE MAPPING"""
            self._set_channel_merge_mapping(**kwargs)

            """CREATE THE CHANNEL UP AND DOWN SCALER LISTS"""
            self._set_upscalers_and_downscalers(**kwargs)
            
            """CREATE THE CHANNEL GAMMA SCALER LISTS"""
            self._set_gamma_scaler(**kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO CREATE CHANNEL MAPPINGS AND SCALERS")
            print(format_exc())


        
    def is_palettized(self, palette_index=0):
        '''returns whether or not there is a valid palette for the bitmap at the index provided'''
        return( self.palette is not None and
                ( (hasattr(self.palette, '__iter__') and len(self.palette) > palette_index)
                  and self.palette[palette_index] is not None) )

    
    def _set_gamma_scaler(self, **kwargs):
        '''creates the list per channel for the gamma scaling'''
        if isinstance(self.gamma,(int,float)):
            self.gamma = [self.gamma]*self.unpacked_channel_count
        elif len(self.gamma) < self.unpacked_channel_count:
            #if there aren't enough indexes in the gamma scalar we repeat
            #the last element in the scalar list for each missign channel
            old_gamma_len = len(self.gamma)
            for i in range(self.unpacked_channel_count-old_gamma_len):
                self.gamma.append(self.gamma[old_gamma_len-1])
        
        self.gamma_scaler = [0]*self.unpacked_channel_count
        #this array will be used to quickly convert a color
        #channel value from a linear value to a gamma scaled value
        for channel in range(self.unpacked_channel_count):
            self.gamma_scaler[channel] = array("f",[0.0]*self.unpacked_channel_count)
            for val in range(256):
                self.gamma_scaler[channel].append(( (float(val)/255)**self.gamma[channel])*255)


    def _set_upscalers_and_downscalers(self, **kwargs):
        '''NEED TO ADD A DESCRIPTION'''
        
        #specifies what depth we want to unpack each channel from
        self.source_depths = FORMAT_CHANNEL_DEPTHS[self.format][:]
        #specifies what depth we want to unpack each channel to
        self.unpacked_depths = FORMAT_CHANNEL_DEPTHS[self._UNPACK_FORMAT][:self.unpacked_channel_count]
        #specifies what depth we want to repack each channel to
        self.target_depths = FORMAT_CHANNEL_DEPTHS[self.target_format][:]
        
        #each index is a list to upscale the source depth to the unpacked depth
        self.channel_upscalers = []
        self.channel_downscalers = []

        if self.channel_merge_mapping is not None:
            self.target_depths = []
            for i in range(len(self.unpacked_depths)):
                self.target_depths.append(FORMAT_CHANNEL_DEPTHS[self.target_format]
                                          [self.channel_merge_mapping[i]])

        
        """BUILD THE UPSCALER ARRAYS"""
        for i in range(len(self.unpacked_depths)):
            #figure out how large the entries in the arrays need to be
            array_enc = INVERSE_PIXEL_ENCODING_SIZES[int(ceil(self.unpacked_depths[self.channel_mapping[i]]/8.0))]
            #make a new array to map the source values to their upscaled values
            self.channel_upscalers.append(array(array_enc, []))

            #this is the amount the values will be scaled to and from depths
            if self.source_depths[self.channel_mapping[i]] == 0: scale = 0.0000000001
            else: scale = (2**self.unpacked_depths[i]-1) / (2**self.source_depths[self.channel_mapping[i]]-1)
            
            for val in range(2**self.source_depths[self.channel_mapping[i]]):
                self.channel_upscalers[i].append(int(round( val * scale )))


        """BUILD THE DOWNSCALER ARRAYS"""
        for i in range(len(self.target_depths)):
            #figure out how large the entries in the arrays need to be
            array_enc = INVERSE_PIXEL_ENCODING_SIZES[int(ceil(self.unpacked_depths[i]/8.0))]
            #make a new array to map the target values to their downscaled values
            self.channel_downscalers.append(array(array_enc, []))
            
            if self.target_depths[i] == 1:
                #if the source depth is 1 bit we use a bias to determine what is white and black
                for val in range(2**self.unpacked_depths[i]):
                    self.channel_downscalers[i].append(int(val >= self.one_bit_bias))
            else:
                #this is the amount the values will be scaled to and from depths
                if self.unpacked_depths[i] == 0: scale = 0.0000000001
                else: scale = (2**self.target_depths[i]-1) / (2**self.unpacked_depths[i]-1)
                
                for val in range(2**self.unpacked_depths[i]):
                    self.channel_downscalers[i].append(int(round( val * scale )))


    def _set_channel_load_mapping(self, **kwargs):
        """THIS FUNCTION CREATES MAPPINGS THAT ALLOW US TO
        SWAP CHANNELS AROUND PER PIXEL AS THEY ARE UNPACKED"""
        
        if "channel_mapping" in kwargs:
            self.channel_mapping = array("b",kwargs["channel_mapping"])
            self.swapping_channels = True
        else:
            self.channel_mapping = array("b",range(self.source_channel_count))
            self.swapping_channels = False

        
        """ONLY RUN IF WE CAN FIND THE FORMAT WE ARE LOADING IN THE CHANNEL MASKS"""
        #it is possible to have a valid format that doesn't have channel masks.
        #if the format is compressed or palettized it wont work with this method
        if self.format in FORMAT_CHANNEL_MASKS:
            
            #create the default offset, mask, and depth arrays
            self.channel_masks = array("Q", FORMAT_CHANNEL_MASKS[self.format])
            self.channel_offsets = array("B", FORMAT_CHANNEL_OFFSETS[self.format])
            self.channel_depths = array("B", FORMAT_CHANNEL_DEPTHS[self.format])

            if "channel_mapping" in kwargs:
                #set the number of channels to how many are in the channel mapping
                self.unpacked_channel_count = len(kwargs["channel_mapping"])
                self.channel_masks = array("I", [])
                self.channel_offsets = array("B", [])
                self.channel_depths = array("B", [])
                """THE BELOW CODE WILL SWAP AROUND THE OFFSETS, MASKS, AND CHANNEL DEPTHS PER CHANNEL.
                THIS WILL ALLOW US TO SWITCH CHANNELS WITH EACH OTHER BY CHANGING THE ORDER WE UNPACK THEM."""
                for i in range(len(self.channel_mapping)):
                    channel = self.channel_mapping[i]
                    
                    if channel < 0 or channel >= self.source_channel_count:
                        """if the channel index provided is outside the number
                        of channels we have, it means to make a blank channel.
                        this will be used for things like A8 to self._UNPACK_FORMAT"""
                        self.channel_masks.append(0)
                        self.channel_offsets.append(0)
                        
                        #we preserve the alpha channel depth so we can set it to full white
                        if i == 0: self.channel_depths.append(FORMAT_CHANNEL_DEPTHS[self.format][0])
                        else: self.channel_depths.append(0)
                    else:
                        """otherwise build the channel masks/offsets/depths from
                        the approporate template arrays for the channel specified"""
                        self.channel_masks.append(FORMAT_CHANNEL_MASKS[self.format][channel])
                        self.channel_offsets.append(FORMAT_CHANNEL_OFFSETS[self.format][channel])
                        self.channel_depths.append(FORMAT_CHANNEL_DEPTHS[self.format][channel])


            '''if this is a DDS format we need to unpack it to 4 channels no matter what. in
            order for that to work we need to pad the channel mapping and the merge mapping'''
            if self.format in DDS_FORMATS and self.unpacked_channel_count < 4:
                #pad the channel mapping
                for i in range(self.unpacked_channel_count, 4):
                    self.channel_mapping.append(i)
                    
                #check if there is a merge mapping
                if "channel_merge_mapping" in kwargs:
                    #pad the merge mapping
                    self.channel_merge_mapping = array("b", kwargs["channel_merge_mapping"])
                    
                    for i in range(self.unpacked_channel_count, 4):
                        self.channel_merge_mapping.append(-1)
                else:
                    #create a merge mapping if none exists
                    self.channel_merge_mapping = array("b", [0,1,2,3])
                    for i in range(4):
                        if self.channel_mapping[i] == -1 or self.channel_mapping[i] >= self.target_channel_count:
                            self.channel_merge_mapping[i] = -1
                            
                self.unpacked_channel_count = 4


    def _set_channel_merge_mapping(self, **kwargs):
        """THIS FUNCTION ALLOWS US TO SPECIFY HOW CHANNELS
        ARE MERGED WHEN CONVERTING TO A DIFFERENT FORMAT"""
        
        """
        channel_merge_mapping:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE ORIGINAL FORMAT. EACH
        INDEX WILL BE THE CHANNEL OF THE TARGET FORMAT TO ADD THE CHANNEL INTO.

        channel_merge_divisors:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE TARGET FORMAT. EACH
        INDEX WILL STORE AN INTEGER. THIS INTEGER WILL BE THE NUMBER OF CHANNELS
        THAT HAVE BEEN ADDED TOGETHER FROM THE ORIGINAL FORMAT INTO THIS CHANNEL.
        THE PURPOSE OF THIS ARRAY WILL BE TO QUICKLY DIVIDE THE ADDED TOGETHER
        CHANNELS TO GET A RANGE WITHIN THE CHANNEL'S DEPTH
        """
        
        #if the unpacked number of channels is more than the target format then we need to merge some
        if self.unpacked_channel_count > self.target_channel_count:
            if "channel_merge_mapping" in kwargs:

                #only use the mapping provided if it is the same length as the unpacked channel count
                if len(kwargs["channel_merge_mapping"]) == self.unpacked_channel_count:
                    if self.channel_merge_mapping is None:
                        self.channel_merge_mapping = array("b",kwargs["channel_merge_mapping"])
                else:
                    print("ERROR: INVALID NUMBER OF CHANNELS IN CHANNEL MERGE MAPPING.\nEXPECTED",
                          self.unpacked_channel_count, "CHANNELS BUT GOT", len(kwargs["channel_merge_mapping"]), ".\n",
                          "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
                    self.texture_block = None

                self.channel_merge_divisors = array("q",[0]*self.target_channel_count)
                
                #loop through the length of the convert channel mapping
                for i in self.channel_merge_mapping:
                    """WHAT WE ARE DOING HERE IS ADDING 1 TO EACH CHANNEL'S DIVISOR IN THE
                    TARGET FORMAT FOR EVERY CHANNEL FROM THE ORIGINAL FORMAT BEING MERGED IN"""
                    if i >= 0:
                        self.channel_merge_divisors[i] += 1
                
            else:
                print("ERROR: CONVERTING FROM FORMAT WITH", self.source_channel_count,
                      "CHANNELS TO FORMAT WITH", self.target_channel_count, "CHANNELS.\n",
                      "A MAPPING IS NEEDED TO SPECIFY WHAT SHOULD BE MERGED WITH WHAT.\n",
                      "DEREFERENCING TEXTURE BLOCK FROM BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
                self.texture_block = None
        else:
            self.channel_merge_mapping = None

        #because the merge mapping will reference index -1 it will
        #be the last index. because we are appending an additional
        #divisor of 256 it will be erased when packed
        if self.channel_merge_mapping is not None and -1 in self.channel_merge_mapping:
            self.channel_merge_divisors.append(CHANNEL_ERASE_DIVISOR)



    def save_to_file(self, **kwargs):
        try:
            """saves the loaded bitmap to a file"""
            
            kwargs['output_path'] = output_path = kwargs.get('output_path',
                                                             self.filepath)
            
            if kwargs['output_path'] is None:
                print("BITMAP SAVE ERROR: MISSING OUTPUT PATH.")
                return
            
            if self.texture_block is None:
                print("BITMAP SAVE ERROR: NO TEXTURE LOADED.")
                return
                
            if bitmap_io is None:
                print("BITMAP SAVE ERROR: BITMAP IO MODULE NOT LOADED.")
                return
            
            ext = kwargs.get('ext').lower()
            #if the extension isnt provided in the
            #kwargs we try to get it from the filepath
            if ext is None:
                splitpath = output_path.splitext(output_path)
                output_path = splitpath[0]
                kwargs['ext'] = ext = splitpath[1][1:].lower()

            if ext not in bitmap_io.file_writers:
                print("BITMAP SAVE ERROR: UNKNOWN BITMAP FILE "+
                      "EXPORT FORMAT: ", ext.lower())
                return
            bitmap_io.file_writers[ext](self, **kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO SAVE BITMAP TO FILE.")
            print(format_exc())


    def load_from_file(self, **kwargs):
        try:
            """loads the current bitmap from a file"""
            kwargs['input_path'] = input_path = kwargs.get('input_path',
                                                           self.filepath)
            
            if kwargs['input_path'] is None:
                print("BITMAP LOAD ERROR: MISSING INPUT PATH.")
                return
                    
            if bitmap_io is None:
                print("BITMAP LOAD ERROR: BITMAP IO MODULE NOT LOADED.")
                return

            ext = kwargs.get('ext').lower()
            #if the extension isnt provided in the
            #kwargs we try to get it from the filepath
            if ext is None:
                splitpath = input_path.splitext(input_path)
                input_path = splitpath[0]
                kwargs['ext'] = ext = splitpath[1][1:].lower()
            
            if ext not in bitmap_io.file_readers:
                print("BITMAP LOAD ERROR: UNKNOWN BITMAP FILE "+
                      "IMPORT FORMAT: ", ext)
                return
            
            bitmap_io.file_readers[ext](self, *kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO LOAD BITMAP FROM FILE.")
            print(format_exc())
        


    def convert_texture(self):
        """Runs all the conversions routines for the parameters specified"""

        #only run if there is a valid texture block loaded
        if self.texture_block is not None:
            try:
                format = self.format
                target_format = self.target_format
            
                '''if we want to reduce the resolution, but we have mipmaps, we can quickly
                reduce it by removing the larger bitmaps and using the mipmaps instead'''
                while self.mipmap_count > 0 and self.downres_amount > 0:
                    if (self.width  in powers_of_2 and
                        self.height in powers_of_2 and
                        self.depth  in powers_of_2):
                        #remove one mipmap level for each sub-bitmap
                        for sub_bitmap_index in range(self.sub_bitmap_count):
                            self.texture_block.pop(0)

                        #divide the dimensions in half and make sure they don't go below the minimum
                        self.width, self.height, self.depth = dimension_lower_bound_check(self.width//2,
                                                                                          self.height//2,
                                                                                          self.depth//2,
                                                                                          format)
                        self.downres_amount -= 1
                        self.mipmap_count -= 1
                        self.texture_info["width"] = self.width
                        self.texture_info["height"] = self.height
                        self.texture_info["depth"] = self.depth
                        self.texture_info["mipmap_count"] = self.mipmap_count
                    else:
                        print("ERROR: CANNOT DOWNSCALE NON-POWER-OF-2 BITMAPS.")
                        self.downres_amount = 0
                
                '''only run this section if we are doing at least one of these things:'''
                #Converting to a different format
                #Downsampling the bitmap
                #Generating mipmaps
                #Swapping the bitmap's channels.
                if (format != target_format or self.downres_amount > 0 or
                    self.swapping_channels or self.generate_mipmaps):
                    
                    '''if the texture is swizzled then need to unswizzle it before we
                    can do certain conversions with it. We can't downsample it while
                    swizzled nor convert to a compressed format(swizzling unsupported)'''
                    if self.swizzled and (self.downres_amount > 0 or self.generate_mipmaps or
                                          target_format in COMPRESSED_FORMATS):
                        if swizzler is not None:
                            self.deswizzler.swizzle_texture(True)
                        else:
                            print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

                    '''figure out if we need to depalettize. some formats wont
                    support palettes, like DXT1-5, and downressing and other
                    operations will require pixels to be explicitely defined'''
                    if (target_format in COMPRESSED_FORMATS or self.downres_amount > 0) and self.is_palettized():
                        self.palettize = False

                    
                    """CONVERT PACKED PIXELS INTO UNPACKED CHANNEL VALUES.
                    CHANNEL SWAPPING IS INTEGRATED INTO UNPACKING THE PIXELS"""
                    if self.packed:
                        #store the dimensions to local variables so we can change them
                        width, height, depth = self.width, self.height, self.depth
                        
                        for mipmap_index in range(self.mipmap_count+1):
                            
                            for sub_bitmap in range(self.sub_bitmap_count):
                                #get the index of the bitmap we'll be working with
                                bitmap_index = sub_bitmap + (mipmap_index*self.sub_bitmap_count)
                                
                                if self.is_palettized(bitmap_index):
                                    #unpack the bitmap's palette and indexing
                                    unpacked_palette, unpacked_pixels = self.palettized_unpacker(self.palette[bitmap_index],
                                                                                                 self.texture_block[bitmap_index])
                                    if not unpacked_pixels:
                                        return False
                                    
                                    '''replace the packed palette with the unpacked one'''
                                    self.palette[bitmap_index] = unpacked_palette
                                else:
                                    unpacked_pixels = self.unpack(bitmap_index, width, height, depth)
                                    if unpacked_pixels is None:
                                        print("ERROR: UNABLE TO UNPACK IMAGE DATA. CONVERSION CANCELLED.")
                                        return False
                                    
                                #now that we are done unpacking the pixel data we
                                #replace the packed array with the unpacked one
                                self.texture_block[bitmap_index] = unpacked_pixels

                            #calculate the dimensions for the next mipmap
                            width, height, depth = dimension_lower_bound_check(width//2,height//2,depth//2)
                            
                        self.packed = False
                        self.palette_packed = False


                    
                    '''DOWNRES BITMAP TO A LOWER RESOLUTION IF STILL NEEDING TO'''
                    #only run if there aren't any mipmaps and
                    #this bitmap still needs to be downressed
                    if self.mipmap_count == 0 and self.downres_amount > 0:
                        if swizzler is not None:
                            for sub_bitmap in range(self.sub_bitmap_count):
                                downressed_pixel_array, width, height, depth = self._downsample_bitmap(self.texture_block[sub_bitmap],
                                                                                                       self.downres_amount, self.width,
                                                                                                       self.height, self.depth, True)
                                
                                #now that we are done repacking the pixel data we replace the old pixel array with the new one
                                self.texture_block[sub_bitmap] = downressed_pixel_array
                                
                            self.downres_amount = 0
                            self.texture_info["width"] = self.width = width
                            self.texture_info["height"] = self.height = height
                            self.texture_info["depth"] = self.depth = depth
                        else:
                            self.downres_amount = 0
                            print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT DOWNRES WITHOUT SWIZZLER.")



                    '''GENERATE MIPMAPS FOR BITMAP'''
                    if self.generate_mipmaps:
                        if swizzler is not None:
                            new_mipmap_count = logs_of_2[max(self.width, self.height, self.depth)]
                            mipmaps_to_make = new_mipmap_count - self.mipmap_count
                            
                            if mipmaps_to_make:
                                
                                #get the current smallest dimensions so we can change them
                                mip_width, mip_height, mip_depth = dimension_lower_bound_check(self.width//(2**self.mipmap_count),
                                                                                               self.height//(2**self.mipmap_count),
                                                                                               self.depth//(2**self.mipmap_count))
                                #Loop for each mipmap we need to make
                                for mipmap in range(self.mipmap_count, new_mipmap_count):
                                    for sub_bitmap in range(self.sub_bitmap_count):
                                        
                                        if self.is_palettized(bitmap_index):
                                            #################################################################################
                                            """############ NEED TO WRITE ROUTINE FOR MAKING PALETTIZED MIPS #############"""
                                            #################################################################################

                                            #FOR NOW WE'LL PREVENT MIPS FROM BEING CREATED BY RESETTING THE MIPMAP COUNT
                                            new_mipmap_count = self.mipmap_count
                                        else:
                                            #get the array of packed pixels we'll be working with
                                            mipmap_pixel_array = self.texture_block[mipmap*self.sub_bitmap_count + sub_bitmap]
                                            
                                            mipmap_pixel_array, _, __, ___ = self._downsample_bitmap(mipmap_pixel_array, 1,
                                                                                                     mip_width, mip_height, mip_depth)
                                            self.texture_block.append(mipmap_pixel_array)
                                    
                                    #calculate the dimensions for the next mipmap
                                    mip_width, mip_height, mip_depth = dimension_lower_bound_check(mip_width//2,
                                                                                                   mip_height//2,
                                                                                                   mip_depth//2)
                                #change the mipmap count in the settings
                                self.texture_info["mipmap_count"] = self.mipmap_count = new_mipmap_count
                        else:
                            print("ERROR: SWIZZLER MODULE NOT LOADED. "+
                                  "CANNOT GENERATE MIPMAPS WITHOUT SWIZZLER.")



                    '''REPACK THE PIXEL DATA TO THE TARGET FORMAT'''
                    if self.repack:
                        #store the dimensions to local variables so we can change them
                        width, height, depth = self.width, self.height, self.depth

                        #if we are palettizing a non-palettized bitmap, we need new palette
                        if self.palettize and not self.is_palettized():
                            self.palette = [None]*(self.mipmap_count+1)*self.sub_bitmap_count

                        for mipmap_index in range(self.mipmap_count+1):
                            for sub_bitmap in range(self.sub_bitmap_count):
                                #get the index of the bitmap we'll be working with
                                bitmap_index = sub_bitmap + (mipmap_index*self.sub_bitmap_count)

                                if self.palettize:
                                    if self.is_palettized(bitmap_index):
                                        #get the unpacked palette and indexing we'll be working with
                                        unpacked_palette = self.palette[bitmap_index]
                                        unpacked_indexing = self.texture_block[bitmap_index]
                                    else:
                                        #pass the pixels over to the function to create a color palette and indexing from it
                                        unpacked_palette, unpacked_indexing = self.palette_picker(self.texture_block[bitmap_index])

                                    packed_palette, packed_indexing = self.palettized_packer(unpacked_palette,
                                                                                             unpacked_indexing)
                                    self.palette[bitmap_index] = packed_palette
                                    self.texture_block[bitmap_index] = packed_indexing
                                else:
                                    repacked_pixel_array = self.pack(self.texture_block[bitmap_index],
                                                                     width, height, depth)
                                    if repacked_pixel_array is None:
                                        print("ERROR: UNABLE TO PACK IMAGE DATA. "+
                                              "CONVERSION CANCELLED.")
                                        return False
                                    
                                    #now that we are done repacking the pixel data we replace the old pixel array with the new one
                                    self.texture_block[bitmap_index] = repacked_pixel_array

                            #calculate the dimensions for the next mipmap
                            width, height, depth = dimension_lower_bound_check(width//2,
                                                                               height//2,
                                                                               depth//2)
                            
                        self.packed = True
                        self.palette_packed = True
                        self.indexing_size = self.target_indexing_size

                """SWIZZLE THE TEXTURE IF POSSIBLE AND THE TARGET SWIZZLE MODE ISNT THE CURRENT SWIZZLE MODE"""
                if not(self.target_format in COMPRESSED_FORMATS):
                    if swizzler is not None:
                        self.reswizzler.swizzle_texture()
                    else:
                        print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT "+
                              "SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

                #now that we have thoroughly messed with the bitmap, we need
                #to change the format and default all the channel mappings
                self.format = target_format
                self._set_all_channel_mappings()
                
                #return that the conversion was successful
                return True
            except:
                print("Error occurred while attempting to convert texture.")
                print(format_exc())
        else:
            print("ERROR: NO TEXTURE LOADED. CANNOT PREFORM BITMAP"+
                  "CONVERSION WITHOUT A LOADED TEXTURE")




    def depalettize_bitmap(self, unpacked_palette, unpacked_indexing):
        """Converts a palettized bitmap into an 8BPP unpalettized version and
        returns it. palette and indexing provided must be in an unpacked format"""
        ucc = self.unpacked_channel_count
        
        depalettized_bitmap = array(self._UNPACK_ARRAY_CODE, [0]*(ucc*len(unpacked_indexing)))

        i = 0

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if ucc == 4:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index*4]
                depalettized_bitmap[i+1] = unpacked_palette[index*4+1]
                depalettized_bitmap[i+2] = unpacked_palette[index*4+2]
                depalettized_bitmap[i+3] = unpacked_palette[index*4+3]
                i += 4
        elif ucc == 2:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index*2]
                depalettized_bitmap[i+1] = unpacked_palette[index*2+1]
                i += 2
        elif ucc == 1:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index]
                i += 1
        
        return depalettized_bitmap



    def _downsample_bitmap(self, unsampled_bitmap, sample_size,
                           width, height, depth, delete_original=False):
        '''this function will halve a bitmap's resolution X number of times. X = self.downres_amount'''
        ucc = self.unpacked_channel_count
        
        gamma = self.gamma
        no_gamma_scale = True

        if max(gamma) != 1.0 or min(gamma) != 1.0:
            no_gamma_scale = False
            
        #calculate the new dimensions of the bitmap
        new_width, new_height, new_depth = dimension_lower_bound_check(width // powers_of_2[sample_size],
                                                                       height // powers_of_2[sample_size],
                                                                       depth // powers_of_2[sample_size])
        """These next three variables are the log of each dimension"""
        log_w, log_h, log_d = (logs_of_2[width],
                               logs_of_2[height],
                               logs_of_2[depth])

        """These next three variables are the log of each new dimension"""
        log_new_w, log_new_h, log_new_d = (logs_of_2[new_width],
                                           logs_of_2[new_height],
                                           logs_of_2[new_depth])

        """These next three variables are how many pixels to merge on each axis"""
        merge_x, merge_y, merge_z = (powers_of_2[log_w-log_new_w],
                                     powers_of_2[log_h-log_new_h],
                                     powers_of_2[log_d-log_new_d])

        #make the new array to place the downsampled pixels into
        downsampled_bitmap = array(self._UNPACK_ARRAY_CODE,
                                   [0]*(new_width*new_height*new_depth*ucc) )
        
        #this is how many pixels from are being merged into one
        pmio = merge_x * merge_y * merge_z

        #this is used in the gamma based merging to scale the 0-255 value to a 0-1 value
        pmd = pmio * 255.0
        
        """THIS PART IS ABSOLUTELY CRUCIAL. In order to easily merge all
        the pixels together we will swizzle them around so that all the
        pixels that will be merged into one are directly next to each
        other, but separated by color channel. so it will look like this:
        
        px1A|px2A|px3A|px4A
        px1R|px2R|px3R|px4R
        px1G|px2G|px3G|px4G
        px1B|px2B|px3B|px4B
        """
        pixel_merge_swizzler = swizzler.Swizzler(texture_converter = self,
                                                 mask_type = "DOWNSAMPLER",
                                                 new_width=new_width,
                                                 new_height=new_height,
                                                 new_depth=new_depth)

        #we provide delete_original as the last argument since we don't necessarily want to delete the original image        
        swizzled_bitmap = pixel_merge_swizzler.swizzle_single_array(unsampled_bitmap, True,
                                                                    ucc, width, height, depth,
                                                                    delete_original)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if no_gamma_scale:
            """merge pixels linearly"""
            if ucc == 4:
                for i in range(0, new_width*new_height*new_depth*4, 4):
                    downsampled_bitmap[i] = (sum( swizzled_bitmap[i*pmio:pmio*(i+1)] )//pmio)
                    downsampled_bitmap[i+1] = (sum( swizzled_bitmap[pmio*(i+1):pmio*(i+2)] )//pmio)
                    downsampled_bitmap[i+2] = (sum( swizzled_bitmap[pmio*(i+2):pmio*(i+3)] )//pmio)
                    downsampled_bitmap[i+3] = (sum( swizzled_bitmap[pmio*(i+3):pmio*(i+4)] )//pmio)
            elif ucc == 2:
                for i in range(0, new_width*new_height*new_depth*2, 2):
                    downsampled_bitmap[i] = (sum( swizzled_bitmap[i*pmio:pmio*(i+1)] )//pmio)
                    downsampled_bitmap[i+1] = (sum( swizzled_bitmap[pmio*(i+1):pmio*(i+2)] )//pmio)
            else:
                for i in range(new_width*new_height*new_depth):
                    downsampled_bitmap[i] = (sum( swizzled_bitmap[i*pmio:pmio*(i+1)] )//pmio)
        else:
            """merge pixels with gamma correction"""
            #DO NOT USE GAMMA BASED MERGING IF THE BITMAP USES LINEAR GRADIENTS, LIKE METERS

            gamma_0 = gamma[0]
            gamma_exp_0 = 1.0/gamma_0
            gamma_scaler_0 = self.gamma_scaler[0]
            
            if ucc > 0:
                gamma_exp_1 = 1.0/gamma[1]
                gamma_scaler_1 = self.gamma_scaler[1]
                
            if ucc > 1:
                gamma_exp_2 = 1.0/gamma[2]
                gamma_scaler_2 = self.gamma_scaler[2]
                
            if ucc > 2:
                gamma_exp_3 = 1.0/gamma[3]
                gamma_scaler_3 = self.gamma_scaler[3]

            if ucc == 4:
                for i in range(0, new_width*new_height*new_depth*4, 4):
                    downsampled_bitmap[i] = int(((sum(map(lambda val: gamma_scaler_0[val], swizzled_bitmap[i*pmio:pmio*(i+1)]))/pmd)**gamma_exp_0 )*255)
                    downsampled_bitmap[i+1] = int(((sum(map(lambda val: gamma_scaler_1[val], swizzled_bitmap[pmio*(i+1):pmio*(i+2)]))/pmd)**gamma_exp_1 )*255)
                    downsampled_bitmap[i+2] = int(((sum(map(lambda val: gamma_scaler_2[val], swizzled_bitmap[pmio*(i+2):pmio*(i+3)]))/pmd)**gamma_exp_2 )*255)
                    downsampled_bitmap[i+3] = int(((sum(map(lambda val: gamma_scaler_3[val], swizzled_bitmap[pmio*(i+3):pmio*(i+4)]))/pmd)**gamma_exp_3 )*255)
            elif ucc == 2:
                for i in range(0, new_width*new_height*new_depth*2, 2):
                    downsampled_bitmap[i] = int(((sum(map(lambda val: gamma_scaler_0[val], swizzled_bitmap[i*pmio:pmio*(i+1)]))/pmd)**gamma_exp_0 )*255)
                    downsampled_bitmap[i+1] = int(((sum(map(lambda val: gamma_scaler_1[val], swizzled_bitmap[pmio*(i+1):pmio*(i+2)]))/pmd)**gamma_exp_1 )*255)
            else:
                for i in range(new_width*new_height*new_depth):
                    downsampled_bitmap[i] = int(((sum(map(lambda val: gamma_scaler_0[val], swizzled_bitmap[i*pmio:pmio*(i+1)]))/pmd)**gamma_exp_0 )*255)
                    
        return(downsampled_bitmap, new_width, new_height, new_depth)


    def _unpack_palettized(self, packed_palette, packed_indexing):
        '''When supplied with a packed palette and indexing,
        this function will return them in an unpacked form'''
        
        """UNPACK THE PALETTE"""
        if self.packed:
              unpacked_palette = self.palette_unpacker(packed_palette)
        else: unpacked_palette = packed_palette
        
        """UNPACK THE INDEXING"""
        if self.packed:
              unpacked_indexing = self.indexing_unpacker(packed_indexing)
        else: unpacked_indexing = packed_indexing
        
        if self.palettize:
            return(unpacked_palette, unpacked_indexing)
        
        #if the bitmap isn't going to stay palettized, we depalettize it
        return(None, self.depalettize_bitmap(unpacked_palette,
                                             unpacked_indexing))


    def _unpack_palette(self, packed_palette):
        """Just a redirect to the _Unpack_Raw function"""
        if not self.palette_packed:
            return packed_palette
        return self.unpack_raw(packed_palette)


    def _unpack_indexing(self, packed_indexing):
        if self.indexing_size not in (1,2,4,8):
            print("ERROR: PALETTIZED BITMAP INDEXING BIT COUNT MUST BE A POWER OF 2")
            return
        
        if self.indexing_size == 8:
            #if the indexing is 8 bits then we can 
            #just copy it directly into a new array
            unpacked_indexing = array("B", packed_indexing)
        else:
            pixel_count = int(( Decimal(len(packed_indexing)) /
                                Decimal(self.indexing_size)) * Decimal(8) )
            BPP = int(ceil(self.indexing_size/8.0))
            unpacked_indexing = array(INVERSE_PIXEL_ENCODING_SIZES[BPP],
                                      [0]*pixel_count)
        
            i = 0
            
            ######################
            '''NEEDS MORE SPEED'''
            ######################
            
            """The indexing will be unpacked in little endian mode"""
            if self.indexing_size == 1:
                for indexing_chunk in packed_indexing:
                    unpacked_indexing[i] = indexing_chunk&1
                    unpacked_indexing[i+1] = (indexing_chunk&2)>>1
                    unpacked_indexing[i+2] = (indexing_chunk&4)>>2
                    unpacked_indexing[i+3] = (indexing_chunk&8)>>3
                    unpacked_indexing[i+4] = (indexing_chunk&16)>>4
                    unpacked_indexing[i+5] = (indexing_chunk&32)>>5
                    unpacked_indexing[i+6] = (indexing_chunk&64)>>6
                    unpacked_indexing[i+7] = (indexing_chunk&128)>>7
                    i += 8
            elif self.indexing_size == 2:
                for indexing_chunk in packed_indexing:
                    unpacked_indexing[i] = indexing_chunk&3
                    unpacked_indexing[i+1] = (indexing_chunk&12)>>2
                    unpacked_indexing[i+2] = (indexing_chunk&48)>>4
                    unpacked_indexing[i+3] = (indexing_chunk&192)>>6
                    i += 4
            elif self.indexing_size == 4:
                for indexing_chunk in packed_indexing:
                    unpacked_indexing[i] = indexing_chunk&15
                    unpacked_indexing[i+1] = (indexing_chunk&240)>>4
                    i += 2

        return unpacked_indexing


    def unpack(self, bitmap_index, width, height, depth):
        """Used for unpacking non-palettized formats"""
        if self.format in FORMAT_UNPACKERS:
            unpacked_pixels = FORMAT_UNPACKERS[self.format](self, bitmap_index,
                                                            width, height, depth)
        elif self.format in RAW_FORMATS:
            if (self.unpacked_channel_count == 1 and
                self.source_channel_count == 1 and sum(self.unpacked_depths) == 8):
                #if there is only 1 channel in the source file and we
                #are unpacking to only 1 channel then we don't need to
                #unpack the channels and we can use the array as it is
                unpacked_pixels = array("B", self.texture_block[bitmap_index])
            else:
                unpacked_pixels = self.unpack_raw(self.texture_block[bitmap_index])
        else:
            print("ERROR: CANNOT FIND FORMAT UNPACK METHOD.")
            return
        
        return unpacked_pixels
        

    def unpack_raw(self, packed_array):
        '''this function takes the loaded raw pixel data texture and unpacks it'''
        offsets = self.channel_offsets
        masks   = self.channel_masks
        upscale = self.channel_upscalers
        fill_value = 0

        if BITS_PER_PIXEL[self.format] in (8, 16, 24, 32, 48, 64):
            #this is a little hack to set the alpha channel value to white if we are erasing it
            if masks[0] == 0:
                fill_value = powers_of_2[self.channel_depths[0]] - 1

            if self.unpacked_channel_count == 4:
                unpacked_array = self._unpack_raw_4_channel(packed_array,
                                                            offsets, masks,
                                                            upscale, fill_value)
            elif self.unpacked_channel_count == 2:
                unpacked_array = self._unpack_raw_2_channel(packed_array,
                                                            offsets, masks,
                                                            upscale, fill_value)
            elif self.unpacked_channel_count == 1:
                unpacked_array = self._unpack_raw_1_channel(packed_array,
                                                            offsets, masks,
                                                            upscale, fill_value)
        else:
            #if each pixel doesn't take up a bytesized amount of
            #space, then there will need to be a function to handle
            #them carefully. there isn't one written yet, so crash
            print("ERROR: CANNOT WORK WITH PIXELS THAT "+
                  "AREN'T EITHER 8, 16, 24, OR 32 BYTES.")
            crash

        return unpacked_array
    
    

    def _unpack_raw_4_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        a_shift, r_shift, g_shift, b_shift = offsets[0], offsets[1], offsets[2], offsets[3]
        a_mask,  r_mask,  g_mask,  b_mask =  masks[0],   masks[1],   masks[2],   masks[3]
        a_scale, r_scale, g_scale, b_scale = upscale[0], upscale[1], upscale[2], upscale[3]
        
        curr_index = 0
        #create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count )
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for pixel in packed_array:
            unpacked_array[curr_index] = a_scale[(pixel&a_mask)>>a_shift]
            unpacked_array[curr_index+1] = r_scale[(pixel&r_mask)>>r_shift]
            unpacked_array[curr_index+2] = g_scale[(pixel&g_mask)>>g_shift]
            unpacked_array[curr_index+3] = b_scale[(pixel&b_mask)>>b_shift]
            curr_index += 4

        return unpacked_array



    def _unpack_raw_2_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        a_shift, i_shift = offsets[0], offsets[1]
        a_mask,  i_mask  = masks[0], masks[1]
        a_scale, i_scale = upscale[0], upscale[1]
        
        curr_index = 0
            
        #create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count )
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for pixel in packed_array:
            unpacked_array[curr_index] = a_scale[(pixel&a_mask)>>a_shift]
            unpacked_array[curr_index+1] = i_scale[(pixel&i_mask)>>i_shift]
            curr_index += 2
                
        return unpacked_array



    def _unpack_raw_1_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        shift, mask, scale = offsets[0], masks[0], upscale[0]        
        curr_index = 0
            
        #create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for pixel in packed_array:
            unpacked_array[curr_index] = scale[(pixel&mask)>>shift]
            curr_index += 1
                
        return unpacked_array


    def _pack_palettized(self, unpacked_palette, unpacked_indexing):
        """Used for turning a palette and indexing into arrays
        suitable for being written to a file in little endian format"""
        
        """PACK THE PALETTE"""
        packed_palette = self.palette_packer(unpacked_palette)

        """PACK THE INDEXING"""
        packed_indexing = self.indexing_packer(unpacked_indexing)
            
        return(packed_palette, packed_indexing)


    def _pack_palette(self, unpacked_palette):
        if BITS_PER_PIXEL[self.target_format] == 24:
            #because we can't store 3 byte integers in an array, the
            #best we can do is remove the padded alpha channel
            packed_palette = bitmap_io.unpad_24bit_array(unpacked_palette)
        else:
            packed_palette = self.pack_raw(unpacked_palette)

        return packed_palette


    def _pack_indexing(self, unpacked_indexing):
        if self.indexing_size not in (1,2,4,8):
            print("ERROR: PALETTIZED BITMAP INDEXING "+
                  "BIT COUNT MUST BE A POWER OF 2")
            return
        
        largest_indexing_value = max(unpacked_indexing)
        
        if largest_indexing_value >= 2**self.target_indexing_size:
            print("ERROR: PALETTE INDEXING CONTAINS TOO LARGE AN ENTRY TO FIT.")
            print("FOUND INDEXING VALUE: ", largest_indexing_value)
            print("LARGEST ALLOWED INDEXING VALUE IS: ", 2**self.target_indexing_size-1)
            return
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        if self.target_indexing_size == 8:
            #if the indexing is 8 bits then we can
            #just copy it directly into a new array
            packed_indexing = array("B", unpacked_indexing)
        else:
            upi = unpacked_indexing
            packed_count = int( (Decimal(len(upi)) / Decimal(8))
                                * Decimal(self.target_indexing_size)  )
            packed_indexing = array("B", [0]*packed_count)
            
            """The indexing will be packed in little endian mode"""
            if self.target_indexing_size == 1:
                for i in range(0, len(packed_indexing)*8, 8):
                    packed_indexing[i//8] = ( upi[i]+        (upi[i+1]<<1) +
                                             (upi[i+2]<<2) + (upi[i+3]<<3) +
                                             (upi[i+4]<<4) + (upi[i+5]<<5) +
                                             (upi[i+6]<<6) + (upi[i+7]<<7) )                    
            elif self.target_indexing_size == 2:
                for i in range(0, len(packed_indexing)*4, 4):
                    packed_indexing[i//4] = ( upi[i]       + (upi[i+1]<<2) +
                                             (upi[i+2]<<4) + (upi[i+3]<<6)) 
            elif self.target_indexing_size == 4:
                for i in range(0, len(packed_indexing)*2, 2):
                    packed_indexing[i//2] = upi[i]+ (upi[i+1]<<4)

        return packed_indexing


    def pack(self, upa, width, height, depth):        
        """Used for packing non-palettized formats"""
        if self.target_format in FORMAT_PACKERS:
            rpa = FORMAT_PACKERS[self.target_format](self, upa,
                                                     width, height, depth)
        elif self.target_format in RAW_FORMATS:
            rpa = self.pack_raw(upa)
        else:
            print("ERROR: CANNOT FIND TARGET FORMAT PACK METHOD.")
            return None
        
        return rpa
    


    def pack_raw(self, unpacked_array):
        '''this function packs the 8-bit pixel array that's been created by the unpacking process'''
        downscale = self.channel_downscalers
        ucc = self.unpacked_channel_count
        
        if BITS_PER_PIXEL[self.target_format] in (8, 16, 24, 32, 48, 64):
            """If the nubmer of unpacked channels is just 1 it
            means we can just use the original array as it is."""
            if ucc == 1 and self.target_channel_count == 1:
                """We also need to check that the pixel is 8 bits, otherwise
                we'll need to put multiple pixels into one array index"""
                if BITS_PER_PIXEL[self.target_format] == 8:
                    packed_array = unpacked_array
                else:
                    packed_array = self._pack_raw_1_channel(unpacked_array,
                                                            downscale, ucc)
            else:
                off = FORMAT_CHANNEL_OFFSETS[self.target_format]
                
                """if we need to merge channels to get the target channel count"""
                #we split here to save time on conversions that don't require merging
                if self.channel_merge_mapping is not None:
                    cmm = self.channel_merge_mapping
                    cmd = self.channel_merge_divisors
                    
                    if ucc == 4:
                        packed_array = self._pack_raw_4_channel_merge(unpacked_array, downscale,
                                                                      ucc, cmm, off, cmd)
                    elif ucc == 2:
                        packed_array = self._pack_raw_2_channel_merge(unpacked_array, downscale,
                                                                      ucc, cmm, off, cmd)
                else:
                    if ucc == 4:
                        packed_array = self._pack_raw_4_channel(unpacked_array,
                                                                downscale, ucc,
                                                                off)
                    elif ucc == 2:
                        packed_array = self._pack_raw_2_channel(unpacked_array,
                                                                downscale, ucc,
                                                                off)
                        
        else:
            #if each pixel doesn't take up a bytesized amount of
            #space, then there will need to be a function to handle
            #them carefully. there isn't one written yet, so crash
            print("ERROR: CANNOT WORK WITH PIXELS THAT "+
                  "AREN'T EITHER 8, 16, 24, OR 32 BYTES.")
            crash

        return packed_array


    def _pack_raw_4_channel(self, upa, downscale, ucc, off):        
        #create the array to hold the pixel data after it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        a_shift, r_shift, g_shift, b_shift = off[0], off[1], off[2], off[3]
        a_scale, r_scale, g_scale, b_scale = downscale[0], downscale[1], downscale[2], downscale[3]

        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(packed_array)*4, 4):
            packed_array[i//4] = ( (a_scale[upa[i]]<<a_shift) +
                                   (r_scale[upa[i+1]]<<r_shift) +
                                   (g_scale[upa[i+2]]<<g_shift) +
                                   (b_scale[upa[i+3]]<<b_shift) )

        return packed_array


    def _pack_raw_2_channel(self, upa, downscale, ucc, off):
        #create the array to hold the pixel data after
        #it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
            
        a_shift, i_shift = off[0], off[1]
        c1_scale, c2_scale = downscale[0], downscale[1]
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(packed_array)*2, 2):
            packed_array[i//2] = ( (c1_scale[upa[i]]<<a_shift) +
                                   (c2_scale[upa[i+1]]<<i_shift) )
        return packed_array


    def _pack_raw_1_channel(self, upa, downscale, ucc, off=None):
        #create the array to hold the pixel data after
        #it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        scale = downscale[0]
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(len(packed_array)):
            packed_array[i] = scale[upa[i]]

        return packed_array


    def _pack_raw_4_channel_merge(self, upa, downscale, ucc, cmm, off, cmd):
        #create the array to hold the pixel data after it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format], [0]*(len(upa)//ucc))
        
        a_t, r_t, g_t, b_t = cmm[0], cmm[1], cmm[2], cmm[3]
        a_shift, r_shift, g_shift, b_shift = off[a_t], off[r_t], off[g_t], off[b_t]
        a_div, r_div, g_div, b_div = cmd[a_t], cmd[r_t], cmd[g_t], cmd[b_t]
        a_rnd, r_rnd, g_rnd, b_rnd = a_div//2, r_div//2, g_div//2, b_div//2        
        a_scale, r_scale, g_scale, b_scale = (downscale[0], downscale[1],
                                              downscale[2], downscale[3])
        
        #if the divisor is 256 it means we're removing the channel
        a_rnd *= int(a_div == CHANNEL_ERASE_DIVISOR)
        r_rnd *= int(r_div == CHANNEL_ERASE_DIVISOR)
        g_rnd *= int(g_div == CHANNEL_ERASE_DIVISOR)
        b_rnd *= int(b_div == CHANNEL_ERASE_DIVISOR)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(packed_array)*4, 4):
            packed_array[i//4] = ( (a_scale[((upa[i]+a_rnd)//a_div)]<<a_shift) +
                                   (r_scale[((upa[i+1]+r_rnd)//r_div)]<<r_shift) +
                                   (g_scale[((upa[i+2]+g_rnd)//g_div)]<<g_shift) +
                                   (b_scale[((upa[i+3]+b_rnd)//b_div)]<<b_shift) )
        return packed_array


    def _pack_raw_2_channel_merge(self, upa, downscale, ucc, cmm, off, cmd):
        #create the array to hold the pixel data after
        #it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        c1_target, c2_target = cmm[0], cmm[1]
        c1_shift, c2_shift = off[c1_target], off[c2_target]
        c1_div, c2_div = cmd[c1_target], cmd[c2_target]
        c1_rnd, c2_rnd = c1_div//2, c2_div//2
        c1_scale, c2_scale = downscale[0], downscale[1]

        #if the divisor is 256 it means we're removing the channel
        c1_rnd *= int(c1_div == CHANNEL_ERASE_DIVISOR)
        c2_rnd *= int(c2_div == CHANNEL_ERASE_DIVISOR)
        
        ######################
        '''NEEDS MORE SPEED'''
        ######################
        
        for i in range(0, len(packed_array)*2, 2):
            packed_array[i//2] = ( (c1_scale[((upa[i]+c1_rnd)//c1_div)]<<c1_shift) +
                                   (c2_scale[((upa[i+1]+c2_rnd)//c2_div)]<<c2_shift) )

        return packed_array


    def _palette_picker(self, unpacked_pixels):
        """Converts a bitmap into and returns an unpacked palette and indexing"""
        crash
        return(unpacked_palette, unpacked_indexing)
