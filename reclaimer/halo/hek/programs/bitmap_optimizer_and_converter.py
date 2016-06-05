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
        
        self.default_conversion_flags["bitm"] = self.make_default_flags()
        self.root_window = BitmapConverterMainWindow(self)

        #Create and start the tag scanning and editing thread
        self.conversion_main_thread = Thread(target=self.conversion_main)
        self.conversion_main_thread.daemon = True
        self.conversion_main_thread.start()
        
        #loop the main window
        self.root_window.mainloop()

        
    #the main loop for continuous function handeling
    #add all continuous, non-self-looping, periodic functions here
    def _main_loop(self):
        while not hasattr(self, "root_window"):
            pass
        
        while not self.close_program:
            #we don't want it to run too often or it'll be laggy
            sleep(self.main_delay)
            self.root_window.total_bitmaps = (len(self.tags["bitm"]) -
                                              self.root_window.bad_bitmaps)
            
            #If the program is being told to close then close
            if self.close_program:
                raise SystemExit(0)
            

    def conversion_main(self):
        rw = self.root_window
        while True:
            #we don't want it to run too often or it'll be laggy
            sleep(self.main_delay)

            #if the tags havent been loaded and we are
            #telling the program to continue with conversion
            if (not rw.tags_loaded) and rw.proceed_with_conversion:
                #reset the status variables
                rw.total_pixel_data_to_process     = 0
                rw.remaining_pixel_data_to_process = 0
                rw.bitmaps_found_2d = rw.bitmaps_found_3d = rw.cubemaps_found=0
                rw.elapsed_time  = rw.estimated_time_remaining = 0.0
                rw.total_bitmaps = rw.remaining_bitmaps = rw.bad_bitmaps = 0
                rw.scan_start_time = time()

                if self.index_tags():
                    rw.tags_indexed = True

                    self.load_tags()
                    
                    rw.tags_loaded = True
                    tags = self.tags['bitm']
                    def_flags = self.default_conversion_flags['bitm']

                    #we need to build the list of conversion flags for each tag
                    for filepath in tags:
                        tags[filepath].tag_conversion_settings = list(def_flags)
                        
                    self.initialize_window_variables()
                else:
                    self.current_tag = "No tags found in selected directory."
                    rw.finish_conversion()
                    
                
            elif rw.tags_loaded and rw.proceed_with_conversion:
                #reset the status variables
                rw.elapsed_time = rw.estimated_time_remaining = 0.0
                rw.scan_start_time = time()
                rw.remaining_pixel_data_to_process = rw.total_pixel_data_to_process
                rw.remaining_bitmaps = rw.total_bitmaps
                
                #are we just scanning the folder or are we doing shiz
                if (self.default_conversion_flags["bitm"][READ_ONLY]):
                    #used below for writing the results of the scan
                    logstr = self.make_log_of_all_bitmaps()
                    self.current_tag = ("Detailed log of all bitmaps "+
                                        "created successfully.")
                else:
                    """SPLIT OFF INTO THE MAIN PROCESSING ROUTINE"""
                    logstr = self.process_bitmap_tags()
                
                #to keep from bloating the RAM, we delete all loaded bitmap tags
                for filepath in tuple(self.tags['bitm']):
                    del self.tags['bitm'][filepath]
                gc.collect()

                #since we are done with the conversion we write
                #the debug log and change the window variables
                if not rw.conversion_cancelled:
                    if (self.default_conversion_flags["bitm"]
                        [WRITE_LOG] and not self.debug >= 1):
                        self.make_log_file(logstr) #save the debug log to a file
                    else:
                        #if we are debugging we don't want to clutter
                        #the folder with lots of logs, so we just print it
                        print(logstr)

                    rw.finish_conversion()


    #run the list update function on the main thread
    def create_initial_tag_list(self):
        self.root_window.tag_list_window.sort_displayed_tags_by(0)



    def make_default_flags(self):
        '''
        If no settings have been defined specifically
        for a tag then the flags below will be used
        
        the first 4 conversion flags are global conversion
        flags and aren't assigned on a per-tag basis

          DONT REPROCESS: Don't process bitmap tags if they have
                          "Processed by Reclaimer" checked
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
          P8 MODE: P8-Bump Conversion Mode (True = Average Bias Mode,
                                            False = Auto Bias Mode)
          MONO KEEP: Channel to keep when converting to A8 or Y8
                     (True = Alpha, False = Intensity)
          MONO SWAP: Swap Alpha and Intensity (Only for A8Y8)
          CK TRANS: Preserve Color Key transparency  (A transparent pixel
                         in DXT1 has black for it's Red, Green, and Blue)
          MIP GEN: Generate mipmaps if a texture doesn't have them down to 1x1
          GAMMA: The gamma exponent to use when downressing
                 a bitmap by merging pixels
          NEW FORMAT: -1=unchanged, 0=A8, 1=Y8, 2=AY8, 3=A8Y8,
                       6=R5G6B5 8=A1R5G5B5, 9=A4R4G4B4, 14=DXT1,
                       15=DXT3, 16=DXT5, 17=P8/A8R8G8B8/X8R8G8B8
        '''
        
        flags = [True, True, False, True, False, False,
                 '0', 0, '127', False, False, False,
                 False, FORMAT_NONE, False, 1.0, " "]

        return flags


    def initialize_window_variables(self):
        rw = self.root_window
        rw.bitmaps_found_2d  = rw.bitmaps_found_3d = 0
        rw.cubemaps_found    = rw.total_bitmaps    = 0
        rw.remaining_bitmaps = rw.bad_bitmaps      = 0
        
        tags_to_remove = []

        #for the conversion variables we want to return
        #a count on how many bitmaps are of what type
        for filepath in self.tags['bitm']:

            #only run if the bitmap contains bitmaps
            tag = self.tags['bitm'][filepath]
            if tag.bitmap_count() and tag.is_power_of_2_bitmap():
                
                b_type = tag.bitmap_type()
                b_format = tag.bitmap_format()
                if b_type == 2:
                    rw.cubemaps_found += 1
                elif b_type == 1:
                    rw.bitmaps_found_3d += 1
                else:
                    rw.bitmaps_found_2d += 1
                
                rw.total_pixel_data_to_process += tag.pixel_data_bytes_size()
            else:
                if tag.bitmap_count():
                    print("Non power-of-2 bitmap found.\n%s\n\n"%tag.filepath)
                else:
                    print("Bitmap with no bitmap data found.\n%s\n\n"%
                          tag.filepath)
                tags_to_remove.append(filepath)
                rw.bad_bitmaps += 1
                
            rw.total_bitmaps += 1

        for filepath in tags_to_remove:
            del self.tags['bitm'][filepath]
        del tags_to_remove
            
        rw.tag_list_window.build_tag_sort_mappings()
        
        #set the status variables
        rw.remaining_pixel_data_to_process = rw.total_pixel_data_to_process
        rw.remaining_bitmaps = len(self.tags['bitm']) - rw.bad_bitmaps
        
        self.current_tag = ("Tags loaded... Please select tags in the "+
                            "tags list window and specify\nthe conversion "+
                            "settings for them in this window.\nWhen you "+
                            'are finished hit "Convert"')
        
        #set up the hack to allow the tag list to
        #be displayed instantly on loading a tagset
        rw.after(0, self.create_initial_tag_list)
        rw.finish_scanning()



    #this function is called by the conversion_main and
    #will loop through all the tags in the collection and
    #process them however each tag's conversion flags say to.
    def process_bitmap_tags(self):
        rw = None
        if hasattr(self, "root_window"):
            rw = self.root_window
        
        #used below for debug writing
        logstr = "Debug log for Halo Bitmap Converter\n"
        def_flags = self.default_conversion_flags['bitm']
        conversion_report = {'bitm':{}}

        #loop through each tag
        for filepath in sorted(self.tags['bitm']):
            tag = self.tags['bitm'][filepath]
            
            if rw is not None and rw.conversion_cancelled:
                break
            
            self.current_tag = filepath

            #this may change after the below function
            #so we get it before that happens
            tagsize = tag.pixel_data_bytes_size()
            if get_will_be_processed(tag, def_flags):
                """DO THE CONVERSION NOW"""
                try:
                    convert_bitmap_tag(tag, root_window=rw, filepath=filepath,
                                   conversion_report=conversion_report['bitm'], 
                                   reprocess=not(def_flags[DONT_REPROCESS]))
                except:
                    print(format_exc())
                    conversion_report['bitm'][filepath] = False
            else:
                conversion_report['bitm'][filepath] = None
            rw.remaining_pixel_data_to_process -= tagsize
            rw.remaining_bitmaps -= 1


        if rw is not None and rw.conversion_cancelled:
            self.current_tag = "Conversion cancelled."
            
            rw.display_new_text = True
            rw.btn_start.config(text="Convert")
            rw.enable_global_settings()
            rw.conversion_cancelled = False
            logstr += "Conversion Cancelled."
        else:
            try:
                backup = self.default_conversion_flags['bitm'][RENAME_OLD]
                '''depending on the conversion settings we
                either rename or delete the original files'''
                logstr += self.make_write_log(conversion_report, backup=backup)
            except:
                print("ERROR OCCURRED WHILE TRYING TO WRITE "+
                      "DEBUG LOG AND/OR RENAME TEMP FILES")
                print(format_exc())
            
            self.current_tag = "Finished converting tags"

        return logstr



    #used when doing a read-only scan of a tagset to figure out what's what
    def make_log_of_all_bitmaps(self):
        logstr = ("CE-XBOX Bitmap Converter: tagset scan results\n\n\n"+
                  "These are the bitmaps located in the tags folder "+
                  "organized by type and then by format.\n\n")
        
        valid_formats = (0,1,2,3,6,8,9,10,11,14,15,16,17)

        base_str = "Bitmap %s --- WxHxD: %sx%sx%s --- Mipmaps: %s\n"

        tag_counts = [0, 0, 0]

        formatted_strs = {}
        tag_header_strs = ["\n\n2D Textures:\n    Count = ",
                           "\n\n3D Textures:\n    Count = ",
                           "\n\nCubemaps:\n    Count = "]
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
                formatted_strs[b_type][b_format] = ("\n\n"+" "*4+"%s Format" %
                                                    format_names[b_format])
                tag_info_strs[b_type][b_format] = {}


        #loop through each tag and create a
        #string that details each bitmap in it
        for filepath in self.tags['bitm']:
            tag = self.tags['bitm'][filepath]
            filesize = (getsize(tag.filepath)-
                        tag.color_plate_data_bytes_size())//1024
            tagstrs  = tag_info_strs[tag.bitmap_type()][tag.bitmap_format()]
            
            #this is the string that holds the data pertaining to this tag
            tagstr = ("\n"+" "*8+filepath+" "*8+"Compiled tag size = %sKB\n" %
                      {True:"less than 1", False:str(filesize)}[filesize <= 0])

            for i in range(tag.bitmap_count()):
                tagstr += (" "*12 + base_str %
                           (i, tag.bitmap_width(i), tag.bitmap_height(i),
                            tag.bitmap_depth(i), tag.bitmap_mipmaps_count(i)) )

            #check if the strings list exists in the spot with 
            if filesize in tagstrs:
                tagstrs[filesize].append(tagstr)
            else:
                tagstrs[filesize] = [tagstr]


        #Take all the tag strings generated above and concatenate them
        #to the appropriate b_format string under the appropriate b_type
        for b_type in (0, 1, 2):
            for b_format in valid_formats:
                for b_size in reversed(sorted(tag_info_strs[b_type][b_format])):
                    for tagstr in tag_info_strs[b_type][b_format][b_size]:
                        tag_counts[b_type] += 1
                        formatted_strs[b_type][b_format] += tagstr


        #concate all the strings to the
        #log in order of b_type and b_format
        for b_type in (0, 1, 2):
            logstr += (tag_header_strs[b_type] + str(tag_counts[b_type]) +
                       "\n" + ''.join(formatted_strs[b_type]))

        return logstr
