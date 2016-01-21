from hashlib import md5
from os.path import abspath, exists, dirname
from traceback import format_exc
from time import time

from ..HEK_Tag_Scanner import HEK_Tag_Scanner
from ....Field_Types import Tag_Index_Ref, Reflexive, Raw_Data_Ref
from supyr_struct.Library import Library
from supyr_struct.Buffer import BytearrayBuffer

class Hash_Cacher(Library):
    Default_Defs_Path = "ReclaimerLib.Halo.HEK.Programs.Tag_Ripper.Defs"
    
    #initialize the class
    def __init__(self, **kwargs):
        Library.__init__(self, **kwargs)

    '''this will significantly speed up indexing tags since the default
    Library.Get_Cls_ID method doesnt open each file and try to read
    the 4CC Tag_Cls from the header, but just matches file extensions'''
    Get_Cls_ID = Library.Get_Cls_ID

    def Load_Tags_and_Run(self):
        This_Dir = dirname(__file__)
        self.Tags_Dir = This_Dir+"\\Name_Caches\\"
        
        Tag_Lib = HEK_Tag_Scanner(Tags_Dir=This_Dir+"\\all_original_tags\\")
        Tag_Lib.Print_To_Console = True
        Tag_Lib.Feedback_Interval = 5
        
        Hash_Buffer = BytearrayBuffer()

        New_Cache = self.Build_Tag(Cls_ID='hashcache')
        New_Cache.Tag_Data.Header.Hash_Size = 16
        New_Cache.Tag_Data.Header.Method    = 'md5'
        New_Cache.Tag_Data.Cache_Name       = 'All Original Halo 1 Tags'
        New_Cache.Tag_Path = This_Dir + "\\Name_Caches\\BASE.hashcache"

        
        print('Press Enter to begin scanning in:\n'+
              '    %s\n\n' % Tag_Lib.Tags_Dir)
        input()
        start = time()
        
        print('Indexing...')
        Tag_Lib.Mode = 1
        
        Tag_Lib.Index_Tags()
        Tag_Lib.Mode = 2
        print('\nFound %s tags...' % Tag_Lib.Tags_Indexed)

        Hash_Map = {}
        
        try:
            Tags_Dir = Tag_Lib.Tags_Dir
            Tags = Tag_Lib.Tags
            Get_Blocks = Tag_Lib.Get_Blocks_By_Paths
            
            for Cls_ID in sorted(Tags):
                if Tag_Lib.Print_To_Console:
                    Tag_Lib.Print_To_Console = False
                    print(" "*4+ "Hashing '%s' tags..." % Cls_ID)
                    Tag_Lib.Print_To_Console = True
                    
                Tag_Ref_Paths   = Tag_Lib.Tag_Ref_Cache.get(Cls_ID,[])
                Reflexive_Paths = Tag_Lib.Reflexive_Cache.get(Cls_ID,[])
                Raw_Data_Paths  = Tag_Lib.Raw_Data_Cache.get(Cls_ID,[])

                Tag_Coll = Tags[Cls_ID]
                
                for Tag_Path in sorted(Tag_Coll):
                    try:
                        Tag_Lib.Current_Tag = Tag_Path
                        Tag = Tag_Lib.Build_Tag(Filepath=Tags_Dir+Tag_Path)
                        Tag_Data = Tag.Tag_Data
                        
                        Tag_Refs   = Get_Blocks(Tag_Ref_Paths,   Tag_Data)
                        Reflexives = Get_Blocks(Reflexive_Paths, Tag_Data)
                        Raw_Datas  = Get_Blocks(Raw_Data_Paths,  Tag_Data)

                        #null out the parts of a tag that can screw
                        #with the hash when compared to a tag meta                        
                        for B in Tag_Refs:
                            B.Tag_Path_Pointer = B.Tag_ID = 0
                            
                        for B in Reflexives:
                            B.ID = B.Reflexive_ID = 0
                            
                        for B in Raw_Datas:
                            B.Unknown_1 = B.Unknown_2 = B.Unknown_3 = B.ID = 0

                        #write the tag data to the hash buffer
                        Tag_Data.Data.TYPE.Writer(Tag_Data.Data, Hash_Buffer, None, 0, 0)
                        Hash = md5(Hash_Buffer).digest()
                        
                        if Hash in Hash_Map:
                            Tag_Lib.Print_To_Console = False
                            print(("WARNING: Hash already exists\n"+
                                   "    Hash:%s\n"+
                                   "    Tag_Path(existing): '%s'\n"+
                                   "    Tag_Path(colliding):'%s'\n")
                                  % (Hash, Hash_Map[Hash], Tag_Path) )
                            Tag_Lib.Print_To_Console = True
                        else:
                            Hash_Map[Hash] = Tag_Path
                            
                        #delete the tag to help conserve ram and reset the hash buffer
                        del Tag_Coll[Tag_Path]
                        del Hash_Buffer[:]
                        Hash_Buffer.seek(0)
                        
                    except Exception:
                        print(format_exc())
                       
            Tag_Lib.Mode = 100
            print('Extending hash cache...')
            
            Cache_Array = New_Cache.Tag_Data.Cache
            Cache_Array.extend(len(Hash_Map))
            i = 0
            for Hash in Hash_Map:
                Cache_Array[i].Hash = Hash
                Cache_Array[i].Hash_Name = Hash_Map[Hash]
                i += 1
                
            print('Writing hash cache...')
            New_Cache.Write(Temp=False, Backup=False, Int_Test=False)
        except:
            Tag_Lib.Mode = 100
            print(format_exc())
        
        Tag_Lib.Mode = 100
        print('-'*80 + '\n'+
              'Finished scanning tags directory.'+
              'Operation took %s seconds.\n'%(time()-start) +
              '\n'+
              'Press enter to exit.')
        input()
        raise SystemExit()
