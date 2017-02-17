from ....misc.defs.objs.xboxsave import *

GDL_SIGKEY =  (b'\x04\x60\x07\x75\xB9\x14\xBF\xE3\x09\xAE'+
               b'\x40\x83\x70\xF1\x8E\xEA\xC0\xD7\xF9\x61')

class GdlSaveTag(XboxSaveTag):
    sigkey  = GDL_SIGKEY
