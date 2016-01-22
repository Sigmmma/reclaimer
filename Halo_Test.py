import cProfile
from traceback import format_exc
from time import time

try:
    from ReclaimerLib.Halo.HEK.Library import Halo_Library

    Test = Halo_Library(Print_Test=True, Save_Test=False, Debug=3,
                        Write_as_Temp=False, Backup_Old_Tags=False,
                        Allow_Corrupt=True,
                        #Valid_Tag_IDs="metr",
                        Print_Options={'Indent':4,
                                       'Printout':True, 'Precision':3,
                                       'Show':['Name', 'Children', 'Type',
                                               'Value', 'Offset', 'Size',
                                               'Index', 'Flags',
                                               'Tag_Path', #'Unique', 'Py_Type',
                                               'Bin_Size', 'Ram_Size'] })
    Test.Run_Test()
    #cProfile.run('Test.Load_Tags_and_Run()')
    #input()

except Exception:
    print(format_exc())
    input()
