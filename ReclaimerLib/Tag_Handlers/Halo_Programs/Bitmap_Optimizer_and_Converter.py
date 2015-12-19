from time import sleep, time
import threading
import gc

from os.path import getsize
from .GUI.Bitmap_Converter_Windows import *
from .HEK_Tag_Library import *
from ...Tag_Operations.Halo_Operations.bitm import *


class Bitmap_Converter_Class(HEK_Tag_Library):

    Log_Filename = "Bitmap_Converter.log"
    
    def __init__(self, **kwargs):
        HEK_Tag_Library.__init__(self, Valid_Tag_IDs="bitm", **kwargs)
        
        self.Default_Conversion_Flags["bitm"] = self.Make_Default_Conversion_Flags()
        self.root_window = Bitmap_Converter_Main_Window(self)

        #Create and start the tag scanning and editing thread
        self.Bitmap_Conversion_Main_Thread = threading.Thread(target=self._Bitmap_Conversion_Main)
        self.Bitmap_Conversion_Main_Thread.daemon = True
        self.Bitmap_Conversion_Main_Thread.start()
        
        #loop the main window
        self.root_window.mainloop()

        
    #the main loop for continuous function handeling
    #add all continuous, non-self-looping, periodic functions here
    def _Main_Loop(self):
        while not hasattr(self, "root_window"):
            pass
        
        while not self.Close_Program:
            #we don't want it to run too often or it'll be laggy
            sleep(self.Main_Delay)
            
            self.root_window.Total_Bitmaps = len(self.Tags["bitm"]) - self.root_window.Bad_Bitmaps
            
            #If the program is being told to close then close
            if self.Close_Program:
                raise SystemExit(0)

    def _Bitmap_Conversion_Main(self):
        root_window = self.root_window
        while True:
            #we don't want it to run too often or it'll be laggy
            sleep(self.Main_Delay)

            #if the tags havent been loaded and we are telling the program to continue with conversion
            if not(root_window.Tags_Loaded) and root_window.Proceed_with_Conversion:
                #reset the status variables
                root_window.Total_Pixel_Data_to_Process = root_window.Remaining_Pixel_Data_to_Process = 0
                root_window.Bitmaps_Found_2D = root_window.Bitmaps_Found_3D = root_window.Cubemaps_Found = 0
                root_window.Elapsed_Time = root_window.Estimated_Time_Remaining = 0.0
                root_window.Total_Bitmaps = root_window.Remaining_Bitmaps = root_window.Bad_Bitmaps = 0
                root_window.Scan_Start_Time = time()

                if self.Index_Tags():
                    root_window.Tags_Indexed = True

                    self.Load_Tags()
                    
                    root_window.Tags_Loaded = True
                    Collection = self.Tags['bitm']
                    Def_Flags = self.Default_Conversion_Flags['bitm']

                    #we need to build the list of conversion flags for each tag.
                    for Tag_Path in Collection:
                        Collection[Tag_Path].Tag_Conversion_Settings = list(Def_Flags)
                        
                    self.Initialize_Window_Variables()
                else:
                    self.Current_Tag = "No tags found in selected directory."
                    root_window.Bitmap_Converter_Finish_Conversion()
                    
                
            elif (root_window.Tags_Loaded and root_window.Proceed_with_Conversion):
                #reset the status variables
                root_window.Elapsed_Time = 0.0
                root_window.Estimated_Time_Remaining = 0.0
                root_window.Scan_Start_Time = time()
                root_window.Remaining_Pixel_Data_to_Process = root_window.Total_Pixel_Data_to_Process
                root_window.Remaining_Bitmaps = root_window.Total_Bitmaps
                
                #are we just scanning the folder or are we doing shiz
                if (self.Default_Conversion_Flags["bitm"][READ_ONLY]):
                    #used below for writing the results of the scan
                    Debug_Log_String = self.Make_Log_of_All_Bitmaps()
                    self.Current_Tag = "Detailed log of all bitmaps created successfully."
                else:
                    """SPLIT OFF INTO THE MAIN PROCESSING ROUTINE"""
                    Debug_Log_String = self.Process_Bitmap_Tags()
                
                #to keep from bloating the RAM, we delete all loaded bitmap tags
                for Tag_Path in tuple(self.Tags['bitm']):
                    del self.Tags['bitm'][Tag_Path]
                gc.collect()

                #since we are done with the conversion we write the debug log and change the window variables
                if not root_window.Conversion_Cancelled:
                    if self.Default_Conversion_Flags["bitm"][WRITE_LOG] and not self.Debug >= 1:
                        self.Make_Log_File(Debug_Log_String) #save the debug log to a file
                    else:
                        #if we are debugging we don't want to clutter the folder with lots of logs, so we just print it
                        print(Debug_Log_String)

                    root_window.Bitmap_Converter_Finish_Conversion()
            else:
                pass


    #run the list update function on the main thread
    def Generate_Initial_Tag_List_From_Empty(self):
        self.root_window.tag_list_window.Sort_Displayed_Tags_by(0)



    def Make_Default_Conversion_Flags(self):
        '''
        If no settings have been defined specifically for a tag then the flags below will be used
        
        the first 4 conversion flags are global conversion flags and aren't assigned on a per-tag basis

        #  DONT REPROCESS: Don't process bitmap tags if they have "Processed by Reclaimer" checked
        #  RENAME OLD: Rename old tags instead of deleting them
        #  READ ONLY: compiles a list of all bitmaps and what their types, 
        #            sizes, etc are instead of converting in any way
        #  WRITE LOG: Write Debug Log
        
        #  PLATFORM: Platform to save as(True = Xbox, False = PC)
        #  SWIZZLED: True = save as swizzled, False = save as deswizzled
        #  DOWNRES: Number of times to cut resolution in half
        #  MULTI SWAP: 0 = don't swap multipurpose channels,
        #              1 = swap for xbox,  2= swap for pc
        #  CUTOFF BIAS: when reducing a channel to 1 bit, values above
        #               this are snapped to 1 and below it are snapped to 0
        #  P8 MODE: P8-Bump Conversion Mode (True = Average Bias Mode, False = Auto Bias Mode)
        #  MONO KEEP: Channel to keep when converting to A8 or Y8 (True = Alpha, False = Intensity)
        #  MONO SWAP: Swap Alpha and Intensity (Only for A8Y8)
        #  CK TRANS: Preserve Color Key transparency  (A transparent pixel
        #                 in DXT1 has black for it's Red, Green, and Blue)
        #  MIP GEN: Generate mipmaps if a texture doesn't have them down to 1x1
        #  GAMMA: The gamma exponent to use when downressing a bitmap by merging pixels
        #  NEW FORMAT: -1=unchanged, 0=A8, 1=Y8, 2=AY8, 3=A8Y8, 6=R5G6B5 8=A1R5G5B5, 
        #               9=A4R4G4B4, 14=DXT1, 15=DXT3, 16=DXT5, 17=P8/A8R8G8B8/X8R8G8B8
        '''
        
        Bitmap_Conversion_Flags = [True, True, False, True, False, False,
                                   '0', 0, '127', False, False, False,
                                   False, FORMAT_NONE, False, 1.0, " "]

        return Bitmap_Conversion_Flags


    def Initialize_Window_Variables(self):
        root_window = self.root_window
        root_window.Bitmaps_Found_2D = root_window.Bitmaps_Found_3D = root_window.Cubemaps_Found = 0
        root_window.Total_Bitmaps = root_window.Remaining_Bitmaps = root_window.Bad_Bitmaps = 0
        
        Tags_to_Remove = []

        #for the conversion variables we want to return
        #a count on how many bitmaps are of what type
        for Tag_Path in self.Tags['bitm']:

            #only run if the bitmap contains bitmaps
            Tag = self.Tags['bitm'][Tag_Path]
            if Tag.Bitmap_Count() and Tag.Is_Power_of_2_Bitmap():
                
                Type = Tag.Bitmap_Type()
                Format = Tag.Bitmap_Format()
                if (Type == 2):
                    root_window.Cubemaps_Found += 1
                elif (Type == 1):
                    root_window.Bitmaps_Found_3D += 1
                else:
                    root_window.Bitmaps_Found_2D += 1
                
                root_window.Total_Pixel_Data_to_Process += Tag.Pixel_Data_Bytes_Size()
            else:
                if Tag.Bitmap_Count():
                    print("Non-power-of-2 dimensions bitmap found.\n", Tag.Tag_Path,"\n\n")
                else:
                    print("Bitmap with no bitmap data found.\n", Tag.Tag_Path,"\n\n")
                Tags_to_Remove.append(Tag_Path)
                root_window.Bad_Bitmaps += 1
                
            root_window.Total_Bitmaps += 1

        for Tag_Path in Tags_to_Remove:
            del self.Tags['bitm'][Tag_Path]
        del Tags_to_Remove
            
        root_window.tag_list_window.Build_Tag_Sort_Mappings()
        
        #set the status variables
        root_window.Remaining_Pixel_Data_to_Process = root_window.Total_Pixel_Data_to_Process
        root_window.Remaining_Bitmaps = len(self.Tags['bitm']) - root_window.Bad_Bitmaps
        
        self.Current_Tag = ("Tags Loaded... Please select tags in the tags list window and specify\n" +
                             'the conversion settings for them in this window.\nWhen you are finished hit "Convert"')
        
        #set up the hack to allow the tag list to be displayed instantly on loading a tagset
        root_window.after(0, self.Generate_Initial_Tag_List_From_Empty)
        root_window.Bitmap_Converter_Finish_Scanning()



    #this function is called by the _Bitmap_Conversion_Main and will loop through all the
    #tags in the collection and process them however each tag's conversion flags say to.
    def Process_Bitmap_Tags(self):
        
        if hasattr(self, "root_window"):
            root_window = self.root_window
        else:
            root_window = None
        
        #used below for debug writing
        Debug_Log_String = "Debug log for Halo Bitmap Converter\n"
        Def_Flags = self.Default_Conversion_Flags['bitm']
        Conversion_Report = {'bitm':{}}

        #loop through each tag
        for Tag_Path in sorted(self.Tags['bitm']):
            Tag = self.Tags['bitm'][Tag_Path]
            
            if root_window is not None and root_window.Conversion_Cancelled:
                break
            
            self.Current_Tag = Tag_Path

            #this may change after the below function so we get it before that happens
            Bitmap_Tag_Size = Tag.Pixel_Data_Bytes_Size()
            if Get_Will_be_Processed(Tag, Def_Flags):
                """DO THE CONVERSION NOW"""
                try:
                    Convert_Bitmap_Tag(Tag, Root_Window=root_window, Tag_Path=Tag_Path,
                                       Conversion_Report=Conversion_Report['bitm'], 
                                       Reprocess=not(Def_Flags[DONT_REPROCESS]))
                except:
                    print(format_exc())
                    Conversion_Report['bitm'][Tag_Path] = False
            else:
                Conversion_Report['bitm'][Tag_Path] = None
            root_window.Remaining_Pixel_Data_to_Process -= Bitmap_Tag_Size
            root_window.Remaining_Bitmaps -= 1


        if root_window is not None and root_window.Conversion_Cancelled:
            self.Current_Tag = "Conversion cancelled."
            
            root_window.Display_New_Text = True
            root_window.btn_start.config(text="Convert")
            root_window.Enable_Global_Settings()
            root_window.Conversion_Cancelled = False
            Debug_Log_String += "Conversion Cancelled."
        else:
            try:
                Backup = self.Default_Conversion_Flags['bitm'][RENAME_OLD]
                '''depending on the conversion settings we
                either rename or delete the original files'''
                Debug_Log_String += self.Make_Tag_Write_Log(Conversion_Report,
                                                            Backup=Backup)
            except:
                print("ERROR OCCURRED WHILE TRYING TO WRITE DEBUG LOG AND/OR RENAME TEMP FILES")
                print(format_exc())
            
            self.Current_Tag = "Finished converting tags"

        return Debug_Log_String



    #used when doing a read-only scan of a tagset to figure out what's what
    def Make_Log_of_All_Bitmaps(self):
        
        Debug_Log_String = ("CE-XBOX Bitmap Converter: Tagset scan results\n\n\nThese are the " + 
                            "bitmaps located in the tags folder organized by type and then by format.\n\n")
        
        Valid_Formats = (0,1,2,3,6,8,9,10,11,14,15,16,17)

        T_Counts = [0, 0, 0]

        F_Strs = {}
        T_Strs = ["\n\n\n2D Textures:\nCount = ",
                  "\n\n\n3D Textures:\nCount = ",
                  "\n\n\nCubemaps:\nCount = "]

        #so we can sort bitmaps by filesize we'll create a dict to hold all
        #the strings before we concate them so we can sort them later by size
        Tag_Info_Strings = {}


        #add dicts for all three types to the tag_info_strings
        for Type in (0, 1, 2):
            F_Strs[Type] = {0:"A8", 1:"Y8", 2:"AY8", 3:"A8Y8", 6:"R5G6B5", 8:"A1R5G6B5", 9:"A4R4G4B4",
                            10:"X8R8G8B8", 11:"A8R8G8B8", 14:"DXT1", 15:"DXT3", 16:"DXT5", 17:"P8-Bump"}
            
            Tag_Info_Strings[Type] = {}

            #and add the formats to each of these new dicts
            for Format in Valid_Formats:
                F_Strs[Type][Format] = "\n\n" + " "*8 + F_Strs[Type][Format] + " Format\n"
                Tag_Info_Strings[Type][Format] = {}


        #loop through each tag and create a string that details each bitmap in it
        for Tag_Path in self.Tags['bitm']:
            Tag = self.Tags['bitm'][Tag_Path]

            File_Size = (getsize(Tag.Tag_Path)-Tag.Color_Plate_Data_Bytes_Size())//1024

            Tag_Data_Strings = Tag_Info_Strings[Tag.Bitmap_Type()][Tag.Bitmap_Format()]
            
            #this is the string that holds the data pertaining to this tag
            Tag_Data_Str = ("\n" + " "*16 + Tag_Path + " "*8 + "Compiled Tag Size = " +
                            {True:"less than 1", False:str(File_Size)}[File_Size <= 0] + "KB" + "\n")

            for i in range(Tag.Bitmap_Count()):
                Tag_Data_Str += (" "*24 + "Bitmap %s --- WxHxD: %sx%sx%s --- Mipmaps: %s\n" %
                                 (i, Tag.Bitmap_Width(i), Tag.Bitmap_Height(i),
                                  Tag.Bitmap_Depth(i), Tag.Bitmap_Mipmaps_Count(i)) )

            #check if the strings list exists in the spot with 
            if File_Size in Tag_Data_Strings:
                Tag_Data_Strings[File_Size].append(Tag_Data_Str)
            else:
                Tag_Data_Strings[File_Size] = [Tag_Data_Str]


        #Take all the tag strings generated above and concatenate them
        #to the appropriate Format string under the appropriate Type
        for Type in (0, 1, 2):
            for Format in Valid_Formats:
                for Filesize in reversed(sorted( Tag_Info_Strings[Type][Format].keys())):
                    for Tag_String in Tag_Info_Strings[Type][Format][Filesize]:
                        
                        if Type in (0, 1, 2):
                            T_Counts[Type] += 1
                            
                            if Format in Valid_Formats:
                                F_Strs[Type][Format] += Tag_String


        #concate all the strings to the debug log in order of Type and Format
        for Type in (0, 1, 2):
            Debug_Log_String += T_Strs[Type] + str(T_Counts[Type]) + "\n"
            
            for Format in F_Strs[Type]:
                Debug_Log_String += F_Strs[Type][Format]

        return Debug_Log_String
