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
    log_filename = 'mozzarilla.log'
    
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
        "Halo 1 OS",
        "Halo 1 Map",
        "Halo 1 Misc",
        )

    tagsdir = ''

    tags_dirs = {
        "halo_1_tags_dir": '',
        "halo_1_os_tags_dir": '',
        }

    # maps the handler name to the tagsdir it uses
    handler_tags_dir_map = {
        "Halo 1": "halo_1_tags_dir",
        "Halo 1 OS": "halo_1_os_tags_dir"
        }

    _curr_handler_index = 0

    widget_picker = def_halo_widget_picker

    def __init__(self, *args, **kwargs):
        # gotta give it a default handler or else the
        # config file will fail to be created as updating
        # the config requires using methods in the handler.
        kwargs['handler'] = MiscHaloLoader()
        Binilla.__init__(self, *args, **kwargs)

        self.settings_menu.delete(0, "end")  # clear the menu
        self.settings_menu.add_command(label="Set tags directory",
                                       command=self.set_tags_dir)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="Edit configuation", command=self.show_config_file)

        self.defs_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Tag set", menu=self.defs_menu)

        for i in range(len(self.handler_names)):
            self.defs_menu.add_command(command=lambda i=i: self.select_defs(i))

        self.defs_menu.add_separator()
        self.handlers = list(self.handlers)
        self.handler_names = list(self.handler_names)

        self.select_defs(silent=True)
        if self.tagsdir is not None:
            print("Tags directory is currently:\n    %s\n" % self.tagsdir)

    def load_tags(self, filepaths=None, def_id=None):
        tagsdir = self.tagsdir
        if tagsdir is None:
            return Binilla.load_tags(self, filepaths, def_id)

        if isinstance(filepaths, tk.Event):
            filepaths = None
        if filepaths is None:
            filetypes = [('All', '*')]
            defs = self.handler.defs
            for id in sorted(defs.keys()):
                filetypes.append((id, defs[id].ext))
            filepaths = askopenfilenames(initialdir=self.last_load_dir,
                                         filetypes=filetypes,
                                         title="Select the tag to load")
            if not filepaths:
                return

        if isinstance(filepaths, str):
            filepaths = (filepaths,)

        # make sure the paths are relative to the current tags directory
        sani = self.handler.sanitize_path
        for path in filepaths:
            if path and len(sani(path).split(tagsdir)) != 2:
                print("Selected tag(s) are not located in the tags directory")
                return

        windows = Binilla.load_tags(self, filepaths, def_id)

        # Give the tag a filepath relative to the current tags directory
        for w in windows:
            w.tag.rel_filepath = sani(w.tag.filepath.split(tagsdir)[-1])

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

    @property
    def tagsdir(self):
        handler_name = self.handler_names[self._curr_handler_index]
        tags_dir_name = self.handler_tags_dir_map.get(handler_name)
        return self.tags_dirs.get(tags_dir_name)

    @tagsdir.setter
    def tagsdir(self, new_val):
        handler_name = self.handler_names[self._curr_handler_index]
        tags_dir_name = self.handler_tags_dir_map.get(handler_name)
        if tags_dir_name is not None:
            self.tags_dirs[tags_dir_name] = self.handler.sanitize_path(new_val)

    def set_tags_dir(self, e=None, *, tagsdir=None):
        if self.tagsdir is None:
            return

        if tagsdir is None:
            tagsdir = askdirectory(initialdir=self.tagsdir,
                                   title="Select the tags directory")

        if tagsdir:
            tagsdir = self.handler.sanitize_path(tagsdir)
            if tagsdir and not tagsdir.endswith(s_c.PATHDIV):
                tagsdir += s_c.PATHDIV
            self.tagsdir = self.last_load_dir = tagsdir

            curr_index = self._curr_handler_index
            name = self.handler_names[curr_index]
            dir_name = self.handler_tags_dir_map.get(name)

            if dir_name is not None:
                self.handlers[curr_index].tagsdir = self.tags_dirs[dir_name]

            print("Tags directory is currently:\n    %s\n" % tagsdir)

    def make_tag_window(self, tag, *, focus=True, window_cls=None):
        w = Binilla.make_tag_window(self, tag, focus=focus,
                                    window_cls=window_cls)
        self.update_tag_window_title(w)
        return w

    def new_tag(self, e=None):
        if self.def_selector_window:
            return
        
        dsw = DefSelectorWindow(
            self, title="Select a tag to create", action=lambda def_id:
            self.load_tags(filepaths='', def_id=def_id))
        self.def_selector_window = dsw
        self.place_window_relative(self.def_selector_window, 30, 50)

    def update_tag_window_title(self, window):
        tagsdir = self.tagsdir
        if not hasattr(window, 'tag'):
            return

        if window.tag is self.config_file:
            return

        window.tag.filepath = self.handler.sanitize_path(window.tag.filepath)
        if tagsdir:
            title = window.tag.filepath.split(tagsdir)[-1]
            try:
                handler_i = self.handlers.index(window.handler)
                title = "[%s] %s" % (self.handler_names[handler_i], title)
            except Exception:
                pass
            window.update_title(title)

    def save_tag(self, tag=None):
        if isinstance(tag, tk.Event):
            tag = None
        if tag is None:
            if self.selected_tag is None:
                return
            tag = self.selected_tag

        # change the tags filepath to be relative to the current tags directory
        tagsdir = self.get_tag_window_by_tag(tag).handler.tagsdir
        if tagsdir:
            if not tagsdir.endswith(s_c.PATHDIV):
                tagsdir += s_c.PATHDIV
            tag.filepath = tagsdir + tag.rel_filepath

        Binilla.save_tag(self, tag)
        return tag

    def save_tag_as(self, tag=None):
        if isinstance(tag, tk.Event):
            tag = None
        if tag is None:
            if self.selected_tag is None:
                return
            tag = self.selected_tag

        # change the tags filepath to be relative to the current tags directory
        tagsdir = self.get_tag_window_by_tag(tag).handler.tagsdir
        if tagsdir:
            if not tagsdir.endswith(s_c.PATHDIV):
                tagsdir += s_c.PATHDIV
            tag.filepath = tagsdir + tag.rel_filepath

        Binilla.save_tag_as(self, tag)

        w = self.get_tag_window_by_tag(tag)
        self.update_tag_window_title(w)
        return tag

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

        entryconfig(menu_index, label=("%s %s" % (name, u'\u2713')))
        if not silent:
            print("Tag set changed to  %s" % name)

        self._curr_handler_index = menu_index
        tagsdir = self.tagsdir

        if tagsdir is not None:
            if tagsdir == '':
                self.tagsdir = tagsdir = (
                    self.curr_dir + "%stags%s" % (s_c.PATHDIV,  s_c.PATHDIV))
            self.last_load_dir = self.tagsdir

            if not silent:
                print("Tags directory is currently:\n    %s" % tagsdir)

        if not silent:
            print()

        self.config_file.data.mozzarilla.selected_handler.data = menu_index

    def load_config(self, filepath=None):
        Binilla.load_config(self, filepath)
        config_data = self.config_file.data

        self._curr_handler_index = config_data.mozzarilla.selected_handler.data
        dir_paths = config_data.directory_paths

        for i in range(len(self.handler_names)):
            handler_name = self.handler_names[i]
            dir_name = self.handler_tags_dir_map.get(handler_name)
            if dir_name is None:
                continue

            dir_path = dir_paths[dir_name].path

            # set the handlers tagsdir so tags are able to use it
            # as a reference when setting/verifying a dependency.
            self.handlers[i].tagsdir = dir_path
            self.tags_dirs[dir_name] = dir_path

    def update_config(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        Binilla.update_config(self, config_file)

        config_data = config_file.data
        mozzarilla_data = config_data.mozzarilla
        dir_paths = config_data.directory_paths

        mozzarilla_data.selected_handler.data = self._curr_handler_index

        # make sure there are enough tagsdir entries in the directory_paths
        if len(dir_paths.NAME_MAP) > len(dir_paths):
            dir_paths.extend(len(dir_paths.NAME_MAP) - len(dir_paths))

        for dir_name in self.tags_dirs:
            tagsdir = self.handler.sanitize_path(self.tags_dirs[dir_name])
            if tagsdir and not tagsdir.endswith(s_c.PATHDIV):
                tagsdir += s_c.PATHDIV
            dir_paths[dir_name].path = tagsdir
