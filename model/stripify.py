import os

from math import sqrt

DEFAULT_TEX = 0
MAX_STRIP_LEN = 2**32-4


class StripTri(list):
    __slots__ = (
        "siblings", "sibling_edges", "added",
        "get_sibling_index", "get_edge_index"
        )

    def __init__(self, v0, v1, v2):
        list.__init__(self, (v0, v1, v2))
        self.added = False
        self.siblings = [None, None, None]
        self.sibling_edges = [(v1, v0, 0),
                              (v2, v1, 0),
                              (v0, v2, 0)]

    def __setattr__(self, attr_name, new_val):
        if attr_name == "sibling_edges":
            self.get_edge_index = new_val.index
        elif attr_name == "siblings":
            self.get_sibling_index = new_val.index
        object.__setattr__(self, attr_name, new_val)

    def __add__(self, new_val): raise NotImplementedError()
    def __iadd__(self, new_val): raise NotImplementedError()
    def append(self): raise NotImplementedError()
    def extend(self): raise NotImplementedError()


class Stripifier():
    ''''''
    # the max length a strip can be
    max_strip_len = MAX_STRIP_LEN

    # whether or not the strips have all been linked together
    linked = False

    _winding = False

    # don't edit any of these directly if you know what's good for you
    vert_map = ()
    vert_data = ()
    all_tris_by_edges = ()
    all_face_dirs = ()
    all_strips = ()
    tri_counts = ()

    def __init__(self, all_tris=None, winding=False, *args, **kwargs):
        '''class initialization'''
        self.load_mesh(all_tris, winding)

    def translate_strip(self, vert_indices):
        '''
        Given a triangle strip that this Stripifier instance
        calculated, this method will return a de-indexed triangle strip.
        The elements in the strip will be the vert data the triangles
        contained when the current mesh was loaded.'''
        vert_data = self.vert_data
        return [vert_data[i][0] for i in vert_indices]

    def get_strip(self, strip_i=0, tex_index=DEFAULT_TEX):
        if tex_index not in self.all_strips:
            raise ValueError("No texture index '%s'" % tex_index)
        elif strip_i not in range(len(self.all_strips[tex_index])):
            raise ValueError("Strip index '%s' not in range(%s)" %
                             (strip_i, len(self.all_strips[tex_index])))

        return self.all_strips[tex_index][strip_i]

    def get_strip_count(self, tex_index=None):
        '''
        Returns the number of strips for the specified texture.
        If unspecified, returns the number of all loaded strips.'''
        indices = (tex_index, ) if tex_index is not None else self.all_strips
        ct = 0
        for i in indices:
            ct += len(self.all_strips[i])
        return ct

    def calc_strip(self, tri, neighbor_i=0, set_added=True):
        '''
        Given a starting triangle and the edge to start navigating,
        this function will return a list of the verts that make up the
        longest strip it can find and whether the strip faces backward.

        If set_added is True, triangles found will be flagged as
        added to a strip. Otherwise they will be de-flagged.'''
        vert_data = self.vert_data
        # each triangle has 3 edges.
        # this is the index of the edge the
        # next triangle will be connected to
        neighbor_i = neighbor_i%3

        strip_dir = self._winding

        seen = set()
        set_added = bool(set_added)

        '''navigate the strip in reverse to find the best place to start'''
        while True:
            # set the last triangle as this one
            last_tri = tri
            tri = tri.siblings[neighbor_i]

            # exit if the strip has ended
            if tri is None or tri.added or id(tri) in seen:
                tri = last_tri
                break

            # get which index the last tri was in the new tri so we can
            # orient outselves and figure out which edge to travel next
            neighbor_i = (tri.get_sibling_index(last_tri) + 1 + strip_dir) % 3

            # reverse the direction of travel
            # and set the triangle as seen
            strip_dir = not strip_dir
            seen.add(id(last_tri))

        # reset the seen set
        seen = set()

        # make a strip starting with the first 2 verts to the triangle
        strip = [tri[neighbor_i], tri[(neighbor_i + 1) % 3]]
        if strip_dir == self._winding:
            strip = strip[::-1]

        '''loop over triangles until the length is maxed or
        we reach a triangle without a neighbor on that edge'''
        curr_dir = strip_dir
        while not(tri.added or id(tri) in seen or len(strip) > self.max_strip_len):
            # get the index of the vert that will be added to the strip
            v_i = tri[(neighbor_i + 2) % 3]

            # add the vert to the strip
            strip.append(v_i)

            # set the last triangle as this one
            last_tri = tri

            # Get the next triangle.
            tri = tri.siblings[(neighbor_i + 1 + curr_dir) % 3]

            # reverse the direction of travel, set the last triangle
            # as added and seen, and increment the strip length
            last_tri.added = set_added
            curr_dir = not curr_dir
            seen.add(id(last_tri))

            # exit if the strip has ended
            if tri is None: break

            # get which index the last tri was in the new tri so we can
            # orient outselves and figure out which edge to travel next
            neighbor_i = tri.get_sibling_index(last_tri)

        return strip, strip_dir

    def link_strips(self):
        '''
        Links the strips that are currently loaded together into one
        large strip. This will introduce degenerate triangles into the
        mesh to link strips.'''
        if self.linked:
            return

        all_strips = self.all_strips
        all_face_dirs = self.all_face_dirs

        max_len = self.max_strip_len
        winding = self._winding

        for tex_index in all_strips:
            strips = all_strips[tex_index]
            face_dirs = all_face_dirs[tex_index]

            # if there are no strips for this mesh, skip it
            if not len(strips):
                continue

            even_fore_strips = []
            even_back_strips = []
            odd_strips = []
            strip_ct = len(strips)

            for i in range(strip_ct):
                strip = strips[i]
                face_dir = face_dirs[i]
                is_even = not (len(strip) & 1)
                if face_dir:
                    if is_even:
                        if winding and len(strip) == 4:
                            even_fore_strips.append(
                                [strip[0], strip[2], strip[1], strip[3]])
                        else:
                            even_back_strips.append(strip)
                    elif winding:
                        odd_strips.append(strip)
                    else:
                        odd_strips.append(list(reversed(strip)))
                elif is_even:
                    if winding and len(strip) == 4:
                        even_back_strips.append(
                            [strip[0], strip[2], strip[1], strip[3]])
                    else:
                        even_fore_strips.append(strip)
                elif winding:
                    odd_strips.append(list(reversed(strip)))
                else:
                    odd_strips.append(strip)

            fully_sorted_strips = [None] * strip_ct
            fully_sorted_face_dirs = [None] * strip_ct
            facing = True
            all_even_strips = (even_back_strips, even_fore_strips)
            if not winding:
                facing = False
                all_even_strips = (even_fore_strips, even_back_strips)

            i = 0
            for even_strips in all_even_strips:
                for s in even_strips:
                    fully_sorted_strips[i] = s
                    fully_sorted_face_dirs[i] = facing
                    i += 1
                facing = not facing

            for j in range(len(odd_strips)):
                fully_sorted_strips[i] = odd_strips[j]
                fully_sorted_face_dirs[i] = winding
                i += 1

            # make lists to hold the new strips, degens, and dirs
            new_strips = []
            new_face_dirs = []

            # get the first set of strips to link together
            strip_i = 1
            strip_ct = len(fully_sorted_strips)

            # get the first strip to link together
            strip0 = fully_sorted_strips[0]
            strip0_dir = fully_sorted_face_dirs[0]

            '''keep linking strips together till none are left'''
            while strip_i < strip_ct or not new_strips:
                strip1 = strip1_dir = None
                if strip0_dir != winding:
                    strip0.insert(0, strip0[0])
                    strip0_dir = not strip0_dir

                # link strips together until their length is maxed
                while strip_i < strip_ct:
                    strip1 = fully_sorted_strips[strip_i]
                    strip1_dir = fully_sorted_face_dirs[strip_i]

                    len0 = len(strip0)
                    len1 = len(strip1)
                    end_dir0 = (strip0_dir == (len0 % 2))
                    add_degen = (end_dir0 == strip1_dir)

                    strip_i += 1
                    # if the strip being added is empty, skip it
                    if len0 + len1 + add_degen + 2 > max_len:
                        # total length will be over max. dont try to combine
                        break
                    elif len1 == 0:
                        continue

                    # if a degen needs to be added, repeat the last vert
                    if add_degen:
                        strip0.append(strip0[-1])

                    if strip0[-1] != strip1[0]:
                        # create the extra degenerate triangles
                        strip0.extend((strip0[-1], strip1[0]))

                    # merge the strips
                    strip0.extend(strip1)

                new_face_dirs.append(strip0_dir)
                new_strips.append(strip0)

                # restart the cycle on the next strip
                strip0_dir = strip1_dir
                strip0 = strip1

            all_strips[tex_index]    = new_strips
            all_face_dirs[tex_index] = new_face_dirs

        self.linked = True

    def load_mesh(self, all_tris=None, winding=False):
        '''Loads a list of triangles into the stripifier.'''
        # Maps each unique vert/uv/norm/color combo to
        # the index it is stored in in vert_data
        self.vert_map = vert_map = {}
        # Stores each unique combination of vert/uv/norm/color number
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

        # whether or not the strips have been linked together
        self.linked = False

        self._winding = winding

        if all_tris is None:
            return
        elif isinstance(all_tris, (list, tuple)):
            all_tris = {DEFAULT_TEX:all_tris}
        elif not isinstance(all_tris, dict):
            raise TypeError("'all_tris' argument must be either a list"
                            ", tuple, or dict, not %s" % type(all_tris))

        # loop over all meshes by texture
        for tex_index in all_tris:
            tris = all_tris[tex_index]

            self.all_tris_by_edges[tex_index] = t_by_e = {}
            self.all_face_dirs[tex_index] = []
            self.all_strips[tex_index] = []
            self.tri_counts[tex_index] = len(tris)
            if not tris:
                continue

            make_tuple = (hasattr(tris[0], "__getitem__") and
                          hasattr(tris[0][0], "__iter__") and
                          not isinstance(tris[0][0], tuple))
            
            for src_tri in tris:
                if make_tuple:
                    v0 = (tuple(src_tri[0]), tex_index)
                    v1 = (tuple(src_tri[1]), tex_index)
                    v2 = (tuple(src_tri[2]), tex_index)
                else:
                    v0 = (src_tri[0], tex_index)
                    v1 = (src_tri[1], tex_index)
                    v2 = (src_tri[2], tex_index)

                # connected faces in a triangle strip must share vert,
                # coordinates, uv coordinates, and normals. This is
                # because the verts are reused for neighboring faces.
                # Need to split strips up by texture coordinates as well.

                v0_i = vert_map.get(v0)
                # get if this first vert doesnt already exist
                if v0_i is None:
                    vert_map[v0] = v0_i = len(vert_data)
                    vert_data.append(v0)

                v1_i = vert_map.get(v1)
                # get if this second vert doesnt already exist
                if v1_i is None:
                    vert_map[v1] = v1_i = len(vert_data)
                    vert_data.append(v1)

                v2_i = vert_map.get(v2)
                # get if this third vert doesnt already exist
                if v2_i is None:
                    vert_map[v2] = v2_i = len(vert_data)
                    vert_data.append(v2)

                tri = StripTri(v0_i, v1_i, v2_i)
                edges = ((v0_i, v1_i, 0),
                         (v1_i, v2_i, 0),
                         (v2_i, v0_i, 0))

                # loop over all 3 edges
                for i in (0, 1, 2):
                    v0_i, v1_i, update_edge_num = edge = edges[i]
                    rev_edge = (v1_i, v0_i, update_edge_num)

                    if edge in t_by_e:
                        # this takes care of update edges, which
                        # is when more than two tris share an edge.
                        while edge in t_by_e:
                            update_edge_num += 1
                            edge = (v0_i, v1_i, update_edge_num)

                        rev_edge = (v1_i, v0_i, update_edge_num)
                        tri.sibling_edges[i] = rev_edge

                    # get the triangle that shares this edge
                    conn_tri = t_by_e.get(rev_edge)

                    if conn_tri:
                        # Some triangle shares this edge, so add it
                        # to this triangle as one of its siblings and
                        # add this triangle to it as one of its siblings
                        tri.siblings[i] = conn_tri
                        conn_tri.siblings[conn_tri.get_edge_index(edge)] = tri

                    # neighbor edges are travelled in reverse.
                    t_by_e[edge] = tri

    def make_strips(self):
        '''Creates triangle strips out of the loaded mesh.'''
        all_tris_by_edges = self.all_tris_by_edges

        '''loop over all meshes by texture'''
        for tex_index in all_tris_by_edges:
            tris = all_tris_by_edges[tex_index]
            self.all_face_dirs[tex_index] = face_dirs = []
            self.all_strips[tex_index] = strips = []

            tri_count = self.tri_counts[tex_index]
            edges = list(tris.keys())

            tris_added = 0
            e_i = 0

            '''create triangle strips for this mesh'''
            while tris_added < tri_count:
                # get the first triangle in the strip
                tri_0 = tris[edges[e_i]]
                e_i += 1

                # if the triangle has already been added
                if tri_0.added:
                    continue

                # calculate the 3 different possible strips
                s0, _ = self.calc_strip(tri_0, 0, False)
                s1, _ = self.calc_strip(tri_0, 1, False)
                s2, _ = self.calc_strip(tri_0, 2, False)

                lens = (len(s0), len(s1), len(s2))

                # use only the largest strip
                # Need to re-run the function so it can also
                # flag the triangles in the strip as added.
                strip_data = self.calc_strip(tri_0, lens.index(max(lens)), True)
                strips.append(strip_data[0])
                face_dirs.append(strip_data[1])

                tris_added += len(strips[-1]) - 2
