from math import sqrt
from struct import pack
from traceback import format_exc

from supyr_struct.buffer import BytearrayBuffer
from .stripify import Stripifier

STRIP_START = b'\x00\x00\x00\x14'
STRIP_LINK  = b'\x00\x00\x00\x17'
MAX_STRIP_LEN = 255 - 1#UInt8_Max - (final null vert)
DEFAULT_TEX = 0
DEFAULT_LOD_K = -90
DEFAULT_LM_INDEX = 0


class G3dCompiler():

    def __init__(self, *args, **kwargs):        
        self.stripifier = Stripifier()
        self.stripifier.max_strip_len = MAX_STRIP_LEN
        self.stripifier.degen_link = False

        #set up the instance variables
        self.import_obj()        


    def import_obj(self, filepath=None):
        ''''''
        #Stores the unorganized verts, norms, and uvs
        self.verts = verts = []
        self.norms = norms = []
        self.uvs   = uvs = []

        '''Stores triangles for the first,(possibly untextured), mesh'''
        tris = []

        #default tex_index to use if one isnt given
        tex_index = DEFAULT_TEX

        '''Stores tri counts for each subobject separated by tex_index.'''
        self.lm_indexes = lm_indexes = {DEFAULT_TEX:DEFAULT_LM_INDEX}
        self.lod_ks     = lod_ks     = {DEFAULT_TEX:DEFAULT_LOD_K}
        self.all_tris   = all_tris   = {DEFAULT_TEX:tris}
        
        self.all_dont_draws = {}
        self.all_vert_maxs  = {}
        self.all_uv_maxs    = {}

        self.bnd_rad = bnd_rad_square = 0.0

        #if the filepath isnt valid, return
        if not filepath:
            return

        '''collect all all tris, verts, uvw, normals, and texture indexes'''
        with open(filepath, 'r') as obj_f:
            for line in obj_f:
                line = line.strip()
                
                if not len(line):
                    continue
                elif line[0] == 'g':
                    #dont need to worry about groups
                    continue
                elif line[0] == '#':
                    #this is either a comment, or an extra piece of data
                    line = line[1:].strip()
                    if line[:6] == '$lod_k':
                        lod_ks[tex_index] = int(line[6:])
                    elif line[:9] == '$lm_index':
                        lm_indexes[tex_index] = int(line[9:])
                elif line[:6] == 'usemtl':
                    line = line[6:].strip(' ').split(' ')[-1]
                    error = False
                    try:
                        tex_index = int(line)
                    except ValueError:
                        error = True

                    if error:
                        raise TypeError("Texture name must be a whole "+
                                        "number, not '%s'"%line[-1][:-1])
                    #make a new triangle block if one for
                    #this material doesnt already exist
                    if tex_index not in all_tris:
                        all_tris[tex_index] = []
                        lm_indexes[tex_index] = DEFAULT_LM_INDEX
                        lod_ks[tex_index]     = DEFAULT_LOD_K
                    tris = all_tris[tex_index]
                elif line[0:2] == 'vt':
                    line = line[2:].strip(' ').split(' ')
                    uvs.append([int(127*(1-float(line[0]))),
                                int(127*(1-float(line[1])))])
                elif line[0:2] == 'vn':
                    line = line[2:].strip(' ').split(' ')
                    norms.append([float(line[0]),
                                  float(line[1]),
                                  float(line[2])])
                    norm = norms[-1]
                    mag = sqrt(norm[0]*norm[0]+
                               norm[1]*norm[1]+
                               norm[2]*norm[2])
                    norm[0] = int(15.5*(norm[0]/mag+1))
                    norm[1] = int(15.5*(norm[1]/mag+1))
                    norm[2] = int(15.5*(norm[2]/mag+1))
                    
                    if norm[0] > 31: norm[0] = 31
                    if norm[1] > 31: norm[1] = 31
                    if norm[2] > 31: norm[2] = 31
                    if norm[0] < 0: norm[0] = 0
                    if norm[1] < 0: norm[1] = 0
                    if norm[2] < 0: norm[2] = 0
                elif line[0] == 'v':
                    line = line[1:].strip(' ').split(' ')
                    verts.append([int(0.5+float(line[0])),
                                  int(0.5+float(line[1])),
                                  int(0.5+float(line[2]))])
                    v = verts[-1]
                    bnd_rad_square = max(v[0]**2 + v[1]**2 + v[2]**2,
                                         bnd_rad_square)
                elif line[0] == 'f':
                    line = line[1:].strip().split(' ')
                    tris.append((tuple(int(i)-1 for i in line[0].split('/')),
                                 tuple(int(j)-1 for j in line[1].split('/')),
                                 tuple(int(k)-1 for k in line[2].split('/'))))
                    
        self.bnd_rad = sqrt(bnd_rad_square)/128
        
        #if no untextured triangles exist, remove the entries
        if len(all_tris.get(DEFAULT_TEX, [None])) == 0:
            del all_tris[DEFAULT_TEX]


    def make_strips(self):
        stripifier = self.stripifier

        '''load the triangles into the stripifier, calculate
        strips, and link them together as best as possible'''
        stripifier.load_mesh(self.all_tris)
        stripifier.make_strips()
        stripifier.link_strips()
        
        verts = self.verts
        uvs   = self.uvs
        
        vert_data  = stripifier.vert_data
        all_degens = stripifier.all_degens
        all_strips = stripifier.all_strips
        
        all_dont_draws = self.all_dont_draws = {}
        all_vert_maxs  = self.all_vert_maxs = {}
        all_uv_maxs    = self.all_uv_maxs = {}
        
        '''calculate the max vert and uv sizes for each strip
        and calculate the dont_draws from the all_degens lists'''
        for tex_index in all_strips:
            strips = all_strips[tex_index]
            degens = all_degens[tex_index]
            
            dont_draws = all_dont_draws[tex_index] = []
            vert_maxs  = all_vert_maxs[tex_index]  = []
            uv_maxs    = all_uv_maxs[tex_index]    = []

            #loop over each strip
            for i in range(len(strips)):
                strip = strips[i]
                degen = degens[i]
                
                #first 2 are never rendered cause theres not 3 verts yet. duh
                d_draw = [1,1]+[0]*(len(strip)-2)

                vert_max = uv_max = 0
                #calcualte the vert and uv maxs
                for v_i in strip:
                    #get the largest vert and uv values
                    vert_max = max(verts[vert_data[v_i][0]]+
                                   [vert_max, -min(verts[vert_data[v_i][0]])])
                    uv_max = max(uvs[vert_data[v_i][1]]+
                                 [uv_max, -min(uvs[vert_data[v_i][1]])])
                
                vert_maxs.append(vert_max)
                uv_maxs.append(uv_max)

                dont_draws.append(d_draw)

                #flag all degen tris as not drawn
                for d in degen:
                    d_draw[d] = 1


    def write_g3d(self, g3d_filepath):
        ''''''
        verts = self.verts
        norms = self.norms
        uvs   = self.uvs

        stripifier = self.stripifier

        all_face_dirs  = stripifier.all_face_dirs
        all_strips     = stripifier.all_strips
        all_dont_draws = self.all_dont_draws
        all_vert_maxs  = self.all_vert_maxs
        all_uv_maxs    = self.all_uv_maxs
        
        vert_data  = stripifier.vert_data
        
        lm_indexes = self.lm_indexes
        lod_ks     = self.lod_ks

        tri_count = sum(stripifier.tri_counts.values())

        #if no strips exist in the mesh, return
        if tri_count == 0:
            return
        
        '''open the g3d output file'''
        with open(g3d_filepath, 'w+b') as g3d_f:
            #write the g3d header
            g3d_f.write(pack('<f', self.bnd_rad)+
                        pack('<I', len(vert_data))+
                        pack('<I', tri_count)+
                        pack('<I', len(all_strips)))

            '''loop over each subobject'''
            for tex_index in all_strips:
                strips = all_strips[tex_index]
                
                if len(strips) == 0:
                    continue
                
                #make a temp buffer to store the data as it's written
                buffer = BytearrayBuffer()

                linked = False
                lm_index = lm_indexes.get(tex_index,0)
                lod_k    = lod_ks.get(tex_index,0)

                face_dirs  = all_face_dirs[tex_index]
                dont_draws = all_dont_draws[tex_index]
                vert_maxs  = all_vert_maxs[tex_index]
                uv_maxs    = all_uv_maxs[tex_index]
                
                '''write the model data'''
                for strip_num in range(len(strips)):
                    strip = strips[strip_num]
                    if len(strip) < 3:
                        continue

                    d_draws  = dont_draws[strip_num]
                    vert_max = vert_maxs[strip_num]
                    uv_max   = uv_maxs[strip_num]

                    #if the face is reversed, set that
                    if face_dirs[strip_num]:
                        face_dir = -1.0
                    else:
                        face_dir = 1.0
                    

                    #write the tristrip header
                    buffer.write(b'\x00\x80\x01\x6C'+pack('<I',len(strip))+
                                 b'\x00\x00\x00\x2D'+ pack('<f',face_dir)+
                                 b'\x00\x00\x80\x3F')#set the uv scale to 1.0

                    '''write the vert data'''
                    if vert_max <= 127:
                        buffer.write(b'\x01\x80'+pack('B',len(strip)+1)+b'\x6A')
                        for i in strip:
                            v = verts[vert_data[i][0]]
                            buffer.write(pack('b',v[0])+
                                         pack('b',v[1])+
                                         pack('b',v[2]))
                        #write the final vert
                        buffer.write(b'\x00'*3)
                    elif vert_max <= 32767:
                        buffer.write(b'\x01\x80'+pack('B',len(strip)+1)+b'\x69')
                        for i in strip:
                            v = verts[vert_data[i][0]]
                            buffer.write(pack('<h',v[0])+
                                         pack('<h',v[1])+
                                         pack('<h',v[2]))
                        #write the final vert
                        buffer.write(b'\x00'*6)
                    else:
                        buffer.write(b'\x01\x80'+pack('B',len(strip)+1)+b'\x68')
                        for i in strip:
                            v = verts[vert_data[i][0]]
                            buffer.write(pack('<i',v[0])+
                                         pack('<i',v[1])+
                                         pack('<i',v[2]))
                        #write the final vert
                        buffer.write(b'\x00'*12)
                    #make sure the data is 4 byte aligned
                    buffer.write(b'\x00'*((4-(len(buffer)%4))%4) )

                    
                    '''write the normals data'''
                    buffer.write(b'\x04\xC0'+pack('B',len(strip))+b'\x6F')
                    for i in range(len(strip)):
                        n = norms[vert_data[strip[i]][2]]
                        buffer.write(pack('<H', n[0]+ (n[1]<<5)+ (n[2]<<10)+
                                                32768*d_draws[i]))

                    #make sure the data is 4 byte aligned
                    buffer.write(b'\x00'*((4-(len(buffer)%4))%4) )

                    
                    '''write the uv data'''
                    if uv_max <= 127:
                        buffer.write(b'\x04\xC0'+pack('B',len(strip))+b'\x66')
                        for i in strip:
                            uv = uvs[vert_data[i][1]]
                            buffer.write(pack('b',uv[0])+ pack('b',uv[1]))
                    elif uv_max <= 32767:
                        buffer.write(b'\x04\xC0'+pack('B',len(strip))+b'\x65')
                        for i in strip:
                            uv = uvs[vert_data[i][1]]
                            buffer.write(pack('<h',uv[0])+ pack('<h',uv[1]))
                    else:
                        buffer.write(b'\x04\xC0'+pack('B',len(strip))+b'\x64')
                        for i in strip:
                            uv = uvs[vert_data[i][1]]
                            buffer.write(pack('<i',uv[0])+ pack('<i',uv[1]))

                    #make sure the data is 4 byte aligned
                    buffer.write(b'\x00'*((4-(len(buffer)%4))%4) )

                    #write the link
                    if linked:
                        buffer.write(STRIP_LINK)
                    else:
                        linked = True
                        buffer.write(STRIP_START)
                #write the subobject header
                g3d_f.write(pack('<H', (len(buffer)+7)//16)+
                            pack('<H', tex_index)+
                            pack('<H', lm_index)+
                            pack('<h', lod_k))

                g3d_f.write(buffer)
                #pad the data to 16 bytes
                g3d_f.write(b'\x00'*((16-((len(buffer)-8)%16))%16) )
