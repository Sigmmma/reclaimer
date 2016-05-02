from array import array
from mmap import mmap
from math import sqrt

from .tag import *

formats_unpalettized = (
    "ABGR_1555", "XBGR_1555",
    "ABGR_8888", "XBGR_8888",
    )

palette_sizes = {
    #measured in bytes
    "ABGR_1555_IDX_4":2,
    "XBGR_1555_IDX_4":2,
    "ABGR_1555_IDX_8":2,
    "XBGR_1555_IDX_8":2,
    "ABGR_8888_IDX_4":4,
    "XBGR_8888_IDX_4":4,
    "ABGR_8888_IDX_8":4,
    "XBGR_8888_IDX_8":4,
    }

pixel_sizes = {
    #measured in bits
    "ABGR_1555_IDX_4":4,
    "XBGR_1555_IDX_4":4,
    "ABGR_8888_IDX_4":4,
    "XBGR_8888_IDX_4":4,
    "A_4_IDX_4":4,
    "I_4_IDX_4":4,
    "ABGR_1555_IDX_8":8,
    "XBGR_1555_IDX_8":8,
    "ABGR_8888_IDX_8":8,
    "XBGR_8888_IDX_8":8,
    "A_8_IDX_8":8,
    "I_8_IDX_8":8,
    "ABGR_1555":16,
    "XBGR_1555":16,
    "ABGR_8888":32,
    "XBGR_8888":32,
    }

class ObjectsPs2Tag(GdlTag):
    texture_data = None

    #use this for reading into file
    #http://opentechschool.github.io/python-data-intro/core/text-files.html

    def extract(self, defs=True, mod=False, tex=False,
                anim=False, individual=True):
        extract_folder = dirname(self.filepath)+'\\data\\'
        mod_folder  = extract_folder+'mod\\'
        tex_folder  = extract_folder+'tex\\'
        anim_folder = extract_folder+'anim\\'
        
        #if the paths dont exist, create them
        if not exists(tex_folder):
            makedirs(tex_folder)
        if not exists(anim_folder):
            makedirs(anim_folder)

        bitmaps = self.data.bitmaps
        texture_data = self.texture_data
        individual = True

        if defs:
            if not exists(extract_folder):
                makedirs(extract_folder)
            defs_file = open(extract_folder+'defs.xml', 'w')
            self.export_defs(defs_file)
            defs_file.close()

        if mod:
            if not exists(mod_folder):
                makedirs(mod_folder)
            self.export_models(individual, mod_folder)
        print(self.filepath)
                


    def export_defs(self, buffer):
        buffer.write('<?xml version="1.0"?>\n')
        buffer.write('# gauntlet dark legacy model and texture defs\n\n')

        objects = self.data.objects
        bitmaps = self.data.bitmaps
        object_defs = self.data.object_defs
        bitmap_defs = self.data.bitmap_defs
        
        idnt = '  '

        #write the model data
        buffer.write('<objs>\n')
        for i in range(len(objects)):
            obj = objects[i]
            f = obj.flags
            buffer.write(idnt+'# %s\n'%i)
            buffer.write((idnt+'<obj inv_rad="%s" bnd_rad="%s">\n')%
                            (obj.inv_rad, obj.bnd_rad))
            for attr in ('alpha', 'sharp', 'blur', 'chrome', 'lmap',
                         'sort_a', 'sort', 'fmt_mask', 'pre_lit',
                         'lit_mask', 'lmap_lit', 'norm_lit', 'dyn_lit'):
                if not f.__getattr__(attr):
                    continue
                buffer.write(idnt*2+ '<set_flag name="%s"/>\n' % attr)
            
            buffer.write(idnt+'</obj>\n')
        buffer.write('</objs>\n')
        
        #write the texture data
        buffer.write('<texs>\n')
        for i in range(len(bitmaps)):
            b = bitmaps[i]
            f = b.flags
            buffer.write(idnt+'<tex format="%s">\n' % b.format.data_name)
            for attr in ('halfres', 'see_alpha', 'clamp_u', 'clamp_v',
                         'animation', 'external', 'tex_shift',
                         'has_alpha', 'invalid', 'dual_tex'):
                if not f.__getattr__(attr):
                    continue
                buffer.write(idnt*2+ '<set_flag name="%s"/>\n' % attr)
                
            if not(f.external or f.animation) :
                buffer.write(idnt+'</tex>\n')
                continue
            for attr in ('lod_k', 'mipmap_count', 'width_64',
                         'log2_of_width', 'log2_of_height',
                         'tex_palette_index', 'tex_palette_count',
                         'tex_shift_index', 'frame_count',
                         'width', 'height', 'size', 'tex_0'):
                buffer.write(idnt*2+
                                '<attr name="%s" value="%s"/>\n' %
                                (attr, b.__getattr__(attr)) )
            buffer.write(idnt+'</tex>\n')
        buffer.write('</texs>\n')

        #write the model definition data
        buffer.write('<obj_defs>\n')
        for i in range(len(object_defs)):
            od = object_defs[i]
            buffer.write((idnt+'<obj_def obj_index="%s" frames="%s" '+
                            'bnd_rad="%s" name="%s" />\n')%( od.obj_index,
                            od.n_frames, od.bnd_rad, od.name))
        buffer.write('</obj_defs>\n')

        #write the texture definition data
        buffer.write('<tex_defs>\n')
        for i in range(len(bitmap_defs)):
            bd = bitmap_defs[i]
            buffer.write((idnt+'<tex_def tex_index="%s" width="%s" '+
                             'height="%s" name="%s"/>\n')% ( bd.tex_index,
                             bd.width, bd.height, bd.name))
        buffer.write('</tex_defs>\n')


    def export_models(self, individual=True, mod_folder='mod\\'):
        prefix = ''
        objects = self.data.objects
        
        if not individual:
            obj_file = open(extract_folder+'mod.obj', 'w')
            obj_file.write('# Gauntlet Dark Legacy 3d model\n'+
                           '#     Written by Moses\n\n')
            start_v = 1
            
        #loop over each object
        for i in range(len(objects)):
            if individual:
                obj_file = open(mod_folder+'%s.obj'%i, 'w')
                obj_file.write('# Gauntlet Dark Legacy 3d model\n'+
                               '#     Written by Moses\n\n')
                start_v = 1
                group = ''
            else:
                group = '%s'%i
                prefix = '%s_'%i

            curr_obj = objects[i]
            tex_index = curr_obj.sub_object_0.tex_index

            #loop over each subobject
            for j in range(len(curr_obj.data.sub_object_models)):
                subobj = curr_obj.data.sub_object_models[j]
                verts = ""
                uvs = ""
                normals = ""

                uv_scale = 1
                vert_scale = 1

                face_dirs = []
                asdf = []
                
                if j:
                    tex_index = curr_obj.data.sub_objects[j-1].tex_index

                obj_file.write('\n')
                obj_file.write('# object %s\n'%j)

                #loop over each primitive
                for primitive in subobj.primitives:
                    sentinel = primitive.sentinel
                    if sentinel in (104, 105, 106):
                        #8/16/32 bit vertex coordinates
                        v = primitive.data
                        for k in range(0, len(v)-3, 3):
                            #make sure to ignore the last vertex
                            verts += 'v %s %s %s\n' % (v[k]*vert_scale,
                                                       v[k+1]*vert_scale,
                                                       v[k+2]*vert_scale)
                            
                    elif sentinel == 111:
                        #16 bit compressed vertex normals
                        vn = primitive.data
                        dirs = [None]*len(vn)
                        
                        for k in range(len(vn)):
                            norm = vn[k]
                            xn = ((norm&31)-15)/15
                            yn = (((norm>>5)&31)-15)/15
                            zn = (((norm>>10)&31)-15)/15
                            
                            #dont need much precision on these
                            normals += 'vn %s %s %s\n' % \
                                   (str(xn)[:7],
                                    str(yn)[:7],
                                    str(zn)[:7])
                            dirs[k] = int(bool(norm&32768))
                        #make sure the first 2 are removed since they
                        #are always 1 and triangle strips are always
                        #made of 2 more verts than there are triangles
                        face_dirs.append(dirs[2:])
                    
                    elif sentinel in (100, 101, 102):
                        #8/16/32 bit uv coordinates
                        vt = primitive.data
                        for k in range(0, len(vt), 2):
                            uvs += 'vt %s %s\n' % (vt[k]*uv_scale/128,
                                                   vt[k+1]*uv_scale/128)
                            
                    elif sentinel == 108:
                        #polyinstance
                        uv_scale = primitive.uv_scale
                        
                #write the verts, uvs, and normals to the obj file
                obj_file.write(verts+'\n')
                obj_file.write(uvs+'\n')
                obj_file.write(normals+'\n')
                
                obj_file.write('g %s\n'%prefix)
                obj_file.write('usemtl %s_0\n'%tex_index)
                
                #generate the faces
                for dirs in face_dirs:
                    for f in range(len(dirs)):
                        if dirs[f]:
                            continue
                        
                        k = start_v + f
                        if f&1:
                            obj_file.write('f %s/%s/%s %s/%s/%s %s/%s/%s\n'%
                                           (k+1,k+1,k+1,k,k,k,k+2,k+2,k+2))
                        else:
                            #swap the vert order of every other face
                            obj_file.write('f %s/%s/%s %s/%s/%s %s/%s/%s\n'%
                                           (k,k,k,k+1,k+1,k+1,k+2,k+2,k+2))
                    start_v += len(dirs)+2
                    
            if individual:
                obj_file.close()
                
        obj_file.close()

    
    def read(self, **kwargs):
        ''''''
        GdlTag.read(self, **kwargs)
        bitmaps = self.data.bitmaps

        textures_filepath = self.textures_filepath
        texture_data      = self.texture_data = [None]*len(bitmaps)
        try:
            with open(textures_filepath, 'r+b') as f:
                rawdata = mmap(f.fileno(), 0)
        except Exception:
            return
        
        for i in range(len(bitmaps)):
            texture_data[i] = []
            if bitmaps[i].frame_count or bitmaps[i].flags.external:
                continue
            
            format  = bitmaps[i].format
            format_name = format.data_name
            
            tex_pointer = bitmaps[i].tex_pointer
            mipmaps     = bitmaps[i].mipmap_count
            
            palette_size = palette_sizes.get(format_name, 0)
            pixel_size   = pixel_sizes.get(format_name, 0)
            
            width  = bitmaps[i].width
            height = bitmaps[i].height

            #go to the start of the palette/pixel data
            rawdata.seek(tex_pointer)

            if palette_size:
                texture_data[i].append(bytearray(rawdata.read((2**pixel_size)*palette_size)))
            for mip in range(mipmaps+1):
                texture_data[i].append(bytearray(rawdata.read((width*height*pixel_size)//8)))
                width = width//2
                height = height//2

    @property
    def textures_filepath(self):
        ''''''
        return dirname(self.filepath) + '\\textures.ps2'

    def write(self, **kwargs):
        ''''''
        filepath = self.textures_filepath
        texture_data = self.texture_data
        bitmaps      = self.data.bitmaps

        curr_pointer = 0
        
        #set the pointers for the texture data
        for i in range(len(bitmaps)):
            if bitmaps[i].frame_count or bitmaps[i].flags.external:
                continue
            
            #set the tex_pointer to the current pointer location
            bitmaps[i].tex_pointer = curr_pointer

            for rawdata in texture_data[i]:
                if isinstance(rawdata, (bytes, bytearray)):
                    curr_pointer += len(rawdata)
                elif isinstance(rawdata, array):
                    curr_pointer += len(rawdata)*rawdata.itemsize

            '''since i dont know what the alignment requirements are on
            the texture data, i'm gonna assume everything needs to be
            4-byte aligned, since that will take care of all cases.'''
            curr_pointer += 4-(curr_pointer%4)

        #write the tag data to its file
        GdlTag.write(self, **kwargs)
        
        temppath   = filepath + ".temp"
        backuppath = filepath + ".backup"

        #open the textures.ps2 file and write the texture data into it
        with open(temppath, 'w+b') as f:
            for i in range(len(bitmaps)):
                if bitmaps[i].frame_count or bitmaps[i].flags.external:
                    continue
                
                f.seek(bitmaps[i].tex_pointer)
                
                for rawdata in texture_data[i]:
                    f.write(rawdata)
                    
        if not bool(kwargs.get('temp',True)):
            self.rename_backup_and_temp(self, filepath, backuppath, temppath,
                                        bool(kwargs.get('backup',True)))
