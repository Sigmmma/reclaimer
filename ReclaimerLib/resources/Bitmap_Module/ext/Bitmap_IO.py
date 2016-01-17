import os
import time

from struct import pack_into, unpack_from, unpack
from array import array
from traceback import format_exc

import mmap

#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
BC = None

DXT_Format_Strings = {"DXT1":"DXT1",
                      "DXT2":"DXT2", "DXT3":"DXT3",
                      "DXT4":"DXT4", "DXT5":"DXT5",
                      "DXN":"ATI2"}
DXT_Format_Strings_I = {"DXT1":"DXT1",
                        "DXT2":"DXT2", "DXT3":"DXT3",
                        "DXT4":"DXT4", "DXT5":"DXT5",
                        "ATI2":"DXN"}

DXT_Texture_Type_Map = {"2D":0, "FLAT":0,
                        "3D":1, "VOLUME":1, "VOL":1, "DEPTH":0,
                        "CUBE":2, "CUBEMAP":2, "CUBE MAP":2, "CUBE_MAP":2}

DXT_Var_Offsets = {0:0, 1:4, 2:8, 3:12, 4:16, 5:20, 6:24, 7:28,
                   8:76, 9:80, 10:84, 11:88, 12:92, 13:96, 14:100, 15:104,
                   16:108, 17:112, 18:116, 19:120, 20:124}

DXT_Var_Defaults = {0:"DDS ".encode('UTF-8'), 1:124, 2:4103, 3:0, 4:0, 5:0, 6:0, 7:0,
                    8:32, 9:0, 10:b'\x00\x00\x00\x00', 11:0, 12:0, 13:0, 14:0, 15:0,
                    16:4096, 17:0, 18:0, 19:0, 20:0}

DXT_Format_ID_Blank = b'\x00\x00\x00\x00'.decode('Latin-1')

DXT_Header_Var_Names = {0:"DDS_Format_Name", 1:"Header_Size", 2:"FLAGS",
                        3:"Height", 4:"Width", 5:"Pitch_or_Linear_Size", 6:"Depth",
                        7:"Mipmap_Count", 8:"Pixel_Struct_Size", 9:"Pixel_Format_Flags",
                        10:"DXT_Format_ID", 11:"BPP",
                        12:"R_Mask", 13:"G_Mask", 14:"B_Mask", 15:"A_Mask",
                        16:"Caps_1", 17:"Caps_2",
                        18:"Reserved_0", 19:"Reserved_1", 20:"Reserved_2"}

TGA_Image_Types = { 0:"BLANK",
                    1:"COLOR_MAPPED", 9:"RLE_COLOR_MAPPED",
                    2:"TRUE_COLOR",  10:"RLE_TRUE_COLOR",
                    3:"MONOCHROME",  11:"RLE_MONOCHROME"}

        
def Save_to_TGA_File(convertor, Extension, Output_Path, **kwargs):
    """Saves the currently loaded texture to a TGA file"""
    
    if ( convertor.Format in (BC.FORMAT_R5G6B5, BC.FORMAT_A4R4G4B4, BC.FORMAT_A8Y8, BC.FORMAT_U8V8) or
         convertor.Format in BC.COMPRESSED_FORMATS):
        print("CANNOT EXTRACT THIS FORMAT TO TGA. EXTRACTING TO DDS INSTEAD.")
        Save_to_DDS_File(convertor, "dds", Output_Path, **kwargs)
        return
    
    if BC.BITS_PER_PIXEL[convertor.Format] > 32:
        print("ERROR: CANNOT SAVE BITMAP OF HIGHER THAN 32 BIT COLOR DEPTH TO DDS.\nCANCELLING TGA SAVE.")
        return
    
    Texture_Description = {"Width":convertor.Width, "Height":convertor.Height*convertor.Depth,
                           "Image_Type":2, "Palettized":False}

    Channel_Count = BC.FORMAT_CHANNEL_COUNTS[convertor.Format]
    
    Texture_Description["Image_Descriptor"] = BC.FORMAT_CHANNEL_DEPTHS[convertor.Format][0]
    Texture_Description["BPP"] = BC.BITS_PER_PIXEL[convertor.Format]

    if Channel_Count in (1,2):
        Texture_Description["Image_Type"] = 3
    
    if convertor.Is_Palettized():
        Texture_Description["Palettized"] = True
        Texture_Description["Color_Map_Type"] = 1
        Texture_Description["Image_Type"] = 1
        Texture_Description["Color_Map_Origin"] = 0
        Texture_Description["Color_Map_Length"] = 2**convertor.Indexing_Size
        Texture_Description["Color_Map_Depth"] = BC.BITS_PER_PIXEL[convertor.Format]
        Texture_Description["Image_Descriptor"] = 0
            
        if convertor.Target_Indexing_Size < 8:
            Texture_Description["BPP"] = 8
        else:
            Texture_Description["BPP"] = convertor.Indexing_Size

    Final_Output_Path = Output_Path
    Width = convertor.Width
    Height = convertor.Height

    for Sub_Bitmap in range(convertor.Sub_Bitmap_Count):                
        if not os.path.exists(os.path.dirname(Output_Path)):
            os.makedirs(os.path.dirname(Output_Path))
            
        if convertor.Sub_Bitmap_Count > 1:
            Final_Output_Path = Output_Path+"_tex"+str(Sub_Bitmap)
        
        with open(Final_Output_Path+"."+Extension, 'w+b') as TGA_File:
            #write the header and get the offset to start writing the pixel data
            Pixel_Start_Offset = Write_TGA_Header(TGA_File, **Texture_Description)

            TGA_File.seek(Pixel_Start_Offset)
            
            if Texture_Description["Palettized"]:
                Palette = Packed_Palette = convertor.Palette[Sub_Bitmap]
                Indexing = Packed_Indexing = convertor.Texture_Block[Sub_Bitmap]
                
                if not convertor.Palette_Packed:
                    Packed_Palette = convertor.Palette_Packer(Palette)
                    
                temp = convertor.Target_Indexing_Size
                '''need to pack the indexing and make sure it's 8-bit
                   since TGA doesn't support less than 8 bit indexing'''
                if convertor.Indexing_Size < 8:
                    convertor.Target_Indexing_Size = 8
                    if convertor.Packed:
                        Packed_Indexing = convertor.Indexing_Packer(convertor.Indexing_Unpacker(Packed_Indexing))
    
                if not convertor.Packed:
                    Packed_Indexing = convertor.Indexing_Packer(Indexing)
                    
                convertor.Target_Indexing_Size = temp
                        
                TGA_File.write(Packed_Palette)
                TGA_File.write(Packed_Indexing)
            else:
                if convertor.Packed:
                    Pixel_Array = convertor.Texture_Block[Sub_Bitmap]
                else:
                    Pixel_Array = convertor.Pack(convertor.Texture_Block[Sub_Bitmap],
                                                 Width, Height, 0)
                    Width, Height, _ = BC.Dimension_Lower_Bound_Check(Width//2, Height//2)
                    if Pixel_Array is None:
                        print("ERROR: UNABLE TO PACK IMAGE DATA.\nCANCELLING TGA SAVE.")
                        return()
                
                if BC.BITS_PER_PIXEL[convertor.Format] == 24:
                    Pixel_Array = Unpad_24Bit_Array(Pixel_Array)
                    
                TGA_File.write(Pixel_Array)


def Save_to_DDS_File(convertor, Extension, Output_Path, **kwargs):
    """Saves the currently loaded texture to a DDS file"""

    if BC.BITS_PER_PIXEL[convertor.Format] > 32:
        print("ERROR: CANNOT SAVE BITMAP OF HIGHER THAN 32 BIT COLOR DEPTH TO DDS.\nCANCELLING DDS SAVE.")
        return

    Texture_Description = {"Width":convertor.Width, "Height":convertor.Height, "Depth":convertor.Depth,
                           "Mipmap_Count":convertor.Mipmap_Count, "Texture_Type":convertor.Texture_Type,
                           "Palettized":False, "Format":convertor.Format}
        
    Channel_Count = 3
    if convertor.Format not in BC.THREE_CHANNEL_FORMATS:
        Channel_Count = BC.FORMAT_CHANNEL_COUNTS[convertor.Format]
    
    if convertor.Format in DXT_Format_Strings:
        Texture_Description["Compressed"] = True
        Texture_Description["DXT_Format_ID"] = DXT_Format_Strings[convertor.Format]
    else:
        Texture_Description["Compressed"] = False
        Texture_Description["BPP"] = BC.BITS_PER_PIXEL[convertor.Format]
        
        if Channel_Count == 1:
            if Texture_Description["Format"] == BC.FORMAT_A8:
                Texture_Description["A_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][0]
            else:
                Texture_Description["R_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][0]
        elif Channel_Count == 2:
            Texture_Description["A_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][0]
            Texture_Description["R_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][1]
        else:
            Texture_Description["A_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][0]
            Texture_Description["R_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][1]
            Texture_Description["G_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][2]
            Texture_Description["B_Mask"] = BC.FORMAT_CHANNEL_MASKS[convertor.Format][3]
            
    Texture_Description["Channel_Count"] = Channel_Count
    
    Final_Output_Path = Output_Path
    Width = convertor.Width
    Height = convertor.Height
    Depth = convertor.Depth

    if not os.path.exists(os.path.dirname(Output_Path)):
        os.makedirs(os.path.dirname(Output_Path))

    if convertor.Texture_Type == BC.TYPE_CUBEMAP:
        with open(Final_Output_Path+"."+Extension, 'w+b') as DDS_File:
            #write the header and get the offset to start writing the pixel data
            Pixel_Start_Offset = Write_DDS_Header(DDS_File, **Texture_Description)
            DDS_File.seek(Pixel_Start_Offset)
            
            #write each of the pixel arrays into the bitmap
            for Sub_Bitmap in range(convertor.Sub_Bitmap_Count):
                #write each of the pixel arrays into the bitmap
                for Mipmap in range(convertor.Mipmap_Count+1):
                    Bitmap_Index = Sub_Bitmap + Mipmap*convertor.Sub_Bitmap_Count
                    
                    if convertor.Is_Palettized():
                        Palette = Unpacked_Palette = convertor.Palette[Bitmap_Index]
                        Indexing = Unpacked_Indexing = convertor.Texture_Block[Bitmap_Index]
                        
                        if convertor.Palette_Packed:
                            Unpacked_Palette = convertor.Palette_Unpacker(Palette)                            
                        if convertor.Packed:
                            Unpacked_Indexing = convertor.Indexing_Unpacker(Indexing)
                            
                        Unpacked_Pixel_Array = convertor.Depalettize_Bitmap(Unpacked_Palette, Unpacked_Indexing)
                        Pixel_Array = convertor.Pack_Raw(Unpacked_Pixel_Array)
                    else:
                        if convertor.Packed:
                            Pixel_Array = convertor.Texture_Block[Bitmap_Index]
                        else:
                            Pixel_Array = convertor.Pack(convertor.Texture_Block[Bitmap_Index],
                                                         Width, Height, Depth)
                            Width, Height, Depth = BC.Dimension_Lower_Bound_Check(Width//2,
                                                                                  Height//2,
                                                                                  Depth//2)
                            if Pixel_Array is None:
                                print("ERROR: UNABLE TO PACK IMAGE DATA.\nCANCELLING DDS SAVE.")
                                return()
                        
                    if BC.BITS_PER_PIXEL[convertor.Format] == 24:
                        Pixel_Array = Unpad_24Bit_Array(Pixel_Array)
                    DDS_File.write(Pixel_Array)
    else:
        for Sub_Bitmap in range(convertor.Sub_Bitmap_Count):
            if convertor.Sub_Bitmap_Count > 1:
                Final_Output_Path = Output_Path+"_"+str(Sub_Bitmap)
            
            with open(Final_Output_Path+".dds", 'w+b') as DDS_File:
                #write the header and get the offset to start writing the pixel data
                Pixel_Start_Offset = Write_DDS_Header(DDS_File, **Texture_Description)
                DDS_File.seek(Pixel_Start_Offset)
                
                #write each of the pixel arrays into the bitmap
                for Mipmap in range(convertor.Mipmap_Count+1):
                    Bitmap_Index = Sub_Bitmap + Mipmap*convertor.Sub_Bitmap_Count
                    
                    if convertor.Is_Palettized():
                        Palette = Unpacked_Palette = convertor.Palette[Bitmap_Index]
                        Indexing = Unpacked_Indexing = convertor.Texture_Block[Bitmap_Index]
                            
                        if convertor.Palette_Packed:
                            Unpacked_Palette = convertor.Palette_Unpacker(Palette)
                        if convertor.Packed:
                            Unpacked_Indexing = convertor.Indexing_Unpacker(Indexing)
                            
                        Pixel_Array = convertor.Pack_Raw(convertor.Depalettize_Bitmap(Unpacked_Palette,
                                                                                      Unpacked_Indexing))
                    else:
                        if convertor.Packed:
                            Pixel_Array = convertor.Texture_Block[Bitmap_Index]
                        else:
                            Pixel_Array = convertor.Pack(convertor.Texture_Block[Bitmap_Index],
                                                         Width, Height, Depth)
                            Width, Height, Depth = BC.Dimension_Lower_Bound_Check(Width//2,
                                                                                  Height//2,
                                                                                  Depth//2)
                            if Pixel_Array is None:
                                print("ERROR: UNABLE TO PACK IMAGE DATA.\nCANCELLING DDS SAVE.")
                                return()
                        
                    if BC.BITS_PER_PIXEL[convertor.Format] == 24:
                        Pixel_Array = Unpad_24Bit_Array(Pixel_Array)
                    DDS_File.write(Pixel_Array)


def Save_to_Raw_Data_File(convertor, Extension, Output_Path, **kwargs):
    """Saves the currently loaded texture to a raw bin file. The file has no
    header and in most cases wont be able to be directly opened be applications."""

    Final_Output_Path = Output_Path

    if not os.path.exists(os.path.dirname(Output_Path)):
        os.makedirs(os.path.dirname(Output_Path))
        
    for Sub_Bitmap in range(convertor.Sub_Bitmap_Count):
        if convertor.Sub_Bitmap_Count > 1:
            Final_Output_Path = Output_Path+"_tex"+str(Sub_Bitmap)
                
        #write each of the pixel arrays into the bitmap
        for Mipmap in range(convertor.Mipmap_Count+1):
            Bitmap_Index = Sub_Bitmap + Mipmap*convertor.Sub_Bitmap_Count
            
            if convertor.Mipmap_Count:
                Final_Output_Path = Output_Path+"_mip"+str(Mipmap)
        
            with open(Final_Output_Path+".bin", 'w+b') as BIN_File:
                if convertor.Is_Palettized():
                    Palette = Packed_Palette = convertor.Palette[Bitmap_Index]
                    Indexing = Packed_Indexing = convertor.Texture_Block[Bitmap_Index]
                    
                    if not convertor.Palette_Packed:
                        Packed_Palette = convertor.Palette_Packer(Palette)
                    if not convertor.Packed:
                        Packed_Indexing = convertor.Indexing_Packer(Indexing)
                        
                    if BC.BITS_PER_PIXEL[convertor.Format] == 24:
                        Packed_Palette = Unpad_24Bit_Array(Packed_Palette)
                    elif BC.BITS_PER_PIXEL[convertor.Format] == 48:
                        Packed_Palette = Unpad_48Bit_Array(Packed_Palette)
                        
                    BIN_File.write(Packed_Palette)
                    BIN_File.write(Packed_Indexing)
                else:
                    if convertor.Packed:
                        Pixel_Array = convertor.Texture_Block[Bitmap_Index]
                    else:
                        Pixel_Array = convertor.Pack(convertor.Texture_Block[Bitmap_Index],
                                                     Width, Height, Depth)
                        Width, Height, Depth = BC.Dimension_Lower_Bound_Check(Width//2,
                                                                              Height//2,
                                                                              Depth//2)
                        if Pixel_Array is None:
                            print("ERROR: UNABLE TO PACK IMAGE DATA.\nCANCELLING DDS SAVE.")
                            return()
                    
                    if BC.BITS_PER_PIXEL[convertor.Format] == 24:
                        Pixel_Array = Unpad_24Bit_Array(Pixel_Array)
                    elif BC.BITS_PER_PIXEL[convertor.Format] == 48:
                        Pixel_Array = Unpad_48Bit_Array(Pixel_Array)
                    BIN_File.write(Pixel_Array)

            

                
def Load_from_TGA_File(convertor, Extension, Input_Path, **kwargs):
    """Loads a TGA file into the convertor. Currently doesn't
    support correcting the upside down nature of Truevision
    images. If an image is Truevision, it will be upside down."""
    Final_Input_Path = Input_Path+"."+Extension
    unable_to_load = False
    
    try:
        with open(Final_Input_Path, 'r+b') as TGA_File:
            
            TGA_Data = mmap.mmap(TGA_File.fileno(), 0, access=mmap.ACCESS_READ)
            
            #General image info
            ID_Length    = unpack_from("B", TGA_Data, 0)[0]
            Color_Mapped = unpack_from("B", TGA_Data, 1)[0]
            Image_Type   = TGA_Image_Types[unpack_from("B", TGA_Data, 2)[0]]
            Compressed = Image_Type[:3] == "RLE"

            #Color map info
            Color_Map_Origin = unpack_from("<H", TGA_Data, 3)[0]
            Color_Map_Length = unpack_from("<H", TGA_Data, 5)[0]
            Color_Map_Depth  = unpack_from("B", TGA_Data,  7)[0]

            #Image origin coordinate
            Image_Origin_X = unpack_from("<H", TGA_Data,  8)[0]
            Image_Origin_Y = unpack_from("<H", TGA_Data, 10)[0]

            #Dimensions and color depth
            Width  = unpack_from("<H", TGA_Data, 12)[0]
            Height = unpack_from("<H", TGA_Data, 14)[0]
            BPP    = unpack_from("B", TGA_Data,  16)[0]
            
            Image_Descriptor = unpack_from("B", TGA_Data, 17)[0]

            #Image descriptor properties
            Alpha_Depth = Image_Descriptor & 15
            Image_H_Flip = bool(Image_Descriptor & 16)
            Image_V_Flip = not bool(Image_Descriptor & 32)
            
            Interleave_Order = (Image_Descriptor & 192) >> 6

            #do another check to make sure image is color mapped
            Color_Mapped = bool(Color_Mapped & int("COLOR_MAPPED" in Image_Type) )

            Texture_Info = {"Width":Width, "Height":Height, "Depth":1,
                            "Texture_Type":"2D", "Mipmap_Count":0,
                            "Sub_Bitmap_Count":1, "Filepath":Input_Path}

            #figure out what color format we've got
            if Color_Mapped:
                if Color_Map_Depth == 8:
                    Texture_Info["Format"] = BC.FORMAT_Y8
                elif Color_Map_Depth == 15:
                    Texture_Info["Format"] = BC.FORMAT_R5G6B5
                elif Color_Map_Depth == 16:
                    Texture_Info["Format"] = BC.FORMAT_A1R5G5B5
                elif Color_Map_Depth == 24:
                    Texture_Info["Format"] = BC.FORMAT_R8G8B8
                elif Color_Map_Depth == 32:
                    Texture_Info["Format"] = BC.FORMAT_A8R8G8B8
                else:
                    print("Unable to load Targa images with",
                          Color_Map_Depth,"bit color palette.")
                    unable_to_load = True
            else:
                if BPP == 1:
                    Texture_Info["Format"] = BC.FORMAT_STENCIL
                    #NOT YET SUPPORTED
                    
                    print("Not yet able to load black and white 1-bit color Targa images.")
                    unable_to_load = True
                elif BPP == 8:
                    if Alpha_Depth == 8:
                        Texture_Info["Format"] = BC.FORMAT_A8
                    else:
                        Texture_Info["Format"] = BC.FORMAT_Y8
                elif BPP == 15:
                    Texture_Info["Format"] = BC.FORMAT_R5G6B5
                elif BPP == 16:
                    if Alpha_Depth == 0:
                        Texture_Info["Format"] = BC.FORMAT_R5G6B5
                    elif Alpha_Depth == 1:
                        Texture_Info["Format"] = BC.FORMAT_A1R5G5B5
                    elif Alpha_Depth == 4:
                        Texture_Info["Format"] = BC.FORMAT_A4R4G4B4
                    else:
                        Texture_Info["Format"] = BC.FORMAT_A8Y8
                elif BPP == 24:
                    Texture_Info["Format"] = BC.FORMAT_R8G8B8
                elif BPP == 32:
                    if Alpha_Depth == 0:
                        Texture_Info["Format"] = BC.FORMAT_X8R8G8B8
                    else:
                        Texture_Info["Format"] = BC.FORMAT_A8R8G8B8
                else:
                    print("Unable to load", BPP, "bit color Targa images.")
                    unable_to_load = True

            #fix the bit depths so calculations work properly
            if Color_Map_Depth == 15:
                Color_Map_Depth = 16
            if BPP == 15:
                BPP = 16

            Palette_Start = 18 + ID_Length
            Image_Start = 18 + ID_Length + ((Color_Map_Depth//8)*Color_Map_Length)

            if Interleave_Order:
                print("Not yet able to load Targa images with interleaved pixels.")
                unable_to_load = True
            if Image_Type == "BLANK":
                print("Targa image is specified as blank in the header. Nothing to load.")
                unable_to_load = True

            if Image_H_Flip:
                print("WARNING: TGA image header says the bitmap is flipped horizontally.",
                      "\nThis library doesnt currently support re-orienting it properly.")
            if Image_V_Flip:
                print("WARNING: TGA image header says the bitmap is flipped vertically.",
                      "\nThis library doesnt currently support re-orienting it properly.")
                
            if unable_to_load:
                return
            

            if Color_Mapped:
                if BC.BITS_PER_PIXEL[Texture_Info["Format"]] == 24:
                    Palette = Pad_24Bit_Array(TGA_Data[Palette_Start:Image_Start])
                else:
                    Palette = array(BC.FORMAT_DATA_SIZES[Texture_Info["Format"]],
                                    TGA_Data[Palette_Start:Image_Start])
                
                #if the color map doesn't start at zero
                #then we need to shift around the palette
                if Color_Map_Origin:
                    Shifted_Palette = Palette[Color_Map_Origin:len(Palette)]
                    Shifted_Palette.extend(Palette[:Color_Map_Origin])
                    Palette = Shifted_Palette
                    
                    Color_Map_Origin = 0

                Indexing = array("B", TGA_Data[Image_Start:Image_Start+Width*Height])
                
                Texture_Info["Palette"] = [Palette]
                Texture_Info["Palettize"] = True
                Texture_Info["Indexing_Size"] = BPP
                Texture_Block = [Indexing]
                
                #load all the bitmap data into the convertor
                convertor.Load_New_Texture(Texture_Block=Texture_Block, Texture_Info=Texture_Info)
            else:
                Texture_Block = []
                Comp = None
                if Compressed: Comp = "rle"
                Bitmap_Bytes_to_Array(TGA_Data[Image_Start:], 0, Texture_Block,
                                      Texture_Info["Format"], Width, Height, Compression=Comp)
                
                convertor.Load_New_Texture(Texture_Block=Texture_Block, Texture_Info=Texture_Info)
    except:
        print(format_exc())



def Load_from_DDS_File(convertor, Extension, Input_Path, **kwargs):
    """Loads a DDS file into the convertor."""
    Final_Input_Path = Input_Path+"."+Extension
    unable_to_load = False
    
    try:
        with open(Final_Input_Path, 'r+b') as DDS_File:
            DDS_Data = mmap.mmap(DDS_File.fileno(), 0, access=mmap.ACCESS_READ)
            
            Height = unpack_from("<I", DDS_Data, 12)[0]
            Width  = unpack_from("<I", DDS_Data, 16)[0]
            Depth  = unpack_from("<I", DDS_Data, 28)[0]
            
            Depth += int(Depth == 0)
            TYPE = BC.TYPE_2D
            Sub_Bitmap_Count = 1
            
            Linear_Size  = unpack_from("<I", DDS_Data, 20)[0]
            Mipmap_Count = unpack_from("<I", DDS_Data, 24)[0]
            Format_Flags = unpack_from("<I", DDS_Data, 80)[0]
            
            DXT_Format_ID = DDS_Data[84:88].decode('Latin-1')

            BPP = unpack_from("<I", DDS_Data, 88)[0]
            R_Mask = unpack_from("<I", DDS_Data, 92)[0]
            G_Mask = unpack_from("<I", DDS_Data, 96)[0]
            B_Mask = unpack_from("<I", DDS_Data, 100)[0]
            A_Mask = unpack_from("<I", DDS_Data, 104)[0]

            Caps_1 = unpack_from("<I", DDS_Data, 108)[0]
            Caps_2 = unpack_from("<I", DDS_Data, 112)[0]

            if DXT_Format_ID == "DX10":
                #there is a DDS_HEADER_DXT10 extended header present...... shit
                print("THIS LIBRARY CANNOT YET LOAD DX10 DDS FILES.")
                return

            #check if the texture is a cubemap and get how many faces exist
            if Caps_2&512:
                TYPE = BC.TYPE_CUBEMAP
                Sub_Bitmap_Count = ((Caps_2&1024)//1024   + (Caps_2&2048)//2048 +
                                    (Caps_2&4096)//4096   + (Caps_2&8192)//8192 +
                                    (Caps_2&16384)//16384 + (Caps_2&32768)//32768)

            #check if the texture is volumetric
            if Caps_2&2097152 and Depth > 1:
                if TYPE == BC.TYPE_CUBEMAP:
                    print("ERROR: DDS HEADER INVALID. TEXTURE SPECIFIED AS BOTH CUBEMAP AND VOLUMETRIC.")
                    return
                TYPE = BC.TYPE_3D
                
            if Format_Flags&4 and DXT_Format_ID != DXT_Format_ID_Blank:
                #if the texture has a compression method
                if DXT_Format_ID in DXT_Format_Strings_I:
                    Format = DXT_Format_Strings_I[DXT_Format_ID]
                else:
                    print("UNKNOWN DDS FORMAT.",DXT_Format_ID,"\nUNABLE TO LOAD DDS TEXTURE.")
                    return
            else:
                if Format_Flags&2:
                    Format = BC.FORMAT_A8
                elif Format_Flags&64:
                    if Format_Flags&1:
                        Format = BC.FORMAT_A8R8G8B8
                    else:
                        Format = BC.FORMAT_R8G8B8
                elif Format_Flags&512:
                    Format = BC.FORMAT_Y8U8V8
                elif Format_Flags&131072:
                    if Format_Flags&1:
                        Format = BC.FORMAT_A8Y8
                    else:
                        Format = BC.FORMAT_Y8
                elif Format_Flags&524288:
                    Format = BC.FORMAT_U8V8


                if BC.FORMAT_CHANNEL_COUNTS[Format] > 1:
                    #create a channel mapping to shift around the
                    #channels according to the masks in the header
                    Channel_Mapping = []
                    Channel_Count = BC.FORMAT_CHANNEL_COUNTS[Format]

            #im not sure if it's photoshop doing this, but it's weird....
            if Mipmap_Count >= 1: Mipmap_Count -= 1
            
            Texture_Info = {"Width":Width, "Height":Height, "Depth":Depth,
                            "Texture_Type":TYPE, "Mipmap_Count":Mipmap_Count,
                            "Sub_Bitmap_Count":Sub_Bitmap_Count,
                            "Format":Format, "Filepath":Input_Path}
            
            Texture_Block = []
            Data_Offset = 128
            
            #loop over each cube face and mipmap and turn them into pixel arrays
            for Cube_Face in range(Sub_Bitmap_Count):
                Mip_Width = Width
                Mip_Height = Height
                Mip_Depth = Depth
                
                for Mipmap in range(Mipmap_Count+1):
                    Bitmap_Index = Cube_Face + Mipmap*Sub_Bitmap_Count
                    Data_Offset = Bitmap_Bytes_to_Array(DDS_Data, Data_Offset, Texture_Block,
                                                        Format, Width, Height, Depth)

                    Mip_Width, Mip_Height, Mip_Depth = BC.Dimension_Lower_Bound_Check(Mip_Width//2,
                                                                                      Mip_Height//2,
                                                                                      Mip_Depth//2)
            convertor.Load_New_Texture(Texture_Block=Texture_Block, Texture_Info=Texture_Info)
    except:
        print(format_exc())


def Get_Size_of_Pixel_Bytes(Format, Width, Height, Depth=1):
    Pixel_Size = BC.PIXEL_ENCODING_SIZES[BC.FORMAT_DATA_SIZES[Format]]

    #make sure the dimensions for the format are correct
    Width, Height, Depth = BC.Dimension_Lower_Bound_Check(Width, Height, Depth, Format)
    
    Bitmap_Size = BC.Pixel_Count_to_Array_Length(Height*Width*Depth, Pixel_Size, Format) * Pixel_Size

    return(Bitmap_Size)



def Bitmap_Bytes_to_Array(Raw_Data, Offset, Texture_Block, Format, Width, Height, Depth=1, **kwargs):
    """This function will create an array of pixels of Width*Height*Depth from
    an iterable, sliceable, object, and append it to the supplied Texture_Block.
    This function will return the offset of the end of the pixel data so that
    textures following the current one can be found."""
    #get the texture encoding
    encoding = BC.FORMAT_DATA_SIZES[Format]

    Pixel_Size = BC.PIXEL_ENCODING_SIZES[encoding]

    #get how many bytes the texture is going to be
    Bitmap_Size = Bitmap_Data_End = Get_Size_of_Pixel_Bytes(Format, Width, Height, Depth)

    #if the data is compressed,we need to uncompress it
    if "Compression" in kwargs and kwargs["Compression"] is not None:
        Compression_Type = kwargs["Compression"].lower()
        if Compression_Type in Decompressors:
            Raw_Data, Bitmap_Data_End = Decompressors[Compression_Type](Raw_Data, Format,
                                                                        Width, Height, Depth)
        else:
            print("ERROR: CANNOT FIND SPECIFIED DECOMPRESOR FOR SUPPLIED PIXEL DATA.",
                  "COMPRESSION TYPE SPECIFIED IS:", Compression_Type)
            crash
    
    '''24 bit images are handled a bit differently since lots of things work on whole powers of 2.
    "2" can not be raised to an integer power to yield "24", whereas it can be for 8, 16, and 32.
    To fix this, the bitmap will be padded with an alpha channel on loading and ignored on saving.
    This will bring the 24 bit image up to 32 bit and make everything work just fine.'''
    if BC.BITS_PER_PIXEL[Format] == 24:
        #if R8G8B8, need to unpack each byte individually and shift and add them together
        Pixel_Array = Pad_24Bit_Array(Raw_Data[Offset:Offset+(Height*Width*Depth*3)])
    elif BC.BITS_PER_PIXEL[Format] == 48:
        #if R16G16B16, need to unpack each short individually and shift and add them together
        Pixel_Array = Pad_48Bit_Array(Raw_Data[Offset:Offset+(Height*Width*Depth*3)])
    else:
        #stream the start and end of the pixels from the raw_bitmap_data into an array
        Pixel_Array = array(encoding, Raw_Data[Offset:Offset+Bitmap_Size])

    #if not enough pixel data was supplied, extra will be added
    if len(Pixel_Array)*Pixel_Size < Bitmap_Size:
        print("WARNING: PIXEL DATA SUPPLIED DID NOT MEET THE SIZE EXPECTED. PADDING WITH ZEROS.")
        Pixel_Array.extend(array(Pixel_Array.typecode, [0]*( (Bitmap_Size//Pixel_Size) - len(Pixel_Array)) ))
    
    #add the pixel array to the current texture block
    Texture_Block.append(Pixel_Array)
    
    return(Offset + Bitmap_Data_End)



def Bitmap_Palette_to_Array(Raw_Data, Offset, Palette_Block, Format, Palette_Count):
    return(Bitmap_Bytes_to_Array(Raw_Data, Offset, Palette_Block, Format, Palette_Count, 1))
    

def Bitmap_Indexing_to_Array(Raw_Data, Offset, Indexing_Block, Width, Height, Depth=1):
    """This function will create an array of pixels of Width*Height*Depth from
       an iterable, sliceable, object. Since indexing never seems to be more
       than 8 bit, we won't worry about higher bit counts. Appends indexing
       array to supplied Indexing_Block and returns the end offset
    """
    Indexing_Block.append( array("B", Raw_Data[Offset:Offset+Width*Height*Depth]) )
    return(Offset+Width*Height*Depth)



def Pad_24Bit_Array(Unpadded_Pixel_Array):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Padded_Pixel_Array = array("I", map(lambda x: (  Unpadded_Pixel_Array[x] +
                                                     (Unpadded_Pixel_Array[x+1]<<8) +
                                                     (Unpadded_Pixel_Array[x+2]<<16) ),
                                        range(0, len(Unpadded_Pixel_Array), 3)  ))
    return(Padded_Pixel_Array)


def Pad_48Bit_Array(Unpadded_Pixel_Array):
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    Padded_Pixel_Array = array("Q", map(lambda x: (  Unpadded_Pixel_Array[x] +
                                                     (Unpadded_Pixel_Array[x+1]<<16) +
                                                     (Unpadded_Pixel_Array[x+2]<<32) ),
                                        range(0, len(Unpadded_Pixel_Array), 3)  ))
    return(Padded_Pixel_Array)



def Unpad_24Bit_Array(Pixel_Array):
    """given a 24BPP pixel data array that has been padded to
    32BPP, this will return an unpadded byte-size array copy.
    The endianness of the data will be little."""
    
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if Pixel_Array.typecode == "I":
        Unpadded_Pixel_Array = array("B", [0]*len(Pixel_Array)*3)
        for i in range(len(Pixel_Array)):
            Unpadded_Pixel_Array[i*3] = Pixel_Array[i]&255
            Unpadded_Pixel_Array[i*3+1] = (Pixel_Array[i]&65280)>>8
            Unpadded_Pixel_Array[i*3+2] = (Pixel_Array[i]&16711680)>>16
    elif Pixel_Array.typecode == "B":
        Unpadded_Pixel_Array = array("B", [0]*(len(Pixel_Array)//4)*3 )
        for i in range(len(Pixel_Array)//4):
            Unpadded_Pixel_Array[i*3] = Pixel_Array[i*4+1]
            Unpadded_Pixel_Array[i*3+1] = Pixel_Array[i*4+2]
            Unpadded_Pixel_Array[i*3+2] = Pixel_Array[i*4+3]
    else:
        print("ERROR: BAD TYPECODE FOR 24BIT PADDED ARRAY.")
        return
        
    return(Unpadded_Pixel_Array)



def Unpad_48Bit_Array(Pixel_Array):
    """given a 48BPP pixel data array that has been padded to
    64BPP, this will return an unpadded byte-size array copy.
    The endianness of the data will be little."""
    
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    
    if Pixel_Array.typecode == "Q":
        Unpadded_Pixel_Array = array("H", [0]*len(Pixel_Array)*3)
        for i in range(len(Pixel_Array)):
            Unpadded_Pixel_Array[i*3] = Pixel_Array[i]&65535
            Unpadded_Pixel_Array[i*3+1] = (Pixel_Array[i]&4294901760)>>16
            Unpadded_Pixel_Array[i*3+2] = (Pixel_Array[i]&281470681743360)>>32
    elif Pixel_Array.typecode == "H":
        Unpadded_Pixel_Array = array("H", [0]*(len(Pixel_Array)//4)*3 )
        for i in range(len(Pixel_Array)//4):
            Unpadded_Pixel_Array[i*3] = Pixel_Array[i*4+1]
            Unpadded_Pixel_Array[i*3+1] = Pixel_Array[i*4+2]
            Unpadded_Pixel_Array[i*3+2] = Pixel_Array[i*4+3]
    else:
        print("ERROR: BAD TYPECODE FOR 48BIT PADDED ARRAY.")
        return
        
    return(Unpadded_Pixel_Array)



def Uncompress_RLE(Compressed_Bytes, Format, Width, Height, Depth=1):
    """given an array compressed with run length encoding, this
    function will uncompress it so it and return the uncompressed array"""

    #get the texture encoding
    encoding = BC.FORMAT_DATA_SIZES[Format]
    BPP = BC.BITS_PER_PIXEL[Format]

    #make sure the dimensions for the format are correct
    Width, Height, Depth = BC.Dimension_Lower_Bound_Check(Width, Height, Depth, Format)

    #get how many bytes the texture is going to be
    Uncompressed_Bytes_Size = Get_Size_of_Pixel_Bytes(Format, Width, Height, Depth)
    Uncompressed_Bytes = bytearray(b'\x00'*Uncompressed_Bytes_Size)

    Pixel_Bytes_Count = Width*Height*Depth*(BPP//8)
    Current_Pixel_Byte = 0
    Read_Pos = 0
    
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    try:
        if BPP == 32:
            while Current_Pixel_Byte < Pixel_Bytes_Count:
                #if this packet is compressed with RLE
                if Compressed_Bytes[Read_Pos]&128:
                    for i in range(0, (Compressed_Bytes[Read_Pos]-127)*4, 4):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+2]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+2] = Compressed_Bytes[Read_Pos+3]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+3] = Compressed_Bytes[Read_Pos+4]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]-127)*4
                    Read_Pos += 5
                else:#if it's a raw packet
                    for i in range(0, (Compressed_Bytes[Read_Pos]+1)*4, 4):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+i+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+i+2]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+2] = Compressed_Bytes[Read_Pos+i+3]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+3] = Compressed_Bytes[Read_Pos+i+4]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]+1)*4
                    Read_Pos += (Compressed_Bytes[Read_Pos]+1)*4+1
        elif BPP == 24:
            while Current_Pixel_Byte < Pixel_Bytes_Count:
                #if this packet is compressed with RLE
                if Compressed_Bytes[Read_Pos]&128:
                    for i in range(0, (Compressed_Bytes[Read_Pos]-127)*3, 3):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+2]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+2] = Compressed_Bytes[Read_Pos+3]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]-127)*3
                    Read_Pos += 4
                else:#if it's a raw packet
                    for i in range(0, (Compressed_Bytes[Read_Pos]+1)*3, 3):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+i+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+i+2]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+2] = Compressed_Bytes[Read_Pos+i+3]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]+1)*3
                    Read_Pos += (Compressed_Bytes[Read_Pos]+1)*3+1
        elif BPP == 16:
            while Current_Pixel_Byte < Pixel_Bytes_Count:
                #if this packet is compressed with RLE
                if Compressed_Bytes[Read_Pos]&128:
                    for i in range(0, (Compressed_Bytes[Read_Pos]-127)*2, 2):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+2]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]-127)*2
                    Read_Pos += 3
                else:#if it's a raw packet
                    for i in range(0, (Compressed_Bytes[Read_Pos]+1)*2, 2):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+i+1]
                        Uncompressed_Bytes[Current_Pixel_Byte+i+1] = Compressed_Bytes[Read_Pos+i+2]
                    Current_Pixel_Byte += (Compressed_Bytes[Read_Pos]+1)*2
                    Read_Pos += (Compressed_Bytes[Read_Pos]+1)*2+1
        else:
            while Current_Pixel_Byte < Pixel_Bytes_Count:
                #if this packet is compressed with RLE
                if Compressed_Bytes[Read_Pos]&128:
                    for i in range(Compressed_Bytes[Read_Pos]-127):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+1]
                    Current_Pixel_Byte += Compressed_Bytes[Read_Pos]-127
                    Read_Pos += 2
                else:#if it's a raw packet
                    for i in range(Compressed_Bytes[Read_Pos]+1):
                        Uncompressed_Bytes[Current_Pixel_Byte+i]   = Compressed_Bytes[Read_Pos+i+1]
                    Current_Pixel_Byte += Compressed_Bytes[Read_Pos]+1
                    Read_Pos += Compressed_Bytes[Read_Pos]+2
    except IndexError:
        #index errors can be silently passed since the bytes
        #have been padded to their expected size already
        #just need to fix the final read offset
        if Compressed_Bytes[Read_Pos]&128:
            Read_Pos += (BPP//8)+1
        else:
            Read_Pos += (Compressed_Bytes[Read_Pos]+1)*(BPP//8)+1

    return(Uncompressed_Bytes, Read_Pos)



File_Writers = {"tga":Save_to_TGA_File, "dds":Save_to_DDS_File,
                "bin":Save_to_Raw_Data_File}
File_Readers = {"tga":Load_from_TGA_File, "dds":Load_from_DDS_File}
Decompressors = {"rle":Uncompress_RLE}


def Write_TGA_Header(TGA_File, **kwargs):
    ''' This function can be used to construct a TGA header. The
        first argument must be the buffer that the TGA file will be
        written to. The keywords that can be supplied are these.

        BPP---(BYTE)
        Width---(SHORT)
        Height---(SHORT)
        ID_Length---(BYTE)
        Image_Type---(BYTE)
        Image_Origin---[(SHORT),(SHORT)]
        Color_Map_Type---(BYTE)
        Color_Map_Depth---(BYTE)
        Color_Map_Origin---(SHORT)
        Color_Map_Length---(SHORT)
        Image_Descriptor---(BYTE)
    '''

    #the default values in case we aren't supplied with any
    ID_Length = 0
    Color_Map_Type = 0
    Image_Type = 2
    Color_Map_Origin = 0
    Color_Map_Length = 0
    Color_Map_Depth = 0
    Image_Origin = [0,0]
    Width = 0
    Height = 0
    BPP = 32
    Image_Descriptor = 32
    
    Header_Buffer = array("B",[0]*18)
    
    if kwargs is not None:
        if "ID_Length" in kwargs:
            ID_Length = kwargs["ID_Length"]
        if "Color_Map_Type" in kwargs:
            Color_Map_Type = kwargs["Color_Map_Type"]
        if "Image_Type" in kwargs:
            Image_Type = kwargs["Image_Type"]
        if "Color_Map_Origin" in kwargs:
            Color_Map_Origin = kwargs["Color_Map_Origin"]
        if "Color_Map_Length" in kwargs:
            Color_Map_Length = kwargs["Color_Map_Length"]
        if "Color_Map_Depth" in kwargs:
            Color_Map_Depth = kwargs["Color_Map_Depth"]
        if "Image_Origin" in kwargs:
            Image_Origin = kwargs["Image_Origin"]
        if "Width" in kwargs:
            Width = kwargs["Width"]
        if "Height" in kwargs:
            Height = kwargs["Height"]
        if "BPP" in kwargs:
            BPP = kwargs["BPP"]
        if "Image_Descriptor" in kwargs:
            Image_Descriptor = 32 + (kwargs["Image_Descriptor"]&223)
        
    pack_into('B',  Header_Buffer, 0,  ID_Length)
    pack_into('B',  Header_Buffer, 1,  Color_Map_Type)
    pack_into('B',  Header_Buffer, 2,  Image_Type)
    pack_into('<H', Header_Buffer, 3,  Color_Map_Origin)
    pack_into('<H', Header_Buffer, 5,  Color_Map_Length)
    pack_into('B',  Header_Buffer, 7,  Color_Map_Depth)
    pack_into('<H', Header_Buffer, 8,  Image_Origin[0])
    pack_into('<H', Header_Buffer, 10, Image_Origin[1])
    
    pack_into('<H', Header_Buffer, 12, Width)
    pack_into('<H', Header_Buffer, 14, Height)
    pack_into('B',  Header_Buffer, 16, BPP)
    pack_into('B',  Header_Buffer, 17, Image_Descriptor)
    
    TGA_File.write(Header_Buffer)
    return(18)




def Write_DDS_Header(DDS_File, **kwargs):
    ''' This function can be used to construct a DDS header. The first
        argument must be the buffer that the DDS file will be written to.
        The keywords that can be supplied are these.

        Compressed---(Boolean)
        Width---(LONG)
        Height---(LONG)
        Depth---(LONG)
        Mipmap_Count---(LONG)
        DXT_Format_ID---(4BYTE STRING)*
        Channel_Count---(LONG 0-4)
        BPP---(LONG)
        R_Mask---(LONG)
        G_Mask---(LONG)
        B_Mask---(LONG)
        A_Mask---(LONG)
    '''


    if kwargs is not None:
        Header_Buffer = array("B",[0]*128)

        for i in range(len(DXT_Var_Offsets)):
            #fill in any missing variables
            if DXT_Header_Var_Names[i] not in kwargs:
                kwargs[DXT_Header_Var_Names[i]] = DXT_Var_Defaults[i]
        
        if not "Compressed" in kwargs:
            print("ERROR: MUST SPECIFY WHETHER OR NOT TEXTURE IS COMPRESSED.\n" )
            return(False)
        
            
        elif isinstance(kwargs["DXT_Format_ID"], str):
            kwargs["DXT_Format_ID"] = kwargs["DXT_Format_ID"][0:4].encode('Latin-1')


        if kwargs["Compressed"]:
            kwargs["Channel_Count"] = 0
        else:
            if (not "Channel_Count" in kwargs  or (not isinstance(kwargs["Channel_Count"], int)) or
                (kwargs["Channel_Count"] > 4 or kwargs["Channel_Count"] < 0)):
                print("ERROR: CHANNEL COUNT OF EITHER 1, 2, 3, OR 4 REQUIRED FOR UNCOMPRESSED TEXTURES.\n")
                return(False)

            """I could worry about checking the validity of the channel masks here, but what's the point?"""


        #figure out if the texture is 2D, a cubemap, or volumetric
        if "Texture_Type" in kwargs and (kwargs["Texture_Type"].upper() in DXT_Texture_Type_Map):
            kwargs["Texture_Type"] = DXT_Texture_Type_Map[kwargs["Texture_Type"].upper()]
        else:
            #default to a 2d texture
            kwargs["Texture_Type"] = 0


        #set the mipmap flag
        if kwargs["Mipmap_Count"] > 0:
            kwargs["FLAGS"] = (kwargs["FLAGS"] & 8917007) + 131072
            kwargs["Caps_1"] = (kwargs["Caps_1"] & 4104) + 4194304
            
        #set the cubemap flags
        if kwargs["Texture_Type"] == 2:
            kwargs["Caps_2"] = 65024
            
        #set the volumetric texture flag
        if kwargs["Depth"] > 1:
            kwargs["FLAGS"] = (kwargs["FLAGS"] & 659471) + 8388608
            kwargs["Caps_2"] = 2097152
            
        #set the complex surface flag
        if kwargs["Texture_Type"] > 0 or kwargs["Mipmap_Count"] > 0:
            kwargs["Caps_1"] = (kwargs["Caps_1"] & 4198400) + 8

            
        #set the pixel format flags
        if kwargs["Compressed"]:
            kwargs["Pixel_Format_Flags"] = 4
            kwargs["FLAGS"] = (kwargs["FLAGS"] & 4294443007) + 524288
        else:
            if kwargs["Channel_Count"] == 1:
                if kwargs["Format"] == BC.FORMAT_A8:
                    kwargs["Pixel_Format_Flags"] = 2
                else:
                    kwargs["Pixel_Format_Flags"] = 131072
            elif kwargs["Channel_Count"] == 2:
                kwargs["Pixel_Format_Flags"] = 131073
            elif kwargs["Channel_Count"] == 3:
                if kwargs["Format"] == BC.FORMAT_Y8U8V8:
                    kwargs["Pixel_Format_Flags"] = 512
                else:
                    kwargs["Pixel_Format_Flags"] = 64
            elif kwargs["Channel_Count"] == 4:
                if kwargs["Format"] == BC.FORMAT_U8V8:
                    kwargs["Pixel_Format_Flags"] = 524288
                else:
                    kwargs["Pixel_Format_Flags"] = 65
                
            kwargs["Pitch_or_Linear_Size"] = kwargs["Width"]*(kwargs["BPP"]//8)*kwargs["Channel_Count"]

        #set the required flags
        kwargs["FLAGS"] = (kwargs["FLAGS"] & 9043976) + 4103
        kwargs["Caps_1"] = (kwargs["Caps_1"] & 4194312) + 4096

        #the mipmap count includes the largest dimension image, so it's always at least 1
        #I think it's photoshop being an idiot and not knowing how mipmaps actually work.
        kwargs["Mipmap_Count"] += 1

        for i in range(len(DXT_Var_Offsets)):
            #Write the variable to the header
            if isinstance(kwargs[DXT_Header_Var_Names[i]], bytes):
                for b in range(len(kwargs[DXT_Header_Var_Names[i]])):
                    pack_into('B', Header_Buffer, DXT_Var_Offsets[i]+b, kwargs[DXT_Header_Var_Names[i]][b] )
            else:
                pack_into('<I', Header_Buffer, DXT_Var_Offsets[i], kwargs[DXT_Header_Var_Names[i]])
            
        DDS_File.write(Header_Buffer)
        #return the offset that we are currently at
        return(128)
    else:
        print("CANNOT CONSTRUCT DXT HEADER WITHOUT PROPER INFORMATION")
        return(False)
