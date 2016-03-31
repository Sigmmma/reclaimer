from os.path import dirname
from time import time
from traceback import format_exc

thisdir = dirname(__file__)

try:
    from reclaimer.halo.hek.programs.ripper.hash_cacher import HashCacher
    
    cacher = HashCacher()
    
    tagsdir = (thisdir+"\\reclaimer\\halo\\hek\\programs\\ripper\\all_original_tags\\")
    cache_name = 'Halo_1_Default'
    cache_description = ('All the tags that are used in the original Halo 1 '+
                         'singleplayer, multiplayer, and ui maps.\n'+
                         'This should always be used, and as the base cache.')
    input('Press Enter to begin scanning in:\n'+
          '    %s\n\n' % tagsdir)
        
    start = time()
    cache = cacher.build_hashcache(cache_name, cache_description, tagsdir)

    input('-'*80 + '\n'+
          'Finished scanning tags directory.'+
          'Operation took %s seconds.\n'%(time()-start) +
          '\n'+
          'Hit enter to print the constructed hashcache.\n'+
          'You may now exit this program at any time.')
    cache.pprint(printout=True)
except Exception:
    print(format_exc())
    input()

raise SystemExit()
