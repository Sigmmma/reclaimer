from traceback import format_exc
from copy import copy
try:
    from supyr_struct.Test import Tag_Test_Class
    from ReclaimerLib.Tag_Constructors.GDL_Constructors.\
         Constructor import Constructor

    if __name__ == '__main__':
        Test = Tag_Test_Class(Debug=3, Allow_Corrupt=True,
                              Print_Test=True, Save_Test=False,
                              Write_as_Temp=True, Backup_Old_Tags=False,
                              Constructor=Constructor,
                              #Valid_Tag_IDs='xbe',
                              Valid_Tag_IDs='objects.ps2',
                              Print_Options={'Indent':4, 'Print_Raw':True,
                                             'Printout':True, 'Precision':3,
                                             'Show':['Name', 'Children', #'Type',
                                                     'Value',#'Offset', 'Py_ID',
                                                     'Index', # 'Elements',
                                                     'Size', #'Flags', 'Unique',
                                                     'Tag_Path', 'Bin_Size','Ram_Size',
                                                     #'All'
                                                     ] })
        Test.Run_Test()
except:
    print(format_exc())
    input()
    
Tag = Test.Tag_Collection['objects.ps2']['gdl\\sum\\OBJECTS.PS2']
