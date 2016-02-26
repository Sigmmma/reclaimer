import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    test = GdlHandler(debug=3, allow_corrupt=True,
                       print_test=False, save_test=False, int_test=False,
                       write_as_temp=True, backup=False,
                       #valid_tag_ids='xbe',
                       valid_tag_ids='objects.ps2',
                       print_options={'indent':4,
                                      'printout':True, 'precision':3,
                                      'show':['name', 'children', #'field',
                                              'value','offset',# 'py_id',
                                              'index', 'flags',# 'size', 'unique',
                                              'tagpath', 'binsize','ramsize',
                                              #'all'
                                              ] })
    #Test.Run_Test()
    cProfile.run('test.load_tags_and_run()')
    objs = test.tags.get('objects.ps2')
    input()
    if objs is not None:
        for tagpath in objs:
            print("Size of: "+tagpath+" = ", objs[tagpath].tagdata.binsize)
            objs[tagpath].pprint(show=('name', 'value', 'children',
                                       'flags', 'trueonly', 'offset',
                                       'raw'),#, 'all'),
                                 printout=True)
    input()
except Exception:
    print(format_exc())
    input()
