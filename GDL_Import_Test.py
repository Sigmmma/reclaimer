import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    test = GdlHandler(debug=3, valid_def_ids='objects', print_test=False)

    test_tag = test.build_tag(def_id='objects')
    test_tag.filepath = ('e:\\Applications\\My Repos\\Reclaimer\\'+
                         'tags\\gdl\\ICE\\OBJECTS.PS2')
    test_tag.import_data()
    print(test_tag)
        
    input('Finished.')
except Exception:
    print(format_exc())
    input()
