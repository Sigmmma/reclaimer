import os
import re
from traceback import format_exc

curr_dir = os.path.abspath(os.curdir).replace('/', '\\')
Words_to_Locate = []
Word_Replacements = []
Flags = None
Mode = "replace"



Words_to_Locate = ['Supyr_Struct']
Word_Replacements = ['supyr_struct']
#Flags = re.IGNORECASE


#for Name in Words_to_Locate:
#    Word_Replacements.append(Name.upper())

print("READY")
input()

class Python_Word_Locator_Replacer():

    def __init__(self, **kwargs):
        if "Directory" in kwargs and kwargs["Directory"] is not None:
            self.Directory = str(kwargs["Directory"])
        else: self.Directory = curr_dir
        
        if "File_Paths" in kwargs and hasattr(kwargs["File_Paths"], '__iter__'):
            self.File_Paths = kwargs["File_Paths"]
        else: self.Allocate_Files()
        
        if "Words_to_Locate" in kwargs and hasattr(kwargs["Words_to_Locate"], '__iter__'):
            self.Words_to_Locate = kwargs["Words_to_Locate"]
        else: self.Words_to_Locate = Words_to_Locate
        
        if "Word_Replacements" in kwargs and hasattr(kwargs["Word_Replacements"], '__iter__'):
            self.Word_Replacements = kwargs["Word_Replacements"]
        else: self.Word_Replacements = Word_Replacements

        if "Mode" in kwargs and kwargs["Mode"] is not None:
            self.Mode = kwargs["Mode"]
        else: self.Mode = Mode


    def Allocate_Files(self):
        self.File_Paths = []
        for root, directories, files in os.walk(self.Directory):
            for filename in files:
                
                base, ext = os.path.splitext(filename)
                filepath = os.path.join(root, filename)
                
                if __file__ != filepath:
                    if ext.lower() in (".py", ".pyw"):
                        self.File_Paths.append(filepath)
                                    
                    self.File_Paths = sorted(self.File_Paths)


    def Run(self, Search_Flags=None):
        for in_path in self.File_Paths:
            out_path = in_path + '.tmp'
            backup_path = in_path+".backup"
            print(in_path)
            try:
                if self.Mode.lower() == "replace":
                    with open(in_path, "r") as in_file, open(out_path, "w") as out_file:
                        modified_string = in_file.read()
                        
                        for i in range(min(len(self.Words_to_Locate), len(self.Word_Replacements)) ):
                            old_word = self.Words_to_Locate[i]
                            new_word = self.Word_Replacements[i]
                            
                            modified_string = re.sub(r'\b%s\b' % old_word, new_word, modified_string)
                    
                        out_file.write(modified_string)
                                    
                    #Try to delete old file
                    try:
                        if os.path.isfile(backup_path):
                            #Try to delete old file
                            try: os.remove(in_path)
                            except: pass
                        else:
                            os.rename(in_path, backup_path)
                        
                        #Try to rename the temp tag to the real tag name
                        try: os.rename(out_path, in_path)
                        except: pass
                    except:
                        print("COULDNT RENAME THIS FILE TO BACKUP\n", in_path)

                elif self.Mode.lower() == "locate":
                    with open(in_path, "r") as in_file:
                        in_string = in_file.read()
                        
                        for word in self.Words_to_Locate:
                            if Search_Flags:
                                  match = re.findall(r'\b%s\b' % word, in_string, Search_Flags)
                            else: match = re.findall(r'\b%s\b' % word, in_string)

                            if match:
                                print("    ", len(match), "Occurances of:", word)
                
            except:
                print(in_path)
                print(format_exc())

if __name__ == "__main__":
    Program = Python_Word_Locator_Replacer()
    Program.Run(Flags)
    print("Done")
    input()
