import cProfile
from traceback import format_exc
from copy import copy
try:
    from ReclaimerLib.GDL.Library import GDL_Library

    Test = GDL_Library(Debug=3, Allow_Corrupt=True,
                       Print_Test=False, Save_Test=False, Int_Test=False,
                       Write_as_Temp=True, Backup_Old_Tags=False,
                       #Valid_Tag_IDs='xbe',
                       Valid_Tag_IDs='objects.ps2',
                       Print_Options={'Indent':4,
                                      'Printout':True, 'Precision':3,
                                      'Show':['Name', 'Children', #'Type',
                                              'Value','Offset',# 'Py_ID',
                                              'Index', 'Flags',# 'Size', 'Unique',
                                              'Tag_Path', 'Bin_Size','Ram_Size',
                                              #'All'
                                              ] })
    #Test.Run_Test()
    cProfile.run('Test.Load_Tags_and_Run()')
    Objs = Test.Tags.get('objects.ps2')
    input()
    if Objs is not None:
        for Tag_Path in Objs:
            print("Size of: "+Tag_Path+" = ", Objs[Tag_Path].Tag_Data.Bin_Size)
            Objs[Tag_Path].Print(Show=('Name','Value','Children','Flags', 'Offset', 'Raw'),
                                 Printout=True)
    input()
except Exception:
    print(format_exc())
    input()
