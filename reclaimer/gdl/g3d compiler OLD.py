import os

from math import sqrt
from pprint import pprint
from struct import pack
from traceback import format_exc
from os.path import basename, splitext, join, abspath, dirname

from supyr_struct.buffer import BytearrayBuffer

STRIP_START = b'\x00\x00\x00\x14'
STRIP_LINK  = b'\x00\x00\x00\x17'
MAX_STRIP_LEN = 255 - 1 - 2#UInt8_Max - (final null vert) - (first 2 verts)
DEFAULT_TEX = 0
DEFAULT_LOD_K = -90
DEFAULT_LM_INDEX = 0

try:
    curr_dir = abspath(os.curdir)
    obj_filepaths = []
    mod_folder = curr_dir

    g3d_filename_base = dirname(mod_folder)+'\\%s.g3d'


    def calc_strip(verts, vert_data, tri, neighbor_i=0, set_added=1, max_len=None):
        ''''''
        #each triangle has 3 edges.
        #this is the index of the edge the
        #next triangle will be connected to
        neighbor_i = neighbor_i%3
        
        strip_len = 0
        last_neighbor_i = neighbor_i
        strip_dir = False
        strip_reversed = False

        #if the max length isnt defined, set it to the max 32 bit unsigned value
        if max_len is None:
            max_len = 2**32-4

        #keep track of which tris have been seen
        seen = set()
        
        '''navigate the strip in reverse to find the best place to start'''
        while True:
            #set the last triangle as this one
            last_tri = tri
            tri = tri[4 + neighbor_i]

            #exit if the strip has ended
            if tri is None or tri[3] or id(tri) in seen:
                tri = last_tri
                break
            
            last_neighbor_i = (neighbor_i + 1 + strip_dir)%3
            
            #get which index the last tri was in the new tri so we can
            #orient outselves and figure out which edge to travel next
            neighbor_i = (tri.index(last_tri)-4 + 1 + strip_dir)%3

            #reverse the direction of travel
            #and set the triangle as seen
            strip_dir = not strip_dir
            seen.add(id(last_tri))
            
        #reset the seen set
        seen = set()
        
        #make a strip starting with the first 2 verts to the triangle
        strip = tri[neighbor_i:neighbor_i+2]
        if neighbor_i == 2:
            strip = [tri[2], tri[0]]
        
        #if the strip direction should be reversed
        if strip_dir:
            #reverse the first 2 verts
            strip = strip[::-1]
            strip_reversed = True
        
        #get the max coordinate value of these first 2 verts and their uvs
        v0_i = tri[neighbor_i]
        v1_i = tri[(1+neighbor_i)%3]
        
        vert_max = max( verts[vert_data[v0_i][0]]+
                        verts[vert_data[v1_i][0]]+
                       [-min(verts[vert_data[v0_i][0]]+
                             verts[vert_data[v1_i][0]])])
        uv_max = max( uvs[vert_data[v0_i][1]]+
                      uvs[vert_data[v1_i][1]]+
                     [-min(uvs[vert_data[v0_i][1]]+
                           uvs[vert_data[v1_i][1]])])
        
        '''loop over triangles until the length is maxed or
        we reach a triangle without a neighbor on that edge'''
        #cant have more than ~252 triangles in a strip since
        #a single byte is used to designate the number.
        while not tri[3] and id(tri) not in seen and strip_len < MAX_STRIP_LEN:
            #get the index of the vert that will be added to the strip
            v_i = tri[(neighbor_i + 2)%3]

            #add the vert to the strip
            strip.append(v_i)

            #get the largest vert and uv values
            vert_max = max(verts[vert_data[v_i][0]]+
                           [vert_max, -min(verts[vert_data[v_i][0]])])
            uv_max = max(uvs[vert_data[v_i][1]]+
                         [uv_max, -min(uvs[vert_data[v_i][1]])])

            #set the last triangle as this one
            last_tri = tri
            
            '''Get the next triangle.
            Starting at 1, every odd numbered triangle will
            have the next triangle chosen from its second edge,
            while every even numbered triangle will have the
            next triangle chosen from its 3rd edge.'''
            tri = tri[4 + (neighbor_i + 1 + strip_dir)%3]

            #reverse the direction of travel, set the last triangle
            #as added and seen, and increment the strip length
            last_tri[3] = set_added
            strip_dir = not strip_dir
            seen.add(id(last_tri))
            strip_len += 1

            #exit if the strip has ended
            if tri is None: break

            #get which index the last tri was in the new tri so we can
            #orient outselves and figure out which edge to travel next
            neighbor_i = tri.index(last_tri)-4
        return strip, strip_reversed, vert_max, uv_max

    #cant link strips together because the max verts and
    #uvs will need to be recomputed for the new strips.
    #Maybe do this after making this a standalone module
    '''
    def link_strips(strips, strip_dirs):
        ''''''
        #a mapping that stores the strips from shortest to longest
        sorted_strips = {}
        sorted_dirs = {}

        #sort the strips and their facing directions by length
        for i in range(len(strips)):
            strip_len = len(strip)
            
            same_len_strips = sorted_strips.get(strip_len, [])
            same_len_strip_dirs = sorted_dirs.get(strip_len, [])
            
            same_len_strips.append(strips[i])
            same_len_strip_dirs.append(face_dirs[i])
            
            sorted_strips[strip_len] = same_len_strips
            sorted_dirs[strip_len]   = same_len_strip_dirs

        #make a list to hold the new strips and dirs after they're linked
        new_strips    = []
        new_face_dirs = []

        strip_lengths = sorted(sorted_strips.keys())
        
        #get the first set of strips to link together
        curr_strips = sorted_strips[strip_lengths[0]]

        #get the first strip to link together
        strip0 = curr_strips.pop()
        
        #keep linking strips together till none are left
        while len(curr_strips):
            pass
    '''

    #locate all the objs in the folder
    for root, directories, files in os.walk(curr_dir):
        for filepath in files:            
            if splitext(filepath)[-1].lower() == ".obj":
                obj_filepaths.append(join(root, filepath))

    #loop over each obj
    for filepath in obj_filepaths:
        g3d_filepath = g3d_filename_base % splitext(basename(filepath))[0]

        #Maps each unique vert/uv/norm combo to
        #the index it is stored in in vert_data
        vert_map = {}
        #stores the largest vert for each strip in each tex_index
        vert_maxs = {}
        #stores the largest uv for each strip in each tex_index
        uv_maxs = {}
        #Stores each unique combination of vert/uv/norm number
        vert_data = []

        #Stores the unorganized verts, norms, and uvs
        verts = []
        norms = []
        uvs = []

        #in case a material index isnt provided in the file, have
        #a default tex_index of None available in all the mappings
        t_by_e = {}
        '''Stores triangles indexed by their tex_index and then their edges.
        The triangle edges they are indexed under are in reverse direction.
        This is because all connected neighboring triangles will
        share the same edge, but in the opposite direction.'''
        all_tris_by_edges = {DEFAULT_TEX:t_by_e}

        '''Stores tri counts for each subobject separated by tex_index.'''
        tri_counts = {DEFAULT_TEX:0}
        lm_indexes = {DEFAULT_TEX:DEFAULT_LM_INDEX}
        lod_ks     = {DEFAULT_TEX:DEFAULT_LOD_K}

        tex_index = DEFAULT_TEX

        bnd_rad_square = 0.0
        tri_count = 0

        '''collect all all tris, verts, uvw, normals, and texture indexes'''
        with open(filepath, 'r') as obj_f:
            for line in obj_f:
                if not len(line):
                    continue
                elif line[0] == 'g':
                    #dont need to worry about groups
                    continue
                elif line[0] == '#':
                    #this is either a comment, or an extra piece of data
                    line = line[1:].strip()
                    if line[:5] == 'lod_k':
                        lod_ks[tex_index] = int(line[5:])
                    elif line[:8] == 'lm_index':
                        lm_indexes[tex_index] = int(line[8:])
                elif line[:6] == 'usemtl':
                    line = line[6:].strip(' ').split(' ')
                    error = False
                    try:
                        tex_index = int(line[-1])
                    except ValueError:
                        error = True

                    if error:
                        raise TypeError("Texture name must be an "+
                                        "integer, not '%s'"%line[-1][:-1])
                    #make a new triangle block if one for
                    #this material doesnt already exist
                    if tex_index not in all_tris_by_edges:
                        tri_counts[tex_index] = 0
                        all_tris_by_edges[tex_index] = {}
                        lm_indexes[tex_index] = DEFAULT_LM_INDEX
                        lod_ks[tex_index] = DEFAULT_LOD_K
                    t_by_e = all_tris_by_edges[tex_index]
                    #print(tex_index)
                elif line[0:2] == 'vt':
                    line = line[2:].strip(' ').split(' ')
                    uvs.append([int(127*(1-float(line[0]))),
                                int(127*(1-float(line[1])))])
                    #print(all_uvs[-1])
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
                    #print(all_norms[-1])
                elif line[0] == 'v':
                    line = line[1:].strip(' ').split(' ')
                    verts.append([int(0.5+float(line[0])),
                                  int(0.5+float(line[1])),
                                  int(0.5+float(line[2]))])
                    v = verts[-1]
                    dist = v[0]**2 + v[1]**2 + v[2]**2
                    if dist > bnd_rad_square:
                        bnd_rad_square = dist
                    #print(verts[-1])
                elif line[0] == 'f':
                    line = line[1:].strip(' ').split(' ')
                    v0 = tuple(int(i)-1 for i in line[0].split('/'))+(tex_index,)
                    v1 = tuple(int(j)-1 for j in line[1].split('/'))+(tex_index,)
                    v2 = tuple(int(k)-1 for k in line[2].split('/'))+(tex_index,)

                    #format is v/vt/vn
                    '''connected faces in a triangle strip must share vert,
                    coordinates, uv coordinates, and normals. This is because
                    the verts are reused for neighboring faces. Will need to
                    split strips up by texture coordinates as well.'''

                    v0_i = vert_map.get(v0)
                    v1_i = vert_map.get(v1)
                    v2_i = vert_map.get(v2)

                    #get if this first vert doesnt already exist
                    if v0_i is None:
                        vert_map[v0] = v0_i = len(vert_data)
                        vert_data.append(v0)
                    #get if this second vert doesnt already exist
                    if v1_i is None:
                        vert_map[v1] = v1_i = len(vert_data)
                        vert_data.append(v1)
                    #get if this third vert doesnt already exist
                    if v2_i is None:
                        vert_map[v2] = v2_i = len(vert_data)
                        vert_data.append(v2)

                    tri_count += 1

                    e = [(v0_i, v1_i),(v1_i, v2_i), (v2_i, v0_i)]
                    
                    #      vert1, vert2, vert3, added,
                    tri = [v0_i,  v1_i,  v2_i,  False,
                    #      sib1, sib2, sib3, edge1, edge2, edge3
                           None, None, None, e[0],  e[1],  e[2]]
                    tri_counts[tex_index] += 1

                    for i in (0,1,2):
                        #get the triangle that shares this edge
                        connected_tri = t_by_e.get(e[i])
                        if connected_tri:
                            '''Some triangle shares this edge, so add it
                            to this triangle as one of its siblings and
                            add this triangle to it as one of its siblings'''
                            tri[4+i] = connected_tri
                            connected_tri[connected_tri.index(e[i][::-1])-3] = tri
                            
                        t_by_e[e[i][::-1]] = tri
        
        print(filepath)
        print('verts', len(verts))
        print('uvs',   len(norms))
        print('norms', len(uvs))
        '''open the g3d output file'''
        with open(g3d_filepath, 'w+b') as g3d_f:
            #if no untextured triangles exist, remove the entries
            if tri_counts[DEFAULT_TEX] == 0:
                del all_tris_by_edges[DEFAULT_TEX]
                del tri_counts[DEFAULT_TEX]
                
            #write the g3d header
            g3d_f.write(pack('<f', sqrt(bnd_rad_square)/128)+
                        pack('<I', len(vert_data))+
                        pack('<I', tri_count)+
                        pack('<I', len(tri_counts)))

            '''loop over each subobject'''
            for tex_index in tri_counts:
                if tri_counts[tex_index] == 0:
                    continue
                #make a temp buffer to store the data as its written
                buffer = BytearrayBuffer()

                v_max  = 0
                uv_max = 0
                linked = False
                
                vert_maxs[tex_index] = []
                uv_maxs[tex_index] = []

                #these contains lists of the verts for
                #each strip that will be created
                strips = []
                dont_draws = []
                face_dirs = []

                tri_count = tri_counts[tex_index]
                tris_added = 0
                strip_len = 0
                i = 0

                t_by_e   = all_tris_by_edges[tex_index]
                lm_index = lm_indexes.get(tex_index)
                lod_k    = lod_ks.get(tex_index)

                edges = list(t_by_e.keys())
                
                print('tex_index', tex_index)
                print('  tri_count', tri_count)
                
                '''create triangle strips for this subobject'''
                while tri_count > tris_added:
                    #get the first triangle in the strip
                    tri_0 = t_by_e[edges[i]]
                    i += 1

                    #if the triangle has already been added
                    if tri_0[3]: continue

                    #calculate the 3 different possible strips
                    strip0, _, __, ___ = calc_strip(verts, vert_data,
                                                    tri_0, 0, 0, MAX_STRIP_LEN)
                    strip1, _, __, ___ = calc_strip(verts, vert_data,
                                                    tri_0, 1, 0, MAX_STRIP_LEN)
                    strip2, _, __, ___ = calc_strip(verts, vert_data,
                                                    tri_0, 2, 0, MAX_STRIP_LEN)

                    lens = (len(strip0), len(strip1), len(strip2))

                    #use only the largest strip
                    '''Need to re-run the function so it can also
                    flag the triangles in the trip as added'''
                    strip, rev, v_max, uv_max = calc_strip(verts, vert_data, tri_0,
                                                           lens.index(max(lens)),
                                                           1, MAX_STRIP_LEN)

                    strips.append(strip)
                    face_dirs.append(rev)
                    vert_maxs[tex_index].append(v_max)
                    uv_maxs[tex_index].append(uv_max)
                    dont_draws.append((1,1,)+(0,)*(len(strip)-2))
                    
                    tris_added += len(strip) - 2
                    print('    strip_tri_count', len(strip)-2)
                
                print('  strip_count', len(strips))
                print()
                        
                '''write the model data'''
                for strip_num in range(len(strips)):
                    strip = strips[strip_num]
                    if len(strip) < 3:
                        continue

                    dont_draw = dont_draws[strip_num]

                    #if the face is reversed, set that
                    if face_dirs[strip_num]:
                        face_dir = -1.0
                    else:
                        face_dir = 1.0
                    
                    vert_max = vert_maxs[tex_index][strip_num]
                    uv_max = uv_maxs[tex_index][strip_num]

                    #write the tristrip header
                    buffer.write(b'\x00\x80\x01\x6C'+pack('<I',len(strip))+
                                 b'\x00\x00\x00\x2D'+
                                 pack('<f',face_dir)+
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
                                                32768*dont_draw[i]))

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
        print('-'*80)

except Exception:
    print(format_exc())

input('finished')
