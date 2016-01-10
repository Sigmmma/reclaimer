import os, tkinter.filedialog
import tkinter as tk

from traceback import format_exc
from tkinter import *
from time import time, sleep
from copy import deepcopy

curr_dir = os.path.abspath(os.curdir)

try:
    from ReclaimerLib.GDL.Library import GDL_Library as Const

    def Validate_and_Set_Str(Var, *args):
        Val = Var.get()
        if len(Val) > Var.Max_Len:
            Val = Val[:Var.Max_Len]
            Var.set(Val)
        Var.Block_Parent[Var.Block_Index] = Val
        Var.Main_Window.Reset_Rollout_Options()
            
    def Validate_and_Set_Int(Var, *args):
        try:    Val = int(Var.get())
        except: Val = None
        if Val is not None:
            Var.Block_Parent[Var.Block_Index] = Val
            
            
    def Validate_and_Set_Float(Var, *args):
        try:    Val = float(Var.get())
        except: Val = None
        if Val is not None:
            Var.Block_Parent[Var.Block_Index] = Val 
            
            
    def Validate_and_Set_Enum(Var, *args):
        try:    Elements = Var.Block_Desc
        except: Elements = None
        if Elements is not None:
            Val = Var.get()
            for i in range(Elements['ENTRIES']):
                if Elements[i]['NAME'] == Val:
                    Var.Block_Parent[Var.Block_Index].Data = Elements[i]['VALUE']
                    return

    def Set_Enum(Widget, i):
        Var = Widget.Field_Var
        Var.set(Var.Block_Desc[i]['NAME'])
        try:    Var.Main_Window.Menu_Cheats.Option_Select()
        except: pass


    def Set_Flag(Widget, i):
        Flag_Var = Widget.Flag_Var
        Var = Flag_Var.Field_Var
        Mask = Flag_Var.Mask
        Inv_Mask = 4294967295-Mask
        
        Data = Var.Block_Parent[Var.Block_Index].Data
        Var.Block_Parent[Var.Block_Index].Data = Flag_Var.get()*Mask+(Data&Inv_Mask)


    class GDL_Editor_Window(Tk):

        Loaded_XBE = None
        
        def __init__(self, **options):
            Tk.__init__(self, **options )
            self.XBE_Const = Const(Valid_Tag_IDs='xbe')
            
            self.title("GDL: XBE Editor V1.5")
            self.geometry("250x655+0+0")
            self.resizable(0, 0)
            
            self.Selected_Char = StringVar(self)
            self.Selected_Cheat = StringVar(self)

            Structs = self.XBE_Const.Defs['xbe'].Structures

            self._Cheat_Flags_Desc         = Structs['No_Types']
            self._Cheat_Weapon_Flags_Desc  = Structs['Weapon_Types']
            self._Cheat_Armor_Flags_Desc   = Structs['Armor_Types']
            self._Cheat_Special_Flags_Desc = Structs['Special_Types']

            #Add the buttons
            self.btn_load = Button(self, text="Load GDL XBE", width=15, command=self.Load_XBE)
            self.btn_load.place(x=15, y=5, anchor=NW)
            self.btn_save = Button(self, text="Save GDL XBE", width=15, command=self.Save_XBE)
            self.btn_save.place(x=135, y=5, anchor=NW)
            
            #create the rollouts to select stuff
            self.Menu_Chars = OptionMenu(self, self.Selected_Char, (),
                                         Func=self.Reload_Char_Window)
            self.Menu_Cheats = OptionMenu(self, self.Selected_Cheat, (),
                                          Func=self.Reload_Cheat_Window)
            
            self.Menu_Chars.config(width=6)
            self.Menu_Chars['menu'].delete(0, 'end')
            self.Menu_Chars.place(x=15, y=35, anchor=NW)
            
            self.Chars_Import = Button(self, text="Import", width=8, command=self._Import_Chars)
            self.Chars_Import.place(x=105, y=38, anchor=NW)
            self.Chars_Export = Button(self, text="Export", width=8, command=self._Export_Chars)
            self.Chars_Export.place(x=175, y=38, anchor=NW)

            
            self.Menu_Cheats.config(width=6)
            self.Menu_Cheats['menu'].delete(0, 'end')
            self.Menu_Cheats.place(x=15, y=195, anchor=NW)
        
            self.Chars_Import = Button(self, text="Import", width=8, command=self._Import_Cheats)
            self.Chars_Import.place(x=105, y=198, anchor=NW)
            self.Chars_Export = Button(self, text="Export", width=8, command=self._Export_Cheats)
            self.Chars_Export.place(x=175, y=198, anchor=NW)

        def _Import_Chars(self):
            if hasattr(self.Loaded_XBE, 'Tag_Data'):
                Filepath = filedialog.askopenfilename(initialdir=curr_dir, defaultextension=".gdl_chars",
                                                      filetypes=[("GDL Characters", "*.gdl_chars"),('All','*')],
                                                      title="Import characters from...")
                if Filepath != "":
                    try:
                        self.Loaded_XBE.Tag_Data.Secret_Characters.Read(Filepath=Filepath)
                        self._Initialize_Windows()
                    except: print(format_exc())
        
        def _Export_Chars(self):
            if hasattr(self.Loaded_XBE, 'Tag_Data'):
                Filepath = filedialog.asksaveasfilename(initialdir=curr_dir, defaultextension=".gdl_chars",
                                                        filetypes=[("GDL Characters", "*.gdl_chars"),('All','*')],
                                                        title="Export the current characters to...")
                if Filepath != "":
                    try:    self.Loaded_XBE.Tag_Data.Secret_Characters.Write(Filepath=Filepath)
                    except: print(format_exc())
            
        def _Import_Cheats(self):
            if hasattr(self.Loaded_XBE, 'Tag_Data'):
                Filepath = filedialog.askopenfilename(initialdir=curr_dir, defaultextension=".gdl_cheats",
                                                      filetypes=[("GDL Cheats", "*.gdl_cheats"),('All','*')],
                                                      title="Import cheats from...")
                if Filepath != "":
                    try:
                        self.Loaded_XBE.Tag_Data.Cheats.Read(Filepath=Filepath)
                        self._Initialize_Windows()
                    except: print(format_exc())
        
        def _Export_Cheats(self):
            if hasattr(self.Loaded_XBE, 'Tag_Data'):
                Filepath = filedialog.asksaveasfilename(initialdir=curr_dir, defaultextension=".gdl_cheats",
                                                        filetypes=[("GDL Cheats", "*.gdl_cheats"),('All','*')],
                                                        title="Export the current cheats to...")
                if Filepath != "":
                    try:    self.Loaded_XBE.Tag_Data.Cheats.Write(Filepath=Filepath)
                    except: print(format_exc())
        
        def Load_XBE(self):
            Filepath = filedialog.askopenfilename(initialdir=curr_dir, title="Select Gauntlet's default.xbe")
            if Filepath != "":
                try:
                    XBE = self.XBE_Const.Build_Tag(Tag_ID="xbe", Filepath=Filepath)
                    if (XBE.Tag_Data.XBE_Image_Header.XBE_Magic != "XBEH" or
                        XBE.Tag_Data.XBE_Certificate.Title_Name != "Gauntlet Dark Legacy"):
                        raise IOError("The selected file does not appear to be a valid GDL default.xbe")
                    
                    self.Loaded_XBE = XBE
                    
                    self._Initialize_Windows()
                except:
                    raise IOError("Could not load file. Make sure it is a valid Gauntlet Dark Legacy XBE.")

        def Save_XBE(self):
            if hasattr(self.Loaded_XBE, "Write"):
                try:    self.Loaded_XBE.Write(Temp=False, Backup=True)
                except: raise IOError("The above error occurred while trying to write XBE file.")
                    

        def Get_Char_Names(self):
            Char_Names = []
            try:
                Chars = self.Loaded_XBE.Tag_Data.Secret_Characters
                for Character in Chars:
                    Char_Names.append(Character.Code)
            except: pass
            return Char_Names
        
        def Get_Cheat_Names(self):
            Cheat_Names = []
            try:
                Cheats = self.Loaded_XBE.Tag_Data.Cheats
                for Cheat in Cheats:
                    Cheat_Names.append(Cheat.Code)
            except: pass
            return Cheat_Names


        def Reset_Rollout_Options(self):
            Char = self.Menu_Chars
            Cheat = self.Menu_Cheats

            Curr_Char = Char.Current_Index
            Curr_Cheat = Cheat.Current_Index
            
            Char['menu'].delete(0, 'end')
            Cheat['menu'].delete(0, 'end')

            Char.Num_Entries = 0
            Cheat.Num_Entries = 0
            
            Char_Names = self.Get_Char_Names()
            Cheat_Names = self.Get_Cheat_Names()
            
            for Name in Char_Names:
                Char.addOption(Name)
            
            for Name in Cheat_Names:
                Cheat.addOption(Name)

            self.Selected_Char.set(Char_Names[Curr_Char])
            self.Selected_Cheat.set(Cheat_Names[Curr_Cheat])
            

        def _Initialize_Windows(self):
            self.Menu_Chars.Current_Index  = self.Menu_Chars.Num_Entries  = 0
            self.Menu_Cheats.Current_Index = self.Menu_Cheats.Num_Entries = 0
            
            self.Reset_Rollout_Options()
                
            self.Menu_Chars.Option_Select(0)
            self.Menu_Cheats.Option_Select(0)


        def Reload_Char_Window(self, Menu, i):
            if i is None:
                i = Menu.Current_Index
                
            Char = self.Loaded_XBE.Tag_Data.Secret_Characters[i]
            self._Reload_Widgets(Menu, Char, Char.DESC)
            self.Selected_Char.set(Char.Code)
            
        def Reload_Cheat_Window(self, Menu, i=None):
            if i is None:
                i = Menu.Current_Index
                
            Cheat = self.Loaded_XBE.Tag_Data.Cheats[i]
            Cheat_Flags = Cheat.Flags
            Cheat_Type = Cheat.Type
                
            Desc = Cheat.DESC
            
            if Cheat_Type.Data == 5:
                Cheat_Flags.DESC = Desc[3] = self._Cheat_Weapon_Flags_Desc
            elif Cheat_Type.Data == 6:
                Cheat_Flags.DESC = Desc[3] = self._Cheat_Armor_Flags_Desc
            elif Cheat_Type.Data == 9:
                Cheat_Flags.DESC = Desc[3] = self._Cheat_Special_Flags_Desc
            else:
                Cheat_Flags.Data = 0
                Cheat_Flags.DESC = Desc[3] = self._Cheat_Flags_Desc

            self._Reload_Widgets(Menu, Cheat, Desc)
            self.Selected_Cheat.set(Cheat.Code)


        def _Reload_Widgets(self, Parent, Data_Block, Desc):
            i = Parent.Current_Index
            
            Root_X = Parent.winfo_x()
            Root_Y = Parent.winfo_y()
            Y = 5
            
            try:    Parent.Child_Canvas.destroy()
            except: pass
            Child_Canvas = Canvas(Main_Window, highlightthickness=0,
                                  width=Main_Window.winfo_width(),
                                  height=Main_Window.winfo_height())
            Child_Canvas.place(x=0, y=Root_Y+30, anchor=NW)
            Parent.Child_Canvas = Child_Canvas

            for i in range(Desc['ENTRIES']):
                This_Desc = Desc[i]
                if This_Desc is None:
                    continue
                
                Type = This_Desc['TYPE']
                Trace_Func = None

                Child_Canvas.create_text(10, Y+3, anchor="nw", text=This_Desc["GUI_NAME"])

                if Type.Is_Data:
                    Field_Var = StringVar(Child_Canvas)
                    
                    Field_Var.Block_Parent = Data_Block
                    Field_Var.Block_Desc   = This_Desc
                    Field_Var.Block_Index  = i
                    Field_Var.Main_Window  = self
                    
                    Block_Val = Data_Block[i]

                    if Type.Is_Enum:
                        Widget_Height = 30
                        New_Widget = OptionMenu(Child_Canvas, Field_Var, (), Func=Set_Enum)
                        
                        New_Widget['menu'].delete(0, 'end')
                        New_Widget.config(width=16)
                        New_Widget.Field_Var = Field_Var
                        
                        for x in range(This_Desc['ENTRIES']):
                            New_Widget.addOption(This_Desc[x]['GUI_NAME'])
                            if Block_Val.Data == This_Desc[x]['VALUE']:
                                Field_Var.set(This_Desc[x]['GUI_NAME'])
                                
                        Trace_Func = lambda name, index, mode, Var=Field_Var:Validate_and_Set_Enum(Var)
                    elif Type.Is_Bool:
                        Widget_Height = 0
                        New_Widget = Canvas(Child_Canvas, highlightthickness=0,
                                            width=Main_Window.winfo_width(),
                                            height=Main_Window.winfo_height())
                        New_Widget.place(x=0, y=Root_Y+Y, anchor=NW)
                        New_Widget.Field_Var = Field_Var
                        
                        for x in range(This_Desc['ENTRIES']):
                            Flag_Var = IntVar(Child_Canvas)
                            Flag_Name = This_Desc[x]['GUI_NAME']
                            Flag_Val = This_Desc[x]['VALUE']

                            Flag_Var.Mask = Flag_Val
                            Flag_Var.Field_Var = Field_Var
                            
                            New_Flag_Button = Checkbutton(New_Widget, text=Flag_Name, variable=Flag_Var,
                                                          onvalue=1, offvalue=0, Index=x, Func=Set_Flag)
                            
                            New_Flag_Button.Parent = New_Widget
                            New_Flag_Button.place(x=0, y=Widget_Height, anchor=NW)
                            New_Flag_Button.Flag_Var = Flag_Var
                            
                            if Block_Val.Data & Flag_Val:
                                New_Flag_Button.select()
                            
                            Widget_Height += 16
                            New_Widget.config(height=Widget_Height)
                    else:
                        Field_Var.set(str(Data_Block[i]))
                        if Type.Is_Str:
                            Field_Var.Max_Len = This_Desc["SIZE"]-1
                            Trace_Func = lambda name, index, mode, Var=Field_Var:Validate_and_Set_Str(Var)
                        else:
                            if issubclass(Type.Py_Type, float):
                                Trace_Func = lambda name, index, mode, Var=Field_Var:Validate_and_Set_Float(Var)
                            else:
                                Trace_Func = lambda name, index, mode, Var=Field_Var:Validate_and_Set_Int(Var)
                                
                        Widget_Height = 20
                        
                        New_Widget = Entry(Child_Canvas, textvariable=Field_Var)
                        New_Widget.config(width=16)
                        New_Widget.Field_Var = Field_Var
                        
                    if Trace_Func is not None:
                        Field_Var.trace('w', Trace_Func)
                    New_Widget.place(x=100, y=Y, anchor=NW)
                    Y += Widget_Height
                    
                Child_Canvas.config(height=Y+5)



    class OptionMenu(tk.OptionMenu):
        def __init__(self, *args, **kwargs):
            self.Child_Canvas = None
            
            self.Current_Index = 0
            self.Num_Entries = 0
            
            self._Func = kwargs["Func"]
            tk.OptionMenu.__init__(self, *args)
            
        def addOption(self, label):
            x = int(self.Num_Entries)
            self["menu"].add_command(label=label, command=lambda:self.Option_Select(x) )
            self.Num_Entries += 1

        def Option_Select(self, i=None):
            if i is None:
                self._Func(self, self.Current_Index)
            else:
                self.Current_Index = i
                self._Func(self, i)
            
    class Checkbutton(tk.Checkbutton):

        def __init__(self, *args, **kwargs):
            self._Func = kwargs["Func"]
            i = kwargs["Index"]
            del kwargs["Func"]
            del kwargs["Index"]
            
            kwargs["command"] = lambda: self.Check(i)
            tk.Checkbutton.__init__(self, *args, **kwargs)
            
        
        def Check(self, i):
            self._Func(self, i)
        
    
    if __name__ == "__main__":
        Main_Window = GDL_Editor_Window()
        Main_Window.mainloop()

except:
    print(format_exc())
    input()
