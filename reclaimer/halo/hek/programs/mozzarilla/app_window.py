from traceback import format_exc
from ...handler import HaloHandler
from ....meta.handler import MapLoader
from ....os_hek.handler import OsHaloHandler
from .widget_picker import *
from supyr_struct.apps.binilla.app_window import Binilla


class Mozzarilla(Binilla):
    app_name = 'Mozzarilla'
    version = '0.1'

    halo_handler = HaloHandler()
    halo_meta_handler = MapLoader()
    halo_os_handler = OsHaloHandler()
    widget_picker = def_halo_widget_picker

    def __init__(self, *args, **kwargs):
        kwargs['handler'] = self.halo_handler
        Binilla.__init__(self, *args, **kwargs)
