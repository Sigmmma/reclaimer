from array import array
from math import log
from mmap import mmap
from struct import unpack
from sys import byteorder as BYTEORDER
from traceback import format_exc

from .tag import *
from ...fields import *
from supyr_struct.defs.block_def import BlockDef

PALETTE_PACK_CHARS = {
    "ABGR_1555_IDX_4":'H',
    "XBGR_1555_IDX_4":'H',
    "ABGR_1555_IDX_8":'H',
    "XBGR_1555_IDX_8":'H',
    "ABGR_8888_IDX_4":'I',
    "XBGR_8888_IDX_4":'I',
    "ABGR_8888_IDX_8":'I',
    "XBGR_8888_IDX_8":'I',
    }

PIXEL_PACK_CHARS = {
    "ABGR_1555":'H',
    "XBGR_1555":'H',
    "ABGR_8888":'I',
    "XBGR_8888":'I',
    }

PALETTE_SIZES = {
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

PIXEL_SIZES = {
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

ALPHA_SIZES = {
    #measured in bits
    "ABGR_1555_IDX_4":1,
    "XBGR_1555_IDX_4":1,
    "ABGR_8888_IDX_4":8,
    "XBGR_8888_IDX_4":8,
    "ABGR_1555_IDX_8":1,
    "XBGR_1555_IDX_8":1,
    "ABGR_8888_IDX_8":8,
    "XBGR_8888_IDX_8":8,
    "ABGR_1555":1,
    "XBGR_1555":1,
    "ABGR_8888":8,
    "XBGR_8888":8,
    }

BLOCK_SIZES = array('B', [1]*256)
BLOCK_SIZES[100] = 8
BLOCK_SIZES[101] = 4
BLOCK_SIZES[102] = 2

BLOCK_SIZES[104] = 12
BLOCK_SIZES[105] = 6
BLOCK_SIZES[106] = 3

BLOCK_SIZES[109] = 8
BLOCK_SIZES[111] = 2

UNPACK_CHARS = ['B']*256
UNPACK_CHARS[100] = 'I'
UNPACK_CHARS[101] = 'H'
UNPACK_CHARS[102] = 'B'

UNPACK_CHARS[104] = 'i'
UNPACK_CHARS[105] = 'h'
UNPACK_CHARS[106] = 'b'

UNPACK_CHARS[109] = 'h'
UNPACK_CHARS[111] = 'H'

#i dont imagine there ever being a use for even a 1024 texture
VALID_DIMS = set([1,2,4,8,16,32,64,128,256,512,1024,2048,4096])

BYTEORDER = '>'
if BYTEORDER == 'little':
    BYTEORDER = '<'

#alpha is always the 4th byte, or most significant
GDL_CHANNELS = "RGBA"
TGA_CHANNELS = "BGRA"

EMPTY_PALETTE = array('B', [])
DEF_ALPA_PAL  = b'\x80'*256


###################
'''xml tag names'''
###################
OBJECTS_PS2_TAG = 'objects_ps2'
OBJ_TAG = 'obj'
TEX_TAG = 'tex'
OBJ_DEF_TAG = 'obj_def'
TEX_DEF_TAG = 'tex_def'

OBJS_TAG = OBJ_TAG+'s'
TEXS_TAG = TEX_TAG+'s'
OBJ_DEFS_TAG = OBJ_DEF_TAG+'s'
TEX_DEFS_TAG = TEX_DEF_TAG+'s'


#set up the filepaths and foldernames that textures, animations,
#models, and definitions will be extracted to and imported from.
ALPHA_PAL_FILENAME = pathdiv+'%s_a_pal.tga'
DEFS_XML_FILENAME  = pathdiv+'defs.xml'
TEXTURE_FILENAME   = pathdiv+'%s.tga'
MIP_FILENAME       = pathdiv+'%s_%s.tga'

DATA_FOLDERNAME = pathdiv+'data'
ANIM_FOLDERNAME = pathdiv+'anim'
MOD_FOLDERNAME  = pathdiv+'mod'
TEX_FOLDERNAME  = pathdiv+'tex'
MIP_ALPHA_FOLDERNAME = pathdiv+'misc'

##############################################################################
'''These are just used for parsing models exported by a maxscript exporter.'''
##############################################################################
g3d_sub_object_struct = Container('g3d sub-object',
    LUInt16("qword count", GUI_NAME="quadword count"),
    LUInt16("tex index",   GUI_NAME="texture index"),
    LUInt16("lm index",    GUI_NAME="light map index"),
    LSInt16("lod k",       GUI_NAME="lod coefficient"),
    
    BytesRaw('data', SIZE=qword_size),
    )

g3d_model_def = BlockDef(
    UInt32('bnd rad'),
    UInt32('vert count'),
    UInt32('tri count'),
                      
    UInt32('g3d sub-object count'),

    Array('g3d sub-objects',
        SIZE='.g3d_sub_object_count',
        SUB_STRUCT=g3d_sub_object_struct
        ),
    NAME="g3d model",
    )

class ObjectsPs2Tag(GdlTag):
    palettes = None
    textures = None
    palette_swizzled = True
    palette_order    = GDL_CHANNELS

    def extract(self, defs=True, mod=False, tex=False,
                anim=False, individual=False, overwrite=False,
                mips=False, alpha_pal=True):
        ''''''
        extract_folder = dirname(self.filepath) + DATA_FOLDERNAME
        mod_folder  = extract_folder + '\\obj mod'
        tex_folder  = extract_folder + TEX_FOLDERNAME
        anim_folder = extract_folder + ANIM_FOLDERNAME
        
        bitmaps = self.data.bitmaps
        textures = self.textures

        if defs:
            self.export_defs(extract_folder, overwrite)

        if tex:
            if self.textures is None or self.palettes is None:
                self.load_textures()
            self.export_textures(tex_folder, overwrite, mips, alpha_pal)
            
        if anim:
            self.export_animations(anim_folder, overwrite)

        if mod:
            self.export_models(mod_folder, individual, overwrite)
                


    def export_defs(self, extract_folder, overwrite=False):
        ''''''
        if exists(extract_folder + DEFS_XML_FILENAME) and not overwrite:
            return
        
        if not exists(extract_folder):
            makedirs(extract_folder)
            
        with open(extract_folder + DEFS_XML_FILENAME, 'w') as df:
            df.write('<?xml version="1.0"?>\n'+
                     '# gauntlet dark legacy model and texture defs\n\n'+
                     '<%s>\n'%OBJECTS_PS2_TAG)

            objects = self.data.objects
            bitmaps = self.data.bitmaps
            object_defs = self.data.object_defs
            bitmap_defs = self.data.bitmap_defs

            idnt = '  '

            #write the model data
            df.write('<%s>\n'%OBJS_TAG)
            for i in range(len(objects)):
                obj = objects[i]
                f = obj.flags
                df.write((idnt+'<%s inv_rad="%s" bnd_rad="%s"># %s\n')%
                                (OBJ_TAG, obj.inv_rad, obj.bnd_rad, i))
                for attr in ('alpha', 'lmap',
                             'sharp', 'blur', 'chrome',
                             'error', 'sort_a', 'sort',
                             'pre_lit', 'lmap_lit', 'norm_lit', 'dyn_lit'):
                    if not f.__getattr__(attr):
                        continue
                    df.write(idnt*2+ '<set_flag name="%s"/>\n' % attr)

                df.write(idnt+'</%s>\n'%OBJ_TAG)
            df.write('</%s>\n'%OBJS_TAG)

            #write the texture data
            df.write('<%s>\n'%TEXS_TAG)
            for i in range(len(bitmaps)):
                b = bitmaps[i]
                f = b.flags
                df.write(idnt + '<%s format="%s"># %s\n' %
                             (TEX_TAG, b.format.data_name, i))
                for attr in ('halfres', 'see_alpha', 'clamp_u', 'clamp_v',
                             'animation', 'external', 'tex_shift',
                             'has_alpha', 'invalid', 'dual_tex'):
                    if not f.__getattr__(attr):
                        continue
                    df.write(idnt*2+ '<set_flag name="%s"/>\n' % attr)

                if not(f.external or f.animation) :
                    df.write(idnt+'</tex>\n')
                    continue
                for attr in ('lod_k', 'mipmap_count', 'width_64',
                             'log2_of_width', 'log2_of_height',
                             'tex_palette_index', 'tex_palette_count',
                             'tex_shift_index', 'frame_count',
                             'width', 'height', 'size', 'tex_0'):
                    df.write(idnt*2+
                                    '<attr name="%s" value="%s"/>\n' %
                                    (attr, b.__getattr__(attr)) )
                df.write(idnt+'</%s>\n'%TEX_TAG)
            df.write('</%s>\n'%TEXS_TAG)

            #write the model definition data
            df.write('<%s>\n'%OBJ_DEFS_TAG)
            for i in range(len(object_defs)):
                od = object_defs[i]
                df.write((idnt+'<%s obj_index="%s" frames="%s" '+
                          'name="%s" /># %s\n') % (OBJ_DEF_TAG,
                          od.obj_index, od.n_frames, od.name, i))
            df.write('</%s>\n'%OBJ_DEFS_TAG)

            #write the texture definition data
            df.write('<%s>\n'%TEX_DEFS_TAG)
            for i in range(len(bitmap_defs)):
                bd = bitmap_defs[i]
                df.write((idnt+'<%s tex_index="%s" width="%s" '+
                          'height="%s" name="%s"/># %s\n') % (TEX_DEF_TAG,
                          bd.tex_index, bd.width, bd.height, bd.name, i))
            df.write('</%s>\n'%TEX_DEFS_TAG)

        df.write('</%s>\n'%OBJECTS_PS2_TAG)
        df.close()


    def export_animations(self, anim_folder=ANIM_FOLDERNAME, overwrite=False):
        ''''''
        pass


    def export_models(self, mod_folder='obj mod',
                      individual=False, overwrite=False):
        ''''''
        obj_num = strip_num = ''
        objects = self.data.objects
        
        if not exists(mod_folder):
            makedirs(mod_folder)
        
        if not individual:
            if exists(mod_folder+'\\mod.obj') and not overwrite:
                return
            obj_file = open(dirname(mod_folder)+'\\mod.obj', 'w')
            obj_file.write('# Gauntlet Dark Legacy 3d model\n'+
                           '#     Written by Moses\n\n')
            start_v = 1

        #make local references to speed up code
        byteorder    = BYTEORDER
        block_sizes  = BLOCK_SIZES
        unpack_chars = UNPACK_CHARS
            
        #loop over each object
        for i in range(len(objects)):
            curr_obj = objects[i]

            #if the object is empty, skip it
            if curr_obj.vert_count == 0:
                continue
            
            if individual:
                if exists(mod_folder+'\\%s.obj'%i) and not overwrite:
                    continue
                obj_file = open(mod_folder+'\\%s.obj'%i, 'w')
                obj_file.write('# Gauntlet Dark Legacy 3d model\n'+
                               '#     Written by Moses\n\n')
                start_v = 1

            tex_index = curr_obj.sub_object_0.tex_index
            
            try:
                #loop over each subobject
                for j in range(len(curr_obj.data.sub_object_models)):
                    subobj = curr_obj.data.sub_object_models[j]
                    stream = subobj.data
                    verts = ""
                    uvs = ""
                    normals = ""
                    unknown = ""

                    uv_scale = 1
                    strip_count = 0

                    faces_drawn = []
                    face_dirs = []

                    #get the length of the stream and set the start to 0
                    stream_len = len(stream)
                    b = 0
                    
                    if j:
                        tex_index = curr_obj.data.sub_objects[j-1].tex_index

                    obj_file.write('\n')
                    obj_file.write('# object %s_%s\n'%(i,j))

                    #scan over all the data in the stream
                    while b < stream_len:
                        #always make sure the stream is 4 byte aligned
                        b += 4 + (4-(b%4))%4
                        
                        sen = stream[b-1]
                        
                        if sen == 108:
                            '''triangle strip'''
                            b += 4
                            continue
                        elif sen == 45:
                            '''face directions and uv scale'''
                            face_dirs.append(unpack('f', stream[b:b+4])[0])
                            uv_scale = unpack('f', stream[b+4:b+8])[0]
                            b += 8
                            continue
                        elif sen == 23 or sen == 20 or sen == 0:
                            '''strip link'''
                            continue

                        #get the info needed to unpack the data
                        size  = block_sizes[sen]
                        char  = unpack_chars[sen]
                        count = stream[b-2]

                        data = array(char, stream[b:b+size*count])
                        if byteorder == ">":
                            #if the system is big endian,
                            #we need to byteswap the data
                            data.byteswap()
                        
                        b += size*count
                        
                        if sen == 106 or (sen == 105 or sen == 104):
                            '''8/16/32 bit vertex coordinates'''
                            #make sure to ignore the last vertex
                            for k in range(0, len(data)-3, 3):
                                verts += 'v %s %s %s\n' % (data[k],
                                                           data[k+1],
                                                           data[k+2])
                            strip_count += 1
                        elif sen == 109:
                            #these are included in lightmaps.
                            #not sure what they are exactly
                            '''16 bit unknown coordinates'''
                            for k in range(0, len(data), 4):
                                unknown += ('#unknown %s %s %s %s\n'%
                                            (data[k],   data[k+1],
                                             data[k+2], data[k+3]))
                        elif sen == 102 or (sen == 101 or sen == 100):
                            '''8/16/32 bit uv coordinates'''
                            for k in range(0, len(data), 2):
                                uvs += 'vt %s %s\n' % (data[k]*uv_scale/128,
                                                       data[k+1]*uv_scale/128)
                        elif sen == 111:
                            '''16 bit compressed vertex normals'''
                            dont_draw = [0]*len(data)
                            
                            for k in range(len(data)):
                                norm = data[k]
                                xn = ((norm&31)-15)/15
                                yn = (((norm>>5)&31)-15)/15
                                zn = (((norm>>10)&31)-15)/15
                                
                                #dont need much precision on these
                                normals += 'vn %s %s %s\n' % (str(xn)[:7],
                                                              str(yn)[:7],
                                                              str(zn)[:7])
                                
                                #the last bit determines if a face is to be
                                #drawn or not. 0 means draw, 1 means dont draw
                                if norm&32768:
                                    dont_draw[k] = 1
                            #make sure the first 2 are removed since they
                            #are always 1 and triangle strips are always
                            #made of 2 more verts than there are triangles
                            faces_drawn.append(dont_draw[2:])
                        else:
                            #dont know what kinda data this is, so skip it
                            print('UNKNOWN DATA STREAM: %s'%sen)
                            print('filepath:%s, object:%s, subobj:%s, loc:%s'%
                                  (self.filepath, i, j, b-(4+size*count)))
                            break
                    
                            
                    #write the verts, uvs, and normals to the obj file
                    obj_file.write(verts+'\n')
                    obj_file.write(uvs+'\n')
                    obj_file.write(normals+'\n')
                    if unknown:
                        obj_file.write(unknown+'\n')
                    
                    obj_file.write('g %s_%s\n'%(i, j))
                    obj_file.write('usemtl %s\n'%tex_index)
                    
                    #generate the faces
                    for k in range(strip_count):
                        dont_draw = faces_drawn[k]
                        if face_dirs[k] == -1.0:
                            face_dir = 0
                        else:
                            face_dir = 1
                        
                        for f in range(len(dont_draw)):
                            #determine if the face is not supposed to be drawn
                            if dont_draw[f]:
                                continue
                            
                            v = start_v + f
                            if (f+face_dir)&1:
                                obj_file.write('f %s/%s/%s %s/%s/%s %s/%s/%s\n'%
                                               (v,v,v,v+1,v+1,v+1,v+2,v+2,v+2))
                            else:
                                #swap the vert order of every other face
                                obj_file.write('f %s/%s/%s %s/%s/%s %s/%s/%s\n'%
                                               (v+1,v+1,v+1,v,v,v,v+2,v+2,v+2))
                        #increment the start vert by the number of verts used
                        start_v += len(dont_draw)+2
            except:
                obj_file.close()
                remove(mod_folder+'\\%s.obj'%i)
                print(format_exc())
            
            if individual:
                obj_file.close()
                
        if not individual:
            obj_file.close()
            

    def export_textures(self, tex_folder=TEX_FOLDERNAME, overwrite=False,
                        mips=False, alpha_pal=True):
        ''''''
        
        if self.palettes is None or self.textures is None:
            return
        
        misc_folder = tex_folder + MIP_ALPHA_FOLDERNAME
        if not exists(misc_folder):
            makedirs(misc_folder)
            
        #unswizzle the palette if it's swizzled
        if self.palette_swizzled:
            self.swizzle_palette()
            
        #swap the color channels around to tga ordering
        if self.palette_order != TGA_CHANNELS:
            self.swap_color_channels()

        #extract the textures
        '''Export alpha channel palettes to their own tga image
        so transparency can be edited for palettized images.'''
        palettes = self.palettes
        textures = self.textures
        bitmaps  = self.data.bitmaps
        
        mipcount = 1
        
        for i in range(len(textures)):
            bitmap   = bitmaps[i]
            palette  = palettes[i]
            mipmaps  = textures[i]
            
            if bitmap.frame_count or bitmap.flags.external or mipmaps is None:
                continue
            
            format_name  = bitmap.format.data_name

            if format_name == "<UNNAMED>":
                print("INVALID FORMAT: index==%s, format==%s, filepath==%s"%
                      (i, bitmap.format.data, self.filepath))
                continue
            

            #create the bytes to go into the header
            if palette:
                has_color_map = b'\x01'
                image_type    = b'\x01'
                color_map_length = int.to_bytes(2**pixel_size, 2, 'little')
                color_map_depth  = int.to_bytes(8*palette_size, 1, 'little')
                bpp = b'\x08'
                image_desc = b'\x20'
            else:
                has_color_map = b'\x00'
                image_type    = b'\x02'
                color_map_length = b'\x00'
                color_map_depth  = b'\x00'
                bpp        = int.to_bytes(pixel_size, 1, 'little')
                image_desc = int.to_bytes(alpha_size+32, 1, 'little')

                palette = EMPTY_PALETTE

            #if extracting all mipmaps, make sure the loop range is all
            if mips:
                mipcount = len(mipmaps)

            #if extracting the alpha palette, do so
            if palette_size and alpha_pal and (overwrite or
                            not exists(misc_folder + ALPHA_PAL_FILENAME%i)):
                with open(misc_folder + ALPHA_PAL_FILENAME%i, 'w+b') as pf:
                    #write the palette header with WxH as 16x16
                    pf.write(b'\x00\x00\x03'+b'\x00'*9+
                             b'\x10\x00\x10\x00\x08\x20')

                    #write the alpha data to the file
                    if alpha_size == 1:
                        #adding 127 makes sure all the bit are 1
                        #except the last one, and dividing by 129
                        #makes sure the value is either 0 or 255.
                        pf.write(array('B',[((palette[j]&32768)+127)//129
                                            for j in range(2**pixel_size)]))
                    else:
                        pf.write(array('B',[palette[j]>>24
                                            for j in range(2**pixel_size)]))

                    #because we are using 8bpp indexing, we need to
                    #pad the rest of the 240 pixels with solid white
                    #for bitmaps with only 16 palette colors.
                    if pixel_size == 4:
                        pf.write(b'\xFF'*15*16)

            width  = bitmap.width
            height = bitmap.height

            for mip in range(mipcount):
                if mip == 0:
                    tgapath = tex_folder + TEXTURE_FILENAME%i
                else:
                    tgapath = misc_folder + MIP_FILENAME %(i,mip)
                    
                if not overwrite and exists(tgapath):
                    continue

                with open(tgapath,'w+b') as tga_file:
                    #set whether or not the image has a color map
                    tga_file.write(b'\x00' + has_color_map + image_type +
                                   b'\x00'*2 + color_map_length +
                                   color_map_depth + b'\x00'*4 +
                                   int.to_bytes(width, 2, 'little') +
                                   int.to_bytes(height, 2, 'little') +
                                   bpp + image_desc)

                    tga_file.write(palette)
                    if pixel_size == 4:
                        pix = mipmaps[mip]
                        '''This looks complicated, but all it does is
                        create a list as long as the number of pixels,
                        then goes through all the pixel indexings.
                        If the index is even, the lower 4 bits are
                        masked off, if the index is odd, the upper 4
                        bits are shifted down by 4. This basically
                        splits the pixels in half and stores one to
                        each index, instead of two in one.
                        Photoshop cant handle 4-bit color indexing.'''
                        tga_file.write(array('B',[pix[j//2]>>4*(j%2)&15
                                             for j in range(width*height)]))
                    else:
                        tga_file.write(mipmaps[mip])

                width  = (width+1)//2
                height = (height+1)//2


    def import_data(self, data_folder=None, update_only=False,
                    xml=True, mod=True, tex=True, anim=True):
        '''Imports data from the data_folder into this objects tag
        and the neighboring animations tag and textures blob.'''
        
        if data_folder is None:
            data_folder = dirname(self.filepath) + DATA_FOLDERNAME
        
        if not exists(data_folder):
            raise IOError(("data_folder '%s' does not exist. "+
                           "Cannot import data.")% data_folder)
        xml_path  = data_folder + DEFS_XML_FILENAME
        tex_path  = data_folder + TEX_FOLDERNAME
        mod_path  = data_folder + MOD_FOLDERNAME
        anim_path = data_folder + ANIM_FOLDERNAME

        if exists(xml_path) and xml:
            self.import_xml(xml_path)

        if exists(mod_path) and mod:
            self.import_mod(mod_path)

        if exists(tex_path) and tex:
            if self.textures is None or self.palettes is None:
                self.load_textures()
            self.import_tex(tex_path)

        if exists(anim_path) and anim:
            self.import_anim(anim_path)


    def import_anim(self, anim_path):
        ''''''
        pass


    def import_mod(self, mod_path):
        ''''''
        objects = self.data.objects
        object_defs = self.data.object_defs

        bitmap_count = len(self.data.bitmaps)
        
        #holds all the model filepaths indexed by their object index
        mod_filepaths = {}

        mod_filepath = mod_path+'\\%s.g3d'

        #try to locate all models by the def name of the model
        for obj_def in object_defs:
            filepath = mod_filepath % obj_def.name
            if exists(filepath):
                mod_filepaths[obj_def.obj_index] = filepath

        #try to locate all models by the index of the model
        for i in range(len(objects)):
            filepath = mod_filepath % i
            if exists(filepath):
                mod_filepaths[i] = filepath

        #load each model one by one
        for i in mod_filepaths:
            obj = objects[i]

            try:
                #load the object data
                with open(mod_filepaths[i], 'rb') as f:
                    g3d_model = g3d_model_def.build(rawdata=f.read())
            except Exception:
                print("Could not load object model %s"%i)
                continue

            #update the vert/tri counts and the bounding radius
            obj.bnd_rad    = g3d_model.bnd_rad
            obj.tri_count  = g3d_model.tri_count
            obj.vert_count = g3d_model.vert_count

            #update the bounding radius in the object_def as well
            object_defs[i].bnd_rad = obj.bnd_rad

            subobjs = obj.data.sub_objects
            subobj_models = obj.data.sub_object_models
            g3d_subobjs = g3d_model.g3d_sub_objects

            #clear and repopulate the subobjects the subobject models arrays
            del subobjs[:]
            del subobj_models[:]
            subobjs.extend(len(g3d_subobjs)-1)
            subobj_models.extend(len(g3d_subobjs))

            #loop over all the subobjects and update the headers and models
            for j in range(len(subobj_models)):
                if j == 0:
                    subobj = obj.sub_object_0
                else:
                    subobj = subobjs[j-1]
                    
                subobj_model = subobj_model[j]
                g3d_subobj   = g3d_subobjs[j]

                #update the header
                subobj.qword_count = g3d_subobj.qword_count + 1
                subobj.tex_index   = g3d_subobj.tex_index
                subobj.lm_index    = g3d_subobj.lm_index
                subobj.lod_k       = g3d_subobj.lod_k

                if subobj.tex_index > bitmap_count:
                    print(('subobject %s in object %s uses texture number %s'+
                           ' which does not exist.')%(j,i,subobj.tex_index))

                #update the model data
                subobj_model.qword_count = g3d_subobj.qword_count
                subobj_model.data        = g3d_subobj.data

            #little bit of cleanup
            del g3d_model


    def import_tex(self, tex_path):
        ''''''
        bitmaps = self.data.bitmaps
        bitmap_defs = self.data.bitmap_defs

        palettes = self.palettes
        textures = self.textures

        #populate the palettes and textures with empty slots
        palettes.extend([None]*(len(bitmaps)-len(palettes)))
        textures.extend([[b''] for i in range(len(bitmaps)-len(textures))])
        
        #holds lists of the texture filepaths and their
        #mipmaps indexed by the tex index of the bitmap
        tex_filepaths = {}
        a_pal_filepaths = {}
        
        tex_filepath = tex_path + TEXTURE_FILENAME
        mip_filepath = tex_path + MIP_ALPHA_FOLDERNAME + MIP_FILENAME
        alpha_filepath = tex_path + MIP_ALPHA_FOLDERNAME + ALPHA_PAL_FILENAME

        '''try to locate all textures, mips, and alpha
        palettes by the def name of the texture'''
        for tex_def in bitmap_defs:
            filepath = tex_filepath % tex_def.name
            if exists(filepath):
                mip = 0
                tex_name = tex_def.name
                tex_index = tex_def.tex_index
                
                flags = bitmaps[tex_index].flags
                if flags.external or flags.animation:
                    continue
                
                tex_filepaths[tex_index] = tex_paths = [filepath]
                
                #if the alpha palette exists, index it
                if exists(alpha_filepath % tex_name):
                    a_pal_filepaths[tex_index] = alpha_filepath % tex_name
                else:
                    a_pal_filepaths[tex_index] = None

                #locate all mipmaps of this texture
                while exists(mip_filepath % (tex_name, mip)):
                    tex_paths.append(mip_filepath % (tex_name, mip))
                    mip += 1

        '''try to locate all textures, mips, and alpha
        palettes by the index of the texture'''
        for i in range(len(bitmaps)):
            filepath = tex_filepath % i
            if exists(filepath):
                mip = 0
                
                flags = bitmaps[i].flags
                if flags.external or flags.animation:
                    continue
                
                tex_filepaths[i] = tex_paths = [filepath]

                #if the alpha palette exists, index it
                if exists(alpha_filepath % i):
                    a_pal_filepaths[i] = alpha_filepath % i
                else:
                    a_pal_filepaths[i] = None

                #locate all mipmaps of this texture
                while exists(mip_filepath % (i, mip)):
                    tex_paths.append(mip_filepath % (i, mip))
                    mip += 1

        '''load each texture one by one'''
        for i in tex_filepaths:
            bitmap = bitmaps[i]

            format_name  = bitmap.format.data_name
            
            palette_size = PALETTE_SIZES.get(format_name, 0)
            pixel_size   = PIXEL_SIZES.get(format_name, 0)
            pal_pack_char = PALETTE_PACK_CHARS.get(format_name, 'B')
            pix_pack_char = PIXEL_PACK_CHARS.get(format_name, 'B')

            mipmap_count = 0

            '''try to get the alpha palette if the bitmap is palettized'''
            if palette_size:
                try:
                    with open(a_pal_filepaths[i], 'rb') as f:
                        alpha_data = f.read()
                        
                    width  = unpack('<H', alpha_data[12:14])[0]
                    height = unpack('<H', alpha_data[14:16])[0]

                    px_start = alpha_data[0]+18
                    px_end   = px_start+2**pixel_size

                    if alpha_data[1]:
                        raise TypeError('Cannot use palettized images '+
                                        'for the alpha palette.')
                    if alpha_data[2]&8:
                        raise TypeError('Cannot use rle tga images.')
                    if alpha_data[2]&3 != 3:
                        raise TypeError('Alpha palette textures must '+
                                        'be saved in greyscale format.')
                    if width*height != 256:
                        raise TypeError('Alpha palette textures must '+
                                        'be 256 pixels(usually 16x16).')

                    #if the image origin doesnt start in the upper left
                    #corner, we need to reassemble the image upside down
                    a_palette = alpha_data[px_start:px_end]
                    if not alpha_data[17]&32:
                        alpha_data, a_palette = a_palette, b''
                        for x in range((height-1)*width, -1, -1*width):
                            a_palette += alpha_data[x:x+width]
                except IOError:
                    #file doesnt exist or cant be opened.
                    a_palette = DEF_ALPA_PAL
                except Exception:
                    print(format_exc())
                    continue


            '''read in the main texture data'''
            try:
                with open(tex_filepaths[i][0], 'rb') as f:
                    tga_data = f.read()

                cm_length = unpack('<H', tga_data[5:7])[0]
                cm_depth  = tga_data[7]

                width  = unpack('<H', tga_data[12:14])[0]
                height = unpack('<H', tga_data[14:16])[0]
                bpp    = tga_data[17]

                #treat 15bit as 16bit
                if cm_depth == 15: cm_depth = 16
                if bpp == 15:      bpp = 16

                pal_start = tga_data[0]+18
                pal_end   = pal_start + cm_length*cm_depth//8
                pix_end   = width*height*bpp//8

                if tga_data[2]&8:
                    raise TypeError('Cannot use rle tga images for mipmaps.')
                if width not in VALID_DIMS or height not in VALID_DIMS:
                    raise TypeError('Mipmap width and height must '+
                                    'both be a power of 2.')

                #read the pixels
                pixels = tga_data[pal_end:pix_end]

                #if the image origin doesnt start in the upper left
                #corner, we need to reassemble the image upside down
                if not tga_data[17]&32:
                    pix_data, pixels = pixels, b''
                    stride = width*bpp//8
                    for x in range((height-1)*stride,-1,-1*stride):
                        pixels += pix_data[x:x+stride]

                '''figure out how to handle the palette'''
                if tga_data[1]:                    
                    if not palette_size:
                        raise TypeError('Tga image is palettized, but '+
                                        'the tag says it should not be.')
                    if palette_size == 32 and cm_depth not in (24,32):
                        raise TypeError('Tga image is not the bit depth'+
                                        'that the tag says it should be.')

                    #keep a copy of the original palette for making
                    #sure that all the mips use the same palette
                    base_palette = tga_data[pal_start:pal_end]

                    #start off with an empty palette so we can
                    #make sure the palette contains 256 colors
                    palette = array(pal_pack_char, b'\x00'*256*palette_size)

                    #merge the alpha palette into the palette
                    if palette_size == 16:
                        '''since photoshop doesnt let you save palettes
                        as 16bit, we will convert 24 and 32bit palettes
                        to 16bit if the tag says it should be 16bit'''
                        if cm_depth == 16:
                            for j in range(len(palette)):
                                palette[j] = (base_palette[j*2]+
                                              ((base_palette[j*2+1]&127)<<8)+
                                               32768*bool(a_palette[j>>1]))
                        elif cm_depth == 24:
                            for j in range(len(palette)):
                                palette[j] = ( (base_palette[j*3]>>3)+
                                              ((base_palette[j*3+1]>>3)<<5)+
                                              ((base_palette[j*3+2]>>3)<<10)+
                                               32768*bool(a_palette[j>>1]))
                        elif cm_depth == 32:
                            for j in range(len(palette)):
                                palette[j] = ( (base_palette[j*4]>>3)+
                                              ((base_palette[j*4+1]>>3)<<5)+
                                              ((base_palette[j*4+2]>>3)<<10)+
                                               32768*bool(a_palette[j>>1]))
                    elif cm_depth == 24:
                        for j in range(len(palette)):
                            palette[j] = (base_palette[j*3]+
                                          (base_palette[j*3+1]<<8)+
                                          (base_palette[j*3+2]<<16)+
                                          (a_palette[j]<<24))
                    elif cm_depth == 32:
                        for j in range(len(palette)):
                            palette[j] = (base_palette[j*4]+
                                          (base_palette[j*4+1]<<8)+
                                          (base_palette[j*4+2]<<16)+
                                          (a_palette[j]<<24))
                    else:
                        raise TypeError('Invalid color map depth.')

                    '''if the pixel size is 4, need to see if we can
                    compress the palette down to 16 colors or less'''
                    if pixel_size == 4:
                        #make a list of each of the unique indexing values
                        idx_map = list(set(pixels))
                        idx_256_to_16 = [0]*256

                        if len(idx_map) > 16:
                            raise TypeError('Tga palette uses more than '+
                                            '16 colors, but the tag says '+
                                            'that it should be <= 16.')

                        #make a new palette of 16 colors
                        new_pal = array(palette.typecode,
                                        b'\x00'*16*palette_size)
                        new_pix = bytearray(pixels)

                        #make the new palette so it that
                        #contains the 16(or less) used colors
                        for j in range(len(idx_map)):
                            new_pal[j] = palette[idx_map[j]]

                        #Make a 256 entry list to map the current indexing
                        #value to which of the 16 possible palette choices
                        for j in range(len(idx_map)):
                            idx_256_to_16[idx_map[j]] = j

                        #iterate over the pixels and build a new pixel array
                        #by mapping the old palette indexes to the new ones
                        for j in range(len(pixels)//2):
                            new_pix[j] = (idx_256_to_16[pixels[j*2]]+
                                          (idx_256_to_16[pixels[j*2+1]]<<4))

                        #rename the new palette and pixels
                        palette = new_pal
                        pixels  = new_pix

                    #store the imported palette to the palettes list
                    palettes[i] = palette

                elif palette_size:
                    raise TypeError('Tga image is not palettized, '+
                                    'but the tag says it should be.')
                elif pixel_size == 32 and bpp == 24:
                    #convert the pixels from BGR to BGRA
                    pixels = array('I', [pixels[i]+
                                        (pixels[i+1]<<8)+
                                        (pixels[i+2]<<16)
                                    for i in range(0,len(pixels),3)])
                elif pixel_size != bpp:
                    raise TypeError('Tga image is not the bit depth'+
                                    'that the tag says it should be.')
                else:
                    #convert the pixels into an array of the right typecode
                    pixels = array(pix_pack_char, pixels)

                #store the imported pixels to the pixels list
                textures[i][0] = pixels
            except Exception:
                print(format_exc())
                continue

            '''update the texture information in the bitmap block'''
            bitmap.width  = width
            bitmap.height = height
            bitmap.width_64 = (width+63)//64
            bitmap.log2_of_width  = int(log(width,  2))
            bitmap.log2_of_height = int(log(height, 2))

            '''loop over all the mips and get their textures'''
            try:
                for mip in range(1, len(tex_filepaths[i])):
                    width  = width//2
                    height = height//2
                    
                    #dont want any mips smaller than 8x8
                    if width < 8 or height < 8: break

                    with open(tex_filepaths[i][mip], 'rb') as f:
                        mip_data = f.read()

                    cm_length = unpack('<H', mip_data[5:7])[0]
                    cm_depth = mip_data[7]
                    bpp = mip_data[17]

                    #treat 15bit as 16bit
                    if cm_depth == 15: cm_depth = 16
                    if bpp == 15:      bpp = 16

                    pal_start = mip_data[0]+18
                    pal_end = pal_start + cm_length*cm_depth//8
                    pix_end = width*height*bpp//8

                    if width != unpack('<H', mip_data[12:14])[0]:
                        raise TypeError('Mip width is not what it should be')
                    if height != unpack('<H', mip_data[14:16])[0]:
                        raise TypeError('Mip height is not what it should be')
                    
                    #read the pixels
                    pixels = mip_data[pal_end:pix_end]

                    #if the image origin doesnt start in the upper left
                    #corner, we need to reassemble the image upside down
                    if not mip_data[17]&32:
                        stride = width*bpp//8
                        pix_data, pixels = pixels, b''
                        for x in range((height-1)*stride,-1,-1*stride):
                            pixels += pix_data[x:x+stride]

                    '''figure out how to handle the palette'''
                    if mip_data[1]:
                        if not palette_size:
                            raise TypeError('Mipmap image is palettized, but '+
                                            'the tag says it should not be.')
                        if base_palette != mip_data[pal_start:pal_end]:
                            raise TypeError('Mipmap palette does not match '+
                                            'the palette of the base image.')
                    elif palette_size:
                        raise TypeError('Mipmap image is not palettized, '+
                                        'but the tag says it should be.')
                    elif pixel_size == 32 and bpp == 24:
                        #convert the pixels from BGR to BGRA
                        pixels = array('I', [pixels[i]+
                                            (pixels[i+1]<<8)+
                                            (pixels[i+2]<<16)
                                        for i in range(0,len(pixels),3)])
                    elif pixel_size != bpp:
                        raise TypeError('Mipmap image is not the bit depth'+
                                        'that the tag says it should be.')

                    #convert the pixels into an array of the right typecode
                    pixels = array(pix_pack_char, mip_data[pal_end:pix_end])

                    #if the pixel size is 4, we need to rebuild the indexing
                    if pixel_size == 4:
                        if len(list(set(pixels))) > 16:
                            raise TypeError('Mipmap palette uses more than '+
                                            '16 colors, but the tag says '+
                                            'that it should be <= 16.')

                        '''iterate over the pixels and build a new pixel array
                        by mapping the old palette indexes to the new ones'''
                        for j in range(len(pixels)//2):
                            new_pix[j] = (idx_256_to_16[pixels[j*2]]+
                                          (idx_256_to_16[pixels[j*2+1]]<<4))
                        pixels = new_pix

                    #add the mipmap pixels to the textures array
                    textures[i].append(pixels)

                    mipmap_count += 1
            except Exception:
                print(format_exc())

            bitmap.mipmap_count = mipmap_count

        #now that all the textures are imported, we need to swap the
        #red and blue channels and swizzle the palette of the imported
        self.swizzle_palette(tex_filepaths.keys())
        self.swap_color_channels(tex_filepaths.keys())

        #FINALLY DONE. GAWD


    def import_xml(self, xml_path):
        ''''''
        objects = self.data.objects
        bitmaps = self.data.bitmaps
        object_defs = self.data.object_defs
        bitmap_defs = self.data.bitmap_defs
        
        with open(xml_path, 'rb') as f:
            xml_data = f.read()


    def swap_color_channels(self, indexes=None):
        '''Swaps the order of the color channels in
        the palettes and the unpalettized textures.
        All that's swapped is the red and blue channels'''
        palettes = self.palettes
        textures = self.textures
        bitmaps = self.data.bitmaps
        
        if palettes is None or textures is None:
            return
            
        if indexes is None:
            #change the ordering identifier string
            if self.palette_order == TGA_CHANNELS:
                self.palette_order = GDL_CHANNELS
            else:
                self.palette_order = TGA_CHANNELS
            indexes = range(min(len(textures), len(palettes)))
        elif isinstance(indexes, int):
            indexes = (indexes,)

        #loop over all the indexes specified
        for i in indexes:
            bitmap = bitmaps[i]
            if bitmap.frame_count or bitmap.flags.external:
                continue
            
            format_name  = bitmap.format.data_name
            palette_size = PALETTE_SIZES.get(format_name, 0)

            #determine if its the palette or pixels that should be modified
            if palette_size:
                pal = palettes[i]
                if pal is None:
                    continue
                if palette_size == 2:
                    #palette colors are 16 bit R5G5B5A1
                    for i in range(len(pal)):
                        col = pal[i]
                        pal[i] = (col&33760)+(((col>>10)+(col<<10))&31775)
                else:
                    #palette colors are 32 bit R8G8B8A8
                    for i in range(len(pal)):
                        col = pal[i]
                        pal[i] = (col&0xFF00FF00)+(((col>>16)+
                                                    (col<<16))&0xFF00FF)
            else:
                texs = textures[i]
                if texs is None:
                    continue
                pixel_size = PIXEL_SIZES.get(format_name, 0)
                if pixel_size == 16:
                    #pixels are 16 bit R5G5B5A1
                    for tex in texs:
                        for i in range(len(tex)):
                            pix = tex[i]
                            tex[i] = (pix&33760)+(((pix>>10)+(pix<<10))&31775)
                else:
                    #pixels are 32 bit R8G8B8A8
                    for tex in texs:
                        for i in range(len(tex)):
                            pix = tex[i]
                            tex[i] = (pix&0xFF00FF00)+(((pix>>16)+
                                                        (pix<<16))&0xFF00FF)
                

    
    def swizzle_palette(self, indexes=None):
        '''Except for the first and last set of 8 colors
        in the palette, the palette has every other set
        of 8 colors swapped with the next set of 8 colors.
        This function swaps the specified palette.
        If index is None, all palettes are swapped.'''

        palettes = self.palettes
        
        if palettes is None:
            return
        
        #invert the swizzle setting
        if indexes is None:
            self.palette_swizzled = not self.palette_swizzled
            indexes = range(len(palettes))
        elif isinstance(indexes, int):
            indexes = (indexes,)
            
        for i in indexes:
            palette = palettes[i]
            if palette is None:
                continue
            #this function won't run if the palette isn't large enough
            for j in range(8, (len(palette)-8)):
                #for this to work, the pixels must each take up
                #one index and there must be 4 channels per pixel
                if (j-8)%32 < 8:
                    palette[j], palette[j+8] = palette[j+8], palette[j]
    
    
    def load_textures(self, **kwargs):
        ''''''
        bitmaps = self.data.bitmaps
        byteorder = BYTEORDER

        textures_filepath = self.textures_filepath
        textures = self.textures = [None]*len(bitmaps)
        palettes = self.palettes = [None]*len(bitmaps)
        try:
            with open(textures_filepath, 'r+b') as f:
                rawdata = mmap(f.fileno(), 0)
        except Exception:
            self.palettes = self.textures = None
            return
        
        for i in range(len(bitmaps)):
            textures[i] = []
            bitmap = bitmaps[i]
            if bitmap.frame_count or bitmap.flags.external:
                continue
            
            format_name = bitmap.format.data_name
            
            tex_pointer = bitmap.tex_pointer
            mipmaps     = bitmap.mipmap_count
            
            palette_size = PALETTE_SIZES.get(format_name, 0)
            pixel_size   = PIXEL_SIZES.get(format_name, 0)
            
            width  = bitmap.width
            height = bitmap.height

            #go to the start of the palette/pixel data
            rawdata.seek(tex_pointer)

            if palette_size:
                palettes[i] = array(PALETTE_PACK_CHARS.get(format_name,'B'),
                                    rawdata.read((2**pixel_size)*palette_size))
                #if the system is big endian we need to byteswap the data
                if byteorder == ">": palettes[i].byteswap()
            for mip in range(mipmaps+1):
                textures[i].append(array(PIXEL_PACK_CHARS.get(format_name,'B'),
                                    rawdata.read((width*height*pixel_size)//8)))
                width  = (width+1)//2
                height = (height+1)//2
                #if the system is big endian we need to byteswap the data
                if byteorder == ">": textures[i].byteswap()


    @property
    def textures_filepath(self):
        ''''''
        return dirname(self.filepath) + '\\textures.ps2'


    def write(self, **kwargs):
        ''''''
        filepath = self.textures_filepath
        textures = self.textures
        palettes = self.palettes
        bitmaps  = self.data.bitmaps

        if palettes and textures:
            curr_pointer = 0

            assert (len(bitmaps) == len(palettes) and
                    len(bitmaps) == len(textures))
            
            #set the pointers for the texture data
            for i in range(len(bitmaps)):
                if bitmaps[i].frame_count or bitmaps[i].flags.external:
                    continue
                
                #set the tex_pointer to the current pointer location
                bitmaps[i].tex_pointer = curr_pointer
                
                palette = palettes[i]
                if palette:
                    if isinstance(palette, (bytes, bytearray)):
                        curr_pointer += len(palette)
                    elif isinstance(palette, array):
                        curr_pointer += len(palette)*palette.itemsize

                for rawdata in textures[i]:
                    if isinstance(rawdata, (bytes, bytearray)):
                        curr_pointer += len(rawdata)
                    elif isinstance(rawdata, array):
                        curr_pointer += len(rawdata)*rawdata.itemsize

                '''since i dont know what the alignment requirements are on
                the texture data, i'm gonna assume everything needs to be
                4-byte aligned, since that will take care of all cases.'''
                curr_pointer += 4-(curr_pointer%4)

        #write the tag data to its file
        return_val = GdlTag.write(self, **kwargs)

        if palettes and textures:
            temppath   = filepath + ".temp"
            backuppath = filepath + ".backup"
            
            #swizzle the palette if it isnt
            if not self.palette_swizzled:
                self.swizzle_palette()
                
            #swap the color channels around to gdl ordering
            if self.palette_order != GDL_CHANNELS:
                self.swap_color_channels()

            #open the textures.ps2 file and write the texture data into it
            with open(temppath, 'w+b') as f:
                palette = palettes[i]
                for i in range(len(bitmaps)):
                    if bitmaps[i].frame_count or bitmaps[i].flags.external:
                        continue
                    
                    f.seek(bitmaps[i].tex_pointer)
                    
                    if palettes[i]:
                        f.write(palettes[i])
                    
                    for rawdata in textures[i]:
                        f.write(rawdata)
                        
            if not bool(kwargs.get('temp',True)):
                self.rename_backup_and_temp(self, filepath,
                                            backuppath, temppath,
                                            bool(kwargs.get('backup',True)))
        return return_val
