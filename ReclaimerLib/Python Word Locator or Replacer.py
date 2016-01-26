import os
import re
from traceback import format_exc

curr_dir = os.path.abspath(os.curdir).replace('/', '\\')
Word_Map = {}
Flags = None
Mode = "locate"


Word_Map = {'Valid_Tag_IDs':'tagids', 'Cls_ID':'tagid', 'Tag_Cls':'tagobj',
            'Tag_Structure':'descriptor', 'Construct':'construct',

            'Tag_Block':'Block', 'Void_Block':'VoidBlock', 'Data_Block':'DataBlock',
            'List_Block':'ListBlock', 'P_List_Block':'PListBlock',
            'Bool_Block':'BoolBlock', 'Enum_Block':'EnumBlock',
            'While_List_Block':'WhileBlock', 'P_While_List_Block':'PWhileBlock',
           
            'Field_Types':'fields', 'Tag_Blocks':'blocks',
            'Constants':'constants', 'Re_Wr_De_En':'re_wr_de_en',
            'Common_Block_Structures':'common_descriptors',
            'Common_Structures':'common_descriptors',
           
            'Field_Type':'Field', 'Tag_Def':'TagDef',
            'Library':'TagLibrary', 'Tag_Test_Library':'TestLibrary',

            '_LGI':'list.__getitem__', '_LSI':'list.__setitem__',
            '_LDI':'list.__delitem__', '_LSO':'list.__sizeof__',
           
            '_OSA':'object.__setattr__', '_OGA':'object.__getattribute__',
            '_ODA':'object.__delattr__', '_OSO':'object.__sizeof__',
           
            '_LApp':'list.append', '_LExt':'list.extend', '_LIns':'list.insert',
           
            'Read':'read', 'Write':'write', 'Get_Tag':'gettag',
            '_Bin_Size':'_binsize', 'Bin_Size':'binsize',
            'Get_Desc':'getdesc', 'Del_Desc':'deldesc', 'Set_Desc':'setdesc',
            'Ins_Desc':'insdesc', 'Res_Desc':'resdesc', 'Make_Unique':'makeunique',
            'Get_Neighbor':'getneighbor', 'Get_Meta':'getmeta',
            'Get_Raw_Data':'getrawdata', 'Validate_Name':'verifyname',
            'Collect_Pointers':'getpointers', 'Set_Pointers':'setpointers',
           
            'Get_Size':'getsize', 'Set_Size':'setsize',
            'Set':'set', 'Set_To':'set_to', 'Unset':'unset',
            
            'Get_Index':'getindex', 'Get_Name':'getname', 'Get_Data':'getdata',
            'Set_Data':'setdata', 'Data_Name':'dataname'
            }
#Flags = re.IGNORECASE

#for Name in Words_to_Locate:
#    Word_Replacements.append(Name.upper())

print("READY")
input()

class Python_Word_Locator_Replacer():

    def __init__(self, **kwargs):
        self.Directory = str(kwargs.get("Directory", curr_dir))
        self.Word_Map = kwargs.get("Word_Map", Word_Map)
        self.Mode = kwargs.get("Mode", Mode)
        self.File_Paths = kwargs.get("File_Paths")
        
        if self.File_Paths is None:
            self.Allocate_Files()


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
                        
                        for old_word in self.Word_Map:
                            new_word = self.Word_Map[old_word]
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
                        
                        for word in self.Word_Map:
                            if Search_Flags:
                                match = re.findall(r'\b%s\b' % word, in_string, Search_Flags)
                            else:
                                match = re.findall(r'\b%s\b' % word, in_string)

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
