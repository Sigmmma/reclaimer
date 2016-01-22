import os
import threading

from os.path import exists
from pprint import pprint
from time import time
from traceback import format_exc

from ..Library import Halo_Library
from ...Field_Types import Tag_Index_Ref, Reflexive, Raw_Data_Ref
from supyr_struct.Library import Library

class HEK_Tag_Scanner(Halo_Library):
    Log_Filename = "HEK_Tag_Scanner.log"
    Print_To_Console = False

    Feedback_Interval = 10
    Feedback_Indent   = 8
    Mode = 0
    
    #initialize the class
    def __init__(self, **kwargs):
        Halo_Library.__init__(self, **kwargs)
        
        #Create and start the feedback printout thread
        self._Feedback_Thread = threading.Thread(target=self._Feedback)
        self._Feedback_Thread.daemon = True
        self._Feedback_Thread.start()


    '''this will significantly speed up indexing tags since the default
    Library.Get_Cls_ID method doesnt open each file and try to read
    the 4CC Tag_Cls from the header, but just matches file extensions'''
    Get_Cls_ID = Library.Get_Cls_ID

    def _Feedback(self):
        start = time()
        while True:
            if self.Print_To_Console and time()-start >= self.Feedback_Interval:
                start = time()
                if self.Mode in range(1, 3):
                    print(' '*self.Feedback_Indent +
                          self.Current_Tag.split(self.Tags_Dir)[-1])


    def Load_Tags(self, Paths = None):        
        #local references for faster access
        Dir       = self.Tags_Dir
        Tags      = self.Tags
        Allow     = self.Allow_Corrupt
        New_Tag   = None
        Build_Tag = self.Build_Tag      

        #Loop over each Cls_ID in the tag paths to load in sorted order
        for Cls_ID in sorted(Tags):
            Tag_Coll = Tags.get(Cls_ID)

            if not isinstance(Tag_Coll, dict):
                Tag_Coll = Tags[Cls_ID] = {}
            
            #Loop through each Tag_Path in Coll in sorted order
            for Tag_Path in sorted(Tags[Cls_ID]):
                
                #only load the tag if it isnt already loaded
                if Tag_Coll.get(Tag_Path) is None:
                    self.Current_Tag = Tag_Path
                        
                    '''incrementing Tags_Loaded and decrementing Tags_Indexed
                    in this loop is done for reporting the loading progress'''
                    
                    try:
                        New_Tag = Build_Tag(Filepath = Dir+Tag_Path,
                                            Allow_Corrupt = Allow)
                        Tag_Coll[Tag_Path] = New_Tag
                        self.Tags_Loaded += 1
                    except (OSError, MemoryError) as e:
                        print(format_exc())
                        print('Not enough accessable memory to continue '+
                              'loading tags. Ran out while opening\\reading:'+
                              ('\n    %s\n    Remaining unloaded tags will ' +
                               'be de-indexed and skipped\n') % Tag_Path)
                        del Tag_Coll[Tag_Path]
                        self.Clear_Unloaded_Tags()
                        return
                    except Exception:
                        print('Error encountered while opening\\reading:'+
                              '\n    %s\n    Tag may be corrupt\n' % Tag_Path )
                        del Tag_Coll[Tag_Path]
                    self.Tags_Indexed -= 1

        #recount how many tags are loaded/indexed
        self.Tally_Tags()
        
        return self.Tags_Loaded
        

    def Load_Tags_and_Run(self):
        self.Print_To_Console = True

        #make a new defs dict
        Defs = {}

        #remove tags from the definitions which never have tag refs in them
        for Cls_ID in sorted(self.Defs.keys()):
            
            #if the key exists in self.Tag_Ref_Cache, copy the def
            if Cls_ID in self.Tag_Ref_Cache:
                Defs[Cls_ID] = self.Defs[Cls_ID]

        #replace self.Defs with the new defs and erase
        #self.Tags and replace it with a fresh one
        self.Defs = Defs
        self.Tags = {}
        self.Reset_Tags(Defs.keys())
        
        input('This program will scan the tags directory and locate\n'
              'tags that reference other tags. A log will be created\n'+
              'in the tags directory and any tag references that\n'+
              'cannot be found in the tags directory will be logged.\n\n'+
              'This program will periodically print the path of the\n'+
              'tag it is currently indexing/loading/scanning relative\n'+
              'to the tags directory as a sort of progress update.\n\n'+
              
              'Press Enter to begin scanning in:\n'+
              '    %s\n\n' % self.Tags_Dir)
        
        #Stream the data from the tags to class
        #constructs so the program can work with them
        print('Indexing...')
        self.Mode = 1
        if self.Index_Tags():
            print('\nLoading %s tags...' % self.Tags_Indexed)
            self.Mode = 2
            self.Load_Tags()

            print('\nScanning %s tags...' % self.Tags_Loaded)
            self.Mode = 3
            Debug_Log = self.Scan_Tags_Dir()
            
            print('\nWriting logfile...')
            self.Mode = 100
            #save the debug log to a file
            self.Make_Log_File(Debug_Log)
        else:
            #if something went wrong earlier this will notify the user
            self.Mode = 100
            input('Tags directory is either empty, doesnt '+
                  'exist, or cannot be accessed')
            raise SystemExit()
        
        self.Mode = 100
        input('-'*80 + '\nFinished scanning tags directory.\n'+
              'Check the tags directory for the log.\n' + '-'*80 +
              '\n\nPress enter to exit.')
        raise SystemExit()
        

    def Scan_Tags_Dir(self, **kwargs):
        #this is the string to store the entire debug log
        Debug_Log_String = ("Debug log for HEK Tag Scanner\n\n\n")
        
        '''loop through both chicago and extended chicago tag types'''
        for Cls_ID in sorted(self.Tag_Ref_Cache.keys()):

            Tag_Ref_Paths = self.Tag_Ref_Cache[Cls_ID]
            if self.Print_To_Console:
                print(" "*4+ "Scanning '%s' tags..." % Cls_ID)

            for Tag_Path in sorted(self.Tags[Cls_ID].keys()):
                Tag = self.Tags[Cls_ID][Tag_Path]
                self.Current_Tag = Tag_Path
                
                try:
                    Missing = self.Get_Blocks_By_Paths(Tag_Ref_Paths,
                                                       Tag.Tag_Data,
                                                       self.Get_Tag_Not_Exist)

                    if len(Missing):
                        Debug_Log_String += "\n\n%s\n" % Tag_Path
                        Block_Name = None
                        
                        for Block in Missing:
                            if Block.NAME != Block_Name:
                                Debug_Log_String += ' '*4 + Block.NAME + '\n'
                                Block_Name = Block.NAME
                            try:
                                Ext = '.'+Block.Tag_Class.Data_Name
                            except Exception:
                                Ext = ''
                            Debug_Log_String += ' '*8 + Block.CHILD + Ext + '\n'
                            
                except Exception:
                    print("ERROR OCCURRED WHILE ATTEMPTING TO SCAN:\n" +
                          '    ' + Tag.Tag_Path + '\n')
                    print(format_exc())
                    continue
                        
        
        return Debug_Log_String
