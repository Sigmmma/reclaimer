from traceback import format_exc
from ..handler import GdlHandler
from .widget_picker import *
from supyr_struct.apps.binilla.app_window import Binilla


class GdlBinilla(Binilla):
    app_name = 'GDL Binilla'
    version = '0.1'

    widget_picker = def_gdl_widget_picker

    def __init__(self, *args, **kwargs):
        kwargs['handler'] = GdlHandler()
        Binilla.__init__(self, *args, **kwargs)
