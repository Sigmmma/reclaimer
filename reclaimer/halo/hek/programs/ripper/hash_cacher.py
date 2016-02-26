from os.path import dirname
from string import digits, ascii_letters
from traceback import format_exc

from ..hek_tag_scanner import HekTagScanner
from ....fields import TagIndexRef, Reflexive, RawDataRef
from supyr_struct.handler import Handler
from supyr_struct.tag import Tag


valid_path_chars = " ()-_%s%s" % (digits, ascii_letters)


class HashCacher(Handler):
    default_defs_path = "reclaimer.halo.hek.programs.ripper.defs"
    
    #initialize the class
    def __init__(self, **kwargs):
        Handler.__init__(self, **kwargs)
        self.tagsdir = dirname(__file__)+"\\hash_caches\\"
        
        self.tag_lib = HekTagScanner()
        self.tag_lib.print_to_console = True
        self.tag_lib.feedback_interval = 5

        self.hashsize = 16
        self.hashmethod = 'md5'
        self.main_hashmap = {}

    '''this will significantly speed up indexing tags since the default
    Handler.get_tag_id method doesnt open each file and try to read
    the 4CC Tag_Cls from the header, but just matches file extensions'''
    get_tag_id = Handler.get_tag_id


    def build_hashcache(self, cache_name, description, tagsdir, subdir=''):
        tag_lib = self.tag_lib
        tag_lib.tagsdir = tagsdir
        
        print('Indexing...')
        tag_lib.mode = 1
        
        tag_lib.index_tags()
        tag_lib.mode = 2
        print('\nFound %s tags...' % tag_lib.tags_indexed)

        hashmap = {}
        
        try:
            tagsdir = tag_lib.tagsdir
            tags    = tag_lib.tags
            
            for tag_id in sorted(tags):
                if tag_lib.print_to_console:
                    tag_lib.print_to_console = False
                    print(" "*4+ "Hashing '%s' tags..." % tag_id)
                    tag_lib.print_to_console = True
                    
                tag_ref_paths   = tag_lib.tag_ref_cache.get(tag_id, ())
                reflexive_paths = tag_lib.reflexive_cache.get(tag_id, ())
                raw_data_paths  = tag_lib.raw_data_cache.get(tag_id, ())

                tag_coll = tags[tag_id]
                
                for tagpath in sorted(tag_coll):
                    try:
                        #if this tag isnt located in the sub
                        #directory being scanned, then skip it
                        if not tagpath.startswith(subdir):
                            continue
                            
                        tag_lib.current_tag = tagpath
                        tag = tag_lib.build_tag(filepath=tagsdir+tagpath)
                        tagdata = tag.tagdata
                        
                        '''need to do some extra stuff for certain
                        tags with fields that are normally zeroed
                        out as tags, but arent as meta'''
                        if tag_id == 'pphy':
                            Data = tagdata.Data
                            Data.Wind_Coefficient = 0
                            Data.Wind_Sine_Modifier = 0
                            Data.Z_Translation_Rate = 0

                        hash_buffer = tag_lib.get_tag_hash(tagdata,
                                                           tag_ref_paths,
                                                           reflexive_paths,
                                                           raw_data_paths)
                        taghash = hash_buffer.digest()
                        
                        if taghash in hashmap:
                            tag_lib.print_to_console = False
                            print(("WARNING: hash already exists\n"+
                                   "    hash:%s\n"+
                                   "    Path(existing): '%s'\n"+
                                   "    Path(colliding):'%s'\n")
                                  % (taghash, hashmap[taghash], tagpath) )
                            tag_lib.print_to_console = True
                        else:
                            hashmap[taghash] = tagpath
                            
                        #delete the tag and hash buffer to help conserve ram
                        del tag_coll[tagpath]
                        del hash_buffer
                        
                    except Exception:
                        print(format_exc())
                       
            tag_lib.mode = 100
            print('Building hashcache...')
            cache = self.hashmap_to_hashcache(hashmap, cache_name, description)
            
            print('Writing hashcache...')
            cache.write(temp=False, backup=False, int_test=False)
            
            return cache
        except:
            tag_lib.mode = 100
            print(format_exc())
        
        tag_lib.mode = 100


    def add_tag_to_hashmap(self, tagpath, hashmap):
        tag_lib  = self.tag_lib
        
        tag     = tag_lib.build_tag(filepath=tag_lib.tagsdir + tagpath)
        tagdata = tag.tagdata
        tag_id  = tag.tag_id      

        hash_buffer = tag_lib.get_tag_hash(tagdata,
                                           tag_lib.tag_ref_cache[tag_id],
                                           tag_lib.reflexive_cache[tag_id],
                                           tag_lib.raw_data_cache[tag_id])
        taghash = hash_buffer.digest()
        #hash buffer to help conserve ram
        del hash_buffer
        
        if taghash in hashmap:
            print(("WARNING: hash already exists\n"+
                   "    hash:%s\n"+
                   "    path(existing): '%s'\n"+
                   "    path(colliding):'%s'\n")
                  % (taghash, hashmap[taghash], tagpath) )
        else:
            hashmap[taghash] = tagpath
        
        return taghash


    def hashmap_to_hashcache(self, hashmap, cache_name="untitled",
                             cache_description='<no description>'):
        cache = self.build_tag(tag_id='hashcache')
        
        cache.tagdata.header.hashsize   = self.hashsize
        cache.tagdata.header.hashmethod = self.hashmethod
        cache.tagdata.cache_name        = str(cache_name)
        cache.tagdata.cache_description = str(cache_description)

        cache_name = ''.join(c for c in cache_name if c in valid_path_chars)
        if not cache_name:
            cache_name = "untitled"
        cache.tagpath = self.tagsdir + cache_name + ".hashcache"
        
        cache_array = cache.tagdata.cache
        cache_array.extend(len(hashmap))
        
        i = 0
        for taghash in sorted(hashmap):
            cache_array[i].hash  = taghash
            cache_array[i].value = hashmap[taghash]
            i += 1

        return cache


    def hashcache_to_hashmap(self, hashcache):
        hashmap = {}
        cache_array = hashcache.tagdata.cache
        
        for mapping in cache_array:
            hashmap[mapping.hash] = mapping.value

        return hashmap


    def load_all_hashmaps(self):
        self.index_tags()
        self.load_tags()
        
        for hashcache in self.tags['hashcache'].values():
            self.update_hashmap(hashcache)


    def update_hashmap(self, new_hashes, hashmap=None, overwrite=False):
        if hashmap is None:
            hashmap = self.main_hashmap
            
        if isinstance(new_hashes, dict):
            if overwrite:
                hashmap.update(new_hashes)
                return
            
            for taghash in new_hashes:
                if taghash not in hashmap:
                    hashmap[taghash] = new_hashes[taghash]
                    
        elif isinstance(new_hashes, Tag):
            new_hashes = new_hashes.tagdata.cache
            
            if overwrite:
                for mapping in new_hashes:
                    hashmap[mapping.hash] = mapping.value
                return
            
            for mapping in new_hashes:
                taghash = mapping.hash
                
                if taghash not in hashmap:
                    hashmap[taghash] = mapping.value
