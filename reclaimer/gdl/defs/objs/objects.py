from array import array
from math import sqrt
from mmap import mmap
from struct import unpack
from sys import byteorder as BYTEORDER
from traceback import format_exc

from .tag import *

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


if BYTEORDER == 'little':
    BYTEORDER = '<'
else:
    BYTEORDER = '>'

#alpha is always the 4th byte, or most significant
GDL_CHANNELS = "RGBA"
TGA_CHANNELS = "BGRA"


EMPTY_PALETTE = array('B', [])

class ObjectsPs2Tag(GdlTag):
    palettes = None
    textures = None
    palette_swizzled = True
    palette_order    = GDL_CHANNELS

    def extract(self, defs=True, mod=False, tex=False,
                anim=False, individual=False, overwrite=False,
                mips=False, alpha_pal=True):
        ''''''
        extract_folder = dirname(self.filepath)+'\\data'
        mod_folder  = extract_folder+'\\mod'
        tex_folder  = extract_folder+'\\tex'
        anim_folder = extract_folder+'\\anim'
        
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
        if exists(extract_folder+'\\defs.xml') and not overwrite:
            return
        
        if not exists(extract_folder):
            makedirs(extract_folder)
            
        with open(extract_folder+'\\defs.xml', 'w') as df:
            df.write('<?xml version="1.0"?>\n')
            df.write('# gauntlet dark legacy model and texture defs\n\n')

            objects = self.data.objects
            bitmaps = self.data.bitmaps
            object_defs = self.data.object_defs
            bitmap_defs = self.data.bitmap_defs
            
            idnt = '  '

            #write the model data
            df.write('<objs>\n')
            for i in range(len(objects)):
                obj = objects[i]
                f = obj.flags
                df.write((idnt+'<obj inv_rad="%s" bnd_rad="%s"># %s\n')%
                                (obj.inv_rad, obj.bnd_rad, i))
                for attr in ('alpha', 'sharp', 'blur', 'chrome', 'lmap',
                             'sort_a', 'sort', 'fmt_mask', 'pre_lit',
                             'lit_mask', 'lmap_lit', 'norm_lit', 'dyn_lit'):
                    if not f.__getattr__(attr):
                        continue
                    df.write(idnt*2+ '<set_flag name="%s"/>\n' % attr)
                
                df.write(idnt+'</obj>\n')
            df.write('</objs>\n')
            
            #write the texture data
            df.write('<texs>\n')
            for i in range(len(bitmaps)):
                b = bitmaps[i]
                f = b.flags
                df.write(idnt + '<tex format="%s"># %s\n' %
                             (b.format.data_name, i))
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
                df.write(idnt+'</tex>\n')
            df.write('</texs>\n')

            #write the model definition data
            df.write('<obj_defs>\n')
            for i in range(len(object_defs)):
                od = object_defs[i]
                df.write((idnt+'<obj_def obj_index="%s" frames="%s" '+
                              'bnd_rad="%s" name="%s" /># %s\n')%
                             (od.obj_index, od.n_frames, od.bnd_rad, od.name,i))
            df.write('</obj_defs>\n')

            #write the texture definition data
            df.write('<tex_defs>\n')
            for i in range(len(bitmap_defs)):
                bd = bitmap_defs[i]
                df.write((idnt+'<tex_def tex_index="%s" width="%s" '+
                                 'height="%s" name="%s"/># %s\n')%
                             ( bd.tex_index, bd.width, bd.height, bd.name, i))
            df.write('</tex_defs>\n')
        df.close()


    def export_animations(self, anim_folder='anim', overwrite=False):
        ''''''
        pass


    def export_models(self, mod_folder='mod',
                      individual=False, overwrite=False):
        ''''''
        obj_num = strip_num = ''
        objects = self.data.objects
        
        if not exists(mod_folder):
            makedirs(mod_folder)
        
        if not individual:
            if exists(dirname(mod_folder)+'\\mod.obj') and not overwrite:
                return
            obj_file = open(dirname(mod_folder)+'\\mod.obj', 'w')
            obj_file.write('# Gauntlet Dark Legacy 3d model\n'+
                           '#     Written by Moses\n\n')
            start_v = 1

        #make local references to speed up code
        byteorder = BYTEORDER
        block_sizes  = BLOCK_SIZES
        unpack_chars = UNPACK_CHARS
        total_offset = 0
            
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

            b = 0
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

                    stream_len = len(stream)
                    
                    if j:
                        tex_index = curr_obj.data.sub_objects[j-1].tex_index

                    obj_file.write('\n')
                    obj_file.write('# object %s_%s\n'%(i,j))

                    #scan over all the data in the stream
                    while b < stream_len:
                        #always make sure the stream is 4 byte aligned
                        b += (4-(b%4))%4
                        
                        sen = stream[b+3]
                        
                        if sen == 108:
                            '''triangle strip'''
                            face_dirs.append(unpack('f', stream[b+12:b+16])[0])
                            uv_scale = unpack('f', stream[b+16:b+20])[0]
                            b += 20
                            continue
                        
                        if sen == 23 or sen == 20 or sen == 0:
                            '''strip link'''
                            b += 4
                            continue

                        #get the info needed to unpack the data
                        size  = block_sizes[sen]
                        char  = unpack_chars[sen]
                        count = stream[b+2]

                        data = array(char, stream[b+4:b+4+size*count])
                        if byteorder == ">":
                            #if the system is big endian,
                            #we need to byteswap the data
                            data.byteswap()
                        
                        b += 4+size*count
                        
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
                            print(('filepath:%s, object:%s, subobject:%s, '+
                                   'loc:%s, absloc:%s' )%
                                  (self.filepath, i, j,
                                   b-4-size*count, total_offset))
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
                        
                total_offset += b
            except:
                obj_file.close()
                remove(mod_folder+'\\%s.obj'%i)
                print(format_exc())
            
            if individual:
                obj_file.close()
                
        if not individual:
            obj_file.close()


    def export_textures(self, tex_folder='tex', overwrite=False,
                        mips=False, alpha_pal=True):
        ''''''
        '''main texture named as  "##.tga"
           palettes named as      "misc\##_a_pal.tga"
           mipmaps named as       "misc\##_XX.tga"
        '''
        
        if self.palettes is None or self.textures is None:
            return
        
        misc_folder = tex_folder + '\\misc'
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
        so transparency can be edited for palettized images.
        Make them 1 pixel tall and 16/256 pixels wide'''
        palettes = self.palettes
        textures = self.textures
        bitmaps = self.data.bitmaps
        
        mipcount = 1
        
        for i in range(len(textures)):
            bitmap   = bitmaps[i]
            palette  = palettes[i]
            mipmaps  = textures[i]
            
            if bitmap.frame_count or bitmap.flags.external or mipmaps is None:
                continue
            
            format_name  = bitmap.format.data_name
            
            palette_size = PALETTE_SIZES.get(format_name, 0)
            pixel_size   = PIXEL_SIZES.get(format_name, 0)
            alpha_size   = ALPHA_SIZES[format_name]

            #create the bytes to go into the header
            if palette:
                has_color_map = b'\x01'
                image_type    = b'\x01'
                color_map_length = int.to_bytes(2**pixel_size, 2, 'little')
                color_map_depth = int.to_bytes(8*palette_size, 1, 'little')
                bpp = b'\x08'
                image_desc = b'\x20'
            else:
                has_color_map = b'\x00'
                image_type    = b'\x02'
                color_map_length = b'\x00'
                color_map_depth = b'\x00'
                bpp        = int.to_bytes(pixel_size, 1, 'little')
                image_desc = int.to_bytes(alpha_size+32, 1, 'little')

                palette = EMPTY_PALETTE

            #if extracting all mipmaps, make sure the loop range is all
            if mips:
                mipcount = len(mipmaps)
                
            #if extracting the alpha palette, do so
            if palette_size and alpha_pal and (overwrite or
                            not exists(misc_folder+'\\%s_a_pal.tga'%i)):
                with open(misc_folder+'\\%s_a_pal.tga'%i, 'w+b') as pf:
                    pf.write(b'\x00\x00\x03'+b'\x00'*9)

                    #write the palette header with either WxH as 16x1 or 16x16
                    if pixel_size == 4:
                        pf.write(b'\x10\x00\x01\x00\x08\x20')
                    else:
                        pf.write(b'\x10\x00\x10\x00\x08\x20')

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
                
            width  = bitmap.width
            height = bitmap.height
            
            for mip in range(mipcount):
                if mip == 0:
                    tgapath = tex_folder+'\\%s.tga'%i
                else:
                    tgapath = misc_folder+'\\%s_%s.tga'%(i,mip)
                    
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
                tex = textures[i]
                if tex is None:
                    continue
                pixel_size = PIXEL_SIZES.get(format_name, 0)
                if pixel_size == 16:
                    #pixels are 16 bit R5G5B5A1
                    for i in range(len(tex)):
                        pix = tex[i]
                        tex[i] = (pix&33760)+(((pix>>10)+(pix<<10))&31775)
                else:
                    #pixels are 32 bit R8G8B8A8
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
