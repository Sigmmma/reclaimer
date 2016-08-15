from hashlib import md5
from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.fields import Field
from supyr_struct.blocks import VoidBlock
from supyr_struct.defs.constants import *

from .hash_cacher import HashCacher
from ....meta.handler import MapLoader

class TagRipper(MapLoader):

    def __init__(self, **kwargs):
        MapLoader.__init__(self, **kwargs)
        
        self.hash_cacher = HashCacher()
        self.tag_lib     = self.hash_cacher.tag_lib

        #make a cache of all the different headers for
        #each type of tag to speed up writing tags
        self.tag_headers = {}
        
        for def_id in sorted(self.tag_lib.defs):
            if len(def_id) != 4:
                continue
            h_desc = self.tag_lib.defs[def_id].descriptor[0]
            
            h_block = [None]
            h_desc['TYPE'].reader(h_desc, h_block, attr_index=0)
            b_buffer = h_block[0].serialize(buffer=BytearrayBuffer(),
                                            calc_pointers=False)
            
            self.tag_headers[def_id] = bytes(b_buffer)

        #load all the hash caches we have
        self.hash_cacher.load_all_hashmaps()

        #create a mapping to map tag class id's to their string representation
        self.def_id_int_name_map = {}

        for val in self.tag_lib.id_ext_map:
            key = int.from_bytes(bytes(val, encoding='latin1'), byteorder='big')
            self.def_id_int_name_map[key] = val


    def rip_tags(self, mappath):
        print('Loading map...')

        halomap = self.build_tag(filepath=mappath, def_id='map')
        tag_array = halomap.data.tag_index

        hashmap = self.hash_cacher.main_hashmap
        hash_buffer = BytearrayBuffer()

        tag_ref_cache   = self.tag_lib.tag_ref_cache
        reflexive_cache = self.tag_lib.reflexive_cache
        raw_data_cache  = self.tag_lib.raw_data_cache

        get_blocks = self.tag_lib.get_blocks_by_paths
        def_id_map = self.def_id_int_name_map

        #change the endianness of the library since we're now
        #going to treat all the meta data as if they were tags
        Field.force_big()

        print('Checking tags against hashmap...')

        for tag_header in tag_array:
            try:
                def_id = def_id_map[tag_header.tag_class_1.data]
            except Exception:
                continue

            tagmeta = tag_header.tag_data.tag_meta

            if isinstance(tagmeta, VoidBlock):
                '''The tag meta data doesnt actually exist,
                so see if it's one of these tag types.'''
                if def_id == 'bitm':
                    #this is a bitmap tag, so check the bitmaps.map
                    #name cache for the name of this bitmap
                    filepath = None
                elif def_id == 'snd!':
                    #this is a sound tag, so check the sounds.map
                    #name cache for the name of this sound
                    filepath = None
                else:
                    continue
            else:
                tag_ref_paths   = tag_ref_cache.get(def_id)
                reflexive_paths = reflexive_cache.get(def_id)
                raw_data_paths  = raw_data_cache.get(def_id)
                
                #null out the parts of a tag that can screw
                #with the hash when compared to a tag meta
                
                #FOR NOW DONT WORRY ABOUT MATCHING THESE TYPES OF TAGS
                if tag_ref_paths:
                    continue
                    tag_ref_blocks = get_blocks(tag_ref_paths[1], tagmeta)
                    for B in tag_ref_blocks:
                        B.tag_path_pointer = B.tag_id = 0
                    
                if reflexive_paths:
                    reflexive_blocks = get_blocks(reflexive_paths[1], tagmeta)
                    for B in reflexive_blocks:
                        B.id = B.reflexive_id = 0
                    
                if raw_data_paths:
                    raw_data_blocks = get_blocks(raw_data_paths[1], tagmeta)
                    for B in raw_data_blocks:
                        B.unknown_1 = B.unknown_2 = B.unknown_3 = B.id = 0

                #need to do some extra stuff for certain tags with fields
                #that are normally zeroed out as tags, but arent as meta
                if def_id == 'pphy':
                    tagmeta.wind_coefficient = 0
                    tagmeta.wind_sine_modifier = 0
                    tagmeta.z_translation_rate = 0
                
                #write the tag data to the hash buffer
                tagmeta.TYPE.writer(tagmeta, hash_buffer, None, 0, 0)

                #get the tag data's hash and try to match it to a path
                taghash = md5(hash_buffer).digest()
                filepath = hashmap.get(taghash)

                del hash_buffer[:]
                hash_buffer.seek(0)

            if filepath is not None:
                print('HIT: %s'%filepath)
            #else:
            #    print('MISS: %s'%def_id)
