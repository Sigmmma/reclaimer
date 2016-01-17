import os
import threading

from os.path import exists
from pprint import pprint
from time import time
from traceback import format_exc

from ..Library import Halo_Library
from ...Field_Types import Tag_Index_Ref
from supyr_struct.Library import Library

class HEK_Tag_Scanner(Halo_Library):
    Log_Filename = "HEK_Tag_Scanner.log"
    Print_To_Console = False

    Print_Interval = 10
    Mode = 0
    
    #initialize the class
    def __init__(self, **kwargs):
        Halo_Library.__init__(self, **kwargs)

        #call the function to build the Tag_Ref_Loc_Cache
        self.Build_Loc_Cache()

        #make a new defs dict
        Defs = {}

        #remove tags from the definitions which never have tag refs in them
        for Cls_ID in sorted(self.Defs.keys()):
            
            #if the key exists in self.Tag_Ref_Loc_Cache, copy the def
            if Cls_ID in self.Tag_Ref_Loc_Cache:
                Defs[Cls_ID] = self.Defs[Cls_ID]

        #replace self.Defs with the new defs and erase
        #self.Tags and replace it with a fresh one
        self.Defs = Defs
        self.Tags = {}
        self.Reset_Tags(Defs.keys())
        
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
            
            if self.Print_To_Console and time()-start >= self.Print_Interval:
                start = time()
                if self.Mode in range(1, 3):
                    print(' '*4+self.Current_Tag.split(self.Tags_Dir)[-1])
                    

    def _Build_Loc_Cache_Loop(self, Desc={}):
        Has_Refs = False
        Refs = {}

        try:
            Type = Desc['TYPE']
        except Exception:
            Type = None
        
        if Type is Tag_Index_Ref:
            return True, None
        elif Type is not None:
            for key in Desc:
                Has_Sub_Refs, Sub_Refs = self._Build_Loc_Cache_Loop(Desc[key])
            
                if Has_Sub_Refs:
                    Has_Refs = True
                    Refs[key] = Sub_Refs
                    
        return Has_Refs, Refs
    

    def Build_Loc_Cache(self):
        '''this is a cache of paths that will be used to
        quickly locate tag references in structures by
        caching all possible locations of a tag reference'''
        self.Tag_Ref_Loc_Cache = {}
        
        for Cls_ID in self.Defs:
            Def = self.Defs[Cls_ID].Tag_Structure

            Has_Refs, Refs = self._Build_Loc_Cache_Loop(Def)
            
            if Has_Refs:
                self.Tag_Ref_Loc_Cache[Cls_ID] = Refs

        

    def Scan_Tags_Dir(self, **kwargs):
        #this is the string to store the entire debug log
        Debug_Log_String = ("Debug log for HEK Tag Scanner\n\n\n")
        
        '''loop through both chicago and extended chicago tag types'''
        for Cls_ID in sorted(self.Tag_Ref_Loc_Cache.keys()):

            Tag_Ref_Paths = self.Tag_Ref_Loc_Cache[Cls_ID]
            if self.Print_To_Console:
                print(" "*4+ "Scanning '%s' tags..." % Cls_ID)

            '''loop through each tag and remove extra
            layers and log them to a debug file'''
            for Tag_Path in sorted(self.Tags[Cls_ID].keys()):
                Tag = self.Tags[Cls_ID][Tag_Path]
                self.Current_Tag = Tag_Path
                
                Missing = []
                
                try:
                    self._Scan_Tags_Dir_Loop(Tag_Ref_Paths,
                                             Tag.Tag_Data, Missing)

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


    def _Scan_Tags_Dir_Loop(self, Paths, Block, Missing):
        if Paths is None:
            if not self.Get_Tag_Exists(Block):
                Missing.append(Block)
            return
        
        elif isinstance(Paths, dict):
            if 'SUB_STRUCT' in Paths:
                Paths = Paths['SUB_STRUCT']
                for i in range(len(Block)):
                    self._Scan_Tags_Dir_Loop(Paths, Block[i], Missing)
            else:
                for key in Paths:
                    self._Scan_Tags_Dir_Loop(Paths[key], Block[key], Missing)
        else:
            raise TypeError("Expected 'Paths' to be of type %s or %s, not %s."%
                            (type(None), type(dict), type(paths)) )


    def Get_Tag_Exists(self, Block):
        #if the string is empty, then it doesnt NOT exist, so return True
        if not Block.CHILD:
            return True
        Tag_Path = self.Tags_Dir
        Tag_Path += Block.CHILD
        
        try:
            Tag_Path += '.'+Block.Tag_Class.Data_Name
        except Exception:
            pass
        
        return exists(Tag_Path)


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
        print('This program will scan the tags directory and locate\n'
              'tags that reference other tags. A log will be created\n'+
              'in the tags directory and any tag references that\n'+
              'cannot be found in the tags directory will be logged.\n\n'+
              'This program will periodically print the path of the\n'+
              'tag it is currently indexing/loading/scanning relative\n'+
              'to the tags directory as a sort of progress update.\n\n'+
              
              'Press Enter to begin scanning in:\n'+
              '    %s\n\n' % self.Tags_Dir)
        input()
        
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
            print('Tags directory is either empty, doesnt '+
                  'exist, or cannot be accessed')
        
        self.Mode = 100
        print('-'*80 + '\nFinished scanning tags directory.\n'+
              'Check the tags directory for the log.\n' + '-'*80 +
              '\n\nPress enter to exit.')
        input()
