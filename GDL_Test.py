import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    valid_id='rom'
   
    test = GdlHandler(debug=3, allow_corrupt=True,
                       print_test=False, save_test=False, int_test=False,
                       write_as_temp=True, backup=False,
                       valid_def_ids=valid_id,
                       print_options={'indent':4,
                                      'printout':True, 'precision':3,
                                      'show':['name', 'children', #'field',
                                              'value','offset',# 'py_id',
                                              'index', 'flags',# 'size', 'unique',
                                              'filepath', 'binsize','ramsize',
                                              #'all'
                                              ] })
    #Test.Run_Test()
    cProfile.run('test.load_tags_and_run()')
    objs = test.tags.get(valid_id)
    input()
    if objs is not None:
        for filepath in objs:
            print("Size of: "+filepath+" = ", objs[filepath].data.binsize)
            objs[filepath].pprint(show=('name', 'value', 'children',
                                        'flags', 'field', 'offset',
                                        'raw'),#, 'all'),
                                  printout=True)
    input()
except Exception:
    print(format_exc())
    input()
