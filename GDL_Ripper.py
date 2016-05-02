import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    test = GdlHandler(debug=3, valid_def_ids='objects', print_test=False)
    input('Hit enter when ready to load.')
    
    test.load_tags_and_run()
    
    input('Hit enter when ready to rip.')
    
    for filepath in test.tags['objects']:
        test.tags['objects'][filepath].extract(True,True,True,True)
        
    input('Extraction finished.')
except Exception:
    print(format_exc())
    input()
