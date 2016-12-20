import tkinter as tk

from os.path import dirname, exists, splitext
from tkinter.filedialog import askopenfilename, asksaveasfilename
from traceback import format_exc

from supyr_struct.buffer import get_rawdata
from supyr_struct.defs.constants import PATHDIV
from supyr_struct.defs.audio.wav import wav_def
from supyr_struct.apps.binilla import editor_constants
from supyr_struct.apps.binilla.field_widgets import *


class DependencyFrame(ContainerFrame):

    def browse_tag(self):
        tag_window = self.tag_window
        app = tag_window.app_root
        curr_handler = app.handler
        new_handler = tag_window.handler

        try:
            app.set_handler(new_handler)

            tags_dir = app.tags_dir
            if not tags_dir.endswith(PATHDIV):
                tags_dir += PATHDIV

            init_dir = tags_dir
            try: init_dir = tags_dir + dirname(self.node.filepath)
            except Exception: pass

            filetypes = []
            for ext in sorted(self.node.tag_class.NAME_MAP):
                if ext == 'NONE':
                    continue
                filetypes.append((ext, '*.%s' % ext))
            if len(filetypes) > 1:
                filetypes = (('All', '*'),) + tuple(filetypes)
            else:
                filetypes.append(('All', '*'))
            filepath = askopenfilename(
                initialdir=init_dir, filetypes=filetypes, title="Select a tag")

            if not filepath:
                return

            filepath = filepath.replace('/', '\\').replace('\\', PATHDIV)
            tag_path, ext = splitext(filepath.lower().split(tags_dir.lower())[-1])
            try:
                self.node.tag_class.set_to(ext[1:])
            except Exception:
                self.node.tag_class.set_to('NONE')
                for filetype in filetypes:
                    ext = filetype[1][1:]
                    if exists(tags_dir + tag_path + ext):
                        self.node.tag_class.set_to(ext[1:])
                        break
            self.node.filepath = tag_path
            self.reload()
        except Exception:
            print(format_exc())

        try: app.set_handler(curr_handler)
        except Exception: pass

    def open_tag(self):
        tag_window = self.tag_window
        app = tag_window.app_root
        curr_handler = app.handler
        new_handler = tag_window.handler

        try:
            app.set_handler(new_handler)
            tags_dir = app.tags_dir
            if not tags_dir.endswith(PATHDIV):
                tags_dir += PATHDIV

            self.flush()

            rel_filepath = '%s.%s' % (self.node.filepath,
                                      self.node.tag_class.enum_name)
            app.load_tags(filepaths=tags_dir + rel_filepath)
            app.set_handler(curr_handler)
        except Exception:
            print(format_exc())
            try: app.set_handler(curr_handler)
            except Exception: pass

    def populate(self):
        '''Destroys and rebuilds this widgets children.'''
        orient = self.desc.get('ORIENT', 'v')[:1].lower()  # get the orientation
        vertical = True
        assert orient in 'vh'

        content = self
        if hasattr(self, 'content'):
            content = self.content
        if self.show_title and content in (None, self):
            content = tk.Frame(self, relief="sunken", bd=self.frame_depth,
                               bg=self.default_bg_color)

        self.content = content
        # clear the f_widget_ids list
        del self.f_widget_ids[:]
        del self.f_widget_ids_map

        f_widget_ids = self.f_widget_ids
        f_widget_ids_map = self.f_widget_ids_map = {}

        # destroy all the child widgets of the content
        for c in list(content.children.values()):
            c.destroy()

        # if the orientation is horizontal, remake its label
        if orient == 'h':
            vertical = False
            self.title_label = tk.Label(
                self, anchor='w', justify='left',
                width=self.title_size, text=self.gui_name,
                bg=self.default_bg_color, fg=self.text_normal_color)
            if self.gui_name != '':
                self.title_label.pack(fill="x", side="left")

        btn_kwargs = dict(
            bg=self.button_color, activebackground=self.button_color,
            fg=self.text_normal_color, bd=self.button_depth,
            disabledforeground=self.text_disabled_color,
            )
        self.browse_btn = tk.Button(
            self, width=3, text='...', command=self.browse_tag, **btn_kwargs)
        self.open_btn = tk.Button(
            self, width=6, text='Open', command=self.open_tag, **btn_kwargs)

        node = self.node
        desc = node.desc
        picker = self.widget_picker
        tag_window = self.tag_window

        field_indices = range(len(node))
        # if the node has a steptree node, include its index in the indices
        if hasattr(node, 'STEPTREE'):
            field_indices = tuple(field_indices) + ('STEPTREE',)

        kwargs = dict(parent=node, tag_window=tag_window,
                      disabled=self.disabled, f_widget_parent=self,
                      vert_oriented=vertical)

        all_visible = self.all_visible
        visible_count = self.visible_field_count

        # if only one sub-widget being displayed, dont
        # display the title of the widget being displayed
        if all_visible:
            pass
        elif hasattr(node, 'STEPTREE'):
            s_node = node['STEPTREE']
            s_desc = desc['STEPTREE']
            if hasattr(s_node, 'desc'):
                s_desc = s_node.desc
            if not s_desc.get('VISIBLE', 1) and visible_count <= 1:
                kwargs['show_title'] = False
        elif visible_count <= 1:
            kwargs['show_title'] = False

        # loop over each field and make its widget
        for i in field_indices:
            sub_node = node[i]
            sub_desc = desc[i]
            if hasattr(sub_node, 'desc'):
                sub_desc = sub_node.desc

            # only display the enumerator if there are more than 2 options
            if i == 0 and sub_desc['ENTRIES'] <= 2:
                continue

            # if the field shouldnt be visible, dont make its widget
            if not(sub_desc.get('VISIBLE', True) or all_visible):
                continue

            widget_cls = picker.get_widget(sub_desc)
            try:
                widget = widget_cls(content, node=sub_node,
                                    attr_index=i, **kwargs)
            except Exception:
                print(format_exc())
                widget = NullFrame(content, node=sub_node,
                                   attr_index=i, **kwargs)

            f_widget_ids.append(id(widget))
            f_widget_ids_map[i] = id(widget)

            if sub_desc.get('NAME') == 'filepath':
                widget.data_entry.bind('<FocusIn>', self.validate_filepath)
                widget.data_entry.bind('<Return>', self.validate_filepath)
                widget.data_entry.bind('<FocusOut>', self.validate_filepath)
                self.validate_filepath()

        # now that the field widgets are created, position them
        if self.show.get():
            self.pose_fields()

    def validate_filepath(self, e=None):
        desc = self.desc
        widget_id = self.f_widget_ids_map.get(desc['NAME_MAP']['filepath'])
        widget = self.content.children.get(str(widget_id))
        if widget is None:
            return

        tags_dir = self.tag_window.handler.tagsdir
        if not tags_dir.endswith(PATHDIV):
            tags_dir += PATHDIV

        filepath = '%s%s.%s' % (tags_dir, self.node.filepath,
                                self.node.tag_class.enum_name)
        filepath = filepath.replace('/', '\\').replace('\\', PATHDIV)
        if exists(filepath):
            widget.data_entry.config(fg=self.text_normal_color)
        else:
            widget.data_entry.config(fg=self.invalid_path_color)

    def pose_fields(self):
        ContainerFrame.pose_fields(self)
        padx, pady, side= self.horizontal_padx, self.horizontal_pady, 'top'
        if self.desc.get('ORIENT', 'v') in 'hH':
            side = 'left'

        self.browse_btn.pack(
            fill='x', side=side, anchor='nw', padx=padx, pady=pady)
        self.open_btn.pack(fill='x', side=side, anchor='nw', padx=padx)

    def reload(self):
        '''Resupplies the nodes to the widgets which display them.'''
        try:
            node = self.node
            desc = self.desc
            f_widgets = self.content.children

            field_indices = range(len(node))
            # if the node has a steptree node, include its index in the indices
            if hasattr(node, 'STEPTREE'):
                field_indices = tuple(field_indices) + ('STEPTREE',)

            f_widget_ids_map = self.f_widget_ids_map
            all_visible = self.all_visible

            # if any of the descriptors are different between
            # the sub-nodes of the previous and new sub-nodes,
            # then this widget will need to be repopulated.
            for i in field_indices:
                sub_node = node[i]
                sub_desc = desc[i]
                if hasattr(sub_node, 'desc'):
                    sub_desc = sub_node.desc

                # only display the enumerator if there are more than 2 options
                if i == 0 and sub_desc['ENTRIES'] <= 2:
                    continue

                w = f_widgets.get(str(f_widget_ids_map.get(i)))

                # if neither would be visible, dont worry about checking it
                if not(sub_desc.get('VISIBLE',1) or all_visible) and w is None:
                    continue

                # if the descriptors are different, gotta repopulate!
                if not hasattr(w, 'desc') or w.desc is not sub_desc:
                    self.populate()
                    return
                
            for wid in self.f_widget_ids:
                w = f_widgets[str(wid)]

                w.parent, w.node = node, node[w.attr_index]
                w.reload()

            self.validate_filepath()
        except Exception:
            print(format_exc())


class SoundSampleFrame(RawdataFrame):

    @property
    def field_ext(self):
        '''The export extension of this FieldWidget.'''
        try:
            if self.parent.parent.compression.enum_name == 'ogg':
                return '.ogg'
        except Exception:
            pass
        return '.wav'

    def import_node(self):
        '''Prompts the user for an exported node file.
        Imports data into the node from the file.'''
        try:
            initialdir = self.tag_window.app_root.last_load_dir
        except AttributeError:
            initialdir = None

        ext = self.field_ext

        filepath = askopenfilename(
            initialdir=initialdir, defaultextension=ext,
            filetypes=[(self.name, "*" + ext), ('All', '*')],
            title="Import sound data from...")

        if not filepath:
            return

        curr_size = None
        index = self.attr_index

        try:
            curr_size = self.parent.get_size(attr_index=index)
            if ext == '.wav':
                # if the file is wav, we need to give it a header
                wav_file = wav_def.build(filepath=filepath)

                sound_data = self.parent.get_root().data.tagdata
                channel_count = sound_data.encoding.data + 1
                sample_rate = 22050 * (sound_data.sample_rate.data + 1)
                wav_fmt = wav_file.data.format

                if wav_fmt.fmt.enum_name not in ('ima_adpcm', 'xbox_adpcm'):
                    raise TypeError(
                        "Wav file audio format must be either ImaADPCM " +
                        "or XboxADPCM, not %s" % wav_fmt.fmt.enum_name)

                if sound_data.encoding.data + 1 != wav_fmt.channels:
                    raise TypeError(
                        "Wav file channel count does not match this sound " +
                        "tags channel count. Expected %s, not %s" %
                        (channel_count, wav_fmt.channels))

                if sample_rate != wav_fmt.sample_rate:
                    raise TypeError(
                        "Wav file sample rate does not match this sound " +
                        "tags sample rate. Expected %skHz, not %skHz" %
                        (sample_rate, wav_fmt.sample_rate))

                if 36 * channel_count != wav_fmt.block_align:
                    raise TypeError(
                        "Wav file block size does not match this sound " +
                        "tags block size. Expected %sbytes, not %sbytes" %
                        (36 * channel_count, wav_fmt.block_align))

                rawdata = wav_file.data.wav_data.audio_data
                self.parent.set_size(len(rawdata), attr_index=index)
                self.parent.parse(rawdata=rawdata, attr_index=index)
                self.node = self.parent[index]
            else:
                rawdata = get_rawdata(filepath=filepath)
                self.parent.set_size(len(rawdata), attr_index=index)
                self.parent.parse(rawdata=rawdata, attr_index=index)
                self.node = self.parent[index]

            # until i come up with a better method, i'll have to rely on
            # reloading the root field widget so stuff(sizes) will be updated
            try:
                self.f_widget_parent.reload()
            except Exception:
                print(format_exc())
                print("Could not reload after importing sound data.")
        except Exception:
            print(format_exc())
            print("Could not import sound data.")
            try: self.parent.set_size(curr_size, attr_index=index)
            except Exception: pass

    def export_node(self):
        try:
            initialdir = self.tag_window.app_root.last_load_dir
        except AttributeError:
            initialdir = None

        ext = self.field_ext

        filepath = asksaveasfilename(
            initialdir=initialdir, defaultextension=ext,
            filetypes=[(self.name, "*" + ext), ('All', '*')],
            title="Export sound data to...")

        if not filepath:
            return

        if ext == '.wav':
            # if the file is wav, we need to give it a header
            try:
                wav_file = wav_def.build()
                wav_file.filepath = filepath
                sound_data = self.parent.get_root().data.tagdata

                wav_fmt = wav_file.data.format
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.channels = sound_data.encoding.data + 1
                wav_fmt.sample_rate = 22050 * (sound_data.sample_rate.data + 1)

                wav_fmt.byte_rate = ((wav_fmt.sample_rate *
                                      wav_fmt.bits_per_sample *
                                      wav_fmt.channels) // 8)

                wav_fmt.block_align = 36 * wav_fmt.channels

                wav_file.data.wav_data.audio_data = self.node
                wav_file.data.wav_header.filesize = wav_file.data.binsize - 12

                wav_file.serialize(temp=False, backup=False, int_test=False)
            except Exception:
                print(format_exc())
                print("Could not export sound data.")
            return

        try:
            if hasattr(self.node, 'serialize'):
                self.node.serialize(filepath=filepath, clone=self.export_clone,
                                    calc_pointers=self.export_calc_pointers)
            else:
                # the node isnt a block, so we need to call its parents
                # serialize method with the attr_index necessary to export.
                self.parent.serialize(filepath=filepath,
                                      clone=self.export_clone,
                                      calc_pointers=self.export_calc_pointers,
                                      attr_index=self.attr_index)
        except Exception:
            print(format_exc())
            print("Could not export sound data.")


class ReflexiveFrame(ArrayFrame):
    def __init__(self, *args, **kwargs):
        ArrayFrame.__init__(self, *args, **kwargs)

        btn_kwargs = dict(
            bg=self.button_color, fg=self.text_normal_color,
            disabledforeground=self.text_disabled_color,
            bd=self.button_depth,
            )

        self.import_all_btn = tk.Button(
            self.buttons, width=10, text='Import all',
            command=self.import_all_nodes, **btn_kwargs)
        self.export_all_btn = tk.Button(
            self.buttons, width=10, text='Export all',
            command=self.export_all_nodes, **btn_kwargs)

        # pack the title, menu, and all the buttons
        for w in (self.export_all_btn, self.import_all_btn):
            w.pack(side="right", padx=(0, 4), pady=(2, 2))

    def set_import_all_disabled(self, disable=True):
        if disable: self.import_all_btn.config(state="disabled")
        else:       self.import_all_btn.config(state="normal")

    def set_export_all_disabled(self, disable=True):
        if disable: self.export_all_btn.config(state="disabled")
        else:       self.export_all_btn.config(state="normal")

    def export_all_nodes(self):
        try:
            w = self.f_widget_parent
        except Exception:
            return
        w.export_node()

    def import_all_nodes(self):
        try:
            w = self.f_widget_parent
        except Exception:
            return
        w.import_node()
