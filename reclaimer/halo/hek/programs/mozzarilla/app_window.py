import os
import tkinter as tk
import zipfile

from os.path import dirname, splitext, realpath
from time import time
from threading import Thread
from traceback import format_exc

from supyr_struct.apps.binilla.app_window import *
from supyr_struct.defs.constants import *
from ...handler import HaloHandler
from ....meta.handler import MapLoader
from ....os_hek.handler import OsHaloHandler
from ....misc.handler import MiscHaloLoader
from .config_def import config_def, guerilla_workspace_def
from .widget_picker import *

default_hotkeys.update({
    '<F2>': "set_tags_dir",
    '<F3>': "show_dependency_viewer",
    '<F4>': "show_tag_scanner",
    })

class Mozzarilla(Binilla):
    app_name = 'Mozzarilla'
    log_filename = 'mozzarilla.log'
    debug = 0

    _mozzarilla_initialized = False

    styles_dir = dirname(__file__) + s_c.PATHDIV + "styles"
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

    dependency_window = None
    tag_scanner_window = None

    window_panes = None
    hierarchy_frame = None
    hierarchy_width = 200

    def __init__(self, *args, **kwargs):
        # gotta give it a default handler or else the
        # config file will fail to be created as updating
        # the config requires using methods in the handler.
        self.debug = kwargs.pop('debug', self.debug)
        kwargs['handler'] = MiscHaloLoader(debug=self.debug)
        self.tags_dir_relative = set(self.tags_dir_relative)
        Binilla.__init__(self, *args, **kwargs)

        self.file_menu.insert_command("Exit", label="Load guerilla config",
                                      command=self.load_guerilla_config)
        self.file_menu.insert_separator("Exit")

        self.settings_menu.delete(0, "end")  # clear the menu
        self.settings_menu.add_command(label="Set tags directory",
                                       command=self.set_tags_dir)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="Edit config", command=self.show_config_file)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(
            label="Load style", command=self.apply_style)
        self.settings_menu.add_command(
            label="Save current style", command=self.make_style)

        # make the tools and tag set menus
        self.tools_menu = tk.Menu(self.main_menu, tearoff=0)
        self.defs_menu = tk.Menu(self.main_menu, tearoff=0)

        self.main_menu.add_cascade(label="Tag set", menu=self.defs_menu)
        self.main_menu.add_cascade(label="Tools", menu=self.tools_menu)

        for i in range(len(self.handler_names)):
            self.defs_menu.add_command(command=lambda i=i:
                                       self.select_defs(i, manual=True))

        self.tools_menu.add_command(
            label="Dependency viewer", command=self.show_dependency_viewer)
        self.tools_menu.add_command(
            label="Scan tags directory", command=self.show_tag_scanner)

        self.defs_menu.add_separator()
        self.handlers = list(self.handlers)
        self.handler_names = list(self.handler_names)

        self.select_defs(manual=False)
        if self.tags_dir is not None:
            print("Tags directory is currently:\n    %s\n" % self.tags_dir)

        self._mozzarilla_initialized = True

        try:
            if self.config_file.data.header.flags.load_last_workspace:
                self.load_last_workspace()
        except Exception:
            pass

        self.make_window_panes()
        self.make_hierarchy_frame(self.window_panes)
        self.make_io_text(self.window_panes)

        self.update_window_settings()
        self.window_panes.add(self.hierarchy_frame)
        self.window_panes.add(self.io_frame)

    def load_last_workspace(self):
        if self._mozzarilla_initialized:
            Binilla.load_last_workspace(self)

    @property
    def tags_dir(self):
        return self.handlers[self._curr_handler_index].tagsdir

    @tags_dir.setter
    def tags_dir(self, new_val):
        handler = self.handlers[self._curr_handler_index]
        handler.tagsdir = handler.sanitize_path(new_val)

    def load_guerilla_config(self):
        fp = askopenfilename(
            initialdir=self.last_load_dir, title="Select the tag to load",
            filetypes=(('Guerilla config', '*.cfg'), ('All', '*')))

        if not fp:
            return

        self.last_load_dir = dirname(fp)
        workspace = guerilla_workspace_def.build(filepath=fp)

        pad_x = self.io_text.winfo_rootx() - self.winfo_x()
        pad_y = self.io_text.winfo_rooty() - self.winfo_y()

        tl_corner = workspace.data.window_header.top_left_corner
        br_corner = workspace.data.window_header.bottom_right_corner

        self.geometry("%sx%s+%s+%s" % (
            br_corner.x - tl_corner.x - pad_x,
            br_corner.y - tl_corner.y - pad_y,
            tl_corner.x, tl_corner.y))

        for tag in workspace.data.tags:
            if not tag.is_valid_tag:
                continue

            windows = self.load_tags(tag.filepath)
            if not windows:
                continue

            w = windows[0]

            tl_corner = tag.window_header.top_left_corner
            br_corner = tag.window_header.bottom_right_corner

            self.place_window_relative(w, pad_x + tl_corner.x,
                                          pad_y + tl_corner.y)
            w.geometry("%sx%s" % (br_corner.x - tl_corner.x,
                                  br_corner.y - tl_corner.y))

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
            if filepaths.startswith('{'):
                filepaths = re.split("\}\W\{", filepaths[1:-1])
            else:
                filepaths = (filepaths, )

        sani = self.handler.sanitize_path
        handler_name = self.handler_names[self._curr_handler_index]

        sanitized_paths = [sani(path) for path in filepaths]

        # make sure all the chosen tag paths are relative
        # to the current tags directory if they must be
        if handler_name in self.tags_dir_relative:
            for path in sanitized_paths:
                if (not path) or len(path.lower().split(tags_dir.lower())) == 2:
                    continue
    
                print("Specified tag(s) are not located in the tags directory")
                return

        windows = Binilla.load_tags(self, sanitized_paths, def_id)

        if not windows:
            print("Change the tag set to load these tag(s).")
            return ()
        tags_dir = self.handler.tagsdir

        # Give the tag a filepath relative to the current tags directory
        for w in windows:
            w.tag.rel_filepath = sani(w.tag.filepath).split(tags_dir)[-1]

        return windows

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

        if not fp:
            return

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

        if not tags_dir:
            return

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

        if window.tag is self.config_file or not tags_dir:
            return

        window.tag.filepath = self.handler.sanitize_path(window.tag.filepath)

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

        if tag is self.config_file:
            return self.save_config()

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

        if not filepath:
            return

        # make sure the filepath is sanitized
        filepath = self.handler.sanitize_path(filepath)

        tags_dir = self.get_tag_window_by_tag(tag).handler.tagsdir
        if not tags_dir.endswith(s_c.PATHDIV):
            tags_dir += s_c.PATHDIV
        rel_filepath = filepath.split(tags_dir)[-1]

        if len(filepath.lower().split(tags_dir.lower())) != 2:
            print("Cannot save outside the tags directory")
            return

        Binilla.save_tag_as(self, tag, filepath)

        tag.rel_filepath = rel_filepath

        w = self.get_tag_window_by_tag(tag)
        self.update_tag_window_title(w)
        return tag

    def set_handler(self, handler=None, index=None, name=None):
        if handler is not None:
            handler_index = self.handlers.index(handler)
            self._curr_handler_index = handler_index
            self.handler = handler
        elif index is not None:
            self._curr_handler_index = handler_index
            self.handler = self.handlers[handler_index]
        elif name is not None:
            handler_index = self.handler_names.index(name)
            self._curr_handler_index = handler_index
            self.handler = self.handlers[handler_index]

    def select_defs(self, menu_index=None, manual=True):
        names = self.handler_names
        if menu_index is None:
            menu_index = self._curr_handler_index

        name = names[menu_index]
        handler = self.handlers[menu_index]

        if name == "Halo 1 Map":
            print("Loading and editing maps is not supported yet, " +
                  "but it would be a pain to remove this button, " +
                  "so I put in this message instead!")
            return

        if handler is None or handler is self.handler:
            return

        if manual:
            print("Changing tag set to %s" % name)
            self.io_text.update_idletasks()

        if isinstance(handler, type):
            self.handlers[menu_index] = handler(debug=self.debug)

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

        if manual:
            self.last_load_dir = tags_dir
            print("Tags directory is currently:\n    %s" % tags_dir)

        if manual:
            print()

        self.config_file.data.mozzarilla.selected_handler.data = menu_index

    def make_io_text(self, master=None):
        if not self._initialized:
            return
        if master is None:
            master = self.root_frame
        Binilla.make_io_text(self, master)

    def make_hierarchy_frame(self, master=None):
        if not self._initialized:
            return
        if master is None:
            master = self.root_frame
        self.hierarchy_frame = HierarchyFrame(
            self, width=self.hierarchy_width)
        self.hierarchy_frame.pack(expand=True, fill='y')

    def make_window_panes(self):
        self.window_panes = tk.PanedWindow(
            self.root_frame, sashrelief='raised', sashwidth=8,
            bd=self.frame_depth, bg=self.frame_bg_color)
        self.window_panes.pack(anchor='nw', fill='both', expand=True)

    def make_config(self, filepath=None):
        if filepath is None:
            filepath = self.config_path

        # create the config file from scratch
        self.config_file = self.config_def.build()
        self.config_file.filepath = filepath

        data = self.config_file.data

        # make sure these have as many entries as they're supposed to
        for block in (data.directory_paths, data.widgets.depths, data.colors,
                      data.tag_dirs):
            block.extend(len(block.NAME_MAP))

        self.update_config()

        c_hotkeys = data.hotkeys
        c_tag_window_hotkeys = data.tag_window_hotkeys

        for k_set, b in ((default_hotkeys, c_hotkeys),
                         (default_tag_window_hotkeys, c_tag_window_hotkeys)):
            default_keys = k_set
            hotkeys = b
            for combo, method in k_set.items():
                hotkeys.append()
                keys = hotkeys[-1].combo

                modifier, key = read_hotkey_string(combo)
                keys.modifier.set_to(modifier)
                keys.key.set_to(key)

                hotkeys[-1].method.set_to(method)

    def apply_config(self, e=None):
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

    def show_dependency_viewer(self, e=None):
        if self.dependency_window is not None:
            return

        self.dependency_window = DependencyWindow(self)
        self.place_window_relative(self.dependency_window, 30, 50)
        self.dependency_window.focus_set()

    def show_tag_scanner(self, e=None):
        if self.tag_scanner_window is not None:
            return

        if not hasattr(self.handler, 'tag_ref_cache'):
            print("Change the current tag set.")
            return

        self.tag_scanner_window = TagScannerWindow(self)
        self.place_window_relative(self.tag_scanner_window, 30, 50)
        self.tag_scanner_window.focus_set()

    def update_window_settings(self):
        if not self._initialized:
            return

        Binilla.update_window_settings(self)
        try:
            for m in (self.defs_menu, self.tools_menu):
                m.config(bg=self.default_bg_color, fg=self.text_normal_color)

            self.window_panes.config(
                bg=self.frame_bg_color, bd=self.frame_depth)
            self.hierarchy_frame.update_window_settings()
        except AttributeError: pass
        except Exception: print(format_exc())

class DependencyWindow(tk.Toplevel, BinillaWidget):

    app_root = None
    handler = None

    zipping = False
    stop_zipping = False

    def __init__(self, app_root, *args, **kwargs): 
        self.handler = app_root.handler
        self.app_root = app_root
        kwargs.update(width=400, height=100, bd=0,
                      highlightthickness=0, bg=self.default_bg_color)
        tk.Toplevel.__init__(self, app_root, *args, **kwargs)

        tagset = app_root.handler_names[app_root._curr_handler_index]
        self.title("[%s] Tag dependency viewer" % tagset)
        self.minsize(width=400, height=100)

        # make the tkinter variables
        self.tag_filepath = tk.StringVar(self)

        # make the frames
        self.filepath_frame = tk.LabelFrame(
            self, text="Select a tag",
            fg=self.text_normal_color, bg=self.default_bg_color)
        self.button_frame = tk.LabelFrame(
            self, text="Actions",
            fg=self.text_normal_color, bg=self.default_bg_color)

        btn_kwargs = dict(
            bg=self.button_color, activebackground=self.button_color,
            fg=self.text_normal_color, bd=self.button_depth,
            disabledforeground=self.text_disabled_color,
            )
        self.display_button = tk.Button(
            self.button_frame, width=25, text='Show dependencies',
            command=self.populate_dependency_tree, **btn_kwargs)

        self.zip_button = tk.Button(
            self.button_frame, width=25, text='Zip tag recursively',
            command=self.recursive_zip, **btn_kwargs)

        self.filepath_entry = tk.Entry(
            self.filepath_frame, textvariable=self.tag_filepath,
            bd=self.entry_depth,
            bg=self.entry_normal_color, fg=self.text_normal_color,
            disabledbackground=self.entry_disabled_color,
            disabledforeground=self.text_disabled_color,
            selectbackground=self.entry_highlighted_color,
            selectforeground=self.text_highlighted_color)
        self.browse_button = tk.Button(
            self.filepath_frame, text="Browse",
            command=self.browse, **btn_kwargs)

        self.display_button.pack(padx=4, pady=2, side=tk.LEFT)
        self.zip_button.pack(padx=4, pady=2, side=tk.RIGHT)

        self.filepath_entry.pack(padx=(4, 0), pady=2, side=tk.LEFT,
                                 expand=True, fill='x')
        self.browse_button.pack(padx=(0, 4), pady=2, side=tk.LEFT)

        self.filepath_frame.pack(fill='x', padx=1)
        self.button_frame.pack(fill='x', padx=1)

        self.transient(app_root)

    def browse(self):
        filetypes = [('All', '*')]

        defs = self.app_root.handler.defs
        for def_id in sorted(defs.keys()):
            filetypes.append((def_id, defs[def_id].ext))
        fp = askopenfilename(initialdir=self.app_root.last_load_dir,
                             filetypes=filetypes, title="Select a tag")

        if not fp:
            return

        fp = self.app_root.handler.sanitize_path(fp)
        self.app_root.last_load_dir = dirname(fp)

        self.filepath_entry.delete(0, tk.END)
        self.filepath_entry.insert(0, fp)

    def destroy(self):
        try:
            self.app_root.dependency_window = None
        except AttributeError:
            pass
        self.stop_zipping = True
        tk.Toplevel.destroy(self)

    def get_tag(self, filepath):
        def_id = self.app_root.handler.get_def_id(filepath)
        tag = self.app_root.get_tag(def_id, filepath)
        if tag is not None:
            return tag
        try:
            return self.app_root.handler.build_tag(filepath=filepath)
        except Exception:
            pass

    def get_dependencies(self, tag):
        handler = self.handler
        def_id = tag.def_id
        dependency_cache = handler.tag_ref_cache.get(def_id)

        if not dependency_cache:
            return ()

        nodes = handler.get_nodes_by_paths(handler.tag_ref_cache[def_id],
                                           tag.data)

        dependencies = []

        for node in nodes:
            # if the node's filepath is empty, just skip it
            if not node.filepath:
                continue
            try:
                ext = '.' + node.tag_class.enum_name
            except Exception:
                ext = ''
            dependencies.append(node.filepath + ext)
        return dependencies

    def populate_dependency_tree(self):
        print('This button doesnt do anything yet.')
        return
        filepath = self.tag_filepath.get()
        if not filepath:
            return

        app = self.app_root
        handler = self.handler = app.handler
        sani = handler.sanitize_path

        handler_name = app.handler_names[app._curr_handler_index]
        if handler_name not in app.tags_dir_relative:
            print("Change the current tag set.")
            return
        else:
            tags_dir = handler.tagsdir

        filepath = sani(filepath)
        if len(filepath.split(tags_dir)) != 2:
            print("Specified tag is not located within the tags directory")
            return

        tag = self.get_tag(filepath)
        if tag is None:
            print("Could not load tag:\n    %s" % filepath)
            return

        print(tag)

    def recursive_zip(self):
        if self.zipping:
            return
        try: self.zip_thread.join()
        except Exception: pass
        self.zip_thread = Thread(target=self._recursive_zip)
        self.zip_thread.daemon = True
        self.zip_thread.start()

    def _recursive_zip(self):
        self.zipping = True
        try:
            self.do_recursive_zip()
        except Exception:
            print(format_exc())
        self.zipping = False

    def do_recursive_zip(self):
        tag_path = self.tag_filepath.get()
        if not tag_path:
            return

        app = self.app_root
        handler = self.handler = app.handler
        sani = handler.sanitize_path

        handler_name = app.handler_names[app._curr_handler_index]
        if handler_name not in app.tags_dir_relative:
            print("Change the current tag set.")
            return
        else:
            tags_dir = handler.tagsdir

        tag_path = sani(tag_path)
        if len(tag_path.split(tags_dir)) != 2:
            print("Specified tag is not located within the tags directory")
            return

        tagzip_path = asksaveasfilename(
            initialdir=self.app_root.last_load_dir, title="Save zipfile to...",
            filetypes=(("zipfile", "*.zip"), ))

        if not tagzip_path:
            return

        # TURN THE BELOW CODE INTO A DAEMON THREAD SO THE
        # APPLICATION ISNT LOCKED WHILE ITS PROGRESSING.
        tag = self.get_tag(tag_path)
        if tag is None:
            print("Could not load tag:\n    %s" % tag_path)
            return

        # make the zipfile to put everything in
        tagzip_path = splitext(tagzip_path)[0] + ".zip"

        tags_to_zip = [tag_path.split(tags_dir)[-1]]
        new_tags_to_zip = []
        seen_tags = set()

        with zipfile.ZipFile(tagzip_path, mode='w') as tagzip:
            # loop over all the tags and add them to the zipfile
            while tags_to_zip:
                for rel_tag_path in tags_to_zip:
                    tag_path = tags_dir + rel_tag_path
                    if self.stop_zipping:
                        print('Recursive zip operation cancelled.\n')
                        return

                    if rel_tag_path in seen_tags:
                        continue
                    seen_tags.add(rel_tag_path)

                    try:
                        print("Adding '%s' to zipfile" % rel_tag_path)
                        tag = self.get_tag(tag_path)
                        new_tags_to_zip.extend(self.get_dependencies(tag))

                        # try to conserve memory a bit
                        del tag

                        tagzip.write(tag_path, arcname=rel_tag_path)
                    except Exception:
                        print("    Could not add '%s' to zipfile." %
                              rel_tag_path)

                    try: app.io_text.update()
                    except Exception: pass

                # replace the tags to zip with the newly collected ones
                tags_to_zip[:] = new_tags_to_zip
                del new_tags_to_zip[:]

        print("\nRecursive zip completed.\n")


class TagScannerWindow(tk.Toplevel, BinillaWidget):

    app_root = None
    handler = None

    scanning = False
    stop_scanning = False
    print_interval = 5

    listbox_index_to_def_id = ()

    def __init__(self, app_root, *args, **kwargs): 
        self.handler = handler = app_root.handler
        self.app_root = app_root
        kwargs.update(bd=0, highlightthickness=0, bg=self.default_bg_color)
        tk.Toplevel.__init__(self, app_root, *args, **kwargs)

        ext_id_map = handler.ext_id_map
        self.listbox_index_to_def_id = [
            ext_id_map[ext] for ext in sorted(ext_id_map.keys())
            if ext_id_map[ext] in handler.tag_ref_cache]

        tagset = app_root.handler_names[app_root._curr_handler_index]

        self.title("[%s] Tag directory scanner" % tagset)
        self.minsize(width=400, height=250)
        self.resizable(0, 0)

        # make the tkinter variables
        self.directory_path = tk.StringVar(self)
        self.logfile_path = tk.StringVar(self)

        # make the frames
        self.directory_frame = tk.LabelFrame(
            self, text="Directory to scan",
            fg=self.text_normal_color, bg=self.default_bg_color)
        self.logfile_frame = tk.LabelFrame(
            self, text="Output log filepath",
            fg=self.text_normal_color, bg=self.default_bg_color)
        self.def_ids_frame = tk.LabelFrame(
            self, text="Select which tag types to scan",
            fg=self.text_normal_color, bg=self.default_bg_color)
        self.button_frame = tk.Frame(
            self.def_ids_frame,bg=self.default_bg_color)

        btn_kwargs = dict(
            bg=self.button_color, activebackground=self.button_color,
            fg=self.text_normal_color, bd=self.button_depth,
            disabledforeground=self.text_disabled_color,
            )

        self.scan_button = tk.Button(
            self.button_frame, text='Scan directory', width=20,
            command=self.scan_directory, **btn_kwargs)
        self.cancel_button = tk.Button(
            self.button_frame, text='Cancel scan', width=20,
            command=self.cancel_scan, **btn_kwargs)
        self.select_all_button = tk.Button(
            self.button_frame, text='Select all', width=20,
            command=self.select_all, **btn_kwargs)
        self.deselect_all_button = tk.Button(
            self.button_frame, text='Deselect all', width=20,
            command=self.deselect_all, **btn_kwargs)

        self.directory_entry = tk.Entry(
            self.directory_frame, textvariable=self.directory_path,
            bd=self.entry_depth,
            bg=self.entry_normal_color, fg=self.text_normal_color,
            disabledbackground=self.entry_disabled_color,
            disabledforeground=self.text_disabled_color,
            selectbackground=self.entry_highlighted_color,
            selectforeground=self.text_highlighted_color)
        self.dir_browse_button = tk.Button(
            self.directory_frame, text="Browse",
            command=self.dir_browse, **btn_kwargs)

        self.logfile_entry = tk.Entry(
            self.logfile_frame, textvariable=self.logfile_path,
            bd=self.entry_depth,
            bg=self.entry_normal_color, fg=self.text_normal_color,
            disabledbackground=self.entry_disabled_color,
            disabledforeground=self.text_disabled_color,
            selectbackground=self.entry_highlighted_color,
            selectforeground=self.text_highlighted_color)
        self.log_browse_button = tk.Button(
            self.logfile_frame, text="Browse",
            command=self.log_browse, **btn_kwargs)

        self.def_ids_scrollbar = tk.Scrollbar(
            self.def_ids_frame, orient="vertical")
        self.def_ids_listbox = tk.Listbox(
            self.def_ids_frame, selectmode=tk.MULTIPLE, highlightthickness=0,
            bg=self.enum_normal_color, fg=self.text_normal_color,
            selectbackground=self.enum_highlighted_color,
            selectforeground=self.text_highlighted_color,
            yscrollcommand=self.def_ids_scrollbar.set)
        self.def_ids_scrollbar.config(command=self.def_ids_listbox.yview)

        for def_id in self.listbox_index_to_def_id:
            tag_ext = handler.id_ext_map[def_id].split('.')[-1]
            self.def_ids_listbox.insert(tk.END, tag_ext)

            # these tag types are massive, so by
            # default dont set them to be scanned
            if def_id in ("sbsp", "scnr"):
                continue
            self.def_ids_listbox.select_set(tk.END)

        for w in (self.directory_entry, self.logfile_entry):
            w.pack(padx=(4, 0), pady=2, side=tk.LEFT, expand=True, fill='x')

        for w in (self.dir_browse_button, self.log_browse_button):
            w.pack(padx=(0, 4), pady=2, side=tk.LEFT)

        for w in (self.scan_button, self.cancel_button):
            w.pack(padx=4, pady=2)

        for w in (self.deselect_all_button, self.select_all_button):
            w.pack(padx=4, pady=2, side=tk.BOTTOM)

        self.def_ids_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        self.def_ids_scrollbar.pack(side=tk.LEFT, fill="y")
        self.button_frame.pack(side=tk.LEFT, fill="y")

        self.directory_frame.pack(fill='x', padx=1)
        self.logfile_frame.pack(fill='x', padx=1)
        self.def_ids_frame.pack(fill='x', padx=1, expand=True)

        self.transient(app_root)

        self.directory_entry.insert(0, handler.tagsdir)
        self.logfile_entry.insert(0, handler.tagsdir + "tag_scanner.log")

    def deselect_all(self):
        self.def_ids_listbox.select_clear(0, tk.END)

    def select_all(self):
        for i in range(len(self.listbox_index_to_def_id)):
            self.def_ids_listbox.select_set(i)

    def get_tag(self, filepath):
        def_id = self.app_root.handler.get_def_id(filepath)
        tag = self.app_root.get_tag(def_id, filepath)
        if tag is not None:
            return tag
        try:
            return self.app_root.handler.build_tag(filepath=filepath)
        except Exception:
            pass

    def dir_browse(self):
        dirpath = askdirectory(
            initialdir=self.directory_path.get(),
            title="Select directory to scan")

        if not dirpath:
            return

        dirpath = self.app_root.handler.sanitize_path(dirpath)
        if not dirpath.endswith(PATHDIV):
            dirpath += PATHDIV

        self.app_root.last_load_dir = dirname(dirpath)
        if len(dirpath.split(self.handler.tagsdir)) != 2:
            print("Chosen directory is not located within the tags directory")
            return

        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, dirpath)

    def log_browse(self):
        filepath = asksaveasfilename(
            initialdir=dirname(self.logfile_entry.get()),
            title="Save scan log to...",
            filetypes=(("tag scanner log", "*.log"), ('All', '*')))

        if not filepath:
            return

        filepath = self.app_root.handler.sanitize_path(filepath)
        self.app_root.last_load_dir = dirname(filepath)

        self.logfile_entry.delete(0, tk.END)
        self.logfile_entry.insert(0, filepath)

    def destroy(self):
        try:
            self.app_root.tag_scanner_window = None
        except AttributeError:
            pass
        self.stop_scanning = True
        tk.Toplevel.destroy(self)

    def cancel_scan(self):
        self.stop_scanning = True

    def scan_directory(self):
        if self.scanning:
            return
        try: self.scan_thread.join()
        except Exception: pass
        self.scan_thread = Thread(target=self._scan_directory)
        self.scan_thread.daemon = True
        self.scan_thread.start()

    def _scan_directory(self):
        self.scanning = True
        try:
            self.scan()
        except Exception:
            print(format_exc())
        self.scanning = False

    def scan(self):
        app = self.app_root
        handler = self.handler
        sani = handler.sanitize_path
        self.stop_scanning = False

        tagsdir = self.handler.tagsdir
        dirpath = sani(self.directory_path.get())
        logpath = sani(self.logfile_path.get())

        if len(dirpath.split(tagsdir)) != 2:
            print("Chosen directory is not located within the tags directory")
            return

        #this is the string to store the entire debug log
        log_name = "HEK Tag Scanner log"
        debuglog = "\n%s%s%s\n\n" % (
            "-"*30, log_name, "-" * (50-len(log_name)))
        debuglog += "tags directory = %s\nscan directory = %s\n\n" % (
            tagsdir, dirpath)
        debuglog += "broken dependencies are listed below\n"

        get_nodes = handler.get_nodes_by_paths
        get_tagref_invalid = handler.get_tagref_invalid

        s_time = time()
        c_time = s_time
        p_int = self.print_interval

        all_tag_paths = {self.listbox_index_to_def_id[int(i)]: [] for i in
                         self.def_ids_listbox.curselection()}
        ext_id_map = handler.ext_id_map
        id_ext_map = handler.id_ext_map

        print("Locating tags...")
        try: app.io_text.update()
        except Exception: pass

        for root, directories, files in os.walk(dirpath):
            if not root.endswith(PATHDIV):
                root += PATHDIV

            root = root.split(tagsdir)[-1]

            for filename in files:
                filepath = sani(root + filename)

                if time() - c_time > p_int:
                    c_time = time()
                    print(' '*4 + filepath)
                    try: app.io_text.update()
                    except Exception: pass

                if self.stop_scanning:
                    print('Tag scanning operation cancelled.\n')
                    return

                tag_paths = all_tag_paths.get(
                    ext_id_map.get(splitext(filename)[-1].lower()))

                if tag_paths is not None:
                    tag_paths.append(filepath)

        # make the debug string by scanning the tags directory
        for def_id in sorted(all_tag_paths.keys()):
            tag_ref_paths = handler.tag_ref_cache[def_id]

            print("Scanning '%s' tags..." % id_ext_map[def_id][1:])
            try: app.io_text.update()
            except Exception: pass
            tags_coll = all_tag_paths[def_id]

            # always display the first tag's filepath
            c_time = time() - p_int + 1

            for filepath in sorted(tags_coll):
                if self.stop_scanning:
                    print('Tag scanning operation cancelled.\n')
                    break

                if time() - c_time > p_int:
                    c_time = time()
                    print(' '*4 + filepath)

                try: app.io_text.update()
                except Exception: pass

                tag = self.get_tag(tagsdir + filepath)
                if tag is None:
                    continue

                try:
                    missed = get_nodes(tag_ref_paths, tag.data,
                                       get_tagref_invalid)

                    if not missed:
                        continue

                    debuglog += "\n\n%s\n" % filepath
                    block_name = None

                    for block in missed:
                        if block.NAME != block_name:
                            debuglog += '%s%s\n' % (' '*4, block.NAME)
                            block_name = block.NAME
                        try:
                            ext = '.' + block.tag_class.enum_name
                        except Exception:
                            ext = ''
                        debuglog += '%s%s\n' % (' '*8, block.STEPTREE + ext)

                except Exception:
                    print("    Could not scan '%s'" % tag.filepath)
                    try: app.io_text.update()
                    except Exception: pass
                    continue

            if self.stop_scanning:
                break

        print("\nScanning took %s seconds." % int(time() - s_time))
        print("Writing logfile...")
        try: app.io_text.update()
        except Exception: pass

        # make and write to the logfile
        try:
            handler.make_log_file(debuglog, logpath)
            print("Scan completed.\n")
            return
        except Exception:
            pass

        print("Could not create log. Printing log to console instead.\n\n")
        try: app.io_text.update()
        except Exception: pass
        for line in debuglog.split('\n'):
            try:
                print(line)
            except Exception:
                print("<COULD NOT PRINT THIS LINE>")
            try: app.io_text.update()
            except Exception: pass

        print("Scan completed.\n")


class HierarchyFrame(BinillaWidget, tk.Frame):

    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault('app_root', master)
        self.app_root = kwargs.pop('app_root')

        kwargs.update(bd=0, highlightthickness=0, bg=self.default_bg_color)
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.directory_frame = DirectoryFrame(self, app_root=self.app_root)
        self.directory_frame.pack(fill='both', expand=True)


class DirectoryFrame(BinillaWidget, tk.Frame):
    tags_dir = None

    def __init__(self, master, *args, **kwargs):
        kwargs.setdefault('app_root', master)
        self.app_root = kwargs.pop('app_root')

        kwargs.update(bg=self.default_bg_color, bd=self.listbox_depth,
            relief='sunken', highlightthickness=0)
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.tags_dir = self.app_root.tags_dir

        self.controls_frame = tk.Frame(self, highlightthickness=0, height=100)
        self.directory_frame = tk.Frame(self, highlightthickness=0)

        self.directory_tree = tk.ttk.Treeview(
            self.directory_frame, selectmode='browse')
        self.scrollbar_y = tk.Scrollbar(
            self.directory_frame, orient='vertical',
            command=self.directory_tree.yview)
        self.directory_tree.config(yscrollcommand=self.scrollbar_y.set)

        self.directory_tree.bind('<<TreeviewOpen>>', self.open_selected)
        self.directory_tree.bind('<<TreeviewClose>>', self.close_selected)
        self.directory_tree.bind('<Double-Button-1>', self.activate_item)

        self.controls_frame.pack(fill='both')
        self.directory_frame.pack(fill='both', expand=True)
        self.directory_tree.pack(side='left', fill='both', expand=True)
        self.scrollbar_y.pack(side='left', fill='both')
        self.reload()

    def reload(self):
        dir_tree = self.directory_tree
        # maybe another time
        #dir_tree["columns"] = ("size")
        #dir_tree.column("size", width=100)
        #dir_tree.heading("size", text='Filesize')

        dir_tree.heading("#0", text='Tagpath')
        self.root_item = dir_tree.insert(
            '', 'end', iid=self.tags_dir , text=self.tags_dir)
        print(dir_tree.item(self.root_item))

    def destroy_subitems(self, item):
        pass

    def generate_subitems(self, item):
        return
        # Log the location of every python file in the defs root
        # search for possibly valid definitions in the defs folder
        for root, directories, files in os.walk(self.defs_filepath):
            for module_path in files:
                base, ext = splitext(module_path)

                fpath = root.split(self.defs_filepath)[-1]

                # make sure the file name ends with .py and isnt already loaded
                if ext.lower() in (".py", ".pyw") and base not in imp_paths:
                    mod_name = (fpath + '.' + base).replace(PATHDIV, '.')
                    imp_paths[mod_name] = join(root, base + ext)

    def open_selected(self, e=None):
        pass

    def close_selected(self, e=None):
        pass

    def activate_item(self, e=None):
        pass
