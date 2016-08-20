from os.path import dirname
from traceback import format_exc
from time import time
this_dir = dirname(__file__)

try:
    from reclaimer.halo.hek.programs.ripper.tag_ripper import TagRipper

    tags_path = ('e:\\Applications\\My Repos\Reclaimer\\tags\\')
    mappath = tags_path + 'longest.map'
    #mappath = tags_path + "precipice.map"
    ripper = TagRipper(debug=5, tagsdir=tags_path+'tags\\', allow_corrupt=True)
    print(ripper.tags.keys())
    input('Press Enter to begin ripping tags from:\n'+
          '    %s\n\n' % mappath)
        
    start = time()
    ripper.rip_tags(mappath)
    
    input('-'*80 + '\n'+
          'Finished ripping tags.\n'+
          'Operation took %s seconds.\n'%(time()-start) +
          '\n'+
          'Press enter to exit.')

except:
    print(format_exc())
    input()
