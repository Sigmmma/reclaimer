import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    test = GdlHandler(debug=3, valid_def_ids='objects', print_test=False)
    inp = ''
    inp = input('Type in extraction operators:\n\n'+
                '  d     == defs\n'+
                '  t     == textures\n'+
                '  m     == models\n'+
                '  a     == animations\n\n'+
                '  i     == individual models\n'+
                '  ow    == overwrite\n'+
                '  mips  == mipmaps\n'+
                '  alpha == alpha palette\n>>> ').lower().split(' ')
    cmd = set(c for c in ('i','m','a','d','t','o',
                          'mips','alpha') if c in inp)
    
    while not cmd:
        inp = input('Type in extraction operators:\n>>> ').lower().split(' ')
        cmd = set(c for c in ('i','m','a','d','t','o',
                              'mips','alpha') if c in inp)

    print('Loading tags. Please wait...')
    
    test.load_tags_and_run()
    
    input('Hit enter when ready to rip.')
    
    for filepath in sorted(test.tags['objects']):
        print('extracting:', filepath)
        test.tags['objects'][filepath].extract(defs='d' in cmd,
                                               mod='m' in cmd,
                                               tex='t' in cmd,
                                               anim='a' in cmd,
                                               individual='i' in cmd,
                                               overwrite='ow' in cmd,
                                               mips='mips' in cmd,
                                               alpha_pal='alpha' in cmd)
        del test.tags['objects'][filepath]
        
    input('Extraction finished.')
except Exception:
    print(format_exc())
    input()
