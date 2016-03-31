import gc

from os.path import getsize
from threading import Thread
from time import sleep, time
from traceback import format_exc

from .gui.bitmap_converter_windows import *
from ..handler import HaloHandler
from ..tag_editing.bitm import *


class BitmapConverter(HaloHandler):

    log_filename = "Bitmap_Converter.log"
    close_program = False #if set to True the program will close
    main_delay = 0.03 #determines how often the main loop is run
    
    def __init__(self, **kwargs):
        HaloHandler.__init__(self, valid_def_ids="bitm", **kwargs)
        
        self.Default_Conversion_Flags["bitm"] = self.Make_Default_Flags()
        self.root_window = Bitmap_Converter_Main_Window(self)

        #Create and start the tag scanning and editing thread
        self.Conversion_Main_Thread = Thread(target=self.Conversion_Main)
        self.Conversion_Main_Thread.daemon = True
        self.Conversion_Main_Thread.start()
        
        #loop the main window
        self.root_window.mainloop()

        
    #the main loop for continuous function handeling
    #add all continuous, non-self-looping, periodic functions here
    def _Main_Loop(self):
        while not hasattr(self, "root_window"):
            pass
        
        while not self.close_program:
            #we don't want it to run too often or it'll be laggy
            sleep(self.main_delay)
            self.root_window.Total_Bitmaps = (len(self.tags["bitm"]) -
                                              self.root_window.Bad_Bitmaps)
            
            #If the program is being told to close then close
            if self.close_program:
                raise SystemExit(0)
            

    def Conversion_Main(self):
        rw = self.root_window
        while True:
            #we don't want it to run too often or it'll be laggy
            sleep(self.main_delay)

            #if the tags havent been loaded and we are telling the program to continue with conversion
            if (not rw.tags_loaded) and rw.Proceed_with_Conversion:
                #reset the status variables
                rw.Total_Pixel_Data_to_Process     = 0
                rw.Remaining_Pixel_Data_to_Process = 0
                rw.Bitmaps_Found_2D = rw.Bitmaps_Found_3D = rw.Cubemaps_Found = 0
                rw.Elapsed_Time  = rw.Estimated_Time_Remaining = 0.0
                rw.Total_Bitmaps = rw.Remaining_Bitmaps = rw.Bad_Bitmaps = 0
                rw.Scan_Start_Time = time()

                if self.index_tags():
                    rw.tags_Indexed = True

                    self.load_tags()
                    
                    rw.tags_loaded = True
                    tags = self.tags['bitm']
                    def_flags = self.Default_Conversion_Flags['bitm']

                    #we need to build the list of conversion flags for each tag.
                    for tagpath in tags:
                        tags[tagpath].Tag_Conversion_Settings = list(def_flags)
                        
                    self.Initialize_Window_Variables()
                else:
                    self.current_tag = "No tags found in selected directory."
                    rw.Finish_Conversion()
                    
                
            elif rw.tags_loaded and rw.Proceed_with_Conversion:
                #reset the status variables
                rw.Elapsed_Time = rw.Estimated_Time_Remaining = 0.0
                rw.Scan_Start_Time = time()
                rw.Remaining_Pixel_Data_to_Process = rw.Total_Pixel_Data_to_Process
                rw.Remaining_Bitmaps = rw.Total_Bitmaps
                
                #are we just scanning the folder or are we doing shiz
                if (self.Default_Conversion_Flags["bitm"][READ_ONLY]):
                    #used below for writing the results of the scan
                    logstr = self.Make_Log_of_All_Bitmaps()
                    self.current_tag = ("Detailed log of all bitmaps "+
                                        "created successfully.")
                else:
                    """SPLIT OFF INTO THE MAIN PROCESSING ROUTINE"""
                    logstr = self.Process_Bitmap_tags()
                
                #to keep from bloating the RAM, we delete all loaded bitmap tags
                for tagpath in tuple(self.tags['bitm']):
                    del self.tags['bitm'][tagpath]
                gc.collect()

                #since we are done with the conversion we write the debug log and change the window variables
                if not rw.Conversion_Cancelled:
                    if (self.Default_Conversion_Flags["bitm"]
                        [WRITE_LOG] and not self.debug >= 1):
                        self.make_log_file(logstr) #save the debug log to a file
                    else:
                        #if we are debugging we don't want to clutter the folder with lots of logs, so we just print it
                        print(logstr)

                    rw.Finish_Conversion()
            else:
                pass


    #run the list update function on the main thread
    def Create_Initial_Tag_List(self):
        self.root_window.tag_list_window.Sort_Displayed_Tags_By(0)



    def Make_Default_Flags(self):
        '''
        If no settings have been defined specifically for a tag then the flags below will be used
        
        the first 4 conversion flags are global conversion flags and aren't assigned on a per-tag basis

          DONT REPROCESS: Don't process bitmap tags if they have "Processed by Reclaimer" checked
          RENAME OLD: Rename old tags instead of deleting them
          READ ONLY: compiles a list of all bitmaps and what their types, 
                    sizes, etc are instead of converting in any way
          WRITE LOG: Write debug Log
        
          PLATFORM: Platform to save as(True = Xbox, False = PC)
          SWIZZLED: True = save as swizzled, False = save as deswizzled
          DOWNRES: Number of times to cut resolution in half
          MULTI SWAP: 0 = don't swap multipurpose channels,
                      1 = swap for xbox,  2= swap for pc
          CUTOFF BIAS: when reducing a channel to 1 bit, values above
                       this are snapped to 1 and below it are snapped to 0
          P8 MODE: P8-Bump Conversion Mode (True = Average Bias Mode, False = Auto Bias Mode)
          MONO KEEP: Channel to keep when converting to A8 or Y8 (True = Alpha, False = Intensity)
          MONO SWAP: Swap Alpha and Intensity (Only for A8Y8)
          CK TRANS: Preserve Color Key transparency  (A transparent pixel
                         in DXT1 has black for it's Red, Green, and Blue)
          MIP GEN: Generate mipmaps if a texture doesn't have them down to 1x1
          GAMMA: The gamma exponent to use when downressing a bitmap by merging pixels
          NEW FORMAT: -1=unchanged, 0=A8, 1=Y8, 2=AY8, 3=A8Y8, 6=R5G6B5 8=A1R5G5B5, 
                       9=A4R4G4B4, 14=DXT1, 15=DXT3, 16=DXT5, 17=P8/A8R8G8B8/X8R8G8B8
        '''
        
        Bitmap_Conversion_Flags = [True, True, False, True, False, False,
                                   '0', 0, '127', False, False, False,
                                   False, FORMAT_NONE, False, 1.0, " "]

        return Bitmap_Conversion_Flags


    def Initialize_Window_Variables(self):
        rw = self.root_window
        rw.Bitmaps_Found_2D  = rw.Bitmaps_Found_3D = 0
        rw.Cubemaps_Found    = rw.Total_Bitmaps    = 0
        rw.Remaining_Bitmaps = rw.Bad_Bitmaps      = 0
        
        tags_to_remove = []

        #for the conversion variables we want to return
        #a count on how many bitmaps are of what type
        for tagpath in self.tags['bitm']:

            #only run if the bitmap contains bitmaps
            tag = self.tags['bitm'][tagpath]
            if tag.Bitmap_Count() and tag.Is_Power_of_2_Bitmap():
                
                b_type = tag.Bitmap_Type()
                b_format = tag.Bitmap_Format()
                if b_type == 2:
                    rw.Cubemaps_Found += 1
                elif b_type == 1:
                    rw.Bitmaps_Found_3D += 1
                else:
                    rw.Bitmaps_Found_2D += 1
                
                rw.Total_Pixel_Data_to_Process += tag.Pixel_Data_Bytes_Size()
            else:
                if tag.Bitmap_Count():
                    print("Non power-of-2 bitmap found.\n%s\n\n"%tag.tagpath)
                else:
                    print("Bitmap with no bitmap data found.\n%s\n\n"%tag.tagpath)
                tags_to_remove.append(tagpath)
                rw.Bad_Bitmaps += 1
                
            rw.Total_Bitmaps += 1

        for tagpath in tags_to_remove:
            del self.tags['bitm'][tagpath]
        del tags_to_remove
            
        rw.tag_list_window.Build_Tag_Sort_Mappings()
        
        #set the status variables
        rw.Remaining_Pixel_Data_to_Process = rw.Total_Pixel_Data_to_Process
        rw.Remaining_Bitmaps = len(self.tags['bitm']) - rw.Bad_Bitmaps
        
        self.current_tag = ("Tags loaded... Please select tags in the "+
                            "tags list window and specify\nthe conversion "+
                            "settings for them in this window.\nWhen you "+
                            'are finished hit "Convert"')
        
        #set up the hack to allow the tag list to
        #be displayed instantly on loading a tagset
        rw.after(0, self.Create_Initial_Tag_List)
        rw.Finish_Scanning()



    #this function is called by the Conversion_Main and will loop through all the
    #tags in the collection and process them however each tag's conversion flags say to.
    def Process_Bitmap_tags(self):
        
        if hasattr(self, "root_window"):
            rw = self.root_window
        else:
            rw = None
        
        #used below for debug writing
        logstr = "Debug log for Halo Bitmap Converter\n"
        def_flags = self.Default_Conversion_Flags['bitm']
        Conversion_Report = {'bitm':{}}

        #loop through each tag
        for tagpath in sorted(self.tags['bitm']):
            tag = self.tags['bitm'][tagpath]
            
            if rw is not None and rw.Conversion_Cancelled:
                break
            
            self.current_tag = tagpath

            #this may change after the below function so we get it before that happens
            tagsize = tag.Pixel_Data_Bytes_Size()
            if Get_Will_be_Processed(tag, def_flags):
                """DO THE CONVERSION NOW"""
                try:
                    Convert_Bitmap_Tag(tag, Root_Window=rw, tagpath=tagpath,
                                       Conversion_Report=Conversion_Report['bitm'], 
                                       Reprocess=not(def_flags[DONT_REPROCESS]))
                except:
                    print(format_exc())
                    Conversion_Report['bitm'][tagpath] = False
            else:
                Conversion_Report['bitm'][tagpath] = None
            rw.Remaining_Pixel_Data_to_Process -= tagsize
            rw.Remaining_Bitmaps -= 1


        if rw is not None and rw.Conversion_Cancelled:
            self.current_tag = "Conversion cancelled."
            
            rw.Display_New_Text = True
            rw.btn_start.config(text="Convert")
            rw.Enable_Global_Settings()
            rw.Conversion_Cancelled = False
            logstr += "Conversion Cancelled."
        else:
            try:
                backup = self.Default_Conversion_Flags['bitm'][RENAME_OLD]
                '''depending on the conversion settings we
                either rename or delete the original files'''
                logstr += self.make_write_log(Conversion_Report, backup=backup)
            except:
                print("ERROR OCCURRED WHILE TRYING TO WRITE "+
                      "DEBUG LOG AND/OR RENAME TEMP FILES")
                print(format_exc())
            
            self.current_tag = "Finished converting tags"

        return logstr



    #used when doing a read-only scan of a tagset to figure out what's what
    def Make_Log_of_All_Bitmaps(self):
        logstr = ("CE-XBOX Bitmap Converter: tagset scan results\n\n\n"+
                  "These are the bitmaps located in the tags folder "+
                  "organized by type and then by format.\n\n")
        
        valid_formats = (0,1,2,3,6,8,9,10,11,14,15,16,17)

        base_str = "Bitmap %s --- WxHxD: %sx%sx%s --- Mipmaps: %s\n"

        tag_counts = [0, 0, 0]

        formatted_strs = {}
        tag_header_strs = ["\n\n2D Textures:\nCount = ",
                           "\n\n3D Textures:\nCount = ",
                           "\n\nCubemaps:\nCount = "]
        format_names = ["A8", "Y8", "AY8", "A8Y8", '', '',
                        "R5G6B5", '', "A1R5G6B5", "A4R4G4B4",
                        "X8R8G8B8", "A8R8G8B8", '', '', "DXT1",
                        "DXT3", "DXT5", "P8-Bump"]

        #so we can sort bitmaps by filesize we'll create a dict to hold all
        #the strings before we concate them so we can sort them later by size
        tag_info_strs = {}


        #add dicts for all three types to the tag_info_strings
        for b_type in (0, 1, 2):
            
            formatted_strs[b_type] = ['']*18
            tag_info_strs[b_type]  = ['']*18

            #and add the formats to each of these new dicts
            for b_format in valid_formats:
                formatted_strs[b_type][b_format] = ("\n\n" + " "*8 + "%s Format" %
                                                    format_names[b_format])
                tag_info_strs[b_type][b_format] = {}


        #loop through each tag and create a string that details each bitmap in it
        for tagpath in self.tags['bitm']:
            tag = self.tags['bitm'][tagpath]
            filesize = (getsize(tag.tagpath)-tag.Color_Plate_Data_Bytes_Size())//1024
            tagstrs  = tag_info_strs[tag.Bitmap_Type()][tag.Bitmap_Format()]
            
            #this is the string that holds the data pertaining to this tag
            tagstr = ("\n"+" "*16+tagpath+" "*8+"Compiled tag size = %sKB\n" %
                      {True:"less than 1", False:str(filesize)}[filesize <= 0])

            for i in range(tag.Bitmap_Count()):
                tagstr += (" "*24 + base_str %
                           (i, tag.Bitmap_Width(i), tag.Bitmap_Height(i),
                            tag.Bitmap_Depth(i), tag.Bitmap_Mipmaps_Count(i)) )

            #check if the strings list exists in the spot with 
            if filesize in tagstrs:
                tagstrs[filesize].append(tagstr)
            else:
                tagstrs[filesize] = [tagstr]


        #Take all the tag strings generated above and concatenate them
        #to the appropriate b_format string under the appropriate b_type
        for b_type in (0, 1, 2):
            for b_format in valid_formats:
                for b_size in reversed(sorted( tag_info_strs[b_type][b_format] )):
                    for tagstr in tag_info_strs[b_type][b_format][b_size]:
                        tag_counts[b_type] += 1
                        formatted_strs[b_type][b_format] += tagstr


        #concate all the strings to the debug log in order of b_type and b_format
        for b_type in (0, 1, 2):
            logstr += (tag_header_strs[b_type] + str(tag_counts[b_type]) +
                       "\n" + ''.join(formatted_strs[b_type]))

        return logstr
