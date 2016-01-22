from hashlib import md5
from supyr_struct.Buffer import BytearrayBuffer
from supyr_struct.Field_Types import Field_Type
from supyr_struct.Tag_Blocks import Void_Block

from .Hash_Cacher import Hash_Cacher
from ....META.Library import Map_Loader

class Tag_Ripper(Map_Loader):

    def __init__(self, **kwargs):
        Map_Loader.__init__(self, **kwargs)
        
        self.Hash_Cacher = Hash_Cacher()
        self.Tag_Loader = self.Hash_Cacher.Tag_Lib

        #make a cache of all the different headers for
        #each type of tag to speed up writing tags
        self.Tag_Header_Cache = {}
        
        for Cls_ID in sorted(self.Tag_Loader.Defs):
            H_Desc = self.Tag_Loader.Defs[Cls_ID].Tag_Structure[0]
            
            H_Block = [None]
            H_Desc['TYPE'].Reader(H_Desc, H_Block, Attr_Index=0)
            H_Buffer = H_Block[0].Write(Buffer=BytearrayBuffer(),
                                        Calc_Pointers=False)
            
            self.Tag_Header_Cache[Cls_ID] = bytes(H_Buffer)

        #load all the hash caches we have
        self.Hash_Cacher.Load_All_Hashmaps()

        #create a mapping to map tag class id's to their string representation
        self.Tag_Class_Int_Name_Map = {}

        for val in self.Tag_Loader.ID_Ext_Map:
            key = int.from_bytes(bytes(val, encoding='latin1'), byteorder='big')
            self.Tag_Class_Int_Name_Map[key] = val


    def Rip_Tags(self, Map_Path):
        print('Loading map...')
        Map = self.Build_Tag(Filepath=Map_Path, Cls_ID='map')
        Tag_Index_Array = Map.Tag_Data.Tag_Index_Header.Tag_Index

        Hashmap = self.Hash_Cacher.Main_Hashmap
        Hash_Buffer = BytearrayBuffer()

        Tag_Ref_Cache   = self.Tag_Loader.Tag_Ref_Cache
        Reflexive_Cache = self.Tag_Loader.Reflexive_Cache
        Raw_Data_Cache  = self.Tag_Loader.Raw_Data_Cache

        Get_Blocks = self.Tag_Loader.Get_Blocks_By_Paths
        Cls_ID_Map = self.Tag_Class_Int_Name_Map

        #change the endianness of the library since we're now
        #going to treat all the meta data as if they were tags
        Field_Type.Force_Big()
        
        print('Checking tags against hashmap...')

        for Tag_Header in Tag_Index_Array:
            Cls_ID = Cls_ID_Map[Tag_Header.Tag_Class_1.Data]

            Tag_Data = Tag_Header.Tag_Data.Tag_Meta

            if isinstance(Tag_Data, Void_Block):
                '''The tag meta data doesnt actually exist,
                so see if it's one of these tag types.'''
                if Cls_ID == 'bitm':
                    #this is a bitmap tag, so check the bitmaps.map
                    #name cache for the name of this bitmap
                    Tag_Path = None
                elif Cls_ID == 'snd!':
                    #this is a sound tag, so check the sounds.map
                    #name cache for the name of this sound
                    Tag_Path = None
                else:
                    continue
            else:
                Tag_Ref_Paths   = Tag_Ref_Cache.get(Cls_ID)
                Reflexive_Paths = Reflexive_Cache.get(Cls_ID)
                Raw_Data_Paths  = Raw_Data_Cache.get(Cls_ID)
                
                #null out the parts of a tag that can screw
                #with the hash when compared to a tag meta
                
                #FOR NOW DONT WORRY ABOUT MATCHING THESE TYPES OF TAGS
                if Tag_Ref_Paths:
                    continue
                    Tag_Ref_Blocks = Get_Blocks(Tag_Ref_Paths[1], Tag_Data)
                    for B in Tag_Ref_Blocks:
                        B.Tag_Path_Pointer = B.Tag_ID = 0
                    
                if Reflexive_Paths:
                    Reflexive_Blocks = Get_Blocks(Reflexive_Paths[1], Tag_Data)
                    for B in Reflexive_Blocks:
                        B.ID = B.Reflexive_ID = 0
                    
                if Raw_Data_Paths:
                    Raw_Data_Blocks = Get_Blocks(Raw_Data_Paths[1], Tag_Data)
                    for B in Raw_Data_Blocks:
                        B.Unknown_1 = B.Unknown_2 = B.Unknown_3 = B.ID = 0

                #need to do some extra stuff for certain tags with fields
                #that are normally zeroed out as tags, but arent as meta
                if Cls_ID == 'pphy':
                    Tag_Data.Wind_Coefficient = 0
                    Tag_Data.Wind_Sine_Modifier = 0
                    Tag_Data.Z_Translation_Rate = 0
                
                #write the tag data to the hash buffer
                Tag_Data.TYPE.Writer(Tag_Data, Hash_Buffer, None, 0, 0)

                #get the tag data's hash and try to match it to a path
                Hash = md5(Hash_Buffer).digest()
                Tag_Path = Hashmap.get(Hash)

            if Tag_Path is not None:
                print('HIT: %s'%Tag_Path)
            #else:
            #    print('MISS: %s'%Cls_ID)

            del Hash_Buffer[:]
            Hash_Buffer.seek(0)
