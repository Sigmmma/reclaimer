import threading
import tkinter.filedialog
from time import time, sleep

from .mtTkinter import *
from .Common_Window_Functions import *
from ....Tag_Operations.Halo_Operations.bitm import *


#used when displaying the format and type in windows
Bitmap_Type_Strings = ("2D Texture", "3D Texture", "Cubemap", "????")
Bitmap_Format_Strings = ("A8", "Y8", "AY8", "A8Y8", "????", "????", "R5G6B5",
                         "????", "A1R5G5B5", "A4R4G4B4", "X8R8G8B8", "A8R8G8B8",
                         "????", "????", "DXT1", "DXT3", "DXT5", "P8 Bump")
Bitmap_Short_Type_Strings = ("2D", "3D", "CUBE", "WHITE")



#compares all the conversion settings of the tag with the tag's data to tell if it will be processed
"""THIS IS USED TO DETERMINE IF THE Convert_Bitmap_Tags SHOULD EVEN BE RUN"""
def Get_Will_be_Processed(Tag, Bitmap_Conversion_Flags):
    #only run if the bitmap contains bitmaps and we are NOT in read-only mode
    if (Tag.Bitmap_Count()==0) or Bitmap_Conversion_Flags["READ ONLY"]:
        return(False)
    
    if Bitmap_Conversion_Flags["DONT REPROCESS"]:
        return(Process_Bitmap_Tag(Tag) or Extracting_Texture(Tag))
    
    return(True)


'''ENTER A DESCRIPTION FOR THIS CLASS WHEN I HAVE TIME'''
class Bitmap_Converter_Main_Window(Tk):

    def __init__(self, Handler, **options):
        Tk.__init__(self, **options )
        
        '''THE PROGRAM MUST BE CLASS WITH VARIABLES SUCH AS TAG_COLLECTION'''
        self.Handler = Handler

        self.title("Halo Bitmap Optimizer & Converter")
        self.geometry("745x405+0+0")
        self.resizable(0, 0)
        self.protocol("WM_DELETE_WINDOW", self.Close_Main_Window)

        #this is used to make it so only 1 window update can be called at a time
        self.Window_Updating = False
        self.Window_Docking_Updating = False
        
        self.Window_Update_Interval = 0.33
        self.Window_Docking_Interval = 0.1
        
        self.Dock_Window_Movement = Dock_Window_Movement
        self.Mini_Maxi_State_Changing = True

        
        self.save_all_tags_as = True

        self.Proceed_with_Conversion = False   #False = do nothing
                                               #True  = index and load tags, or convert tags if already loaded
        
        self.Tags_Indexed = False   #False = program is still indexing tags
                                    #True  = tags indexed and ready to be loaded
        
        self.Tags_Loaded = False   #False = program just loaded
                                   #True  = tags indexed and ready to convert
        
        self.Conversion_Cancelled = False   #used to signal to the conversion routine to cancel conversion


        #Statistics variables
        self.Bitmaps_Found_2D = 0
        self.Bitmaps_Found_3D = 0
        self.Cubemaps_Found = 0
        self.Total_Bitmaps = 0
        self.Elapsed_Time = 0.0
        self.Total_Pixel_Data_to_Process = 0
        self.Estimated_Time_Remaining = 0.0
        self.Remaining_Bitmaps = 0
        self.Remaining_Pixel_Data_to_Process = 0
        
        #we'll use this to know how many tags we've skipped while iterating the tag collection
        self.Bad_Bitmaps = 0
        
        self.Scan_Start_Time = 0.0
        #set this to true when wanting to have the program display exactly what's in the "Current_Tag" string
        self.Display_New_Text = False
        
        #used for setting the position of the child windows so when you move the main it moves the others
        self.Previous_Pos_X = 0
        self.Previous_Pos_Y = 0
        self.docking_state = True

        #Window variables that we'll use as an intermediary between user input and giving to the program
        self.TK_Tags_Directory = StringVar(self)
        
        self.TK_Dont_Reprocess_Tags = IntVar(self)
        self.TK_Backup_Edited_Tags = IntVar(self)
        self.TK_Read_Only = IntVar(self)
        self.TK_Write_Debug_Log = IntVar(self)
        
        self.TK_Platform_to_Save_as = IntVar(self)
        self.TK_Swizzle_Bitmap = IntVar(self)
        self.TK_Number_of_Times_to_Halve_Resolution = StringVar(self)
        
        self.TK_Multipurpose_Swap_Setting = IntVar(self)

        self.TK_Alpha_Cutoff_Bias = StringVar(self)
        self.TK_Alpha_Cutoff_Bias.set("127")
        self.TK_P8_Conversion_Mode = IntVar(self)
        self.TK_Channel_to_Keep = IntVar(self)
        self.TK_Swap_A8Y8_Alpha_and_Intensity = IntVar(self)
        self.TK_Preserve_CK_Transparency = IntVar(self)
        
        self.TK_Conversion_Format_Setting = IntVar(self)
        self.TK_Target_Extract_Format = StringVar(self)
        self.TK_Mipmap_Gen_Setting = IntVar(self)
        self.TK_Target_Extract_Format.set(" ")
        
        self.Displayed_Info_String = ('For information on what each setting does and how to use this '+
                                      'program,\nopen and look through the "Useful help" window.')

        #Make the menu bar
        self.menubar = Menu(self)
        self.menubar.add_command(label="Useful Help", command=self.Show_Bitmap_Converter_Help)
        self.menubar.add_command(label="Toggle All Tags to XBOX Format", command=self.Save_All_Tags_as)
        self.menubar.add_command(label="Un-dock Windows", command=self.Toggle_Window_Docking)
        self.menubar.add_command(label="Invert Selection", command=self.Invert_Selection)
        self.config(menu=self.menubar)

        #--------------------------------------------------------------
        #Create the TAGS DIRECTORY field
        self.Tags_Field_Name = Canvas(self, width=487, height=45, highlightthickness=0)
        self.Tags_Field_Name.place(x=4, y=4, anchor=NW)
        self.Tags_Field_Name.config(bd=2, relief=GROOVE)
        self.Tags_Field_Text = self.Tags_Field_Name.create_text(13, 3, anchor="nw")
        self.Tags_Field_Name.itemconfig(self.Tags_Field_Text, text="Tags Folder")

        #Create the TAGS DIRECTORY box
        self.Tags_Directory_Field = Entry(self, textvariable=self.TK_Tags_Directory)
        self.Tags_Directory_Field.place(x=18, y=24, anchor=NW)
        self.Tags_Directory_Field.insert(INSERT, self.Handler.Tags_Directory)
        self.Tags_Directory_Field.config(width=57, state=DISABLED)

        #Add the buttons
        self.btn_browse = Button(self.Tags_Field_Name, text="Browse...", width=10, command=self.Make_Bitmap_Converter_Browse)
        self.btn_browse.place(x=362, y=16, anchor=NW)

        self.btn_start = Button(self.Tags_Field_Name, text="Load", width=7, command=self.Bitmap_Converter_Run_Pressed)
        self.btn_start.place(x=432, y=16, anchor=NW)

        #--------------------------------------------------------------
        #Create the GLOBAL PARAMETERS field
        self.Global_Parameters_Root = Canvas(self, width=135, height=95, highlightthickness=0)
        self.Global_Parameters_Root.place(x=4, y=51, anchor=NW)
        self.Global_Parameters_Name_Text = self.Global_Parameters_Root.create_text(8, 5, anchor="nw")
        self.Global_Parameters_Root.itemconfig(self.Global_Parameters_Name_Text, text="Global Parameters")
        self.Global_Parameters_Root.config(bd=2, relief=GROOVE)

        #Create the GLOBAL PARAMETERS check buttons
        self.Checkbox_Dont_Reprocess_Tags = Checkbutton(self.Global_Parameters_Root, text="Dont reprocess tags",
                                                        variable=self.TK_Dont_Reprocess_Tags, onvalue=1, offvalue=0,
                                                        command=self.Set_Dont_Reprocess_Tags_Variable)
        self.Checkbox_Backup_Old_Tags = Checkbutton(self.Global_Parameters_Root, text="Backup old tags",
                                                    variable=self.TK_Backup_Edited_Tags, onvalue=1, offvalue=0,
                                                    command=self.Set_Backup_Old_Tags_Variable)
        self.Checkbox_Read_Only = Checkbutton(self.Global_Parameters_Root, text="Read only mode",
                                              variable=self.TK_Read_Only, onvalue=1, offvalue=0,
                                              command=self.Set_Read_Only_Variable)
        self.Checkbox_Write_Debug_Log = Checkbutton(self.Global_Parameters_Root, text="Write debug log",
                                                    variable=self.TK_Write_Debug_Log, onvalue=1, offvalue=0,
                                                    command=self.Set_Write_Debug_Log_Variable)

        self.Checkbox_Dont_Reprocess_Tags.select()
        self.Checkbox_Backup_Old_Tags.select()
        self.Checkbox_Write_Debug_Log.select()
        
        self.Checkbox_Dont_Reprocess_Tags.place(x=4, y=23, anchor=NW)
        self.Checkbox_Backup_Old_Tags.place(x=4, y=41, anchor=NW)
        self.Checkbox_Read_Only.place(x=4, y=59, anchor=NW)
        self.Checkbox_Write_Debug_Log.place(x=4, y=77, anchor=NW)
        #--------------------------------------------------------------
        
        #Create the GENERAL PARAMETERS field
        self.General_Parameters_Root = Canvas(self, width=236, height=95, highlightthickness=0)
        self.General_Parameters_Root.place(x=137, y=51, anchor=NW)
        self.General_Parameters_Name_Text = self.General_Parameters_Root.create_text(8, 5, anchor="nw")
        self.General_Parameters_Root.itemconfig(self.Global_Parameters_Name_Text, text="General Conversion Parameters")
        self.General_Parameters_Root.config(bd=2, relief=GROOVE)

        #Create the GENERAL PARAMETERS buttons
        self.Radio_Save_as_Xbox = Radiobutton(self.General_Parameters_Root, text="Save as Xbox tag",
                                              variable=self.TK_Platform_to_Save_as, value=1,
                                              command=self.Set_Platform_to_Save_as_Variable)
        self.Radio_Save_as_PC = Radiobutton(self.General_Parameters_Root, text="Save as PC tag",
                                            variable=self.TK_Platform_to_Save_as, value=0,
                                            command=self.Set_Platform_to_Save_as_Variable)
        self.Radio_Save_as_Swizzled = Radiobutton(self.General_Parameters_Root, text="Save as swizzled",
                                                  variable=self.TK_Swizzle_Bitmap, value=1,
                                                  command=self.Set_Swizzle_Mode_Variable)
        self.Radio_Save_as_Unswizzled = Radiobutton(self.General_Parameters_Root, text="Save as un-swizzled",
                                                    variable=self.TK_Swizzle_Bitmap, value=0,
                                                    command=self.Set_Swizzle_Mode_Variable)
        self.Spinbox_Times_to_Halve_Resolution = Spinbox(self.General_Parameters_Root, from_=0, to=12, width=3,
                                                         textvariable=self.TK_Number_of_Times_to_Halve_Resolution,
                                                         state="readonly", command=self.Set_Number_of_Times_to_Halve_Variable)
        self.Times_to_Halve_Resolution_Text = self.General_Parameters_Root.create_text(45, 75, anchor="nw")
        
        self.Radio_Save_as_Xbox.place(x=4, y=23, anchor=NW)
        self.Radio_Save_as_PC.place(x=112, y=23, anchor=NW)
        self.Radio_Save_as_Swizzled.place(x=4, y=49, anchor=NW)
        self.Radio_Save_as_Unswizzled.place(x=112, y=49, anchor=NW)
        self.Spinbox_Times_to_Halve_Resolution.place(x=8, y=72, anchor=NW)
        self.General_Parameters_Root.itemconfig(self.Times_to_Halve_Resolution_Text, text="Number of times to halve resolution")
        #--------------------------------------------------------------

        #Create the MULTIPURPOSE SWAP field
        self.Multipurpose_Swap_Root = Canvas(self, width=116, height=95, highlightthickness=0)
        self.Multipurpose_Swap_Root.place(x=375, y=51, anchor=NW)
        self.Multipurpose_Swap_Name_Text = self.Multipurpose_Swap_Root.create_text(8, 5, anchor="nw")
        self.Multipurpose_Swap_Root.itemconfig(self.Multipurpose_Swap_Name_Text, text="Multipurpose Swap")
        self.Multipurpose_Swap_Root.config(bd=2, relief=GROOVE)

        #Create the MULTIPURPOSE SWAP radio buttons
        self.Radio_Dont_Swap_Multipurpose = Radiobutton(self.Multipurpose_Swap_Root, text="None",
                                                        variable=self.TK_Multipurpose_Swap_Setting, value=0,
                                                        command=self.Set_Multipurpose_Swap_Variable)
        self.Radio_Swap_Multipurpose_to_Xbox = Radiobutton(self.Multipurpose_Swap_Root, text="Swap PC to Xbox",
                                                           variable=self.TK_Multipurpose_Swap_Setting, value=1, 
                                                           command=self.Set_Multipurpose_Swap_Variable)
        self.Radio_Swap_Multipurpose_to_PC = Radiobutton(self.Multipurpose_Swap_Root, text="Swap Xbox to PC",
                                                         variable=self.TK_Multipurpose_Swap_Setting, value=2,
                                                         command=self.Set_Multipurpose_Swap_Variable)

        self.Radio_Dont_Swap_Multipurpose.select()
        self.Radio_Dont_Swap_Multipurpose.place(x=4, y=23, anchor=NW)
        self.Radio_Swap_Multipurpose_to_Xbox.place(x=4, y=48, anchor=NW)
        self.Radio_Swap_Multipurpose_to_PC.place(x=4, y=73, anchor=NW)
        #--------------------------------------------------------------
        
        #Create the FORMAT SPECIFIC PARAMETERS field
        self.Format_Specific_Parameters_Root = Canvas(self, width=238, height=133, highlightthickness=0)
        self.Format_Specific_Parameters_Root.place(x=4, y=148, anchor=NW)
        self.Format_Specific_Parameters_Name_Text = self.Format_Specific_Parameters_Root.create_text(8, 5, anchor="nw")
        self.Format_Specific_Parameters_Root.itemconfig(self.Format_Specific_Parameters_Name_Text, text="Format Specific Parameters")
        self.Format_Specific_Parameters_Root.config(bd=2, relief=GROOVE)

        #Create the FORMAT SPECIFIC PARAMETERS buttons
        self.Spinbox_Alpha_Cutoff_Bias = Spinbox(self.Format_Specific_Parameters_Root, from_=0, to=255, width=3,
                                                 textvariable=self.TK_Alpha_Cutoff_Bias, state="readonly",
                                                 command=self.Set_Alpha_Cutoff_Bias_Variable, repeatinterval=5)    
        self.Radio_Auto_Bias_Mode = Radiobutton(self.Format_Specific_Parameters_Root, text="Auto-bias",
                                                variable=self.TK_P8_Conversion_Mode, value=0,
                                                command=self.Set_P8_Conversion_Mode_Variable)
        self.Radio_Average_Bias_Mode = Radiobutton(self.Format_Specific_Parameters_Root, text="Average-bias",
                                                   variable=self.TK_P8_Conversion_Mode, value=1,
                                                   command=self.Set_P8_Conversion_Mode_Variable)
        self.Radio_Keep_Intensity_Channel = Radiobutton(self.Format_Specific_Parameters_Root, text="Intensity(RGB)",
                                                        variable=self.TK_Channel_to_Keep, value=0,
                                                        command=self.Set_Monochrome_Channel_to_Keep_Variable)
        self.Radio_Keep_Alpha_Channel = Radiobutton(self.Format_Specific_Parameters_Root, text="Alpha",
                                                    variable=self.TK_Channel_to_Keep, value=1,
                                                    command=self.Set_Monochrome_Channel_to_Keep_Variable)
        self.Checkbox_Swap_A8Y8_Channels = Checkbutton(self.Format_Specific_Parameters_Root, text="Swap A8Y8 channels",
                                                       variable=self.TK_Swap_A8Y8_Alpha_and_Intensity, onvalue=1, offvalue=0,
                                                       command=self.Set_Swap_Alpha_and_Intensity_Variable)
        self.Checkbox_Preserve_CK_Transparency = Checkbutton(self.Format_Specific_Parameters_Root, text="C-Key Transparent",
                                                             variable=self.TK_Preserve_CK_Transparency, onvalue=1, offvalue=0,
                                                             command=self.Set_Preserve_CK_Transparency_Variable)

        self.Spinbox_Alpha_Cutoff_Bias.place(x=28, y=20, anchor=NW)
        self.Radio_Auto_Bias_Mode.place(x=18, y=53, anchor=NW)
        self.Radio_Average_Bias_Mode.place(x=126, y=53, anchor=NW)
        self.Radio_Keep_Intensity_Channel.place(x=18, y=90, anchor=NW)
        self.Radio_Keep_Alpha_Channel.place(x=126, y=90, anchor=NW)
        self.Checkbox_Swap_A8Y8_Channels.place(x=2, y=113, anchor=NW)
        self.Checkbox_Preserve_CK_Transparency.place(x=123, y=113, anchor=NW)
        
        self.Alpha_Cutoff_Bias_Text = self.Format_Specific_Parameters_Root.create_text(69, 23, anchor="nw")
        self.P8_Bump_Conversion_Mode_Text = self.Format_Specific_Parameters_Root.create_text(8, 40, anchor="nw")
        self.Monochrome_Channel_to_Keep_Text = self.Format_Specific_Parameters_Root.create_text(6, 75, anchor="nw")
        
        self.Format_Specific_Parameters_Root.itemconfig(self.Alpha_Cutoff_Bias_Text, text="Alpha cutoff bias")
        self.Format_Specific_Parameters_Root.itemconfig(self.P8_Bump_Conversion_Mode_Text, text="P-8 Bump Conversion Mode")
        self.Format_Specific_Parameters_Root.itemconfig(self.Monochrome_Channel_to_Keep_Text, text="Monochrome Channel to Keep")
        #--------------------------------------------------------------
        
        #Create the FORMAT TO CONVERT TO field
        self.Format_to_Convert_to_Root = Canvas(self, width=247, height=133, highlightthickness=0)
        self.Format_to_Convert_to_Root.place(x=244, y=148, anchor=NW)
        self.Format_to_Convert_to_Name_Text = self.Format_to_Convert_to_Root.create_text(8, 5, anchor="nw")
        self.Format_to_Convert_to_Root.itemconfig(self.Format_to_Convert_to_Name_Text, text="Format to Convert to")
        self.Format_to_Convert_to_Root.config(bd=2, relief=GROOVE)

        #Create the FORMAT TO CONVERT TO radio buttons
        self.Radio_Dont_Change_Format = Radiobutton(self.Format_to_Convert_to_Root, text="Unchanged",
                                                    variable=self.TK_Conversion_Format_Setting,
                                                    value=FORMAT_NONE, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_DXT1 = Radiobutton(self.Format_to_Convert_to_Root, text="DXT1",
                                              variable=self.TK_Conversion_Format_Setting,
                                              value=FORMAT_DXT1, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_DXT3 = Radiobutton(self.Format_to_Convert_to_Root, text="DXT3",
                                              variable=self.TK_Conversion_Format_Setting,
                                              value=FORMAT_DXT3, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_DXT5 = Radiobutton(self.Format_to_Convert_to_Root, text="DXT5",
                                              variable=self.TK_Conversion_Format_Setting,
                                              value=FORMAT_DXT5, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_R5G6B5 = Radiobutton(self.Format_to_Convert_to_Root, text="R5G6B5",
                                                variable=self.TK_Conversion_Format_Setting,
                                                value=FORMAT_R5G6B5, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_A1R5G5B5 = Radiobutton(self.Format_to_Convert_to_Root, text="A1R5G5B5*",
                                                  variable=self.TK_Conversion_Format_Setting,
                                                  value=FORMAT_A1R5G5B5, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_A4R4G4B4 = Radiobutton(self.Format_to_Convert_to_Root, text="A4R4G4B4",
                                                  variable=self.TK_Conversion_Format_Setting,
                                                  value=FORMAT_A4R4G4B4, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_P8_Bump = Radiobutton(self.Format_to_Convert_to_Root, text="P8*/32Bit",
                                                 variable=self.TK_Conversion_Format_Setting,
                                                 value=FORMAT_P8, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_A8Y8 = Radiobutton(self.Format_to_Convert_to_Root, text="A8Y8*",
                                              variable=self.TK_Conversion_Format_Setting,
                                              value=FORMAT_A8Y8, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_AY8 = Radiobutton(self.Format_to_Convert_to_Root, text="AY8*",
                                             variable=self.TK_Conversion_Format_Setting,
                                             value=FORMAT_AY8, command=self.Set_Format_to_Save_as_Variable)
        self.Radio_Save_as_A8_or_Y8 = Radiobutton(self.Format_to_Convert_to_Root, text="A8/Y8*",
                                                  variable=self.TK_Conversion_Format_Setting,
                                                  value=FORMAT_A8, command=self.Set_Format_to_Save_as_Variable)

        self.Checkbox_Mipmap_Gen = Checkbutton(self.Format_to_Convert_to_Root, text="Mipmap Gen",
                                               variable=self.TK_Mipmap_Gen_Setting, onvalue=1, offvalue=0,
                                               command=self.Set_Mipmap_Gen_Setting_Variable)        
        self.Option_Menu_Extract_to = OptionMenu(self.Format_to_Convert_to_Root, self.TK_Target_Extract_Format,
                                                 ' ', 'DDS', 'TGA', command=self.Set_Target_Extract_Variable)

        self.Option_Menu_Extract_to.config(width=3)

        self.Radio_Dont_Change_Format.place(x=5, y=24, anchor=NW)
        self.Radio_Save_as_DXT1.place(x=84, y=24, anchor=NW)
        self.Radio_Save_as_DXT3.place(x=138, y=24, anchor=NW)
        self.Radio_Save_as_DXT5.place(x=188, y=24, anchor=NW)
        self.Radio_Save_as_R5G6B5.place(x=5, y=52, anchor=NW)
        self.Radio_Save_as_A1R5G5B5.place(x=68, y=52, anchor=NW)
        self.Radio_Save_as_A4R4G4B4.place(x=150, y=52, anchor=NW)
        self.Radio_Save_as_P8_Bump.place(x=5, y=78, anchor=NW)
        self.Radio_Save_as_A8Y8.place(x=78, y=78, anchor=NW)
        self.Radio_Save_as_AY8.place(x=132, y=78, anchor=NW)
        self.Radio_Save_as_A8_or_Y8.place(x=180, y=78, anchor=NW)
        
        self.Checkbox_Mipmap_Gen.place(x=10, y=106, anchor=NW)
        self.Option_Menu_Extract_to.place(x=160, y=103, anchor=NW)
        
        self.Extract_to_Text = self.Format_to_Convert_to_Root.create_text(105, 110, anchor="nw")
        self.Format_to_Convert_to_Root.itemconfig(self.Extract_to_Text, text="Extract to:")  

        
        #--------------------------------------------------------------

        #Create SCAN STATUS field
        self.Scan_Status_Root = Canvas(self, width=495, height=65, highlightthickness=0)
        self.Scan_Status_Root.place(x=1, y=286, anchor=NW)
        self.Scan_Status_Text_1 = self.Scan_Status_Root.create_text(5, 5, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_1, text="2D bitmaps found:-")    
        self.Scan_Status_Text_2 = self.Scan_Status_Root.create_text(5, 25, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_2, text="3D bitmaps found:-")    
        self.Scan_Status_Text_3 = self.Scan_Status_Root.create_text(5, 45, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_3, text="Cubemaps found: -")
        
        self.Scan_Status_Text_4 = self.Scan_Status_Root.create_text(150, 45, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_4, text="Elapsed time:--")
        self.Scan_Status_Text_5 = self.Scan_Status_Root.create_text(150, 25, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_5, text="Total bitmaps:-")
        self.Scan_Status_Text_6 = self.Scan_Status_Root.create_text(150, 5, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_6, text="Total data:-----")
        
        self.Scan_Status_Text_8 = self.Scan_Status_Root.create_text(310, 25, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_8, text="Remaining bitmaps:-")    
        self.Scan_Status_Text_9 = self.Scan_Status_Root.create_text(310, 5, anchor="nw")
        self.Scan_Status_Root.itemconfig(self.Scan_Status_Text_9, text="Remaining data:-----")

        self.Text_Scan_Status_2D_Bitmaps_Found = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=6)
        self.Text_Scan_Status_2D_Bitmaps_Found.place(x=100, y=5, anchor=NW)
        self.Text_Scan_Status_3D_Bitmaps_Found = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=6)
        self.Text_Scan_Status_3D_Bitmaps_Found.place(x=100, y=25, anchor=NW)
        self.Text_Scan_Status_Cubemaps_Found = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=6)
        self.Text_Scan_Status_Cubemaps_Found.place(x=100, y=45, anchor=NW)

        self.Text_Scan_Status_Elapsed_Time = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=11)
        self.Text_Scan_Status_Elapsed_Time.place(x=225, y=45, anchor=NW)
        self.Text_Scan_Status_Total_Bitmaps = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=11)
        self.Text_Scan_Status_Total_Bitmaps.place(x=225, y=25, anchor=NW)
        self.Text_Scan_Status_Total_Data = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=11)
        self.Text_Scan_Status_Total_Data.place(x=225, y=5, anchor=NW)

        self.Text_Scan_Status_Remaining_Bitmaps = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=11)
        self.Text_Scan_Status_Remaining_Bitmaps.place(x=410, y=25, anchor=NW)
        self.Text_Scan_Status_Remaining_Data = Text(self.Scan_Status_Root, height=1, bg='#ece9d8', state=DISABLED, width=11)
        self.Text_Scan_Status_Remaining_Data.place(x=410, y=5, anchor=NW)
        #--------------------------------------------------------------

        #Create DISPLAYED INFO field
        self.Current_Tag_Root = Canvas(self, width=500, height=55)
        self.Current_Tag_Root.place(x=0, y=354, anchor=NW)

        self.Displayed_Info_Text_Box = Text(self.Current_Tag_Root, height=3, bg='#ece9d8', state=NORMAL, width=70)
        self.Displayed_Info_Text_Box.insert(INSERT, self.Displayed_Info_String)
        self.Displayed_Info_Text_Box.config(state=DISABLED)
        self.Displayed_Info_Text_Box.place(x=0, y=0, anchor=NW)

        
        self.Disable_Settings_Window_Buttons()
        self.tag_list_window = Bitmap_Converter_List_Window(Handler, self)
        self.help_window = Bitmap_Converter_Help_Window(self)
        
        self.tag_data_canvas = Bitmap_Converter_Data_Window(Handler, self)
        self.tag_data_canvas.place(x=495, y=2, anchor=NW)

        self.Child_Windows = (self.tag_list_window,)
        self.Close_Help()

        self.bind("<Map>", self._Maximize_Children)
        self.bind("<Unmap>", self._Minimize_Children)

        self.tag_list_window.bind("<Map>", self.tag_list_window._Maximize_Parent)
        self.tag_list_window.bind("<Unmap>", self.tag_list_window._Minimize_Parent)


        #Create and start the window update thread
        self.Window_Docking_Thread = threading.Thread(target=self._Window_Docking_Daemon)
        self.Window_Docking_Thread.daemon = True
        self.Window_Docking_Thread.start()

        #Create and start the window update thread
        self.Window_Update_Thread = threading.Thread(target=self._Main_Window_Update)
        self.Window_Update_Thread.daemon = True
        self.Window_Update_Thread.start()

        self.Mini_Maxi_State_Changing = False


    def _Minimize_Children(self, *args):
        Minimize_Maximize_Children_with_Parent(self, self.Child_Windows, "MIN")
    def _Maximize_Children(self, *args):
        Minimize_Maximize_Children_with_Parent(self, self.Child_Windows, "MAX")


    def _Window_Docking_Daemon(self):
        '''AFTER THE WINDOW IS CREATED THIS FUNCTION WILL
        LOOP CONTINUOUSLY DOCK MOVEMENT OF CHILD WINDOWS'''
        while not self.Handler.Close_Program:
            #we don't want it to run too often or it'll be laggy
            sleep(self.Window_Docking_Interval)
            
            #calls a function to lock the position of the provided child windows to the provided parent window
            if not(self.Window_Docking_Updating):
                self.after(0, (lambda:(self.Dock_Window_Movement(self, self.Child_Windows))))


    def _Main_Window_Update(self):
        '''AFTER THE WINDOW IS CREATED THIS FUNCTION WILL
        LOOP CONTINUOUSLY AND UPDATE ALL INFO IT'''
        while not self.Handler.Close_Program:
            #we don't want it to run too often or it'll be laggy
            sleep(self.Window_Update_Interval)
                
            #if the program is being told to display new, literal text
            if self.Display_New_Text:
                if not(self.Window_Updating):
                    self.after(0, (lambda:(self.Update_Bitmap_Converter_Main_Window(self.Handler.Current_Tag))))
                    self.Display_New_Text = False
            else:
                if self.Proceed_with_Conversion:
                    if self.Tags_Indexed:
                        if self.Tags_Loaded:
                            if (self.Handler.Default_Conversion_Flags["bitm"]["READ ONLY"]):
                                update_string = "Compiling detailed list of all tags: "
                            else:
                                update_string = "Processing tag: " + self.Handler.Current_Tag
                        else:
                            if self.Tags_Indexed:
                                update_string = "Tags indexed... Loading: " + self.Handler.Current_Tag
                                self.Total_Bitmaps = self.Handler.Tags_Indexed
                                self.Remaining_Bitmaps = self.Handler.Tags_Loaded
                            else:
                                update_string = ""
                    else:
                        update_string = "Searching for bitmap tags... Currently looking at: " + self.Handler.Current_Tag
                        self.Total_Bitmaps = self.Handler.Tags_Indexed

                    if not(self.Window_Updating):
                        self.after(0, (lambda:(self.Update_Bitmap_Converter_Main_Window(update_string))))


            
    #This function is to make the window to browse for the tags folder
    def Make_Bitmap_Converter_Browse(self):
        if not(self.Proceed_with_Conversion):
            Tags_Dir_Str = tkinter.filedialog.askdirectory(initialdir=self.Handler.Tags_Directory,
                                                           title='Select a folder containing bitmap tags')
            Tags_Dir_Str = Tags_Dir_Str.replace('/', '\\')
            if(len(Tags_Dir_Str)):
                if Tags_Dir_Str[-1] != '\\':
                    Tags_Dir_Str += "\\"
                self.Tags_Directory_Field.config(state=NORMAL)
                self.Tags_Directory_Field.delete(0,END)
                self.Tags_Directory_Field.insert(0,Tags_Dir_Str)
                self.Handler.Tags_Directory = self.Tags_Directory_Field.get()
                self.Handler.Data_Directory = (self.Handler.Tags_Directory.split(os.path.basename
                                                                                (os.path.normpath(
                                                                                    self.Handler.Tags_Directory)))[0] + "data")
                self.Tags_Directory_Field.config(state=DISABLED)


    def Show_Bitmap_Converter_Help(self):
        try:
            self.help_window.update()
            self.help_window.deiconify()
        except: pass

    def Close_Help(self):
        try: self.help_window.withdraw()
        except: pass
            
    def Close_Main_Window(self):
        self.Proceed_with_Conversion = False
        self.Handler.Close_Program = True
        self.destroy()


    #this function applies the xbox and swizzle conversion flags to all bitmaps
    def Save_All_Tags_as(self):
        if self.Tags_Loaded:
            Bitmap_Collection = self.Handler.Tag_Collection["bitm"]
            
            for Index in range(len(self.tag_list_window.Displayed_Tag_Index_Mapping)):
                Tag_Path = self.tag_list_window.Displayed_Tag_Index_Mapping[Index]
                Bitmap_Collection[Tag_Path].Tag_Conversion_Settings["PLATFORM"] = self.save_all_tags_as
                Bitmap_Collection[Tag_Path].Tag_Conversion_Settings["SWIZZLED"] = self.save_all_tags_as
                self.tag_list_window.Set_Listbox_Entry_Color(Index, Tag_Path)
              
            if self.save_all_tags_as:
                self.menubar.entryconfig(2, label="Toggle All Tags to PC Format")
            else:
                self.menubar.entryconfig(2, label="Toggle All Tags to XBOX Format")

            self.save_all_tags_as = not(self.save_all_tags_as)

            if len(self.tag_list_window.Selected_Tags):
                if Bitmap_Collection[self.tag_list_window.Selected_Tags[0]].Tag_Conversion_Settings["PLATFORM"]:
                    self.Radio_Save_as_Xbox.select()
                else:
                    self.Radio_Save_as_PC.select()
                    
                if Bitmap_Collection[self.tag_list_window.Selected_Tags[0]].Tag_Conversion_Settings["SWIZZLED"]:
                    self.Radio_Save_as_Swizzled.select()
                else:
                    self.Radio_Save_as_Unswizzled.select()

        
    def Toggle_Window_Docking(self):
        if self.docking_state:
            self.docking_state = False
            self.menubar.entryconfig(3, label="Dock Windows")
        else:
            self.docking_state = True
            self.menubar.entryconfig(3, label="Un-dock Windows")


    def Invert_Selection(self):
        self.tag_list_window.Invert_Selection()
            

    #These function disables all buttons when starting a scan
    def Bitmap_Converter_Run_Pressed(self):
        if self.Proceed_with_Conversion:
            if self.Tags_Loaded and not(self.Handler.Default_Conversion_Flags["bitm"]["READ ONLY"]):
                self.Bitmap_Converter_Cancel_Conversion()
        else:
            if not(self.Conversion_Cancelled):
                self.Proceed_with_Conversion = True
                
                self.Close_Help()
                self.Disable_Global_Settings()
                self.Disable_Settings_Window_Buttons()
                
                if self.Tags_Loaded:
                    if self.Handler.Default_Conversion_Flags["bitm"]["READ ONLY"]:
                        self.btn_start.config(text="Logging")
                    else:
                        self.btn_start.config(text="Cancel")
                else:
                    self.btn_start.config(text="Indexing")
                    self.btn_browse.config(state=DISABLED)
                    self.btn_start.config(state=DISABLED)


    #These function enables all buttons when a scan finishes
    def Bitmap_Converter_Finish_Scanning(self):
        self.Proceed_with_Conversion = False
        
        self.Display_New_Text = True
        self.btn_start.config(state=NORMAL)
        self.btn_start.config(text="Run")
        self.Enable_Global_Settings()
        self.Enable_Settings_Window_Buttons()

    #These function enables all buttons when a conversion finishes
    def Bitmap_Converter_Finish_Conversion(self):
        self.Handler.Reset_Tags()
        self.Tags_Indexed = False
        self.Tags_Loaded = False
        self.Proceed_with_Conversion = False
        
        self.tag_list_window.Initialize_Tag_Sort_Mappings()
        self.tag_list_window.Reset_Lists()
        
        self.Display_New_Text = True
        self.btn_start.config(text="Load")
        self.btn_start.config(state=NORMAL)
        self.btn_browse.config(state=NORMAL)
        self.Enable_Global_Settings()

    #These function enables all buttons when a conversion is cancelled
    def Bitmap_Converter_Cancel_Conversion(self):
        self.Handler.Current_Tag = "Cancelling conversion... Please wait..."
        self.btn_start.config(text="Wait...")
        self.Display_New_Text = True
        self.Proceed_with_Conversion = False
        
        self.Conversion_Cancelled = True

    def Disable_Global_Settings(self):
        for Widget in(self.Checkbox_Dont_Reprocess_Tags,self.Checkbox_Backup_Old_Tags,
                      self.Checkbox_Read_Only,self.Checkbox_Write_Debug_Log):
            Widget.config(state=DISABLED)
            
    def Enable_Global_Settings(self):
        for Widget in(self.Checkbox_Dont_Reprocess_Tags,self.Checkbox_Backup_Old_Tags,
                      self.Checkbox_Read_Only,self.Checkbox_Write_Debug_Log):
            Widget.config(state=NORMAL)

    def Disable_Settings_Window_Buttons(self):
        for Widget in(self.Radio_Save_as_Xbox,self.Radio_Save_as_PC,self.Radio_Save_as_Swizzled,
                      self.Radio_Save_as_Unswizzled,self.Spinbox_Times_to_Halve_Resolution,
                      self.Radio_Dont_Swap_Multipurpose,self.Radio_Swap_Multipurpose_to_Xbox,self.Radio_Swap_Multipurpose_to_PC,
                      self.Spinbox_Alpha_Cutoff_Bias,self.Radio_Auto_Bias_Mode,self.Radio_Average_Bias_Mode,
                      self.Radio_Keep_Intensity_Channel,self.Radio_Keep_Alpha_Channel,
                      self.Checkbox_Swap_A8Y8_Channels,self.Checkbox_Preserve_CK_Transparency,
                      self.Radio_Dont_Change_Format,self.Radio_Save_as_DXT1,self.Radio_Save_as_DXT3,
                      self.Radio_Save_as_DXT5,self.Radio_Save_as_R5G6B5,self.Radio_Save_as_A1R5G5B5,
                      self.Radio_Save_as_A4R4G4B4,self.Radio_Save_as_P8_Bump,self.Radio_Save_as_A8Y8,
                      self.Radio_Save_as_AY8,self.Radio_Save_as_A8_or_Y8, self.Option_Menu_Extract_to,
                      self.Checkbox_Mipmap_Gen):
            Widget.config(state=DISABLED)


    def Enable_Settings_Window_Buttons(self):
        Widget_List = (self.Radio_Save_as_Xbox,self.Radio_Save_as_PC,self.Radio_Save_as_Swizzled,
                       self.Radio_Save_as_Unswizzled,self.Spinbox_Times_to_Halve_Resolution,
                       self.Radio_Dont_Swap_Multipurpose,self.Radio_Swap_Multipurpose_to_Xbox,self.Radio_Swap_Multipurpose_to_PC,
                       self.Spinbox_Alpha_Cutoff_Bias,self.Radio_Auto_Bias_Mode,self.Radio_Average_Bias_Mode,
                       self.Radio_Keep_Intensity_Channel,self.Radio_Keep_Alpha_Channel,
                       self.Checkbox_Swap_A8Y8_Channels,self.Checkbox_Preserve_CK_Transparency,
                       self.Radio_Dont_Change_Format,self.Radio_Save_as_DXT1,self.Radio_Save_as_DXT3,
                       self.Radio_Save_as_DXT5,self.Radio_Save_as_R5G6B5,self.Radio_Save_as_A1R5G5B5,
                       self.Radio_Save_as_A4R4G4B4,self.Radio_Save_as_P8_Bump,self.Radio_Save_as_A8Y8,
                       self.Radio_Save_as_AY8, self.Radio_Save_as_A8_or_Y8, self.Option_Menu_Extract_to,
                       self.Checkbox_Mipmap_Gen)

        for Widget in Widget_List:
            Widget.config(state=NORMAL)
        
        self.Spinbox_Times_to_Halve_Resolution.config(state="readonly")
        self.Spinbox_Alpha_Cutoff_Bias.config(state="readonly")


    #this function selects the proper buttons based on what tag has been selected
    #if multiple tags have been selected this function is skipped
    def Select_Proper_Settings_Window_Settings(self):
        Bitmap_Collection = self.Handler.Tag_Collection["bitm"]
        Widget_List = []

        Tag = self.Handler.Tag_Collection["bitm"][self.tag_list_window.Selected_Tags[0]]
        Conversion_Flags = Tag.Tag_Conversion_Settings
        
        if Tag.Bitmap_Count() != 0 and Tag.Bitmap_Format() == 14:
            Conversion_Flags["CK TRANS"] = True
            self.TK_Preserve_CK_Transparency.set(1)

        if Conversion_Flags["PLATFORM"]:
            self.Radio_Save_as_Xbox.select()
        else: self.Radio_Save_as_PC.select()
            
        if Conversion_Flags["SWIZZLED"]:
            self.Radio_Save_as_Swizzled.select()
        else: self.Radio_Save_as_Unswizzled.select()
            
        self.TK_Number_of_Times_to_Halve_Resolution.set(Conversion_Flags["DOWNRES"])
        
        if Conversion_Flags["MULTI SWAP"] == 1:
            self.Radio_Swap_Multipurpose_to_Xbox.select()
        elif Conversion_Flags["MULTI SWAP"] == 2:
            self.Radio_Swap_Multipurpose_to_PC.select()
        else: self.Radio_Dont_Swap_Multipurpose.select()
            
        self.TK_Alpha_Cutoff_Bias.set(Conversion_Flags["CUTOFF BIAS"])
        
        if Conversion_Flags["P8 MODE"]:
            self.Radio_Average_Bias_Mode.select()
        else: self.Radio_Auto_Bias_Mode.select()
            
        if Conversion_Flags["MONO KEEP"]:
            self.Radio_Keep_Alpha_Channel.select()
        else: self.Radio_Keep_Intensity_Channel.select()
            
        if Conversion_Flags["MONO SWAP"]:
            self.TK_Swap_A8Y8_Alpha_and_Intensity.set(1)
        else: self.TK_Swap_A8Y8_Alpha_and_Intensity.set(0)
            
        if Conversion_Flags["CK TRANS"]:
            self.TK_Preserve_CK_Transparency.set(1)
        else: self.TK_Preserve_CK_Transparency.set(0)
            
        if Conversion_Flags["NEW FORMAT"] == FORMAT_DXT1:
            self.Radio_Save_as_DXT1.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_DXT3:
            self.Radio_Save_as_DXT3.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_DXT5:
            self.Radio_Save_as_DXT5.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_R5G6B5:
            self.Radio_Save_as_R5G6B5.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_A1R5G5B5:
            self.Radio_Save_as_A1R5G5B5.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_A4R4G4B4:
            self.Radio_Save_as_A4R4G4B4.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_P8:
            self.Radio_Save_as_P8_Bump.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_A8Y8:
            self.Radio_Save_as_A8Y8.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_AY8:
            self.Radio_Save_as_AY8.select()
        elif Conversion_Flags["NEW FORMAT"] == FORMAT_A8:
            self.Radio_Save_as_A8_or_Y8.select()
        else:
            self.Radio_Dont_Change_Format.select()

        self.TK_Target_Extract_Format.set(Conversion_Flags["EXTRACT TO"])
        
        self.TK_Mipmap_Gen_Setting.set(Conversion_Flags["MIP GEN"])
            

    #This function updates all the information in the main window's widgets
    def Update_Bitmap_Converter_Main_Window(self, NewText=None):
        self.Window_Updating = True
            
        #Update the message text if supplied with a non-blank string
        if (NewText is not None and NewText!=(self.Displayed_Info_Text_Box.get('0.0',END+"-1c"))):
            self.Displayed_Info_Text_Box.config(state=NORMAL)
            self.Displayed_Info_Text_Box.delete('0.0', END)
            self.Displayed_Info_Text_Box.insert(INSERT, NewText)
            self.Displayed_Info_Text_Box.config(state=DISABLED)

        
        self.Elapsed_Time = int(time() - self.Scan_Start_Time)
        
        Elapsed_Time_String = (str(self.Elapsed_Time//3600)+"h:"+
                               str((self.Elapsed_Time%3600)//60)+"m:"+
                               str(self.Elapsed_Time%60)+"s")
        
        Total_Pixel_Data_String = (str(self.Total_Pixel_Data_to_Process//1048576)[:9]+"MB")
        Remaining_Pixel_Data_String = Tempstring = (str(self.Remaining_Pixel_Data_to_Process//1048576)[:9]+"MB")

        Widget_Values = (self.Bitmaps_Found_2D, self.Bitmaps_Found_3D, self.Cubemaps_Found,
                         self.Total_Bitmaps, self.Remaining_Bitmaps, Elapsed_Time_String,
                         Total_Pixel_Data_String, Remaining_Pixel_Data_String)
        Widgets = (self.Text_Scan_Status_2D_Bitmaps_Found, self.Text_Scan_Status_3D_Bitmaps_Found,
                   self.Text_Scan_Status_Cubemaps_Found, self.Text_Scan_Status_Total_Bitmaps,
                   self.Text_Scan_Status_Remaining_Bitmaps, self.Text_Scan_Status_Elapsed_Time,
                   self.Text_Scan_Status_Total_Data, self.Text_Scan_Status_Remaining_Data)

        for i in range(len(Widget_Values)):
            if (Widgets[i].get('0.0',END+"-1c") != str(Widget_Values[i])):
                Widgets[i].config(state=NORMAL)
                Widgets[i].delete('0.0', END)
                Widgets[i].insert(INSERT, str(Widget_Values[i]))
                Widgets[i].config(state=DISABLED)

        self.Window_Updating = False




    """
    THESE NEXT FUNCTIONS ARE FOR CHANGING CONVERSION VARIABLES BASED ON WHICH SETTING IS CLICKED
    """


    def Set_Dont_Reprocess_Tags_Variable(self):
        self.Handler.Default_Conversion_Flags["bitm"]["DONT REPROCESS"] = self.TK_Dont_Reprocess_Tags.get()
        self._Set_Selection_Color(range(len(self.tag_list_window.Displayed_Tag_Index_Mapping)))
        
    def Set_Backup_Old_Tags_Variable(self):
        self.Handler.Default_Conversion_Flags["bitm"]["RENAME OLD"] = self.TK_Backup_Edited_Tags.get()
        
    def Set_Read_Only_Variable(self):
        self.Handler.Default_Conversion_Flags["bitm"]["READ ONLY"] = self.TK_Read_Only.get()
        if self.TK_Read_Only.get():
            if not self.Handler.Default_Conversion_Flags["bitm"]["WRITE LOG"]:
                self.Checkbox_Write_Debug_Log.select()
            self.Checkbox_Write_Debug_Log.config(state=DISABLED)
        else:
            self.Checkbox_Write_Debug_Log.config(state=NORMAL)
        self._Set_Selection_Color(range(len(self.tag_list_window.Displayed_Tag_Index_Mapping)))
        
    def Set_Write_Debug_Log_Variable(self):
        if self.Handler.Default_Conversion_Flags["bitm"]["READ ONLY"]:
            self.Checkbox_Write_Debug_Log.select()
            self.Checkbox_Write_Debug_Log.config(state=DISABLED)
        else:
            self.Handler.Default_Conversion_Flags["bitm"]["WRITE LOG"] = self.TK_Write_Debug_Log.get()
        
    def Set_Platform_to_Save_as_Variable(self):
        self._Set_Selection_Flag("PLATFORM", self.TK_Platform_to_Save_as, bool)
        self._Set_Selection_Color()
        
    def Set_Swizzle_Mode_Variable(self):
        self._Set_Selection_Flag("SWIZZLED", self.TK_Swizzle_Bitmap, bool)
        self._Set_Selection_Color()
        
    def Set_Number_of_Times_to_Halve_Variable(self):
        self._Set_Selection_Flag("DOWNRES", self.TK_Number_of_Times_to_Halve_Resolution)
        self._Set_Selection_Color()
        
    def Set_Multipurpose_Swap_Variable(self):
        self._Set_Selection_Flag("MULTI SWAP", self.TK_Multipurpose_Swap_Setting)
        self._Set_Selection_Color()
        
    def Set_Alpha_Cutoff_Bias_Variable(self):
        self._Set_Selection_Flag("CUTOFF BIAS", self.TK_Alpha_Cutoff_Bias)
        
    def Set_P8_Conversion_Mode_Variable(self):
        self._Set_Selection_Flag("P8 MODE", self.TK_P8_Conversion_Mode, bool)
                
    def Set_Monochrome_Channel_to_Keep_Variable(self):
        self._Set_Selection_Flag("MONO KEEP", self.TK_Channel_to_Keep, bool)
        
    def Set_Swap_Alpha_and_Intensity_Variable(self):
        self._Set_Selection_Flag("MONO SWAP", self.TK_Swap_A8Y8_Alpha_and_Intensity, bool)
        self._Set_Selection_Color()
        
    def Set_Preserve_CK_Transparency_Variable(self):
        self._Set_Selection_Flag("CK TRANS", self.TK_Preserve_CK_Transparency, bool)
        
    def Set_Format_to_Save_as_Variable(self):
        self._Set_Selection_Flag("NEW FORMAT", self.TK_Conversion_Format_Setting)
        self._Set_Selection_Color()
        
    def Set_Mipmap_Gen_Setting_Variable(self):
        self._Set_Selection_Flag("MIP GEN", self.TK_Mipmap_Gen_Setting)
        self._Set_Selection_Color()
        
    def Set_Target_Extract_Variable(self, *args):
        self._Set_Selection_Flag("EXTRACT TO", self.TK_Target_Extract_Format)
        self._Set_Selection_Color()

    def _Set_Selection_Flag(self, Flag_Name, Window_Var, Type=None):
        for Tag_Path in self.tag_list_window.Selected_Tags:
            Flags = self.Handler.Tag_Collection["bitm"][Tag_Path].Tag_Conversion_Settings
            if Type: Flags[Flag_Name] = Type(Window_Var.get())
            else:    Flags[Flag_Name] = Window_Var.get()

    def _Set_Selection_Color(self, Indexes = None):
        if Indexes is None:
            Indexes = self.tag_list_window.Tag_List_Listbox.curselection()
        for Index in Indexes:
            Tag_Path = self.tag_list_window.Displayed_Tag_Index_Mapping[int(Index)]
            self.tag_list_window.Set_Listbox_Entry_Color(Index, Tag_Path)



class Bitmap_Converter_Data_Window(Canvas):

    def __init__(self, Handler, Parent, **options):
        options.update({"width":250, "height":155, "highlightthickness":0})
        Canvas.__init__(self, Parent, **options )
        
        '''THE PARENT MUST BE A PROGRAM CLASS WITH VARIABLES SUCH AS TAG_COLLECTION'''
        self.Handler = Handler
        self.Parent = Parent

        self.TK_Selected_Bitmap_Index = StringVar(self)
        self.TK_Selected_Bitmap_Index.set("")

        #--------------------------------------------------------------
        
        #Create BITMAP INDEX SELECTION field

        self.Tag_Data_Selected_Bitmap_Data_Root = Canvas(self, width=236, height=142, highlightthickness=0)
        self.Tag_Data_Selected_Bitmap_Data_Root.config(bd=2, relief=GROOVE)
        self.Tag_Data_Selected_Bitmap_Data_Root.place(x=5, y=2, anchor=NW)
        self.Tag_Data_Selected_Bitmap_Data_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(60, 28, anchor="nw")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Selected_Bitmap_Data_Text, text="Selected Bitmap Information")

        self.Tag_Data_Selected_Bitmap_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(8, 7, anchor="nw")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Selected_Bitmap_Text, text="Current bitmap:"+" "*14 + "out of:")
        
        self.Selected_Bitmap_Index = Spinbox(self.Tag_Data_Selected_Bitmap_Data_Root, from_=0, to=0, width=2,
                                             textvariable=self.TK_Selected_Bitmap_Index, state="readonly",
                                             command=self.Display_Selected_Bitmap)
        self.Tag_Data_Bitmap_Count_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=2)
        self.Selected_Bitmap_Index.place(x=90, y=7, anchor=NW)
        self.Tag_Data_Bitmap_Count_Box.place(x=165, y=7, anchor=NW)

        #--------------------------------------------------------------
        #Create SELECTED BITMAP DATA field

        self.Tag_Data_Height_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(10, 48, anchor="nw")
        self.Tag_Data_Width_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(10, 71, anchor="nw")
        self.Tag_Data_Depth_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(10, 94, anchor="nw")
        self.Tag_Data_Mipmaps_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(10, 119, anchor="nw")
        self.Tag_Data_Type_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(125, 48, anchor="nw")
        self.Tag_Data_Format_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(115, 71, anchor="nw")
        self.Tag_Data_Swizzled_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(110, 94, anchor="nw")
        self.Tag_Data_Platform_Text = self.Tag_Data_Selected_Bitmap_Data_Root.create_text(110, 119, anchor="nw")
        
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Height_Text, text="Height:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Width_Text, text="Width:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Depth_Text, text="Depth:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Type_Text, text="Type:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Format_Text, text="Format:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Swizzled_Text, text="Swizzled:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Mipmaps_Text, text="Mipmaps:")
        self.Tag_Data_Selected_Bitmap_Data_Root.itemconfig(self.Tag_Data_Platform_Text, text="Platform:")

        self.Tag_Data_Height_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=5)
        self.Tag_Data_Width_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=5)
        self.Tag_Data_Depth_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=5)
        self.Tag_Data_Mipmaps_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=5)
        self.Tag_Data_Type_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=8)
        self.Tag_Data_Format_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=8)
        self.Tag_Data_Swizzled_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=8)
        self.Tag_Data_Platform_Box = Text(self.Tag_Data_Selected_Bitmap_Data_Root, height=1, bg='#ece9d8', state=DISABLED, width=8)
        
        self.Tag_Data_Height_Box.place(x=58, y=46, anchor=NW)
        self.Tag_Data_Width_Box.place(x=58, y=69, anchor=NW)
        self.Tag_Data_Depth_Box.place(x=58, y=92, anchor=NW)
        self.Tag_Data_Mipmaps_Box.place(x=58, y=115, anchor=NW)
        self.Tag_Data_Type_Box.place(x=160, y=46, anchor=NW)
        self.Tag_Data_Format_Box.place(x=160, y=69, anchor=NW)
        self.Tag_Data_Swizzled_Box.place(x=160, y=92, anchor=NW)
        self.Tag_Data_Platform_Box.place(x=160, y=115, anchor=NW)
        
                    
    #when called this function will update the info in the tag data box to show the single tag that is selected
    def Display_Selected_Bitmap(self):
        Handler = self.Handler
        Selection = self.Parent.tag_list_window.Tag_List_Listbox.curselection()
        #only run if just 1 bitmap is selected
        if len(Selection) == 1:
            Tag_Path = self.Parent.tag_list_window.Displayed_Tag_Index_Mapping[int(Selection[0])]
            Tag = Handler.Tag_Collection["bitm"][Tag_Path]
            
            #only run if the tag contains bitmaps
            Bitmap_Count = Tag.Bitmap_Count()
            if Bitmap_Count:
                for Widget in(self.Tag_Data_Height_Box, self.Tag_Data_Width_Box, self.Tag_Data_Depth_Box,
                              self.Tag_Data_Mipmaps_Box, self.Tag_Data_Type_Box, self.Tag_Data_Format_Box,
                              self.Tag_Data_Swizzled_Box, self.Tag_Data_Platform_Box,self.Tag_Data_Bitmap_Count_Box):
                    Widget.config(state=NORMAL)

                self.Selected_Bitmap_Index.config(to=(Bitmap_Count-1))
                Bitmap_Block_Index = int(self.Selected_Bitmap_Index.get())
                Type = Tag.Bitmap_Type(Bitmap_Block_Index)
                Format = Tag.Bitmap_Format(Bitmap_Block_Index)

                for widg in (self.Tag_Data_Bitmap_Count_Box, self.Tag_Data_Height_Box,
                             self.Tag_Data_Width_Box, self.Tag_Data_Depth_Box,
                             self.Tag_Data_Mipmaps_Box, self.Tag_Data_Type_Box,
                             self.Tag_Data_Swizzled_Box, self.Tag_Data_Format_Box,
                             self.Tag_Data_Platform_Box):
                    widg.delete('1.0', END)
                
                self.Tag_Data_Bitmap_Count_Box.insert(INSERT, str(Bitmap_Count-1))
                self.Tag_Data_Height_Box.insert(INSERT, str(Tag.Bitmap_Height(Bitmap_Block_Index)))
                self.Tag_Data_Width_Box.insert(INSERT, str(Tag.Bitmap_Width(Bitmap_Block_Index)))
                self.Tag_Data_Depth_Box.insert(INSERT, str(Tag.Bitmap_Depth(Bitmap_Block_Index)))
                self.Tag_Data_Mipmaps_Box.insert(INSERT, str(Tag.Bitmap_Mipmaps_Count(Bitmap_Block_Index)))
                self.Tag_Data_Swizzled_Box.insert(INSERT, str(Tag.Swizzled()).upper())
                self.Tag_Data_Format_Box.insert(INSERT, Bitmap_Format_Strings[Format])

                if Type < len(Bitmap_Short_Type_Strings):
                    self.Tag_Data_Type_Box.insert(INSERT, Bitmap_Short_Type_Strings[Type])
                else:
                    self.Tag_Data_Type_Box.insert(INSERT, "UNKNOWN")
                    
                if Tag.Is_Xbox_Bitmap:
                    if Tag.Processed_by_Reclaimer():
                        self.Tag_Data_Platform_Box.insert(INSERT, 'XBOX')
                    else:
                        self.Tag_Data_Platform_Box.insert(INSERT, 'ARSENIC')
                else:
                    self.Tag_Data_Platform_Box.insert(INSERT, 'PC')

                for Widget in(self.Tag_Data_Height_Box, self.Tag_Data_Width_Box, self.Tag_Data_Depth_Box,
                              self.Tag_Data_Mipmaps_Box, self.Tag_Data_Type_Box, self.Tag_Data_Format_Box,
                              self.Tag_Data_Swizzled_Box, self.Tag_Data_Platform_Box,self.Tag_Data_Bitmap_Count_Box):
                    Widget.config(state=DISABLED)





'''ENTER A DESCRIPTION FOR THIS CLASS WHEN I HAVE TIME'''
class Bitmap_Converter_List_Window(Toplevel):

    def __init__(self, Handler, Parent, **options):
        Toplevel.__init__(self, Parent, **options )
        
        '''THE PROGRAM MUST BE CLASS WITH VARIABLES SUCH AS TAG_COLLECTION'''
        self.Handler = Handler
        self.Parent = Parent

        #used to determine if it is safe to try to populate the taglist window
        self.populating_tag_window = False
        #this is used for determining how the list is currently sorted
        self.tag_list_sort_type = 0
        #this is used for determining whether the list is reversed or not
        self.tag_list_sort_reversed = False
        unknown = "UNKNOWN FORMAT  "
        self.Bitmap_Format_Literals = ("A8"+" "*16, "Y8"+" "*16, "AY8"+" "*14, "A8Y8"+" "*12, unknown, unknown, "R5G6B5"+" "*7,
                                       unknown, "A1R5G5B5"+" "*2, "A4R4G4B4"+" "*2, "X8R8G8B8"+" "*3,"A8R8G8B8"+" "*3,
                                       unknown, unknown, "DXT1"+" "*12, "DXT3"+" "*12, "DXT5"+" "*12,"P8"+" "*16)
        self.Bitmap_Type_Literals = ("2D Bitmap   ", "3D Bitmap   ", "Cube Map    ", "White      ")
        
        
        self.Initialize_Tag_Sort_Mappings()
        
        self.protocol("WM_DELETE_WINDOW", self.Parent.Close_Main_Window)
        self.title("Tag List")

        self.Previous_Pos_X = 0
        self.Previous_Pos_Y = 457
        self.geometry("743x200+"+str(self.Previous_Pos_X)+"+"+str(self.Previous_Pos_Y))

        self.resizable(0, 1)
        self.minsize(width=743, height=200)
        self.maxsize(width=743, height=2048)

        #Make the menu bar
        self.tag_list_menubar = Menu(self)
        tag_list_menubar = self.tag_list_menubar
        
        tag_list_menubar.add_command(label="Sort by Path", command=lambda:(self.Sort_Displayed_Tags_by(0, True)) )
        tag_list_menubar.add_command(label="Sort by Type", command=lambda:(self.Sort_Displayed_Tags_by(2, True)) )
        tag_list_menubar.add_command(label="Sort by Format", command=lambda:(self.Sort_Displayed_Tags_by(4, True)) )
        tag_list_menubar.add_command(label="Sort by Pixel Data Bytes", command=lambda:(self.Sort_Displayed_Tags_by(6, True)) )
        
        self.Types_Settings_Menu = Menu(tag_list_menubar, tearoff=False)
        self.Formats_Settings_Menu = Menu(tag_list_menubar, tearoff=False)
        
        #we'll reference these locally to save screen space
        Types_Settings_Menu = self.Types_Settings_Menu
        Formats_Settings_Menu = self.Formats_Settings_Menu
        
        tag_list_menubar.add_cascade(label="Enable/Disable Types",underline=0, menu=Types_Settings_Menu)
        tag_list_menubar.add_cascade(label="Enable/Disable Formats",underline=0, menu=Formats_Settings_Menu)
        
        self.config(menu=tag_list_menubar)


        i = 0
        for Type in (0,1,2):
            Types_Settings_Menu.add_command(label=(Bitmap_Type_Strings[Type]+" "+u'\u2713'),
                                            command=lambda T=Type:self.Toggle_Types_Allowed(T) )
            
        for Format in (0,1,2,3,6,8,9,10,11,14,15,16,17):
            Formats_Settings_Menu.add_command(label=(Bitmap_Format_Strings[Format]+" "+u'\u2713'),
                                              command=lambda i=i, F=Format:self.Toggle_Formats_Allowed(i, F) )
            i += 1

        self.Tag_List_Scrollbar_Y = Scrollbar(self, orient="vertical")
        self.Tag_List_Scrollbar_X = Scrollbar(self, orient="horizontal")
        self.Tag_List_Listbox = Listbox(self, width=90, height=194,selectmode=EXTENDED,
                                        xscrollcommand=self.Tag_List_Scrollbar_X.set,
                                        yscrollcommand=self._Scroll_Tag_List, highlightthickness=0)
        
        self.Tag_Data_Listbox = Listbox(self, width=25, height=194,selectmode=EXTENDED,
                                        yscrollcommand=self._Scroll_Tag_Data, highlightthickness=0)
        
        self.Tag_List_Scrollbar_X.config(command=self.Tag_List_Listbox.xview)
        self.Tag_List_Scrollbar_Y.config(command=self._Scroll_Both_List_Boxes)

        self.Tag_List_Scrollbar_X.pack(side="bottom", fill="x")
        self.Tag_List_Scrollbar_Y.pack(side="right", fill="y")
        self.Tag_List_Listbox.pack(side="left",fill="both", expand=True)
        self.Tag_Data_Listbox.pack(side="right",fill="both", expand=True)
        self.Tag_List_Listbox.bind('<<ListboxSelect>>',self.Set_Selected_Tags_List )
        self.Tag_Data_Listbox.bind('<<ListboxSelect>>',self.Move_Selection_to_Paths_List )


    def _Minimize_Parent(self, *args):
        Minimize_Maximize_Children_with_Parent(self.Parent, self.Parent.Child_Windows, "MIN")
    def _Maximize_Parent(self, *args):
        Minimize_Maximize_Children_with_Parent(self.Parent, self.Parent.Child_Windows, "MAX")


    def Reset_Lists(self):
        self.Tag_List_Listbox.delete(0, END)
        self.Tag_Data_Listbox.delete(0, END)


    def Initialize_Tag_Sort_Mappings(self):
        #since the order of the displayed tags can vary based on how we want to display them,
        #we use this list to map the index's of the selected tags into the path of the tag 
        self.Displayed_Tag_Index_Mapping = []
        
        #this is used to store the paths of the tags that are selected. this makes
        #it easy to change the flags by iterating through the list and changing them
        self.Selected_Tags = []
        
        #there are 4 types and 18 formats
        self.Bitmap_Formats_Shown = [ True ]*18
        self.Bitmap_Types_Shown = [ True ]*4
        
        #we'll build these once the tags are loaded. they serve the same purpose
        #as the above list, to make it easy and fast to change the displayed tags
        self.Bitmaps_Indexed_By_Type_and_Format = [[],[],[],[]]
        for Type in range(4):
            for Format in range(18):
                self.Bitmaps_Indexed_By_Type_and_Format[Type].append([])
        self.Bitmaps_Indexed_By_Size = {}


    def Build_Tag_Sort_Mappings(self):
        #we want to build the different sort lists for the displaying of the tags
        for Tag_Path in self.Handler.Tag_Collection["bitm"]:
            #only run if the bitmap contains bitmaps
            Tag = self.Handler.Tag_Collection["bitm"][Tag_Path]
                
            Type = Tag.Bitmap_Type()
            Format = Tag.Bitmap_Format()

            #put together the lists that'll allow us to visually sort the tags in different ways
            Pixel_Data_Bytes = Tag.Pixel_Data_Bytes_Size()
            
            if not(Pixel_Data_Bytes in self.Bitmaps_Indexed_By_Size):
                self.Bitmaps_Indexed_By_Size[Pixel_Data_Bytes] = []

            self.Bitmaps_Indexed_By_Type_and_Format[Type][Format].append(Tag_Path)
            self.Bitmaps_Indexed_By_Size[Pixel_Data_Bytes].append(Tag_Path)


    def Set_Selected_Tags_List(self, event=None):
        '''used to set which tags are selected when the tags listbox
        is clicked so we can easily edit their conversion variables'''
        self.Selected_Tags = []
        Indexes = self.Tag_List_Listbox.curselection()
        if len(Indexes) > 1:
            for Index in Indexes:
                self.Selected_Tags.append(self.Displayed_Tag_Index_Mapping[int(Index)])
                
        elif len(Indexes) == 1:
            self.Selected_Tags = [self.Displayed_Tag_Index_Mapping[int(Indexes[0])]]

            self.Parent.Select_Proper_Settings_Window_Settings()
            
            self.Parent.tag_data_canvas.TK_Selected_Bitmap_Index.set("0")
            self.Parent.tag_data_canvas.Display_Selected_Bitmap()


    def Invert_Selection(self):
        if self.Parent.Tags_Loaded:
            self.Tag_List_Listbox.selection_clear(first=0, last=len(self.Displayed_Tag_Index_Mapping))
            
            for Index in range(len(self.Displayed_Tag_Index_Mapping)):
                Tag_Path = self.Displayed_Tag_Index_Mapping[Index]
                
                #if the index wasn't selected we select it
                if Tag_Path not in self.Selected_Tags:
                    self.Tag_List_Listbox.selection_set(Index)
            self.Set_Selected_Tags_List()


    #if we select a tag by clicking the data list we'll select it in the paths list instead
    def Move_Selection_to_Paths_List(self, event=None):
        if (len(self.Tag_Data_Listbox.curselection()) > 0 ):
            self.Tag_List_Listbox.selection_set(self.Tag_Data_Listbox.curselection()[0])
            self.Set_Selected_Tags_List()
        
        
    def Toggle_Types_Allowed(self, Type):
        if self.Bitmap_Types_Shown[Type]:
            self.Types_Settings_Menu.entryconfig(Type, label=(Bitmap_Type_Strings[Type]))
            self.Bitmap_Types_Shown[Type] = False
        else:
            self.Types_Settings_Menu.entryconfig(Type, label=(Bitmap_Type_Strings[Type]+" "+u'\u2713'))
            self.Bitmap_Types_Shown[Type] = True

        self.Sort_Displayed_Tags_by(self.tag_list_sort_type)
        
    def Toggle_Formats_Allowed(self, Menu_Element, Format):
        if self.Bitmap_Formats_Shown[Format]:
            self.Formats_Settings_Menu.entryconfig(Menu_Element, label=(Bitmap_Format_Strings[Format]))
            self.Bitmap_Formats_Shown[Format] = False
        else:
            self.Formats_Settings_Menu.entryconfig(Menu_Element, label=(Bitmap_Format_Strings[Format]+" "+u'\u2713'))
            self.Bitmap_Formats_Shown[Format] = True

        self.Sort_Displayed_Tags_by(self.tag_list_sort_type)


    def Sort_Displayed_Tags_by(self, Sort_By, Enable_Reverse=False):
        if self.Parent.Tags_Loaded and not(self.populating_tag_window):
            self.Displayed_Tag_Index_Mapping = []

            Formats_Shown  = self.Bitmap_Formats_Shown
            Types_Shown    = self.Bitmap_Types_Shown
            Display_Map    = self.Displayed_Tag_Index_Mapping
            By_Type_Format = self.Bitmaps_Indexed_By_Type_and_Format

            Bitm_Collection = self.Handler.Tag_Collection["bitm"]
            if Sort_By == 0:#sorting by path
                for Tag_Path in sorted(Bitm_Collection.keys()):
                    Tag = Bitm_Collection[Tag_Path]
                    #only run if the bitmap contains bitmaps
                    if Tag.Bitmap_Count()!= 0:
                        if Formats_Shown[Tag.Bitmap_Format()] and Types_Shown[Tag.Bitmap_Type()]:
                            Display_Map.append(Tag_Path)
                            
            elif Sort_By == 2:#sorting by type
                for Type in range(4):#loop through each format
                    for Format in range(18):
                        #only add the tag index to the list if we've enabled it
                        if Formats_Shown[Format] and Types_Shown[Type]:
                            Display_Map.extend(By_Type_Format[Type][Format])
                            
            elif Sort_By == 4:#sorting by format
                for Format in range(18):#loop through each format
                    for Type in range(4):
                        #only add the tag index to the list if we've enabled it
                        if Formats_Shown[Format] and Types_Shown[Type]:
                            Display_Map.extend(By_Type_Format[Type][Format])
                            
            else:#sorting by size
                Byte_Sizes_in_Order = sorted(self.Bitmaps_Indexed_By_Size)
                for Tag_Size in Byte_Sizes_in_Order:
                    for Tag_Path in self.Bitmaps_Indexed_By_Size[Tag_Size]:     
                        Tag = Bitm_Collection[Tag_Path]
                        
                        if Formats_Shown[Tag.Bitmap_Format()] and Types_Shown[Tag.Bitmap_Type()]:
                            Display_Map.append(Tag_Path)
                    
            self.tag_list_sort_type = Sort_By
            if not(self.tag_list_sort_reversed) and Enable_Reverse:
                self.tag_list_sort_reversed = True
                Display_Map.reverse()
            else:
                self.tag_list_sort_reversed = False
                
            self.Populate_Tag_List_Boxes()


    def Populate_Tag_List_Boxes(self):
        if not self.populating_tag_window:
            self.populating_tag_window = True
            self.Reset_Lists()

            #used to keep track of which index we are creating
            Current_Tag_List_Index = 0
            for Index in range(len(self.Displayed_Tag_Index_Mapping)):
                Tag_Path = self.Displayed_Tag_Index_Mapping[Index]
                
                self.Tag_List_Listbox.insert(END,Tag_Path)
                Tag = self.Handler.Tag_Collection["bitm"][Tag_Path]

                self.Set_Listbox_Entry_Color(END, Tag_Path)
                
                Current_Tag_List_Index += 1

                Bitmap_Type = Tag.Bitmap_Type()
                Bitmap_Format = Tag.Bitmap_Format()

                Tag_String = self.Bitmap_Type_Literals[Bitmap_Type] + self.Bitmap_Format_Literals[Bitmap_Format]

                Bitmap_Size = Tag.Pixel_Data_Bytes_Size()
                if Bitmap_Size < 1024:
                    Tag_String += str(Bitmap_Size) +"  B"
                else:
                    if Bitmap_Size < 1048576:
                        Tag_String += str((Bitmap_Size+512)//1024) +"  KB"
                    else:
                        Tag_String += str((Bitmap_Size+524288)//1048576) +"  MB"
                
                self.Tag_Data_Listbox.insert(END,Tag_String)
                
            self.populating_tag_window = False
        

    def Set_Listbox_Entry_Color(self, Listbox_Index, Tag_Path):
        if Get_Will_be_Processed(self.Handler.Tag_Collection["bitm"][Tag_Path],
                                 self.Handler.Default_Conversion_Flags["bitm"]):
            self.Tag_List_Listbox.itemconfig(Listbox_Index, bg='dark green', fg='white')
        else:
            self.Tag_List_Listbox.itemconfig(Listbox_Index, bg='white', fg='black')
            

    #these next functions are used for scrolling both tag list boxes at once.
    #they need to be in this class since they use the inherited Handler
    #reference to know where the listbox and scrollbar objects are
    def _Scroll_Both_List_Boxes(self, *args):
        self.Tag_List_Listbox.yview(*args)
        self.Tag_Data_Listbox.yview(*args)
        
    def _Scroll_Tag_List(self, *args):
        if (self.Tag_Data_Listbox.yview() != self.Tag_List_Listbox.yview()):
            self.Tag_Data_Listbox.yview_moveto(args[0])
        self.Tag_List_Scrollbar_Y.set(*args)

    def _Scroll_Tag_Data(self, *args):
        if (self.Tag_List_Listbox.yview() != self.Tag_Data_Listbox.yview()):
            self.Tag_List_Listbox.yview_moveto(args[0])
        self.Tag_List_Scrollbar_Y.set(*args)




'''ENTER A DESCRIPTION FOR THIS CLASS WHEN I HAVE TIME'''
class Bitmap_Converter_Help_Window(Toplevel):

    def __init__(self, Parent, **options):
        Toplevel.__init__(self, Parent, **options )
        
        self.Parent = Parent
        self.is_alive = True
        
        self.title("Useful Help")
        self.geometry("440x400")
        self.resizable(0, 1)
        self.minsize(width=300, height=300)
        self.protocol("WM_DELETE_WINDOW", self.Close_Help)

        #Make the menu bar
        self.help_window_menubar = Menu(self)
        Str_Tmp = ["Steps to using this program", "Global Parameters", "General Parameters",
                   "Multipurpose Swap", "Format Specific Parameters",
                   "Format Conversion", "Miscellaneous"]
        for i in range(len(Str_Tmp)):
            self.help_window_menubar.add_command(label=Str_Tmp[i], command=lambda i=i:(self.Change_Displayed_Help(i)) )
            
        self.config(menu=self.help_window_menubar)

        self.Help_Window_Scrollbar_Y = Scrollbar(self, orient="vertical")

        self.Displayed_Help_Text_Box = Text(self, bg='#ece9d8', state=NORMAL, yscrollcommand=self.Help_Window_Scrollbar_Y.set)
        self.Displayed_Help_Text_Box.insert(INSERT, "Click a button on the menubar above.")
        self.Displayed_Help_Text_Box.config(state=NORMAL, wrap=WORD)
        
        self.Help_Window_Scrollbar_Y.config(command=self.Displayed_Help_Text_Box.yview)

        self.Help_Window_Scrollbar_Y.pack(side="right", fill="y")
        self.Displayed_Help_Text_Box.pack(side="left",fill="both", expand=True)



    def _Minimize_Parent(self, *args):
        Minimize_Maximize_Children_with_Parent(self.Parent, self.Parent.Child_Windows, "MIN")
    def _Maximize_Parent(self, *args):
        Minimize_Maximize_Children_with_Parent(self.Parent, self.Parent.Child_Windows, "MAX")
        

    def Close_Help(self):
        self.withdraw()
    
    def Change_Displayed_Help(self, Help_Type):
        self.Displayed_Help_Text_Box.delete('0.0', END)

        if Help_Type == 0:
            New_Help_String = ('Steps:\n\n1: click "Browse..." and select the folder containing bitmaps that you want to operate on. ' +
                               'This does not have to be a root tags folder, just a folder containing bitmap tags.\n\n' +
                               '2: Hit "Load" and wait for the program to say it is finished indexing and loading all the tags.\n\n' +
                               '3: Choose a tag or multiple tags in the "Tag List" window and, in the main window, specify what format you ' +
                               'want them converted to, how many times to cut the resolution in half, and any other conversion settings.\n\n' +
                               '4: Hit "Run"\n\n5: Go make a sandwich cause this may take a while.....\n\n' +
                               '6: Once the conversion is finished, a debug log will be created in the folder where the bitmap converter is ' +
                               "located and the tag list will be cleared. The log's name will be the timestamp of when it was created.")

        elif Help_Type == 1:
            New_Help_String = ("---Don't reprocess tags---\n   Tells the program to ignore tags that have already been processed and to ignore"+
                               ' tags that have no conversion settings different than how the tag currently is. This box is checked by default and'+
                               ' unchecking it should only be done if you want all the tags to be processed.\n\n   Unchecking the "' + "Don't" +
                               ' reprocess tags" box can be useful if you wish to prune the uncompressed original TIFF data from the tag to' +
                               ' reduce its size. This data is pruned by tool when the tag is compiled into a map, but if you wish to reduce'+
                               ' the size of your tags folder or reduce the size of tags you upload to Halomaps, then this may come of use.'+
                               '\n\n\n---Backup old tags---\n   Tells the program to rename the tag being modified with a ".backup" extension' +
                               ' after it has completely written the new, modified tag. Only the oldest backup will be kept; reprocessing' +
                               ' a tag will not edit the .backup file.'+
                               '\n\n\n---Read only mode---\n   Prevents the program from making edits to tags. Instead, a detailed log will be' +
                               ' created containing a list of all the bitmaps located in the folder that was specified. The bitmaps will be sorted' +
                               ' by type(2d, 3d, cubemap), then format(r5g6b5, dxt1, a8r8g8b8, etc), then the number of bytes the pixel data takes up.'+
                               '\n\n\n---Write debug log---\n   Tells the program to write a log of any successes and errors encountered while' +
                               ' preforming the conversion. If a tag is skipped it will be reported as an error.')
        elif Help_Type == 2:
            New_Help_String = ('---Save as Xbox/PC tag---\n   Xbox and PC bitmaps are slightly different in the way they are saved. Xbox has the' +
                               ' pixel data for each bitmap padded to a certain multiple of bytes and cubemaps have the order of their mipmaps and' +
                               ' faces changed. A few other differences exist, but these all make a big difference. Save to the correct format.' +
                               '\n\n---Save as swizzled/un-swizzled---\n   Texture swizzling is not supported on PC Halo, but is required for good' +
                               ' preformance in non-DXT bitmaps on Xbox Halo. Swizzling swaps pixels around in a texture and makes them unviewable to' +
                               ' humans. For PC, save as un-swizzled; for Xbox, save as swizzled. DXT textures can not be swizzled so'+" don't"+' worry.' +
                               '\n\n---Number of times to halve resolution---\n   I tried to think of a shorter way to phrase it, I really did. This is' +
                               ' pretty obvious, but what' + " isn't" + ' so obvious is that if a bitmap has mipmaps the way the program will halve' +
                               ' resolution is by removing however many of the biggest mipmaps you tell it to.' +
                               '\n   If no mipmaps exist (HUD elements for example) the program will use a slower method of downresing, using a simple' +
                               ' bilinear filter to merge pixels.')
        elif Help_Type == 3:
            New_Help_String = ('   PC multipurpose bitmaps channel usage:\nAlpha: Color Change\nRed: Detail Mask\nGreen:' +
                               ' Self Illumination\nBlue: Specular\Reflection\n\n   Xbox multipurpose bitmaps channel usage:' +
                               ' \nAlpha: Detail Mask\nRed: Specular\Reflection\nGreen: Self Illumination\nBlue: Color change\n\n   This program can swap the' +
                               ' channels from PC order to Xbox order or vice versa. If you want to swap them though, make sure you are converting to a' +
                               " format that supports all the channels that you want to keep. For example, swapping an Xbox texture's channels to PC will" +
                               ' require an alpha channel in the new texture if you want to keep the color change channel.\n\n***NOTE*** If a' +
                               ' multipurpose swap setting is used then it will override the "Swap A8Y8 channels" setting if it is also set.')
        elif Help_Type == 4:
            New_Help_String = ("---Alpha cutoff bias---\n   Some formats (DXT1 and A1R5G5B5) are able to have an alpha channel, but it's limited to one bit." +
                               ' This means the only possible values are solid white or solid black. "Alpha cutoff bias" is used as the divider where' +
                               ' an alpha value above it is considered solid white and a value below it is considered solid black. The default value is 127.' +
                               '\n\n---P-8 Bump Conversion Mode---\n   P8-bump only has a palette of 250 colors to choose from and when you compress a 32bit' +
                               ' or 16bit texture to it you are likely to lose some detail. This palette does not at all cover the full range of normals that' +
                               ' you may see in a normal map, and in fact actually misses a lot of the top left, top right, bottom left, and bottom right' +
                               ' tangent vectors that you may see. The two modes I have created each use the palette differently to achieve different results.' +
                               "\n   I could go into the specifics of this problem and how/why these two conversion methods exist, but here's the short simple" +
                               ' answer: Auto-bias is good when you want to preserve the depth of the normal map and Average-bias is good when you want to' +
                               ' preserve the smoothness of the normal map. Auto-bias sacrifices smoothness to allow the normal maps to stay vibrant and strong' +
                               " while Average-bias sacrifices the depth and strength of the normal map to allow the color gradient to stay more or less smooth." +
                               '\n   The default, and usually the best mode to use, is Auto-bias as the drop in smoothness is usually unnoticible.' +
                               '\n\n---Monochrome channel to keep---\n   In A8 format only the alpha data is stored and the intensity channel(RGB merged) is' +
                               ' assumed to be solid black.\n   In Y8 only the intensity channel is stored and the alpha is assumed to be solid white.' +
                               '\n   In AY8 only the pixel data of 1 channel is stored (just like in A8 and Y8), but this pixel data is used for both the' +
                               ' alpha and intensity channels. That means the same exact image is shared between the alpha and intensity channels no' +
                               ' matter what. This is useful for reticles for example.\n   This setting serves two purposes; to specify whether you want to' +
                               ' convert to A8 or Y8 when you select "A8/Y8*", and to specify which one of these two channels to keep when you convert to AY8.' +
                               ' Since only either the alpha or intensity pixel data is saved when converting to AY8 you need to specify which to use.' +
                               ' The default setting is intensity.\n\n---Swap A8Y8 channels---\n   On PC, HUD textures used in meters(like health and ammo)' +
                               ' have to be 32bit color. The RGB channels are used for the image that is displayed and the alpha is used for the gradient mask'
                               ' that erases parts of the meter if they are below a certain value.\n   On XBOX, HUD textures used in meters(like health and' +
                               ' ammo) have to be in a monochrome format. The alpha channel is used for the image that is displayed and the intensity channel' +
                               ' is used for the gradient mask that erases parts of the meter if they are below a certain value.\n   HUD meters converted from' +
                               ' PC to Xbox need to have their intensity and alpha channels swapped. This setting will swap them when you convert to or from' +
                               " an A8Y8 bitmap.\n\n---Color-Key Transparency---\n   You may know the DXT formats by Guerilla's names:" +
                               '"Compressed with color-key transparency"(DXT1), "Compressed with explicit alpha"(DXT3), and "Compressed with interpolated alpha"' +
                               '(DXT5). DXT1 bitmaps are actually capable of having an alpha channel, though it has some strict limitations. First off the alpha' +
                               " channel is 1bit, meaning either solid white or solid black. The other, BIGGER, limitation is that if a pixel's alpha is set to" +
                               ' full black then the red, green, and blue for that pixel are also full black.\n   This type of alpha channel is perfect for things' +
                               " where it renders as transparency, like on the holes for the warthog's chaingun belt, but should NEVER be used for things" +
                               ' where the alpha channel does not function as transparency, like in a multipurpose map or the base map in an environment shader.' +
                               '\n   This setting also determines whether or not an alpha channel is saved with P8 bitmaps. A transparent pixel, just like in DXT1'+
                               ', will be solid black in color.\n\n"Alpha cutoff bias" affects what is determined to be white and what is determined to be black.')
        elif Help_Type == 5:
            New_Help_String = ('---Format to convert to---\nMore or less straight forward, but there are a few miscellaneous things you' +
                               ' should be aware of before you convert formats.\n\n* This program is capable of converting to the DXT formats,' +
                               ' though it uses a slightly different method for compression than Tool uses. This different method actually creates' +
                               ' better UI textures compressed as DXT5 than Tool, having little to no artifacts in most cases. My compression method' +
                               " isn't perfect though, and is absolute poopy crap when compressing normal maps to DXT. If a texture doesn't look good" +
                               ' as DXT when tool creates it try having tool compress it as 32 bit color and have this program turn it into DXT.' +
                               " The results may shock you.\n\n* Not all the formats this program can convert to are" +
                               ' supported by Custom Edition. P8-bump, A8Y8, AY8, Y8, and A8 are Xbox only formats.\n\n* Converting to 32bit color was' +
                               ' an afterthought and as such I did not make a button specifically for it. You CAN convert the Xbox only formats(P8,' +
                               ' A8Y8, AY8, Y8, A8) to 32 bit color though, as this would be the only way to make a usable Custom Edition texture from' +
                               ' them. When one of these formats is selected, the "P8*/32Bit"' + " button's function will be converting the bitmaps to" +
                               " 32 bit color. If a 32bit, 16bit, or DXT texture is selected though, the button's function will be converting the" +
                               ' selected tags to P-8 bump. If a mixture of these formats is selected the appropriate conversion will be used.' +
                               '\n\n* Bitmaps that are not a power of 2 dimensions will be skipped entirely. So much of this program revolves around' +
                               ' the bitmaps being in power of 2 dimensions that I did not want to try and rework all of it just to get those very' +
                               ' rare bitmap types incorporated. The CMD window will notify you of any bitmaps that are not power of 2 dimensions' +
                               ' and/or corrupt.\n\n---Extract to---\nSelf explanatory, but there are a few things you should be aware of.\n   1: ' +
                               'The folder that you selected when you hit "Browse" and "Load" will be considered as the "tags" folder. The folder that ' +
                               'the "tags" folder is in will have a "data" folder created in it'+"(if it doesn't already exist) and that is where the " +
                               'extracted bitmaps will be placed.\n   2: TGA can not handle having exactly 2 channels(A8Y8), nor can it handle 16 bit color ' +
                               'in the form of R5G6B6 or A4R4G4B4, nor ANY of the DXT formats. DDS will be used if you try to export one of these to TGA')
        elif Help_Type == 6:
            New_Help_String = ('* If the program encounters an error it will be displayed on the Python CLI screen (the black empty CMD screen).' +
                               '\n\n* If you wish to move the windows independent of each other click "Un-dock Windows" on the menu bar.' +
                               '\n\n* The "Tag List" window can sort the tags 4 different ways. If the same sorting method is clicked again it' +
                               ' will reverse the order the tags are displayed.\n\n* If you want to only show certain types of tags you can' +
                               ' enable and disable which ones show up in the Tag List window. Look under the "Enable/Disable Types" and' +
                               ' "Enable/Disable Formats" and uncheck the types/formats you' + " don't want to show up." +
                               '\n\n* I was originally planning a preview thumbnail, but because it would slow down browsing through tags and' +
                               ' would be more annoying to implement than I care to deal with, I decided not to. Just deal with it and open' +
                               ' the tags in guerilla to see what they look like.\n\n* During the tag load/conversion process the text box at' +
                               ' the bottom of the main window will give information on which tag is being processed.' +
                               '\n\n* A Tag being highlighted in green signifies that, based on the tags current conversion settings, it will be' +
                               ' processed in some way when "Run" is clicked. If a tag is white it will be ignored when "Run" is clicked.' +
                               '\n\n* The "Selected Tag Information" window will display information about the selected tag, but ONLY if JUST one' +
                               ' tag is selected. If more than one tag is selected the info displayed will not update. Selecting a different bitmap' +
                               'index on the same window will change which bitmap the window is displaying information about.' +
                               '\n\n* If the program seems to be frozen then check the Python CLI screen(the black empty CMD screen). If it shows an' +
                               ' error then the program may indeed have frozen or crashed. If not then just give it time. Depending on how you are' +
                               ' converting it and the bitmaps dimensions, a conversion may take from a tenth of a second to 3 minutes.' +
                               " BUT AT LEAST IT'S AUTOMATED RIGHT?!?!?!\n\nMade by Moses")
        else:
            New_Help_String = ""
        
        self.Displayed_Help_Text_Box.insert(INSERT, New_Help_String)

