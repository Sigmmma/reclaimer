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

    # maps the handler name to the tags_dir it uses
    handler_tags_dir_map = {
        "Halo 1": "halo_1_tags_dir",
        "Halo 1 OS": "halo_1_os_tags_dir",
        "Halo 1 Map": "halo_1_map_tags_dir",
        "Halo 1 Misc": "halo_1_misc_tags_dir"
        }

    # names of the handlers that MUST load tags from within their tags_dir
    tags_dir_relative = (
        "Halo 1",
        "Halo 1 OS",
        )

    _curr_handler_index = 0

    widget_picker = def_halo_widget_picker

    def __init__(self, *args, **kwargs):
        # gotta give it a default handler or else the
        # config file will fail to be created as updating
        # the config requires using methods in the handler.
        kwargs['handler'] = MiscHaloLoader()
        self.tags_dir_relative = set(self.tags_dir_relative)
        Binilla.__init__(self, *args, **kwargs)

        self.settings_menu.delete(0, "end")  # clear the menu
        self.settings_menu.add_command(label="Set tags directory",
                                       command=self.set_tags_dir)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="Apply config", command=self.apply_config)
        self.settings_menu.add_command(
            label="Edit config", command=self.show_config_file)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="Load style", command=self.load_style)
        self.settings_menu.add_command(
            label="Save current style", command=self.make_style)

        self.defs_menu = tk.Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Tag set", menu=self.defs_menu)

        for i in range(len(self.handler_names)):
            self.defs_menu.add_command(command=lambda i=i:
                                       self.select_defs(i, manual=True))

        self.defs_menu.add_separator()
        self.handlers = list(self.handlers)
        self.handler_names = list(self.handler_names)

        self.select_defs(manual=False)
        if self.tags_dir is not None:
            print("Tags directory is currently:\n    %s\n" % self.tags_dir)

    @property
    def tags_dir(self):
        return self.handlers[self._curr_handler_index].tagsdir

    @tags_dir.setter
    def tags_dir(self, new_val):
        handler = self.handlers[self._curr_handler_index]
        handler.tagsdir = self.handler.sanitize_path(new_val)

    def load_tags(self, filepaths=None, def_id=None):
        tags_dir = self.tags_dir
        # if there is not tags directory, this can be loaded normally
        if tags_dir is None:
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

        sani = self.handler.sanitize_path
        handler_name = self.handler_names[self._curr_handler_index]

        sanitized_paths = [sani(path) for path in filepaths]

        # make sure all the chosen tag paths are relative
        # to the current tags directory if they must be
        if handler_name in self.tags_dir_relative:
            for path in sanitized_paths:
                if (not path) or len(path.split(tags_dir)) == 2:
                    continue
    
                print("Specified tag(s) are not located in the tags directory")
                return

        windows = Binilla.load_tags(self, sanitized_paths, def_id)
        tags_dir = self.handler.tagsdir

        # Give the tag a filepath relative to the current tags directory
        for w in windows:
            w.tag.rel_filepath = sani(w.tag.filepath).split(tags_dir)[-1]

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

    def set_tags_dir(self, e=None, *, tags_dir=None):
        if self.tags_dir is None:
            return

        if tags_dir is None:
            tags_dir = askdirectory(initialdir=self.tags_dir,
                                   title="Select the tags directory")

        if tags_dir:
            tags_dir = self.handler.sanitize_path(tags_dir)
            if tags_dir and not tags_dir.endswith(s_c.PATHDIV):
                tags_dir += s_c.PATHDIV
            self.tags_dir = self.last_load_dir = tags_dir

            curr_index = self._curr_handler_index
            name = self.handler_names[curr_index]
            dir_name = self.handler_tags_dir_map[name]

            print("Tags directory is currently:\n    %s\n" % tags_dir)

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
        tags_dir = self.tags_dir
        if not hasattr(window, 'tag'):
            return

        if window.tag is self.config_file:
            return

        window.tag.filepath = self.handler.sanitize_path(window.tag.filepath)
        if tags_dir:
            title = window.tag.filepath.split(tags_dir)[-1]
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

        # make sure the filepath is sanitized
        tag.filepath = self.handler.sanitize_path(tag.filepath)

        # change the tags filepath to be relative to the current tags directory
        if hasattr(tag, "rel_filepath"):
            tags_dir = self.get_tag_window_by_tag(tag).handler.tagsdir
            if not tags_dir.endswith(s_c.PATHDIV):
                tags_dir += s_c.PATHDIV
            tag.filepath = tags_dir + tag.rel_filepath

        Binilla.save_tag(self, tag)
        return tag

    def save_tag_as(self, tag=None, filepath=None):
        if isinstance(tag, tk.Event):
            tag = None
        if tag is None:
            if self.selected_tag is None:
                return
            tag = self.selected_tag

        if not hasattr(tag, "serialize"):
            return

        if filepath is None:
            ext = tag.ext
            orig_filepath = tag.filepath
            filepath = asksaveasfilename(
                initialdir=dirname(orig_filepath), defaultextension=ext,
                title="Save tag as...", filetypes=[
                    (ext[1:], "*" + ext), ('All', '*')] )
        else:
            filepath = tag.filepath

        # make sure the filepath is sanitized
        filepath = self.handler.sanitize_path(filepath)

        Binilla.save_tag_as(self, tag, filepath)

        # change the tags filepath to be relative to the current tags directory
        if hasattr(tag, "rel_filepath"):
            tags_dir = self.get_tag_window_by_tag(tag).handler.tagsdir
            if not tags_dir.endswith(s_c.PATHDIV):
                tags_dir += s_c.PATHDIV
            tag.filepath = tags_dir + tag.rel_filepath

        w = self.get_tag_window_by_tag(tag)
        self.update_tag_window_title(w)
        return tag

    def select_defs(self, menu_index=None, manual=True):
        names = self.handler_names
        if menu_index is None:
            menu_index = self._curr_handler_index

        name = names[menu_index]
        handler = self.handlers[menu_index]

        if handler is None or handler is self.handler:
            return

        if manual:
            print("Changing tag set to %s" % name)
            self.io_text.update_idletasks()

        if isinstance(handler, type):
            self.handlers[menu_index] = handler()

        self.handler = self.handlers[menu_index]

        entryconfig = self.defs_menu.entryconfig
        for i in range(len(names)):
            entryconfig(i, label=names[i])

        entryconfig(menu_index, label=("%s %s" % (name, u'\u2713')))
        if manual:
            print("    Finished")

        self._curr_handler_index = menu_index
        tags_dir = self.tags_dir

        if tags_dir == '':
            self.tags_dir = tags_dir = (
                self.curr_dir + "%stags%s" % (s_c.PATHDIV,  s_c.PATHDIV))
        self.last_load_dir = self.tags_dir

        if manual:
            self.last_load_dir = tags_dir
            print("Tags directory is currently:\n    %s" % tags_dir)

        if manual:
            print()

        self.config_file.data.mozzarilla.selected_handler.data = menu_index

    def make_config(self, filepath=None):
        if filepath is None:
            filepath = self.config_path

        # create the config file from scratch
        self.config_file = self.config_def.build()
        self.config_file.filepath = filepath

        data = self.config_file.data

        # make sure these have as many entries as they're supposed to
        for block in (data.directory_paths, data.widget_depths, data.colors,
                      data.tag_dirs):
            block.extend(len(block.NAME_MAP))

        self.update_config()

    def apply_config(self):
        Binilla.apply_config(self)
        config_data = self.config_file.data

        self._curr_handler_index = config_data.mozzarilla.selected_handler.data
        tag_dirs = config_data.tag_dirs

        try:
            self.select_defs()
        except Exception:
            pass

        for i in range(len(self.handler_names)):
            handler_name = self.handler_names[i]
            dir_path = tag_dirs[self.handler_tags_dir_map[handler_name]].path

            # set the handlers tags_dir so tags are able to use it
            # as a reference when setting/verifying a dependency.
            self.handlers[i].tagsdir = dir_path

    def update_config(self, config_file=None):
        if config_file is None:
            config_file = self.config_file
        Binilla.update_config(self, config_file)

        config_data = config_file.data
        mozzarilla_data = config_data.mozzarilla
        tag_dirs = config_data.tag_dirs

        mozzarilla_data.selected_handler.data = self._curr_handler_index

        for i in range(len(self.handler_names)):
            handler = self.handlers[i]
            dir_name = self.handler_tags_dir_map.get(self.handler_names[i])

            if isinstance(handler, type):
                # Since we dont load all the handlers right at the start, some
                # may still just be the class objects rather than instances.
                # This isnt going to change since making instances and loading
                # all the tagdefs would take a long time, so instead just call
                # the handlers class methods with None for the class instance.
                tags_dir = handler.sanitize_path(None, handler.tagsdir)
            else:
                tags_dir = handler.sanitize_path(handler.tagsdir)

            if tags_dir and not tags_dir.endswith(s_c.PATHDIV):
                tags_dir += s_c.PATHDIV

            tag_dirs[dir_name].path = handler.tagsdir = tags_dir
