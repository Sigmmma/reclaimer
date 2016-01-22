from os.path import dirname
from string import digits, ascii_letters
from traceback import format_exc

from ..HEK_Tag_Scanner import HEK_Tag_Scanner
from ....Field_Types import Tag_Index_Ref, Reflexive, Raw_Data_Ref
from supyr_struct.Library import Library
from supyr_struct.Tag import Tag


Valid_Path_Chars = " ()-_%s%s" % (digits, ascii_letters)


class Hash_Cacher(Library):
    Default_Defs_Path = "ReclaimerLib.Halo.HEK.Programs.Tag_Ripper.Defs"
    
    #initialize the class
    def __init__(self, **kwargs):
        Library.__init__(self, **kwargs)
        self.Tags_Dir = dirname(__file__)+"\\Hash_Caches\\"
        
        self.Tag_Lib = HEK_Tag_Scanner()
        self.Tag_Lib.Print_To_Console = True
        self.Tag_Lib.Feedback_Interval = 5

        self.Hash_Size = 16
        self.Hash_Method = 'md5'
        self.Main_Hashmap = {}

    '''this will significantly speed up indexing tags since the default
    Library.Get_Cls_ID method doesnt open each file and try to read
    the 4CC Tag_Cls from the header, but just matches file extensions'''
    Get_Cls_ID = Library.Get_Cls_ID


    def Build_Hashcache(self, Cache_Name, Cache_Description,
                        Tags_Dir, Sub_Dir=''):
        Tag_Lib = self.Tag_Lib
        Tag_Lib.Tags_Dir = Tags_Dir
        
        print('Indexing...')
        Tag_Lib.Mode = 1
        
        Tag_Lib.Index_Tags()
        Tag_Lib.Mode = 2
        print('\nFound %s tags...' % Tag_Lib.Tags_Indexed)

        Hashmap = {}
        
        try:
            Tags_Dir = Tag_Lib.Tags_Dir
            Tags = Tag_Lib.Tags
            
            for Cls_ID in sorted(Tags):
                if Tag_Lib.Print_To_Console:
                    Tag_Lib.Print_To_Console = False
                    print(" "*4+ "Hashing '%s' tags..." % Cls_ID)
                    Tag_Lib.Print_To_Console = True
                    
                Tag_Ref_Paths   = Tag_Lib.Tag_Ref_Cache[Cls_ID]
                Reflexive_Paths = Tag_Lib.Reflexive_Cache[Cls_ID]
                Raw_Data_Paths  = Tag_Lib.Raw_Data_Cache[Cls_ID]

                Tag_Coll = Tags[Cls_ID]
                
                for Tag_Path in sorted(Tag_Coll):
                    try:
                        #if this tag isnt located in the sub
                        #directory being scanned, then skip it
                        if not Tag_Path.startswith(Sub_Dir):
                            continue
                            
                        Tag_Lib.Current_Tag = Tag_Path
                        Tag = Tag_Lib.Build_Tag(Filepath=Tags_Dir+Tag_Path)
                        Tag_Data = Tag.Tag_Data
                        
                        '''need to do some extra stuff for certain
                        tags with fields that are normally zeroed
                        out as tags, but arent as meta'''
                        if Cls_ID == 'pphy':
                            Data = Tag_Data.Data
                            Data.Wind_Coefficient = 0
                            Data.Wind_Sine_Modifier = 0
                            Data.Z_Translation_Rate = 0

                        Hash_Buffer = Tag_Lib.Get_Tag_Hash(Tag_Data,
                                                           Tag_Ref_Paths,
                                                           Reflexive_Paths,
                                                           Raw_Data_Paths)
                        Hash = Hash_Buffer.digest()
                        
                        if Hash in Hashmap:
                            Tag_Lib.Print_To_Console = False
                            print(("WARNING: Hash already exists\n"+
                                   "    Hash:%s\n"+
                                   "    Path(existing): '%s'\n"+
                                   "    Path(colliding):'%s'\n")
                                  % (Hash, Hashmap[Hash], Tag_Path) )
                            Tag_Lib.Print_To_Console = True
                        else:
                            Hashmap[Hash] = Tag_Path
                            
                        #delete the tag and hash buffer to help conserve ram
                        del Tag_Coll[Tag_Path]
                        del Hash_Buffer
                        
                    except Exception:
                        print(format_exc())
                       
            Tag_Lib.Mode = 100
            print('Building hashcache...')
            Cache = self.Hashmap_To_Hashcache(Hashmap, Cache_Name,
                                               Cache_Description)
            
            print('Writing hashcache...')
            Cache.Write(Temp=False, Backup=False, Int_Test=False)
        except:
            Tag_Lib.Mode = 100
            print(format_exc())
        
        Tag_Lib.Mode = 100

        return Cache


    def Add_Tag_To_Hashmap(self, Tag_Path, Hashmap):
        Tag_Lib  = self.Tag_Lib
        
        Tag = Tag_Lib.Build_Tag(Filepath=Tag_Lib.Tags_Dir + Tag_Path)
        Tag_Data = Tag.Tag_Data
        Cls_ID   = Tag.Cls_ID      

        Hash_Buffer = Tag_Lib.Get_Tag_Hash(Tag_Data,
                                           Tag_Lib.Tag_Ref_Cache[Cls_ID],
                                           Tag_Lib.Reflexive_Cache[Cls_ID],
                                           Tag_Lib.Raw_Data_Cache[Cls_ID])
        Hash = Hash_Buffer.digest()
        #hash buffer to help conserve ram
        del Hash_Buffer
        
        if Hash in Hashmap:
            print(("WARNING: Hash already exists\n"+
                   "    Hash:%s\n"+
                   "    Path(existing): '%s'\n"+
                   "    Path(colliding):'%s'\n")
                  % (Hash, Hashmap[Hash], Tag_Path) )
        else:
            Hashmap[Hash] = Tag_Path
        
        return Hash


    def Hashmap_To_Hashcache(self, Hashmap, Cache_Name="untitled",
                             Cache_Description='<no description>'):
        Cache = self.Build_Tag(Cls_ID='hashcache')
        
        Cache.Tag_Data.Header.Hash_Size  = self.Hash_Size
        Cache.Tag_Data.Header.Method     = self.Hash_Method
        Cache.Tag_Data.Cache_Name        = str(Cache_Name)
        Cache.Tag_Data.Cache_Description = str(Cache_Description)

        Cache_Name = ''.join(c for c in Cache_Name if c in Valid_Path_Chars)
        if not Cache_Name:
            Cache_Name = "untitled"
        Cache.Tag_Path = self.Tags_Dir + Cache_Name + ".hashcache"
        
        Cache_Array = Cache.Tag_Data.Cache
        Cache_Array.extend(len(Hashmap))
        
        i = 0
        for Hash in sorted(Hashmap):
            Cache_Array[i].Hash      = Hash
            Cache_Array[i].Hash_Name = Hashmap[Hash]
            i += 1

        return Cache


    def Hashcache_To_Hashmap(self, Hashcache):
        Hashmap = {}
        Cache_Array = Hashcache.Tag_Data.Cache
        
        for Mapping in Cache_Array:
            Hashmap[Mapping.Hash] = Mapping.Hash_Name

        return Hashmap


    def Load_All_Hashmaps(self):
        self.Index_Tags()
        self.Load_Tags()
        
        for Hashcache in self.Tags['hashcache'].values():
            self.Update_Hashmap(Hashcache)


    def Update_Hashmap(self, New_Hashes, Hashmap=None, Overwrite=False):
        if Hashmap is None:
            Hashmap = self.Main_Hashmap
            
        if isinstance(New_Hashes, dict):
            if Overwrite:
                Hashmap.update(New_Hashes)
                return
            
            for Hash in New_Hashes:
                if Hash not in Hashmap:
                    Hashmap[Hash] = New_Hashes[Hash]
                    
        elif isinstance(New_Hashes, Tag):
            New_Hashes = New_Hashes.Tag_Data.Cache
            
            if Overwrite:
                for Mapping in New_Hashes:
                    Hashmap[Mapping.Hash] = Mapping.Hash_Name
                return
            
            for Mapping in New_Hashes:
                Hash = Mapping.Hash
                
                if Hash not in Hashmap:
                    Hashmap[Hash] = Mapping.Hash_Name
