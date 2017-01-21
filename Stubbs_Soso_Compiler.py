import os, struct, supyr_struct

from time import time
from tkinter import *
from tkinter.filedialog import askdirectory
from traceback import format_exc

from supyr_struct.field_types import FieldType, BytearrayRaw
from supyr_struct.defs.constants import fcc, PATHDIV
from supyr_struct.defs.block_def import BlockDef
from reclaimer.halo.stubbs.defs.soso import soso_def

force_little = FieldType.force_little
force_normal = FieldType.force_normal

PATHDIV = PATHDIV
curr_dir = os.path.abspath(os.curdir) + PATHDIV

bitm_fcc = fcc('bitm', 'big')

def make_soso_tag(meta_path, tags_dir=curr_dir + "tags" + PATHDIV):
    soso_tag = soso_def.build()
    try:
        # force reading in little endian since meta data is ALL little endian
        force_little()

        # make a new tag
        tagdata = soso_tag.data.tagdata

        # get the dependencies to put in the new tag
        tag_paths = get_tag_paths(meta_path + '.data')

        with open(meta_path, 'rb') as f:
            meta_data = bytearray(f.read())

        # insert the bitmap dependency strings
        for tag_path in tag_paths[1:]:
            offset = int(tag_path[0]) - 4
            path = tag_path[1].encode()
            if path:
                meta_data[offset:offset+4] = struct.pack('<I', len(path))
                meta_data += path + b'\x00'

        # populate that new tag with the meta data
        tagdata.parse(rawdata=meta_data)

        # replace the filepath
        soso_tag.filepath = tags_dir + tag_paths[0] + ".stubbs_shader_model"

        # force fix the endianness
        force_normal()
    except Exception:
        force_normal()
        raise

    return soso_tag


def get_tag_paths(data_path):
    tag_paths = ['']
    try:
        with open(data_path, 'r') as f:
            for line in f:
                if line.lower().startswith('filename'):
                    tag_paths[0] = line.split('|')[-1].split('\n')[0]
                elif line.lower().startswith('dependency'):
                    offset, tag_path = line.split('\n')[0].split('|')[1:3]
                    tag_paths.append((offset, tag_path))
    except Exception:
        print(format_exc())
    return tag_paths


class StubbsSosoCompiler(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Stubbs soso tag compiler v1.0")
        self.geometry("400x120+0+0")
        self.resizable(0, 0)

        self.meta_dir = StringVar(self)
        self.tags_dir = StringVar(self)
        self.tags_dir.set(curr_dir + 'tags' + PATHDIV)

        # make the frames
        self.meta_dir_frame = LabelFrame(self, text="Directory of metadata")
        self.tags_dir_frame = LabelFrame(self, text="Output tags directory")
        
        # add the filepath boxes
        self.meta_dir_entry = Entry(
            self.meta_dir_frame, textvariable=self.meta_dir)
        self.tags_dir_entry = Entry(
            self.tags_dir_frame, textvariable=self.tags_dir)
        self.meta_dir_entry.config(width=55, state=DISABLED)
        self.tags_dir_entry.config(width=55, state=DISABLED)

        # add the buttons
        self.compile_btn = Button(
            self, text="Compile", width=15, command=self.compile_models)
        self.meta_dir_browse_btn = Button(
            self.meta_dir_frame, text="Browse",
            width=6, command=self.meta_dir_browse)
        self.tags_dir_browse_btn = Button(
            self.tags_dir_frame, text="Browse",
            width=6, command=self.tags_dir_browse)

        # pack everything
        self.meta_dir_entry.pack(expand=True, fill='x', side='left')
        self.tags_dir_entry.pack(expand=True, fill='x', side='left')
        self.meta_dir_browse_btn.pack(fill='both', side='left')
        self.tags_dir_browse_btn.pack(fill='both', side='left')

        self.meta_dir_frame.pack(expand=True, fill='both')
        self.tags_dir_frame.pack(expand=True, fill='both')
        self.compile_btn.pack(fill='both', padx=5, pady=5)

    def meta_dir_browse(self):
        dirpath = askdirectory(initialdir=self.meta_dir.get())
        if dirpath:
            self.meta_dir.set(dirpath)
        
    def tags_dir_browse(self):
        dirpath = askdirectory(initialdir=self.tags_dir.get())
        if dirpath:
            self.tags_dir.set(dirpath)

    def compile_models(self):
        print('Compiling shader_models\n')
        start = time()
        meta_dir = self.meta_dir.get()
        tags_dir = self.tags_dir.get()

        if not meta_dir.endswith(PATHDIV):
            meta_dir += PATHDIV

        if not tags_dir.endswith(PATHDIV):
            tags_dir += PATHDIV

        for root, dirs, files in os.walk(meta_dir):
            if not root.endswith(PATHDIV):
                root += PATHDIV

            for filename in files:
                filepath = root + filename
                if not filename.lower().endswith('[soso].meta'):
                    continue

                print('Compiling %s' % filepath.split(meta_dir)[-1])

                tag = make_soso_tag(filepath, tags_dir)
                tag.serialize(temp=False, backup=False, int_test=False)
        print('\nFinished. Took %s seconds' % (time() - start))

try:
    compiler = StubbsSosoCompiler()
    compiler.mainloop()
except Exception:
    print(format_exc())
    input()

