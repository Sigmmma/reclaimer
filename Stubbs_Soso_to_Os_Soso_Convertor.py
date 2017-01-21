import os, supyr_struct

from math import sqrt
from time import time
from tkinter import *
from tkinter.filedialog import askdirectory
from traceback import format_exc

from supyr_struct.defs.constants import fcc, PATHDIV
from supyr_struct.defs.block_def import BlockDef
from reclaimer.halo.stubbs.defs.soso import soso_def as stubbs_soso_def
from reclaimer.halo.os_v3_hek.defs.soso import soso_def as os_soso_def


PATHDIV = PATHDIV
curr_dir = os.path.abspath(os.curdir) + PATHDIV


def stubbs_soso_to_os_soso(soso_path):
    stubbs_soso_tag = stubbs_soso_def.build(filepath=soso_path)
    os_soso_tag = os_soso_def.build()
    os_soso_tag.filepath = os.path.splitext(soso_path)[0] + '.shader_model'

    os_soso_data = os_soso_tag.data.tagdata.soso_attrs
    stubbs_soso_data = stubbs_soso_tag.data.tagdata.soso_attrs
    bump_props = stubbs_soso_data.bump_properties

    # move the data from the stubbs tag into the open sauce tag
    os_soso_data.model_shader = stubbs_soso_data.model_shader
    os_soso_data.color_change_source = stubbs_soso_data.color_change_source
    os_soso_data.self_illumination = stubbs_soso_data.self_illumination
    os_soso_data.texture_scrolling = stubbs_soso_data.texture_scrolling
    os_soso_data.reflection_properties = stubbs_soso_data.reflection_properties

    # make a new shader extension for the bump map
    os_soso_data.os_shader_model_ext.STEPTREE.extend(1)
    os_ext = os_soso_data.os_shader_model_ext.STEPTREE[0]
    os_ext.base_normal_coefficient = bump_props.bump_scale
    os_ext.base_normal_map = bump_props.bump_map

    return os_soso_tag


class StubbsSosoToOsSosoConvertor(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Stubbs Shader_model to Os Shader_model Convertor v1.0")
        self.geometry("500x70+0+0")
        self.resizable(0, 0)

        self.tags_dir = StringVar(self)
        self.tags_dir.set(curr_dir + 'tags' + PATHDIV)

        # make the frame
        self.tags_dir_frame = LabelFrame(self, text="Output tags directory")
        
        # add the filepath boxes
        self.tags_dir_entry = Entry(
            self.tags_dir_frame, textvariable=self.tags_dir)
        self.tags_dir_entry.config(width=55, state=DISABLED)

        # add the buttons
        self.convert_btn = Button(
            self, text="Convert stubbs_shader_models",
            width=15, command=self.convert_models)
        self.tags_dir_browse_btn = Button(
            self.tags_dir_frame, text="Browse",
            width=6, command=self.tags_dir_browse)

        # pack everything
        self.tags_dir_entry.pack(expand=True, fill='x', side='left')
        self.tags_dir_browse_btn.pack(fill='both', side='left')

        self.tags_dir_frame.pack(expand=True, fill='both')
        self.convert_btn.pack(fill='both', padx=5, pady=5)
        
    def tags_dir_browse(self):
        dirpath = askdirectory(initialdir=self.tags_dir.get())
        if dirpath:
            self.tags_dir.set(dirpath)

    def convert_models(self):
        print('Converting stubbs_shader_models\n')
        start = time()
        tags_dir = self.tags_dir.get()

        if not tags_dir.endswith(PATHDIV):
            tags_dir += PATHDIV

        for root, dirs, files in os.walk(tags_dir):
            if not root.endswith(PATHDIV):
                root += PATHDIV

            for filename in files:
                filepath = root + filename
                if os.path.splitext(filename)[-1].lower() != '.stubbs_shader_model':
                    continue

                print('Converting %s' % filepath.split(tags_dir)[-1])

                soso_tag = stubbs_soso_to_os_soso(filepath)
                soso_tag.serialize(temp=False, backup=False)
        print('\nFinished. Took %s seconds' % (time() - start))

try:
    converter = StubbsSosoToOsSosoConvertor()
    converter.mainloop()
except Exception:
    print(format_exc())
    input()

