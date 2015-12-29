from array import array
from os.path import splitext

from ..Field_Types import *
from ..Defs.Objs.bitm import *

from ReclaimerLib.resources.Bitmap_Module import Bitmap_Convertor as BC
from ReclaimerLib.resources.P8_Palette import *



"""##################"""
### CHANNEL MAPPINGS ###
"""##################"""


"""These channel mappings are for swapping MULTIPURPOSE channels from
pc to xbox format and vice versa from 4 channel source to 4 channel target"""
#                      (A, R, G, B)
PC_ARGB_TO_XBOX_ARGB = (1, 3, 2, 0)
XBOX_ARGB_TO_PC_ARGB = (3, 0, 2, 1)

Format_Name_List = { -1:None,
                     0:"A8", 1:"Y8", 2:"AY8", 3:"A8Y8",
                     4:"UNUSED1",5:"UNUSED2",
                     6:"R5G6B5", 7:"UNUSED3", 8:"A1R5G5B5", 9:"A4R4G4B4",
                     10:"X8R8G8B8", 11:"A8R8G8B8",
                     12:"UNUSED4", 13:"UNUSED5",
                     14:"DXT1", 15:"DXT3", 16:"DXT5", 17:"P8-BUMP"}

I_Format_Name_List = { "A8":0, "Y8":1, "AY8":2, "A8Y8":3,
                       "UNUSED1":4, "UNUSED2":5,
                       "R5G6B5":6, "UNUSED3":7, "A1R5G5B5":8, "A4R4G4B4":9,
                       "X8R8G8B8":10, "A8R8G8B8":11,
                       "UNUSED4":12, "UNUSED5":13,
                       "DXT1":14, "DXT3":15, "DXT5":16, "P8-BUMP":17}

Type_Name_List = { 0:"2D", 1:"3D", 2:"CUBE" }

global Tex_Infos
Tex_Infos = []


#load the palette for p-8 bump maps
P8_Palette = Load_Palette()

BC.FORMAT_P8 = "P8-BUMP"

"""ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
BC.Define_Format(Format_ID=BC.FORMAT_P8,
                 Raw_Format=True,
                 Channel_Count=4,
                 Channel_Depths=(8,8,8,8),
                 Channel_Masks=(4278190080, 16711680, 65280, 255),
                 Channel_Offsets=(24,16,8,0))

'''Constants that determine which index
each of the flags are in per tag'''
DONT_REPROCESS = 0
RENAME_OLD = 1
READ_ONLY = 2
WRITE_LOG = 3
PLATFORM = 4
SWIZZLED = 5
DOWNRES = 6
MULTI_SWAP = 7
CUTOFF_BIAS = 8
P8_MODE = 9
MONO_KEEP = 10
MONO_SWAP = 11
CK_TRANS = 12
NEW_FORMAT = 13
MIP_GEN = 14
GAMMA = 15
EXTRACT_TO = 16

def Process_Bitmap_Tag(Tag):
    '''this function will return whether or not the conversion
    routine below should be run on a bitmap based on its format,
    type, etc and how they compare to the conversion variablers'''
    
    Flags = Tag.Tag_Conversion_Settings
    
    #check if the bitmap has already been processed, or
    #is a PC bitmap or if we are just creating a debug log
    if Tag.Processed_by_Reclaimer or not(Tag.Is_Xbox_Bitmap):
        Format = Tag.Bitmap_Format()

        #if all these are true we skip the tag
        if ( Flags[DOWNRES]=='0' and Flags[MULTI_SWAP] == 0 and
             Flags[NEW_FORMAT] == FORMAT_NONE and Flags[MIP_GEN]== False and
             Tag.Is_Xbox_Bitmap == Flags[PLATFORM] and
             (Flags[MONO_SWAP] == False or Format!= FORMAT_A8Y8) and
             (Tag.Swizzled() == Flags[SWIZZLED] or
              Format_Name_List[Format] in BC.DDS_FORMATS) ):
            return(False)
    return True


def Extracting_Texture(Tag):
    '''determines if a texture extraction is to take place'''
    return(Tag.Tag_Conversion_Settings[EXTRACT_TO] != " ")


def Convert_Bitmap_Tag(Tag, **kwargs):
    '''tons of possibilities here. not gonna try to name
    them. Basically this is the main conversion routine'''
    del Tex_Infos[:]

    Conversion_Flags = Tag.Tag_Conversion_Settings

    Root_Window = kwargs.get("Root_Window",None)
    New_Bitmap = kwargs.get("New_Bitmap",None)
    Tag_Path = kwargs.get("Tag_Path",Tag.Tag_Path)
    Conversion_Report = kwargs.get("Conversion_Report",{})
    Reprocess = kwargs.get("Reprocess", False)
    
    '''if ANY of the bitmaps does not have a power of 2 dimensions height/width/depth
    then we need to break out of this since we can't work with it properly'''
    for i in range(Tag.Bitmap_Count()):
        if not(Tag.Is_Power_of_2_Bitmap(i)):
            Conversion_Report[Tag_Path] = False
            return False
    

    """GET THE FLAGS FOR THE CONVERSION SETTINGS
    THAT DON'T DEPEND ON BITMAP FORMAT OR TYPE"""
    Save_As_Xbox = Conversion_Flags[PLATFORM]
    Swizzler_Mode = Conversion_Flags[SWIZZLED]
    Downres_Amount = int(Conversion_Flags[DOWNRES])
    Alpha_Cutoff_Bias = int(Conversion_Flags[CUTOFF_BIAS])
    P8_Mode = Conversion_Flags[P8_MODE]
    Channel_to_Keep = Conversion_Flags[MONO_KEEP]
    Color_Key_Transparency = Conversion_Flags[CK_TRANS]
    New_Format = Format_Name_List[Conversion_Flags[NEW_FORMAT]]
    Multi_Swap = Conversion_Flags[MULTI_SWAP]
    Mono_Swap = Conversion_Flags[MONO_SWAP]
    Gamma = Conversion_Flags[GAMMA]
    Generate_Mipmaps = Conversion_Flags[MIP_GEN]
    Export_Format = Conversion_Flags[EXTRACT_TO]

    Processing_Bitmap = Process_Bitmap_Tag(Tag)

    """CREATE THE BITMAP CONVERTER MODULE"""
    BM = BC.Bitmap_Manipulator()

    '''BEFORE WE TRY TO LOAD THE PIXEL DATA WE NEED TO
    MAKE SURE THE DESCRIPTION OF EACH BITMAP IS WORKABLE'''
    Bad_Bitmaps = Fix_Mipmap_Counts(Tag)

    if len(Bad_Bitmaps) > 0:
        print("WARNING: BAD BITMAP BLOCK INFORMATION ENCOUNTERED WHILE PROCESSING THIS TAG:\n",
              Tag_Path, "\n", "THE INDEXES THAT WERE BAD ARE AS FOLLOWS:", Bad_Bitmaps,
              "\nCannot process bitmap until you manually fix this.\n")
        Load_Status = False
    else:
        '''CONVERT THE RAW PIXEL DATA INTO ORGANIZED ARRAYS OF PIXELS'''
        Load_Status = Parse_Bitmap_Blocks(Tag)

    #If an error was encountered during the load attempt or the conversion was cancelled we quit
    if Root_Window and (not Load_Status or Root_Window.Conversion_Cancelled):
        Conversion_Report[Tag_Path] = False
        return False
        

    """LOOP THROUGH ALL THE BITMAPS, FIGURE OUT HOW THEY'RE BEING CONVERTED AND CONVERT THEM"""
    for i in range(Tag.Bitmap_Count()):
        Format = Format_Name_List[Tag.Bitmap_Format(i)]
        Type = Type_Name_List[Tag.Bitmap_Type(i)]
        Target_Format = New_Format

        #get the texture block to be loaded
        Tex_Block = list(Tag.Tag_Data.Data.Processed_Pixel_Data.Data[i])
        Tex_Info = Tex_Infos[i]

        """MAKE SOME CHECKS TO FIGURE OUT WHICH FORMAT WE ARE
        REALLY CONVERTING TO (IT'S NOT STRAIGHTFORWARD)"""
        if Target_Format == BC.FORMAT_P8:
            #since this button is shared between p-8 and 32 bit we make another check
            #also make sure this ISN'T a cubemap
            if (Format in (BC.FORMAT_R5G6B5, BC.FORMAT_A1R5G5B5, BC.FORMAT_A4R4G4B4,
                          BC.FORMAT_X8R8G8B8, BC.FORMAT_A8R8G8B8) and Type != BC.TYPE_CUBEMAP):
                Target_Format = BC.FORMAT_P8
            elif Format == BC.FORMAT_Y8:
                Target_Format = BC.FORMAT_X8R8G8B8
            else: Target_Format = BC.FORMAT_A8R8G8B8
                
        elif Target_Format not in BC.VALID_FORMATS:
            Target_Format = Format
        else:
            if Target_Format in BC.DDS_FORMATS and Type == "3D":
                Target_Format = Format
                print("CANNOT CONVERT 3D TEXTURES TO DXT FORMAT.")
                
            if not(Channel_to_Keep) and Target_Format == BC.FORMAT_A8:
                Target_Format = BC.FORMAT_Y8
                
            """ SINCE THESE THREE FORMATS CAN BE EASILY INTERCHANGED JUST
            BY CHANGING THE FORMAT IDENTIFIER, THAT'S WHAT WE'LL DO"""
            if (Format in (BC.FORMAT_A8, BC.FORMAT_Y8, BC.FORMAT_AY8) and
                Target_Format in (BC.FORMAT_A8, BC.FORMAT_Y8, BC.FORMAT_AY8)):
                Tex_Info["Format"] = Format = Target_Format


        """CHOOSE WHICH CHANNEL MAPPINGS TO USE AND DO EXTRA TARGET FORMAT CHECKS"""
        Channel_Mapping, Channel_Merge_Mapping, Target_Format = Get_Channel_Mappings(Format, Mono_Swap,
                                                                                     Target_Format,
                                                                                     Multi_Swap,
                                                                                     Channel_to_Keep)
        Palette_Picker = None
        Palettize = False
        
        """IF WE ARE CONVERTING TO P8 THIS IS WHERE WE SELECT THE SPECIFIC SETTINGS"""
        if Format == BC.FORMAT_P8:
            Palette_Picker = P8_Palette.ARGB_Array_to_P8_Array_Auto
            Palettize = True
        else:
            if Target_Format == BC.FORMAT_P8:
                Palettize = True
                
                if BC.FORMAT_CHANNEL_COUNTS[Format] == 4:
                    if Color_Key_Transparency and Format not in (BC.FORMAT_X8R8G8B8, BC.FORMAT_R5G6B5):
                        #auto-bias
                        if P8_Mode == 0:
                            Palette_Picker = P8_Palette.ARGB_Array_to_P8_Array_Auto_Alpha
                        else:#average-bias
                            Palette_Picker = P8_Palette.ARGB_Array_to_P8_Array_Average_Alpha
                    else:
                        #auto-bias
                        if P8_Mode == 0:
                            Palette_Picker = P8_Palette.ARGB_Array_to_P8_Array_Auto
                        else:#average-bias
                            Palette_Picker = P8_Palette.ARGB_Array_to_P8_Array_Average

        #we want to preserve the color key transparency of
        #the original image if converting to the same format
        if Format == Target_Format and Target_Format in (BC.FORMAT_P8, BC.FORMAT_DXT1):
            Color_Key_Transparency = True

        """LOAD THE TEXTURE INTO THE BITMAP CONVERTER"""
        BM.Load_New_Texture(Texture_Block = Tex_Block,
                            Texture_Info = Tex_Info)
        
        #build the initial conversion settings list from the above settings
        Conv_Settings = {"Swizzler_Mode":Swizzler_Mode,
                         "One_Bit_Bias":Alpha_Cutoff_Bias,
                         "Downres_Amount":Downres_Amount,
                         "Color_Key_Transparency":Color_Key_Transparency,
                         "Gamma":Gamma, "Palettize":Palettize,
                         "Generate_Mipmaps":Generate_Mipmaps}


        #add the variable settings into the conversion settings list
        Conv_Settings["Target_Format"] = Target_Format
        if Channel_Mapping is not None:
            Conv_Settings["Channel_Mapping"] = Channel_Mapping
        if Channel_Merge_Mapping is not None:
            Conv_Settings["Channel_Merge_Mapping"] = Channel_Merge_Mapping
        if Palette_Picker is not None:
            Conv_Settings["Palette_Picker"] = Palette_Picker

        if Conv_Settings["Target_Format"] != BC.FORMAT_P8:
            Conv_Settings["Palettize"] = False

            
        """LOAD THE CONVERSION SETTINGS INTO THE BITMAP CONVERTER"""
        BM.Load_New_Conversion_Settings(**Conv_Settings)

        """RUN THE CONVERSION ROUTINE ON THE BITMAP CONVERTOR"""
        if Processing_Bitmap:
            Status = BM.Convert_Texture()
        else:
            Status = True
        

        if Export_Format != " ":
            Path = BM.Filepath
            if Tag.Bitmap_Count() > 1:
                Path += ("_"+str(i))
            BM.Save_to_File(Output_Path = Path, Ext = Export_Format)
                

        """IF THE CONVERSION WAS SUCCESSFUL WE UPDATE THE TAG'S DATA TO THE NEW FORMAT AND
        SWIZZLE MODE.   IF WE WERE ONLY EXTRACTING THE TEXTURE WE DON'T RESAVE THE TAG"""
        if Status and (Processing_Bitmap or Reprocess):
            Texture_Root = Tag.Tag_Data.Data.Processed_Pixel_Data.Data[i]
            
            if len(BM.Texture_Block) and isinstance(BM.Texture_Block[0], array):
                #change the type of data for the bitmap pixels to ANY array block.
                #All Py_Array Field_Types use the same writer, thus any Py_Array Field_Type will work
                Texture_Root.Set_Desc('TYPE', UInt8_Array, 'SUB_STRUCT')

            #set the data block to the newly converted one
            Texture_Root.Read(BM.Texture_Block)
            #set the flag showing that the bitmap is either swizzled or not swizzled
            Tag.Swizzled(BM.Swizzled, i)

            #change the bitmap format to the new format
            Tag.Bitmap_Format(i, I_Format_Name_List[Target_Format])
        else:
            if not Extracting_Texture(Tag):
                print("Error occurred while attempting to convert the tag:")
                print(Tag_Path+"\n")
                Conversion_Report[Tag_Path] = False
                return False

    if Processing_Bitmap or Reprocess:
        """RECALCULATE THE BITMAP HEADER AND FOOTER DATA AFTER POSSIBLY CHANGING IT ABOVE"""
        Bitmap_Sanitize(Tag)
        
        #SET THE TAG'S CHARACTERISTICS TO XBOX OR PC FORMAT
        Tag.Set_Platform(Save_As_Xbox)

        #SET THE "PROCESSED BY RECLAIMER" FLAG
        Tag.Processed_by_Reclaimer(True)
        
        #IF THE FORMAT IS P8 OR PLATFORM IS XBOX WE NEED TO ADD PADDING
        Add_Bitmap_Padding(Tag, Save_As_Xbox)
        
        """FINISH BY RESAVING THE TAG"""
        Save_Status = Tag.Write()
        Conversion_Report[Tag_Path] = Save_Status
        return Save_Status
    else:
        if Export_Format == " ":
            Conversion_Report[Tag_Path] = False
            return False
        else:
            Conversion_Report[Tag_Path] = None
            return None



def Parse_Bitmap_Blocks(Tag):
    '''converts the raw pixel data into arrays of pixel
    data and replaces the raw data in the tag with them'''
    
    Pixel_Data = Tag.Tag_Data.Data.Processed_Pixel_Data
    Raw_Bitmap_Data = Pixel_Data.Data

    Tags_Dir = Tag.Library.Tags_Dir
    Data_Dir = Tag.Library.Data_Dir
    
    #this is the block that will hold all of the bitmap blocks
    Root_Texture_Block = List_Block(Tag.Definition.Structures['Pixel_Root_Desc'])
    
    #Read the pixel data blocks for each bitmap
    for i in range(Tag.Bitmap_Count()):
        
        #since we need this information to read the bitmap we extract it
        Max_Width, Max_Height, Max_Depth, = Tag.Bitmap_Width_Height_Depth(i)
        Type = Tag.Bitmap_Type(i)
        Format = Format_Name_List[Tag.Bitmap_Format(i)]
        Mipmap_Count = Tag.Bitmap_Mipmaps_Count(i) + 1
        Sub_Bitmap_Count = BC.SUB_BITMAP_COUNTS[Type_Name_List[Type]]

        #Get the offset of the pixel data for this bitmap within the raw pixel data
        Offset = Tag.Bitmap_Data_Offset(i)

        #this texture info is used in manipulating the texture data
        Tex_Infos.append({"Width":Max_Width, "Height":Max_Height, "Depth":Max_Depth,
                          "Format":Format, "Mipmap_Count":(Mipmap_Count-1),
                          "Sub_Bitmap_Count":Sub_Bitmap_Count, "Swizzled":Tag.Swizzled(),
                          "Texture_Type":Type_Name_List[Type],
                          "Filepath":splitext(Tag.Tag_Path.replace(Tags_Dir,Data_Dir))[0]})
        
        """IF THE TEXTURE IS IN P-8 FORMAT THEN WE NEED TO
        PROVIDE THE PALETTE AND SOME INFORMATION ABOUT IT"""
        if Format == BC.FORMAT_P8:
            Tex_Infos[-1]["Palette"] = [P8_Palette.P8_Palette_32Bit[0]]*Mipmap_Count
            Tex_Infos[-1]["Palette_Packed"] = False
            Tex_Infos[-1]["Indexing_Size"] = 8
        
        '''this is the block that will hold each mipmap,
        texture slice, and cube face of the bitmap'''
        Root_Texture_Block.append()
        Tex_Block = Root_Texture_Block[-1]
        
        if Tag.Is_Xbox_Bitmap:
            for Sub_Bitmap_Index in range(Sub_Bitmap_Count):
                for Mipmap in range(Mipmap_Count):
                    Width, Height, Depth = BC.Get_Mipmap_Dimensions(Max_Width, Max_Height,
                                                                    Max_Depth, Mipmap, Format)
                    if Format == BC.FORMAT_P8:
                        Pixel_Count = Width*Height
                        Tex_Block.append(Raw_Bitmap_Data[Offset:Offset+Pixel_Count])
                        Offset += Pixel_Count
                    else:
                        Offset = BC.Bitmap_IO.Bitmap_Bytes_to_Array(Raw_Bitmap_Data, Offset,
                                                                    Tex_Block, Format,
                                                                    Width, Height, Depth)
                
                #now we calculate and skip the amount of padding
                #that we need to in order to get to the next texture
                Bitmap_Padding, Sub_Bitmap_Padding = Calc_Padding_Size(Tag, i)
                Offset += Sub_Bitmap_Padding
                
            Offset += Bitmap_Padding
            
        else:
            for Mipmap in range(Mipmap_Count):
                Width, Height, Depth = BC.Get_Mipmap_Dimensions(Max_Width, Max_Height,
                                                                Max_Depth, Mipmap, Format)           
                #Loop for each cubemap face(or only once if not a cubemap)
                for Sub_Bitmap_Index in range(Sub_Bitmap_Count):
                    if Format == BC.FORMAT_P8:
                        Pixel_Count = Width*Height
                        Tex_Block.append(Raw_Bitmap_Data[Offset:Offset+Pixel_Count])
                        Offset += Pixel_Count
                    else:
                        Offset = BC.Bitmap_IO.Bitmap_Bytes_to_Array(Raw_Bitmap_Data, Offset,
                                                                    Tex_Block, Format,
                                                                    Width, Height, Depth)
    Pixel_Data.Set_Desc('CHILD', Root_Texture_Block.DESC)
    Pixel_Data.Data = Root_Texture_Block
    '''now that we've successfully built the bitmap
    blocks from the raw data we replace the raw data'''
    if Tag.Is_Xbox_Bitmap:
        '''it's easier to work with bitmaps in one format so
        we'll switch the mipmaps from XBOX to PC ordering'''
        Tag.Change_Sub_Bitmap_Ordering(False)

    return True





def Fix_Mipmap_Counts(Tag):
    '''Some original xbox bitmaps have fudged up mipmap counts and cause issues.
    This function will scan through all a bitmap's bitmaps and check that they
    fit within their calculated pixel data bounds. This is done by checking if
    a bitmap's calculated size is both within the side of the total pixel data
    and less than the next bitmap's pixel data start'''
    
    Bad_Bitmap_Index_List = []
    
    for i in range(Tag.Bitmap_Count()):
        
        #if this is the last bitmap
        if i == (Tag.Bitmap_Count()-1):
            #this is how many bytes of texture data there is total
            Max_Data_Size = Tag.Pixel_Data_Bytes_Size()
        else:
            #this is the start of the next bitmap's pixel data
            Max_Data_Size = Tag.Bitmap_Data_Offset(i+1)

        Check = True
        
        while Check:
            Mipmap_Count = Tag.Bitmap_Mipmaps_Count(i)
            Current_Bytes_Size = Calc_Bitmap_Size(Tag, i)
            Current_Bytes_Size += Tag.Bitmap_Data_Offset(i)

            if Current_Bytes_Size > Max_Data_Size:
                #the mipmap count is zero and the bitmap still will
                #not fit within the space provided. Something's wrong
                if Mipmap_Count == 0:
                    Bad_Bitmap_Index_List.append(i)
                    Check = False
                Tag.Bitmap_Mipmaps_Count(i, Mipmap_Count - 1)
            else:
                Check = False
            
    return Bad_Bitmap_Index_List




def Add_Bitmap_Padding(Tag, Save_As_Xbox):
    '''Given a tag, this function will create and apply padding to
    each of the bitmaps in it to make it XBOX compatible. This function
    will also add the number of bytes of padding to the internal offsets'''

    """The offset of each bitmap's pixel data needs to be increased by
    the padding of all the bitmaps before it. This variable will be
    used for knowing the total amount of padding before each bitmap.

    DO NOT RUN IF A BITMAP ALREADY HAS PADDING."""
    Cumulative_Pixel_Data = 0

    for i in range(Tag.Bitmap_Count()):
        Sub_Bitmap_Count = 1
        if Tag.Bitmap_Type(i) == TYPE_CUBEMAP:
            Sub_Bitmap_Count = 6
            
        Pixel_Data_Block = Tag.Tag_Data.Data.Processed_Pixel_Data.Data[i]

        """BECAUSE THESE OFFSETS ARE THE BEGINNING OF THE PIXEL
        DATA WE ADD THE NUMBER OF BYTES OF PIXEL DATA BEFORE
        WE CALCULATE THE NUMBER OF BYTES OF THIS ONE"""
        #apply the offset to the tag
        Tag.Bitmap_Data_Offset(i, Cumulative_Pixel_Data)

        """ONLY ADD PADDING IF THE BITMAP IS P8 FORMAT OR GOING ON XBOX"""
        if Save_As_Xbox or Tag.Bitmap_Format(i) == BC.FORMAT_P8:
            #calculate how much padding to add to the xbox bitmaps
            Bitmap_Padding, Cubemap_Padding = Calc_Padding_Size(Tag, i)
            
            #add the number of bytes of padding to the total
            Cumulative_Pixel_Data += Bitmap_Padding + (Cubemap_Padding*Sub_Bitmap_Count)

            #if this bitmap has padding on each of the sub-bitmaps
            if Cubemap_Padding:
                Mipmap_Count = Tag.Bitmap_Mipmaps_Count(i) + 1
                for j in range(6):
                    if isinstance(Pixel_Data_Block[0], array):
                        Pixel_Data_Block.insert(j*(Mipmap_Count + 1) + Mipmap_Count,
                                                array('B', [0]*Cubemap_Padding))
                    elif isinstance(Pixel_Data_Block[0], bytearray):
                        Pixel_Data_Block.insert(j*(Mipmap_Count + 1) + Mipmap_Count,
                                                bytearray(Cubemap_Padding))
                    
            #add the main padding to the end of the bitmap block
            if isinstance(Pixel_Data_Block[0], array):
                Pixel_Data_Block.append(array('B', [0]*Bitmap_Padding))
            elif isinstance(Pixel_Data_Block[0], bytearray):
                Pixel_Data_Block.append(bytearray(Bitmap_Padding))

        #add the number of bytes this bitmap is to the
        #total bytes so far(multiple by sub-bitmap count)
        Cumulative_Pixel_Data += Calc_Bitmap_Size(Tag, i)*Sub_Bitmap_Count

    #update the total number of bytes of pixel data
    #in the tag by all the padding that was added
    Tag.Pixel_Data_Bytes_Size(Cumulative_Pixel_Data)


def Calc_Bitmap_Size(Tag, Bitmap_Index):
    '''Given a bitmap index and a tag, this function
    will calculate how many bytes the data takes up.
    THIS FUNCTION WILL NOT TAKE INTO ACCOUNT THE NUMBER OF SUB-BITMAPS'''

    #since we need this information to read the bitmap we extract it
    Max_Width, Max_Height, Max_Depth, = Tag.Bitmap_Width_Height_Depth(Bitmap_Index)
    Format = Format_Name_List[Tag.Bitmap_Format(Bitmap_Index)]

    #this is used to hold how many pixels in total all this bitmaps mipmaps add up to
    Pixels_Count = 0
    
    for Mipmap in range(Tag.Bitmap_Mipmaps_Count(Bitmap_Index) + 1):
        Width, Height, Depth = BC.Get_Mipmap_Dimensions(Max_Width, Max_Height,
                                                     Max_Depth, Mipmap, Format)
        Pixels_Count += Width * Height * Depth

    Bytes_Count = Pixels_Count
    
    #based on the format, each pixel takes up a different amount of bytes
    if Format != BC.FORMAT_P8:
        Bytes_Count = (Pixels_Count * BC.BITS_PER_PIXEL[Format]) // 8

    return Bytes_Count
            


def Calc_Padding_Size(Tag, Bitmap_Index):
    '''Calculates how many bytes of padding need to be added
    to a bitmap to properly align it in the texture cache'''

    #first we need to know how many bytes the bitmap data takes up
    Bytes_Count = Calc_Bitmap_Size(Tag, Bitmap_Index)
    Cubemap_Padding = 0

    #if there are sub-bitmaps we calculate the amount of padding for them
    if Tag.Bitmap_Type(Bitmap_Index) == TYPE_CUBEMAP:
        Cubemap_Padding = ((CUBEMAP_PADDING -
                            (Bytes_Count%CUBEMAP_PADDING))
                           %CUBEMAP_PADDING)
        Bytes_Count = (Bytes_Count + Cubemap_Padding) * 6

    Bitmap_Padding = (BITMAP_PADDING -
                      (Bytes_Count%BITMAP_PADDING))%BITMAP_PADDING
    
    return(Bitmap_Padding, Cubemap_Padding)


def Bitmap_Sanitize(Tag):
    '''after we've edited with the bitmap in whatever ways we did this will
    #tie up all the loose ends and recalculate all the offsets and stuff'''
    
    #Prune the original TIFF data from the tag
    Tag.Tag_Data.Data.Compressed_Color_Plate_Data.Data = bytearray()

    #Read the pixel data blocks for each bitmap
    for i in range(Tag.Bitmap_Count()):
        Format = Format_Name_List[Tag.Bitmap_Format(i)]
        Flags = Tag.Bitmap_Flags(i)
        Old_W, Old_H, _ = Tag.Bitmap_Width_Height_Depth(i)
        
        Reg_Point_X, Reg_Point_Y = Tag.Registration_Point_XY(i)
        TexInfo = Tex_Infos[i]
        
        #set the flags to the new value
        Flags.Palletized = (Format == BC.FORMAT_P8)
        Flags.Compressed = (Format in BC.COMPRESSED_FORMATS)
        
        Tag.Bitmap_Width_Height_Depth(i, (TexInfo["Width"],
                                          TexInfo["Height"],
                                          TexInfo["Depth"]))
        Tag.Bitmap_Mipmaps_Count(i, TexInfo["Mipmap_Count"])
        Tag.Registration_Point_XY(i, (Reg_Point_X//(Old_W//TexInfo["Width"]),
                                      Reg_Point_Y//(Old_H//TexInfo["Height"])))



def Get_Channel_Mappings(Format, Mono_Swap, Target_Format,
                         Multi_Swap, Channel_to_Keep):
    """Goes through a ton of checks to figure out which channel
    mapping to use for converting(and returns it). Also checks a
    few exception cases where converting to that format would
    be bad and instead resets the target format to the source format"""
    
    Channel_Count = BC.FORMAT_CHANNEL_COUNTS[Format]
    Target_Channel_Count = BC.FORMAT_CHANNEL_COUNTS[Target_Format]
    Channel_Mapping = None
    Channel_Merge_Mapping = None
    if Channel_Count == 4:
        if Target_Channel_Count == 4:
            """THIS TAKES CARE OF ALL THE MULTIPURPOSE CHANNEL SWAPPING"""
            if Multi_Swap == 1:
                #SWAP CHANNELS FROM PC TO XBOX
                Channel_Mapping = PC_ARGB_TO_XBOX_ARGB
                        
            elif Multi_Swap == 2:
                #SWAP CHANNELS FROM XBOX TO PC
                Channel_Mapping = XBOX_ARGB_TO_PC_ARGB
        
        else:
            """THIS TAKES CARE OF CONVERTING FROM A
            4 CHANNEL FORMAT TO MONOCHROME"""
            if Target_Format in (BC.FORMAT_A8, BC.FORMAT_Y8,
                                 BC.FORMAT_AY8, BC.FORMAT_P8):
                if Channel_to_Keep:
                    #keep the alpha channel
                    Channel_Mapping = BC.Anything_to_A8
                    if Format == BC.FORMAT_P8:
                        Channel_Merge_Mapping = BC.M_ARGB_to_A8
                else:
                    #keep the intensity channel
                    Channel_Merge_Mapping = BC.M_ARGB_to_Y8
                    
            elif Target_Format == BC.FORMAT_A8Y8:
                if Mono_Swap:
                    Channel_Merge_Mapping = BC.M_ARGB_to_Y8A8
                else:
                    Channel_Merge_Mapping = BC.M_ARGB_to_A8Y8
            
    elif Channel_Count == 2:
        """THIS TAKES CARE OF CONVERTING FROM A
        2 CHANNEL FORMAT TO OTHER FORMATS"""

        if Format == BC.FORMAT_A8Y8:
            if Mono_Swap:
                if Target_Format == BC.FORMAT_A8Y8:
                    Channel_Mapping = BC.A8Y8_to_Y8A8
                    
                elif Target_Channel_Count == 4:
                    Channel_Mapping = BC.Y8A8_to_ARGB
                
            elif Target_Channel_Count == 4:
                Channel_Mapping = BC.A8Y8_to_ARGB
                
            elif Target_Format in (BC.FORMAT_A8, BC.FORMAT_Y8, BC.FORMAT_AY8):
                if Channel_to_Keep:
                    #keep the alpha channel
                    Channel_Mapping = BC.Anything_to_A8
                else:
                    #keep the intensity channel
                    Channel_Mapping = BC.A8Y8_to_Y8
    
    elif Channel_Count == 1:
        """THIS TAKES CARE OF CONVERTING FROM A
        1 CHANNEL FORMAT TO OTHER FORMATS"""
        if Target_Channel_Count == 4:
            if Format == BC.FORMAT_A8:
                Channel_Mapping = BC.A8_to_ARGB
                    
            elif Format == BC.FORMAT_Y8:
                Channel_Mapping = BC.Y8_to_ARGB
                    
            elif Format == BC.FORMAT_AY8:
                Channel_Mapping = BC.AY8_to_ARGB
                
        elif Target_Channel_Count == 2:
            if Format == BC.FORMAT_A8:
                Channel_Mapping = BC.A8_to_A8Y8
                
            elif Format == BC.FORMAT_Y8:
                Channel_Mapping = BC.Y8_to_A8Y8
                
            elif Format == BC.FORMAT_AY8:
                Channel_Mapping = BC.AY8_to_A8Y8
                
    return(Channel_Mapping, Channel_Merge_Mapping, Target_Format)
