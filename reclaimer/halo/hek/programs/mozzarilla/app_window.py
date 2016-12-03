import tkinter as tk

from os.path import dirname
from traceback import format_exc

from supyr_struct.apps.binilla.app_window import *
from supyr_struct.defs.constants import *
from ...handler import HaloHandler
from ....meta.handler import MapLoader
from ....os_hek.handler import OsHaloHandler
from ....misc.handler import MiscHaloLoader
from .config_def import config_def
from .widget_picker import *


class Mozzarilla(Binilla):
    app_name = 'Mozzarilla'
    config_path = dirname(__file__) + '%smozzarilla.cfg' % PATHDIV

    config_def = config_def

    handlers = (
        HaloHandler,
        OsHaloHandler,
        MapLoader,
        MiscHaloLoader,
        )

    handler_names = (
        "Halo 1",
        "Halo 1 Open Sauce",
        "Halo 1 Map",
        "Halo 1 Misc",
        )

    _curr_handler_index = 0

    widget_picker = def_halo_widget_picker

    def __init__(self, *args, **kwargs):
        kwargs['handler'] = None
        Binilla.__init__(self, *args, **kwargs)

        self.main_menu.delete("Options")
        self.options_menu.destroy()
        del self.options_menu

        self.defs_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Tag set", menu=self.defs_menu)

        for i in range(len(self.handler_names)):
            self.defs_menu.add_command(command=lambda i=i: self.select_defs(i))

        self.defs_menu.add_separator()
        self.handlers = list(self.handlers)
        self.handler_names = list(self.handler_names)

        self.select_defs(silent=True)

    def load_config(self, filepath=None):
        Binilla.load_config(self)

        mozzarilla_data = self.config_file.data.mozzarilla
        self._curr_handler_index = mozzarilla_data.selected_handler.data

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

    def select_defs(self, menu_index=None, silent=False):
        names = self.handler_names
        if menu_index is None:
            menu_index = self._curr_handler_index

        name = names[menu_index]
        handler = self.handlers[menu_index]

        if handler is None or handler is self.handler:
            return

        if not silent:
            print("Changing tag set to %s" % name)
            self.update_idletasks()

        if isinstance(handler, type):
            self.handlers[menu_index] = handler()
        self.handler = self.handlers[menu_index]

        entryconfig = self.defs_menu.entryconfig
        for i in range(len(names)):
            entryconfig(i, label=names[i])

        self._curr_handler_index = menu_index

        entryconfig(menu_index, label=("%s %s" % (name, u'\u2713')))
        if not silent:
            print("Tag set changed to  %s" % name)

    def update_config(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        mozzarilla_data = config_file.data.mozzarilla

        mozzarilla_data.selected_handler.data = self._curr_handler_index

        Binilla.update_config(self, config_file)
