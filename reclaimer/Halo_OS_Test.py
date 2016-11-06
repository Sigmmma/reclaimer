import cProfile
from traceback import format_exc
from time import time

try:
    from reclaimer.halo.os_hek.handler import OsHaloHandler
    #cProfile.run('test = HaloHandler(debug=5)')
    #input()
    test = OsHaloHandler( print_test=True, save_test=False, debug=5,
                          write_as_temp=True, backup=False,
                          allow_corrupt=True,
                          #valid_def_ids=('gelc'),
                          print_options={'indent':4,
                                         'printout':True, 'precision':3,
                                         'show':['name', 'steptrees', 'type',
                                                 'value', 'offset',# 'size', 
                                                 'index', 'flags',# 'node_id',
                                                 'filepath', #'unique', 'node_cls',
                                                 'binsize', 'ramsize'] })
    test.prompt_test()
    #cProfile.run('test.prompt_test()')
    #input()

except:
    print(format_exc())
    input()