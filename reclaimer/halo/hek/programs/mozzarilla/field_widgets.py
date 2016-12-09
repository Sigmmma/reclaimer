import tkinter as tk

from supyr_struct.apps.binilla import editor_constants
from supyr_struct.apps.binilla.field_widgets import *


class DependencyFrame(ContainerFrame):

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
        f_widget_ids = self.f_widget_ids

        # clear the f_widget_ids list
        del f_widget_ids[:]

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

        node = self.node
        desc = node.desc
        picker = self.widget_picker
        app_root = self.app_root

        field_indices = range(len(node))
        # if the node has a steptree node, include its index in the indices
        if hasattr(node, 'STEPTREE'):
            field_indices = tuple(field_indices) + ('STEPTREE',)

        kwargs = dict(parent=node, app_root=app_root, disabled=self.disabled,
                      f_widget_parent=self, vert_oriented=vertical)

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

        # now that the field widgets are created, position them
        if self.show.get():
            self.pose_fields()

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

            f_widgets_by_i = {}
            for wid in self.f_widget_ids:
                w = f_widgets[str(wid)]
                f_widgets_by_i[w.attr_index] = w

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

                w = f_widgets_by_i.get(i)

                # if neither would be visible, dont worry about checking it
                if not(sub_desc.get('VISIBLE',1) or all_visible) and w is None:
                    continue

                # if the descriptors are different, gotta repopulate!
                if w.desc is not sub_desc:
                    self.populate()
                    return
                
            for wid in self.f_widget_ids:
                w = f_widgets[str(wid)]

                w.parent, w.node = node, node[w.attr_index]
                w.reload()
        except Exception:
            print(format_exc())
