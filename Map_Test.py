import cProfile
from traceback import format_exc
from time import time

try:
    from ReclaimerLib.Halo.META.Library import Halo_Library

    if __name__ == '__main__':
        Test = Halo_Library(Print_Test=True, Save_Test=False, Debug=3,
                            Write_as_Temp=False, Backup_Old_Tags=False,
                            Valid_Tag_IDs="map",
                            Allow_Corrupt=True,
                            Print_Options={'Indent':4,
                                           'Printout':True, 'Precision':3,
                                           'Show':['Name', 'Children', 'Type',
                                                   'Value', #'Offset', 'Size',
                                                   'Index', 'Flags',
                                                   'Tag_Path', #'Unique', 'Py_Type',
                                                   'Bin_Size', 'Ram_Size'] })
        Test.Run_Test()
        #cProfile.run('Test.Load_Tags_and_Run()')
        #input()

except:
    print(format_exc())
    input()
