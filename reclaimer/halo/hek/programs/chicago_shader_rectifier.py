import os

from traceback import format_exc
from ..library import HaloLibrary
from supyr_struct.fields import Void

class ShaderRectifier(HaloLibrary):
    target_id = "schi"
    backup_Tags = False

    log_filename = "Chicago_Shader_Rectifier.log"
    
    #initialize the class
    def __init__(self, **kwargs):
        if "target_id" in kwargs:
            self.target_id = kwargs["target_id"]
        if "backup" in kwargs:
            self.backup = kwargs["backup"]
        kwargs["valid_tag_ids"] = ("schi","scex")
        HaloLibrary.__init__(self, **kwargs)


    #This is used to convert extended chicago tags
    #into regular ones and remove all extra layers
    def convert_shaders(self, **kwargs):
        #this is the string to store the entire debug log
        logstr = ("Debug log for CE-XBOX Shader Rectifier\n\n\n" +
                  "Removed extra layers from:\n\n")

        target_def = self.get_def(self.target_id)
        
        '''loop through both chicago and extended chicago tag types'''
        for tag_id in self.tags:

            '''loop through each tag and remove extra
            layers and log them to a debug file'''
            for tagpath in sorted(self.tags[tag_id]):
                tag = self.tags[tag_id][tagpath]
                try:

                    '''CONVERT THE TAG'''
                    if tag_id == 'schi' and self.target_id == 'scex':                    
                        tag.convert_to_scex()
                        del self.tags[tag_id][tagpath]
                    elif tag_id == 'scex' and self.target_id == 'schi':                    
                        tag.convert_to_schi()
                        del self.tags[tag_id][tagpath]

                    '''REMOVE THE EXTRA LAYERS FROM THE TAG'''
                    el = tag.tagdata.Data.Extra_Layers.Extra_Layers_Array
                    if len(el):
                        logstr += "\n"+tag.tagpath +"\nExtra Layers:"
                        
                        #we loop through each extra layer for the debug log
                        for layer in el:
                            #add the extra layer's path to the debug log
                            try:
                                ext = '.'+layer.Tag_Class.data_name
                            except Exception:
                                ext = ''
                            logstr += "\n    " + layer.CHILD + ext

                        #void out the extra layers
                        tag.tagdata.Data.Extra_Layers.set_desc('TYPE', Void)

                    new_tag_path = tag.tagpath.split(self.tagsdir)[1]
                    self.tags[tag_id][new_tag_path] = tag
                    tag.definition = target_def
                except:
                    print("ERROR OCCURRED WHILE ATTEMPTING TO CONVERT:\n" +
                          '    ' + tag.tagpath + '\n')
                    print(format_exc())
        #swap the tags around in the tag collection
        if self.target_id == 'scex':
            self.tags['scex'].update(self.tags['schi'])
            self.tags['schi'].clear()
        else:
            self.tags['schi'].update(self.tags['scex'])
            self.tags['scex'].clear()


        report, write_exceptions = self.write_tags(print_errors=False)
        logstr += write_exceptions
        
        #create the debug and take care of renaming and deleting tags
        logstr += self.make_write_log(report, backup=self.backup)
        
        return logstr
        

    def load_tags_and_run(self):
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
              '\n    %s\n\n' % self.tagsdir)
        
        #Stream the data from the tags to class
        #constructs so the program can work with them
        if self.index_tags():
            self.load_tags()
        
            #now we finally fix/convert the shaders
            results = self.convert_shaders()
            
            #save the debug log to a file
            self.make_log_file(results)
        else:
            #if something went wrong earlier this will notify the user
            input('Tags directory is either empty, doesnt '+
                  'exist, or cannot be accessed')
            raise SystemExit()
        
        input('-'*80 + '\nFinished rectifying shaders.\nCheck the tags '+
              'directory for the changelog.\n' + '-'*80 +
              '\n\nPress enter to exit.')
    
