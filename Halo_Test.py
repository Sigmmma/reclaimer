from traceback import format_exc
from time import time
try:
    from supyr_struct.Test import Tag_Test_Class
    from ReclaimerLib.Tag_Constructors.Halo_Constructors.\
         HEK.Constructor import Constructor

    if __name__ == '__main__':
        Test = Tag_Test_Class(Print_Test=True, Save_Test=False, Debug=3,
                              Write_as_Temp=False, Backup_Old_Tags=False,
                              #Valid_Tag_IDs="ustr",
                              Constructor = Constructor,
                              Print_Options={'Indent':4, 'Print_Raw':False,
                                             'Printout':True, 'Precision':3,
                                             'Show':['Name', 'Children', 'Type',
                                                     'Value', 'Offset', 'Size',
                                                     'Elements', 'Index', #'Flags',
                                                     'Tag_Path', #'Unique', 
                                                     'Bin_Size', 'Ram_Size'] })
        Test.Run_Test()
        '''
        Test.Full_Debugging = False
        True_Times = []
        False_Times = []
        
        for i in range(30):
            start = time()
            Test.Load_Tags_and_Run()
            if Test.Full_Debugging:
                True_Times.append(time()-start)
            else:
                False_Times.append(time()-start)
            
            Test.Full_Debugging = not Test.Full_Debugging

        print("Debugging Times:")
        print(True_Times)
        print("Average Debugging Time:", sum(True_Times)/len(True_Times))
        print("Non-Debugging Times:")
        print(False_Times)
        print("Average Non-Debugging Time:", sum(False_Times)/len(False_Times))
        '''
except:
    print(format_exc())
    input()
    
Strings = Test.Tag_Collection['ustr']
TT = Strings['halo\strings\multiplayer_game_text.unicode_string_list']
TD = TT.Tag_Data.Data

#TT.Print(Show="All", Printout=True)
t = TD.Strings
