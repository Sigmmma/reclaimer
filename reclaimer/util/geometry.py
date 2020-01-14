#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import ceil, log, sqrt
from sys import float_info
from reclaimer.util import matrices


def point_distance_to_plane(point, plane, use_double_rounding=False,
                            round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23)
    # return True if point is on forward side of plane, otherwise False
    # take into account rounding errors for 32bit floats
    delta_max = 2**(
        int(log(abs(plane[3]) + float_info.epsilon, 2)) -
        mantissa_len) + abs(round_adjust)
    delta = matrices.dot_product(plane[:3], point) - plane[3]
    if abs(delta) < delta_max:
        # point lies on plane
        return 0.0
    return delta


def point_distance_to_line(point, line, use_double_rounding=False,
                           round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23)
    line_point = matrices.Point(line[0])
    line_dir   = matrices.Ray(line[1]).normalized
    dist = matrices.Ray.cross(line_dir, line_point - point).mag

    # return True if point is on forward side of plane, otherwise False
    # take into account rounding errors for 32bit floats
    delta_max = 2**(
        int(ceil(log(abs(dist) + float_info.epsilon, 2))) -
        mantissa_len) + abs(round_adjust)
    if abs(dist) < delta_max:
        # point lies on plane
        return 0.0
    return dist


def is_point_on_plane(point, plane, use_double_rounding=False,
                      round_adjust=0):
    return point_distance_to_plane(
        point, plane, use_double_rounding, round_adjust) == 0


def is_point_on_line(point, line, use_double_rounding=False,
                     round_adjust=0):
    return point_distance_to_line(
        point, line, use_double_rounding, round_adjust) == 0


def is_point_on_front_side_of_plane(point, plane, on_plane_ok=False,
                                    use_double_rounding=False,
                                    round_adjust=0):
    '''
    Returns if point iterable(x,y,z) is on the front side of
    plane iterable(x,y,z,delta).
    Either with single or double rounding.
    '''
    rounded_dist = point_distance_to_plane(
        point, plane, use_double_rounding, round_adjust)
    if on_plane_ok:
        return rounded_dist >= 0
    return rounded_dist > 0


def is_point_on_back_side_of_plane(point, plane, on_plane_ok=False,
                                   use_double_rounding=False,
                                   round_adjust=0):
    rounded_dist = point_distance_to_plane(
        point, plane, use_double_rounding, round_adjust) < 0
    if on_plane_ok:
        return rounded_dist <= 0
    return rounded_dist < 0


def is_point_on_front_side_of_planes(point, planes, on_plane_ok=False,
                                     use_double_rounding=False,
                                     round_adjust=0):
    for plane in planes:
        if not is_point_on_front_side_of_plane(
            point, plane, on_plane_ok, use_double_rounding, round_adjust):
            return False
    return True


def is_point_on_back_side_of_planes(point, planes, on_plane_ok=False,
                                    use_double_rounding=False,
                                    round_adjust=0):
    for plane in planes:
        if not is_point_on_back_side_of_plane(
            point, plane, on_plane_ok, use_double_rounding, round_adjust):
            return False
    return True


def find_intersect_line_of_planes(plane_0, plane_1, use_double_rounding=False,
                                  round_adjust=0, normalize=False):
    # returns an arbitrary point where the provided planes intersect.
    # if they do not intersect, None will be returned instead.
    plane_0 = Plane(plane_0)
    plane_1 = Plane(plane_1)
    plane_0.normalize()
    plane_1.normalize()
    plane_0_dir = matrices.Ray(plane_0[:3])
    plane_1_dir = matrices.Ray(plane_1[:3])
    line_dir = matrices.Ray.cross(plane_0_dir, plane_1_dir)
    determinant = line_dir.mag_sq
    if determinant <= float_info.epsilon:
        # planes are parallel. ignore
        return

    line_point = (
        (matrices.Ray.cross(line_dir, plane_0_dir) * plane_1[3]) +
        (matrices.Ray.cross(plane_1_dir, line_dir) * plane_0[3])) / determinant

    max_comp = 2
    if abs(line_dir[0]) >= abs(line_dir[1]):
        if abs(line_dir[0]) >= abs(line_dir[2]):
            max_comp = 0
    elif abs(line_dir[1]) >= abs(line_dir[2]):
        max_comp = 1

    line_point -= line_dir * (line_point[max_comp] / line_dir[max_comp])
    if normalize:
        line_dir.normalize()

    return line_point, line_dir


def find_intersect_point_of_lines(line_0, line_1, use_double_rounding=False,
                                  round_adjust=0, ignore_check=False):
    # returns an arbitrary point where the provided lines intersect.
    # if they do not intersect, None will be returned instead.
    v0, d0 = matrices.Point(line_0[0]), matrices.Ray(line_0[1])
    v1, d1 = matrices.Point(line_1[0]), matrices.Ray(line_1[1])
    assert len(v0) == len(v1)
    assert len(d0) == len(d1)
    if d0.is_zero or d1.is_zero:
       # one or both vectors are the zero-vector
        return None

    try:
        reduced, result = matrices.Matrix(
            [(a, -b) for a, b in zip(d0, d1)]).row_reduce(
            matrices.Matrix([v0[i] - v1[i] for i in range(len(v0))]))
    except matrices.CannotRowReduce:
        return None

    intersect_a = v0 - d0 * result[0][0]
    intersect_b = v1 - d1 * result[1][0]
    if ignore_check or matrices.are_vectors_equal(
            intersect_a, intersect_b, use_double_rounding, round_adjust):
        # point lies on both lines
        return intersect_a + (intersect_b - intersect_a) / 2

    return None


def find_intersect_point_of_planes(plane_0, plane_1, plane_2, use_double_rounding=False,
                                   round_adjust=0, ignore_check=False):
    try:
        reduced, result = matrices.Matrix(
            (plane_0[:-1], plane_1[:-1], plane_2[:-1])).row_reduce(
                matrices.Matrix([plane_0[3], plane_1[3], plane_2[3]]))
    except matrices.CannotRowReduce:
        return None

    return matrices.Point((result[0][0], result[1][0], result[2][0]))


def plane_from_verts(v0, v1, v2):
    p_dir = matrices.Ray.cross(matrices.line_from_verts(v1, v0),
                               matrices.line_from_verts(v1, v2))
    p_dir.normalize()
    if p_dir.is_zero:
        return None

    return (p_dir[0], p_dir[1], p_dir[2],
            v1[0]*p_dir[0] + v1[1]*p_dir[1] + v1[2]*p_dir[2])


def are_planes_equal(plane_0, plane_1, use_double_rounding=False,
                     round_adjust=0):
    p0 = Plane(plane_0)
    p1 = Plane(plane_1)
    p0.normalize()
    p1.normalize()
    return matrices.are_vectors_equal(p0, p1, use_double_rounding, round_adjust)


class Plane(matrices.FixedLengthList, matrices.Ray):
    __slots__ = ()
    def __init__(self, initializer=(0, 0, 1, 0)):
        assert len(initializer) == 4
        list.__init__(self, initializer)
    def __eq__(self, other):
        return are_planes_equal(self, other)
    @property
    def is_zero(self): return not(self[0] or self[1] or self[2])
    @property
    def magnitude_sq(self): return self[0]**2 + self[1]**2 + self[2]**2
    @property
    def magnitude(self): return sqrt(self[0]**2 + self[1]**2 + self[2]**2)
    mag_sq = magnitude_sq
    mag = magnitude

    @property
    def i(self): return self[0]
    @i.setter
    def i(self, new_val): self[0] = float(new_val)
    @property
    def j(self): return self[1]
    @j.setter
    def j(self, new_val): self[1] = float(new_val)
    @property
    def k(self): return self[2]
    @k.setter
    def k(self, new_val): self[2] = float(new_val)
    @property
    def d(self): return self[3]
    @d.setter
    def d(self, new_val): self[3] = float(new_val)

    def normalize(self):
        div = self.mag
        if div:
            self[0] /= div
            self[1] /= div
            self[2] /= div
            self[3] *= div

    def is_point_on_plane(self, point, use_double_rounding=False,
                          round_adjust=0):
        return is_point_on_plane(
            point, self, use_double_rounding, round_adjust)

    def is_point_on_plane_front(self, point, on_plane_ok=False,
                                use_double_rounding=False, round_adjust=0):
        return is_point_on_front_side_of_plane(
            point, self, on_plane_ok, use_double_rounding, round_adjust)

    def is_point_on_plane_front(self, point, on_plane_ok=False,
                                use_double_rounding=False, round_adjust=0):
        return is_point_on_back_side_of_plane(
            point, self, on_plane_ok, use_double_rounding, round_adjust)

    def find_intersect_line_with_plane(self, other, use_double_rounding=False,
                                       round_adjust=0):
        return find_intersect_line_of_planes(
            self, other, use_double_rounding, round_adjust)


class EdgeLoopNode(list):
    __slots__ = ("vert_index", )

    def __init__(self, vert_index=-1, *children, edges=(), seen=None):
        self.vert_index = int(vert_index)
        if seen is None:
            seen = set()

        if self.vert_index in seen:
            return

        seen.add(self.vert_index)

        if not isinstance(edges, dict):
            edges_by_verts = {}
            for edge in set(edges):
                edges_by_verts.setdefault(edge[0], []).append(edge)
                edges_by_verts.setdefault(edge[1], []).append(edge)

            for vert_index in edges_by_verts:
                self.append(EdgeLoopNode(
                    vert_index, edges=edges_by_verts))
        else:
            for edge in edges.get(self.vert_index, ()):
                if edge[0] == self.vert_index:
                    self.append(EdgeLoopNode(edge[1], edges=edges, seen=set(seen)))

    def __str__(self, **kw):
        depth = kw.pop("depth", 0)
        kw["depth"] = depth + 1
        indent_str = " " * (2 * depth)

        string = "%sEdgeLoopNode(%s" % (indent_str, self.vert_index)
        if not self.is_leaf:
            string += ",\n"
            for node in self:
                string += node.__str__(**kw) + ",\n"
            string += indent_str
        return string + ")"

    __repr__ = __str__

    def walk_edge_loops(self, curr_loop=(), seen=None, horizontal=False):
        if seen is None:
            seen = set()

        if (not horizontal or self.is_leaf) and self.vert_index != -1:
            curr_loop += (self.vert_index, )

        if self.vert_index in seen:
            yield curr_loop
            return

        seen.add(self.vert_index)
        if self.is_leaf:
            yield curr_loop
            return

        # walk down the length of the loop
        for node in self:
            yield from node.walk_edge_loops(curr_loop, seen, horizontal)

        if self.vert_index == -1 or not horizontal:
            return

        # walk horizontally across the loops
        for i in range(len(self)):
            for j in range(len(self)):
                if i == j: continue
                seen_h = {self.vert_index}
                for loop in self[i].walk_edge_loops((self.vert_index, ), seen_h):
                    yield from self[j].walk_edge_loops(loop[::-1], set(seen_h))

    @property
    def is_leaf(self): return not len(self)

    @property
    def depth(self):
        if self.is_leaf:
            return 0
        depth = max(n.depth for n in self)
        if self.vert_index != -1:
            depth += 1
        return depth


def planes_to_verts_and_edge_loops(planes, center, plane_dir=True, max_plane_ct=32,
                                   use_double_rounding=False, round_adjust=0):
    assert len(center) == 3
    # make a set out of the planes to remove duplicates
    planes = list(set(tuple(Plane(p).normalized) for p in planes))
    indices_by_planes = {p: set() for p in planes}

    if len(planes) > max_plane_ct:
        raise ValueError(
            "Provided more planes(%s) than the max plane count(%s)" %
            (len(planes), max_plane_ct))

    is_point_inside_form = (is_point_on_front_side_of_planes if plane_dir
                            else is_point_on_back_side_of_planes)

    # find the intersect points of all planes within the polyhedron
    intersects = []
    intersect_weights = []
    for i in range(len(planes)):
        p0 = planes[i]
        p0_indices = indices_by_planes[p0]
        for j in range(len(planes)):
            if j == i: continue
            p1 = planes[j]
            p1_indices = indices_by_planes[p1]
            for k in range(len(planes)):
                if k == i or k == j: continue
                p2 = planes[k]
                p2_indices = indices_by_planes[p2]

                intersect = find_intersect_point_of_planes(p0, p1, p2)
                if intersect is None or not is_point_inside_form(
                        intersect, planes, True, round_adjust=round_adjust):
                    continue

                weight = abs(matrices.Ray.cross(p0[: -1], p1[: -1]) *
                             matrices.Ray(p2[: -1]))
                better_vert_index = None
                similar_verts = set()
                for w in range(len(intersects)):
                    if matrices.are_vectors_equal(
                            intersects[w], intersect,
                            round_adjust=round_adjust / weight):
                        if intersect_weights[w] > weight:
                            better_vert_index = w
                        else:
                            similar_verts.add(w)

                if better_vert_index is None:
                    # adding a new vert
                    vert_index = len(intersects)
                    intersects.append(intersect)
                    intersect_weights.append(weight)
                else:
                    # using a better intersect than this one
                    vert_index = better_vert_index
                    intersect = intersects[better_vert_index]
                    weight = intersect_weights[better_vert_index]

                # overwrite existing verts with a more accurate one
                for v_i in similar_verts:
                    intersects[v_i] = intersect
                    intersect_weights[v_i] = weight

                p0_indices.add(vert_index)
                p1_indices.add(vert_index)
                p2_indices.add(vert_index)

    vert_map = {}
    vert_rebase_map = [None] * len(intersects)
    pruned_intersects = []
    pruned_intersect_weights = []
    for i in range(len(intersects)):
        vert = tuple(intersects[i])
        if vert not in vert_map:
            vert_map[vert] = len(vert_map)
            pruned_intersects.append(intersects[i])
            pruned_intersect_weights.append(intersect_weights[i])
        vert_rebase_map[i] = vert_map[vert]

    for indices in indices_by_planes.values():
        new_indices = set()
        for i in indices:
            new_indices.add(vert_rebase_map[i])
        indices.clear()
        indices.update(new_indices)

    intersects = pruned_intersects
    intersect_weights = pruned_intersect_weights
    #for i in range(len(intersects)):
    #    print(intersect_weights[i], intersects[i])

    # Get intersection lines by crossing each plane with each other plane.
    lines_by_planes = {plane: set() for plane in planes}
    for p0_i in range(len(planes) - 1):
        for p1_i in range(p0_i + 1, len(planes)):
            p0 = planes[p0_i]
            p1 = planes[p1_i]

            line = find_intersect_line_of_planes(p0, p1)
            if line is None:
                continue

            lines_by_planes[p0].add((tuple(line[0]), tuple(line[1])))
            lines_by_planes[p1].add((tuple(line[0]), tuple(-line[1])))


    edges_by_planes = {plane: set() for plane in planes}
    used_vert_indices = set()
    for plane, lines in lines_by_planes.items():
        used_vert_counts = {i: [] for i in indices_by_planes[plane]}

        # count how many lines each vert lies on
        for line in lines:
            line_weight = matrices.Ray(line[1]).mag
            vert_indices_on_line = set()
            for v_i in used_vert_counts:
                if is_point_on_line(intersects[v_i], line,
                                    round_adjust=(round_adjust/(
                                        intersect_weights[v_i] * line_weight))):
                    vert_indices_on_line.add(v_i)

            # filter out verts only intersecting one line
            if len(vert_indices_on_line) >= 2:
                for v_i in vert_indices_on_line:
                    used_vert_counts[v_i].append(line)

        verts_on_lines = {line: [] for line in lines}
        for v_i, used_lines in used_vert_counts.items():
            if len(used_lines) < 2: continue
            for line in used_lines:
                verts_on_lines[line].append(v_i)

        for line in lines:
            if len(verts_on_lines[line]) < 2:
                continue

            line_point, line_dir = line
            sorted_verts_on_line = {}
            axis = 0
            # figure out which axis has the most precision
            for i in range(1, len(line_dir)):
                if abs(line_dir[i]) > abs(line_dir[axis]):
                    axis = i

            # sort the vertices by how far along the line they are
            for v_i in verts_on_lines[line]:
                axis_val = intersects[v_i][axis]
                dist = (axis_val - line_point[axis]) / line_dir[axis]
                sorted_verts_on_line[dist] = v_i

            verts_on_line = [sorted_verts_on_line[dist]
                             for dist in sorted(sorted_verts_on_line)]

            # if the edge chain will go opposite the line, reverse it
            if matrices.Ray(intersects[verts_on_line[0]] -
                            intersects[verts_on_line[-1]]) * matrices.Ray(line[1]) < 0:
                verts_on_line = verts_on_line[::-1]

            # generate edges that ascendingly follow this line
            for i in range(len(verts_on_line) - 1):
                v0_i = verts_on_line[i]
                v1_i = verts_on_line[i + 1]
                # planes intersect and are not parallel
                edges_by_planes[plane].add((v0_i, v1_i))
                used_vert_indices.update((v0_i, v1_i))


    # prune the unused verts
    verts = [None] * len(used_vert_indices)
    vert_map = {}
    i = 0
    for vert_index in used_vert_indices:
        vert_map[vert_index] = i
        verts[i] = intersects[vert_index]
        i += 1

    for plane, edges in edges_by_planes.items():
        new_edges = set()
        for edge in edges:
            new_edges.add((vert_map[edge[0]], vert_map[edge[1]]))
        edges.clear()
        edges.update(new_edges)

    edge_loops = []
    # loop over each edge and put together an edge loop list
    # by visiting the edges shared by each vert index
    for plane, edges in edges_by_planes.items():
        if not edges:
            continue

        try:
            edge_loop = edges_to_edge_loop(edges, plane, verts)
        except Exception:
            from traceback import format_exc
            print(format_exc())
            continue

        if not edge_loop:
            continue

        edge_loops.append(edge_loop)

    #print("PLANES:", )
    #i = 0
    #for plane in edges_by_planes:
    #    print(i, plane)
    #    for e in edges_by_planes[plane]:
    #        print(e)
    #    print()
    #    i += 1

    #i = 0
    #print("VERTS:", len(verts))
    #for vert in verts:
    #    print(i, vert)
    #    i += 1

    #print("TRIS:", sum(len(edge_loop) - 2 for edge_loop in edge_loops))
    #for edge_loop in edge_loops:
    #    print(edge_loop)

    return verts, edge_loops


def get_is_valid_edge_loop(edge_loop, plane, verts):
    vert_ct = len(edge_loop)
    if vert_ct < 3:
        return False

    # if the edge loop would construct triangles facing the
    # wrong direction, we need to reverse the edge loop
    for i in range(vert_ct):
        tri_plane = matrices.Ray(matrices.vertex_cross_product(
            verts[edge_loop[i]],
            verts[edge_loop[(i + 1) % vert_ct]],
            verts[edge_loop[(i + 2) % vert_ct]]))

        if matrices.dot_product(tri_plane, plane[: 3]) < 0:
            # facing opposite directions
            return False

    return True


def edges_to_edge_loop(edges, plane, verts):
    edge_loop_nodes = EdgeLoopNode(-1, edges=edges)
    #print("DEPTH: ", edge_loop_nodes.depth)
    #print(edges)
    #input(edge_loop_nodes)
    edge_loop = ()
    for curr_loop in edge_loop_nodes.walk_edge_loops():
        if len(curr_loop) < 3 or curr_loop[0] != curr_loop[-1]:
            continue

        curr_loop = curr_loop[: -1]
        if len(curr_loop) < len(edge_loop):
            continue
        elif get_is_valid_edge_loop(curr_loop, plane, verts):
            edge_loop = curr_loop

    for curr_loop in edge_loop_nodes.walk_edge_loops(horizontal=True):
        if len(curr_loop) < 3 or curr_loop[0] != curr_loop[-1]:
            continue

        curr_loop = curr_loop[: -1]
        if len(curr_loop) < len(edge_loop):
            continue
        elif get_is_valid_edge_loop(curr_loop, plane, verts):
            edge_loop = curr_loop

    #print("CHOSEN: ", edge_loop)
    #print()
    if len(edge_loop) < 3:
        return None

    return list(edge_loop)
