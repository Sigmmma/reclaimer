import os

from math import sqrt

DEFAULT_TEX = 0
MAX_STRIP_LEN = 2**32-4

class Stripifier():

    #the max length a strip can be
    max_strip_len = MAX_STRIP_LEN
    
    def __init__(self, all_tris=None, *args, **kwargs):
        ''''''
        self.load_mesh(all_tris)

    
    def calc_strip(self, tri, neighbor_i=0, set_added=1):
        ''''''
        vert_data = self.vert_data
        #each triangle has 3 edges.
        #this is the index of the edge the
        #next triangle will be connected to
        neighbor_i = neighbor_i%3
        
        strip_len = 0
        last_neighbor_i = neighbor_i
        strip_dir = False
        strip_reversed = False

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
        
        '''loop over triangles until the length is maxed or
        we reach a triangle without a neighbor on that edge'''
        #cant have more than ~252 triangles in a strip since
        #a single byte is used to designate the number.
        while not(tri[3] or id(tri) in seen or strip_len > self.max_strip_len):
            #get the index of the vert that will be added to the strip
            v_i = tri[(neighbor_i + 2)%3]

            #add the vert to the strip
            strip.append(v_i)

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
        return strip, strip_reversed
    

    def link_strips(self):
        ''''''
        return
        all_strips = self.all_strips
        all_degens = self.all_degens
        all_face_dirs = self.all_face_dirs

        for tex_index in all_strips:
            strips = all_strips[tex_index]
            face_dirs = all_face_dirs[tex_index]
            
            #a mapping that stores the strips from shortest to longest
            sorted_strips = {}
            sorted_dirs = {}

            #if there are no strips for this mesh, skip it
            if not len(strips):
                continue

            #sort the strips and their facing directions by length
            for i in range(len(strips)):
                strip = strips[i]
                strip_len = len(strip)
                
                same_len_strips = sorted_strips.get(strip_len, [])
                same_len_strip_dirs = sorted_dirs.get(strip_len, [])
                
                same_len_strips.append(strips[i])
                same_len_strip_dirs.append(face_dirs[i])
                
                sorted_strips[strip_len] = same_len_strips
                sorted_dirs[strip_len]   = same_len_strip_dirs

            #make a list to hold the new strips and dirs after they're linked
            new_degens    = []
            new_strips    = []
            new_face_dirs = []

            strip_lengths = sorted(sorted_strips.keys())
            
            #get the first set of strips to link together
            curr_strips = sorted_strips[strip_lengths[0]]

            #get the first strip to link together
            strip0 = curr_strips.pop()

            
            '''keep linking strips together till none are left'''
            while len(curr_strips):
                new_degens.append([])

            all_degens[tex_index]    = new_degens
            all_strips[tex_index]    = new_strips
            all_face_dirs[tex_index] = new_face_dirs


    def load_mesh(self, all_tris=None):
        #Maps each unique vert/uv/norm/color combo to
        #the index it is stored in in vert_data
        self.vert_map = vert_map = {}
        #Stores each unique combination of vert/uv/norm/color number
        self.vert_data = vert_data = []
        
        '''Stores triangles indexed by their tex_index and then their edges.
        The triangle edges they are indexed under are in reverse direction.
        This is because all connected neighboring triangles will
        share the same edge, but in the opposite direction.'''
        self.all_tris_by_edges = {}
        
        '''Stores lists of the direction of each tex_indexs triangle strips.
        False == strip is facing properly. True == strip is facing inverted.'''
        self.all_face_dirs = {}

        '''Stores the triangle strip lists indexed by their tex_index'''
        self.all_strips = {}
        
        '''Stores tri counts for each subobject separated by tex_index'''
        self.tri_counts = {}

        '''Stores the indexes of the degenerate triangles for each strip
        in each tex_index'''
        self.all_degens = {}
        
        if all_tris is None:
            return
        elif isinstance(all_tris, (list, tuple)):
            all_tris = {DEFAULT_TEX:all_tris}
        elif not isinstance(all_tris, dict):
            raise TypeError("'all_tris' argument must be either a list"+
                            ", tuple, or dict, not %s"%type(all_tris))

        #loop over all meshes by texture
        for tex_index in all_tris:
            tris = all_tris[tex_index]
            
            self.all_tris_by_edges[tex_index] = t_by_e = {}
            self.all_face_dirs[tex_index] = []
            self.all_strips[tex_index] = []
            self.tri_counts[tex_index] = len(tris)
            self.all_degens[tex_index] = []
            
            for tri in tris:
                v0 = tuple(tri[0])+(tex_index,)
                v1 = tuple(tri[1])+(tex_index,)
                v2 = tuple(tri[2])+(tex_index,)

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

                edges = [(v0_i, v1_i), (v1_i, v2_i), (v2_i, v0_i)]
                
                #      [vert1, vert2, vert3, added,
                #       sib1,  sib2,  sib3,
                #       edge1, edge2, edge3]
                tri = [v0_i,  v1_i,  v2_i,  False,
                       None, None, None,
                       edges[0], edges[1], edges[2]]

                '''loop over all 3 edges'''
                for i in (0,1,2):
                    #get the triangle that shares this edge
                    conn_tri = t_by_e.get(edges[i])
                    if conn_tri:
                        '''Some triangle shares this edge, so add it
                        to this triangle as one of its siblings and
                        add this triangle to it as one of its siblings'''
                        tri[4+i] = conn_tri
                        conn_tri[conn_tri.index(edges[i][::-1])-3] = tri

                    #neighbor edges are travelled in reverse.
                    t_by_e[edges[i][::-1]] = tri

    
    def make_strips(self):
        all_tris_by_edges = self.all_tris_by_edges
        
        '''loop over all meshes by texture'''
        for tex_index in all_tris_by_edges:
            tris = all_tris_by_edges[tex_index]
            self.all_face_dirs[tex_index] = face_dirs = []
            self.all_strips[tex_index] = strips = []
            self.all_degens[tex_index] = degens = []
            
            tri_count = self.tri_counts[tex_index]
            edges = list(tris.keys())
            
            tris_added = 0
            e_i = 0
            
            '''create triangle strips for this mesh'''
            while tri_count > tris_added:
                #get the first triangle in the strip
                tri_0 = tris[edges[e_i]]
                e_i += 1

                #if the triangle has already been added
                if tri_0[3]:
                    continue

                #calculate the 3 different possible strips
                s0, _ = self.calc_strip(tri_0, 0, 0)
                s1, _ = self.calc_strip(tri_0, 1, 0)
                s2, _ = self.calc_strip(tri_0, 2, 0)

                lens = (len(s0), len(s1), len(s2))

                #use only the largest strip
                '''Need to re-run the function so it can also
                flag the triangles in the strip as bring added'''
                strip, rev = self.calc_strip(tri_0, lens.index(max(lens)), 1)

                face_dirs.append(rev)
                strips.append(strip)
                degens.append([])
                
                tris_added += len(strip) - 2
