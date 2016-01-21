from traceback import format_exc
try:
    from supyr_struct.Test import Tag_Test_Library
    
    if __name__ == '__main__':
        Test = Tag_Test_Library(Debug=3, Print_Test=True, Save_Test=False,
                                Write_as_Temp=True, Backup_Old_Tags=False,
                                Valid_Tag_IDs="sote_eep_save",
                                Defs_Path="ReclaimerLib\\misc\\Defs\\",
                              
                                Print_Options={'Indent':4,
                                               'Printout':True, 'Precision':3,
                                               'Show':['Name', 'Children', 'Type',
                                                       'Value', 'Offset',# 'Size',
                                                       'Index', 'Flags',
                                                       'Tag_Path', #'Unique', 
                                                       'Bin_Size', 'Ram_Size',
                                                       #'All'
                                                       ] })
        Test.Run_Test()
except Exception:
    print(format_exc())
    input()

TT = Test.Tags['tga']['test32.tga']
TD = TT.Tag_Data
