import tkinter as tk

from traceback import format_exc
from ...handler import HaloHandler
from ....meta.handler import MapLoader
from ....os_hek.handler import OsHaloHandler
from ....misc.handler import MiscHaloLoader
from .widget_picker import *
from supyr_struct.apps.binilla.app_window import *


class Mozzarilla(Binilla):
    app_name = 'Mozzarilla'
    version = '0.2'

    handlers = {
        "Halo 1": HaloHandler,
        "Halo 1 Open Sauce": OsHaloHandler,
        "Halo 1 Map Meta": MapLoader,
        "Halo 1 Misc": MiscHaloLoader,
        }

    _handler_menu_loc = {
        "Halo 1": 0,
        "Halo 1 Open Sauce": 1,
        "Halo 1 Map Meta": 2,
        "Halo 1 Misc": 3,
        }

    widget_picker = def_halo_widget_picker

    def __init__(self, *args, **kwargs):
        kwargs['handler'] = None
        Binilla.__init__(self, *args, **kwargs)

        self.main_menu.delete("Options")
        self.options_menu.destroy()
        del self.options_menu

        self.defs_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Tag set", menu=self.defs_menu)

        for n in ("", " Open Sauce", " Map Meta", " Misc"):
            n = "Halo 1" + n
            self.defs_menu.add_command(command=lambda n=n: self.select_defs(n))

        self.defs_menu.add_separator()

        self.select_defs("Halo 1", True)

    def load_tag_as(self, e=None):
        '''Prompts the user for a tag to load and loads it.'''
        if self.def_selector_window:
            return
        
        filetypes = [('All', '*')]
        defs = self.handler.defs
        for def_id in sorted(defs.keys()):
            filetypes.append((def_id, defs[def_id].ext))
        fp = askopenfilename(initialdir=self.last_load_dir,
                             filetypes=filetypes,
                             title="Select the tag to load")
        if fp != "":
            self.last_load_dir = dirname(fp)
            dsw = DefSelectorWindow(
                self, title="Which tag is this", action=lambda def_id:
                self.load_tags(filepaths=fp, def_id=def_id))
            self.def_selector_window = dsw
            self.place_window_relative(self.def_selector_window, 30, 50)

    def new_tag(self, e=None):
        if self.def_selector_window:
            return
        
        dsw = DefSelectorWindow(
            self, title="Select a tag to create", action=lambda def_id:
            self.load_tags(filepaths='', def_id=def_id))
        self.def_selector_window = dsw
        self.place_window_relative(self.def_selector_window, 30, 50)

    def select_defs(self, def_set, silent=False):
        handler = self.handlers.get(def_set)
        menu_locs = self._handler_menu_loc
        if handler is None or handler is self.handler:
            return

        if not silent:
            print("Changing tag set to %s" % def_set)
            self.update_idletasks()

        if isinstance(handler, type):
            handler = self.handlers[def_set] = handler()
        self.handler = self.handlers[def_set]

        entryconfig = self.defs_menu.entryconfig
        for label in self._handler_menu_loc.keys():
            entryconfig(menu_locs[label], label=label)

        entryconfig(menu_locs[def_set], label=("%s %s" % (def_set, u'\u2713')))
        if not silent:
            print("Tag set changed to  %s" % def_set)
