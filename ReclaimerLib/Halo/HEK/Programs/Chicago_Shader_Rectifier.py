import os

from traceback import format_exc
from ..Library import Halo_Library
from supyr_struct.Field_Types import Void

class Shader_Rectifier(Halo_Library):
    Target_Tag = "schi"
    Backup_Tags = False

    Log_Filename = "Chicago_Shader_Rectifier.log"
    
    #initialize the class
    def __init__(self, **kwargs):
        
        if "Target_Tag" in kwargs:
            self.Target_Tag = kwargs["Target_Tag"]
        if "Backup_Tags" in kwargs:
            self.Backup_Tags = kwargs["Backup_Tags"]
        kwargs["Valid_Tag_IDs"] = ("schi","scex")
        Halo_Library.__init__(self, **kwargs)


    #This is used to convert extended chicago tags
    #into regular ones and remove all extra layers
    def Convert_Shaders_Tags(self, **kwargs):
        #this is the string to store the entire debug log
        Debug_Log_String = ("Debug log for CE-XBOX Shader Rectifier\n\n\n" +
                            "Removed extra layers from:\n\n")

        Target_Def = self.Get_Def(self.Target_Tag)
        
        '''loop through both chicago and extended chicago tag types'''
        for Cls_ID in self.Tags:

            '''loop through each tag and remove extra
            layers and log them to a debug file'''
            for Tag_Path in sorted(self.Tags[Cls_ID]):
                Tag = self.Tags[Cls_ID][Tag_Path]
                try:

                    '''CONVERT THE TAG'''
                    if Cls_ID != self.Target_Tag:                    
                        Tag.Convert_to_Other_Chicago()
                        del self.Tags[Cls_ID][Tag_Path]

                    '''REMOVE THE EXTRA LAYERS FROM THE TAG'''
                    EL = Tag.Tag_Data.Data.Extra_Layers.Extra_Layers_Array
                    if len(EL):
                        Debug_Log_String += "\n"+Tag.Tag_Path +"\nExtra Layers:"
                        
                        #we loop through each extra layer for the debug log
                        for i in range(len(EL)):
                            #add the extra layer's path to the debug log
                            try:
                                Ext = '.'+EL[i].Tag_Class.Data_Name
                            except Exception:
                                Ext = ''
                            Debug_Log_String += "\n    " + EL[i].CHILD + Ext

                        #void out the extra layers
                        Tag.Tag_Data.Data.Extra_Layers.Set_Desc('TYPE', Void)

                    New_Tag_Path = Tag.Tag_Path.split(self.Tags_Dir)[1]
                    self.Tags[Cls_ID][New_Tag_Path] = Tag
                    Tag.Definition = Target_Def
                except:
                    print("ERROR OCCURRED WHILE ATTEMPTING TO CONVERT:\n" +
                          '    ' + Tag.Tag_Path + '\n')
                    print(format_exc())
        #swap the tags around in the tag collection
        if self.Target_Tag == 'scex':
            self.Tags['scex'].update(self.Tags['schi'])
            self.Tags['schi'].clear()
        else:
            self.Tags['schi'].update(self.Tags['scex'])
            self.Tags['scex'].clear()


        Conversion_Report,Write_Exceptions = self.Write_Tags(Print_Errors=False)
        Debug_Log_String += Write_Exceptions
        
        #create the debug and take care of renaming and deleting tags
        Debug_Log_String += self.Make_Write_Log(Conversion_Report,
                                                Backup=self.Backup_Tags)
        
        return(Debug_Log_String)
        

    def Load_Tags_and_Run(self):
        input('This program will scan the tags directory and any \n"shader_'+
              'transprent_chicago_extended" tags that it finds will be \n'+
              'converted to regular chicago shaders to fix blending issues.\n'+
              
              '\nExtended chicago tags will NOT be deleted after being '+
              'converted. \nExtra layers will be removed from all '+
              'shader_transprent_chicago tags \nand converted '+
              'shader_transprent_chicago_extended tags.\n'+
              
              '\nAfter conversion a log will be created in this folder '+
              'detailing \nwhich tags had extra layers removed, the paths of '+
              'those extra \nlayers, and errors that occurred.\n'+
              '\nPress Enter to begin converting the shaders in:'+
              '\n    %s\n\n' % self.Tags_Dir)
        
        #Stream the data from the tags to class
        #constructs so the program can work with them
        if self.Index_Tags():
            self.Load_Tags()
        
            #now we finally fix/convert the shaders
            Results_Log = self.Convert_Shaders_Tags()
            
            #save the debug log to a file
            self.Make_Log_File(Results_Log)
        else:
            #if something went wrong earlier this will notify the user
            input('Tags directory is either empty, doesnt '+
                  'exist, or cannot be accessed')
            raise SystemExit()
        
        input('-'*80 + '\nFinished rectifying shaders.\nCheck the tags '+
              'directory for the changelog.\n' + '-'*80 +
              '\n\nPress enter to exit.')
    
