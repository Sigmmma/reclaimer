'''
This module implements some basic matrix classes
'''
from math import log, sqrt, cos, sin, atan2, asin, acos, pi
from sys import float_info


class CannotRowReduce(ValueError): pass
class MatrixNotInvertable(ValueError): pass


def are_points_equal(point_0, point_1, use_double_rounding=False,
                     round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23) - round_adjust
    for val_0, val_1 in zip(point_0, point_1):
        # take into account rounding errors for 32bit floats
        val = max(abs(val_0), abs(val_1))
        delta_max = 2**(int(log(val + float_info.epsilon, 2)) - mantissa_len)
        if abs(val_1 - val_0) > delta_max:
            return False
    return True


def are_planes_equal(plane_0, plane_1, use_double_rounding=False,
                     round_adjust=0):
    p0 = Plane(plane_0)
    p1 = Plane(plane_1)
    p0.normalize()
    p1.normalize()
    return are_points_equal(p0, p1, use_double_rounding, round_adjust)


def point_distance_to_plane(point, plane, use_double_rounding=False,
                            round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23) - round_adjust
    # return True if point is on forward side of plane, otherwise False
    # take into account rounding errors for 32bit floats
    delta_max = 2**(
        int(log(abs(plane[3] + float_info.epsilon), 2)) -
        mantissa_len)
    delta = dot_product(plane[:3], point) - plane[3]
    if abs(delta) < delta_max:
        # point lies on plane
        return 0.0
    return delta


def is_point_on_plane(point, plane, use_double_rounding=False,
                      round_adjust=0):
    return point_distance_to_plane(
        point, plane, use_double_rounding, round_adjust) == 0


def is_point_on_front_side_of_plane(point, plane, on_plane_ok=False,
                                    use_double_rounding=False,
                                    round_adjust=0):
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
                                  round_adjust=0):
    # returns an arbitrary point where the provided planes intersect.
    # if they do not intersect, None will be returned instead.
    line_dir = Ray.cross(plane_0[:3], plane_1[:3])
    if line_dir.is_zero:
        # planes are parallel. ignore
        return None

    line_dir.normalize()
    lines_matrix = Matrix((plane_0[: 3], plane_1[: 3], line_dir))
    reduced, result = lines_matrix.row_reduce(
        Matrix((plane_0[3], plane_1[3], 0))
        )
    line_point = Point((result[0][0], result[1][0], result[2][0]))
    return line_point, line_dir


def find_intersect_point_of_lines(line_0, line_1, use_double_rounding=False,
                                  round_adjust=0, ignore_check=False):
    # returns an arbitrary point where the provided lines intersect.
    # if they do not intersect, None will be returned instead.
    v0, d0 = Point(line_0[0]), Ray(line_0[1])
    v1, d1 = Point(line_1[0]), Ray(line_1[1])
    assert len(v0) == len(v1)
    assert len(d0) == len(d1)
    if d0.is_zero or d1.is_zero:
       # one or both vectors are the zero-vector
        return None

    try:
        reduced, result = Matrix([(a, -b) for a, b in zip(d0, d1)]).row_reduce(
            Matrix([v0[i] - v1[i] for i in range(len(v0))]))
    except CannotRowReduce:
        return None

    intersect_a = v0 - d0 * result[0][0]
    intersect_b = v1 - d1 * result[1][0]
    if ignore_check or are_points_equal(intersect_a, intersect_b,
                                        use_double_rounding, round_adjust):
        # point lies on both lines
        return intersect_a + (intersect_b - intersect_a) / 2

    return None


def planes_to_verts_and_edge_loops(planes, plane_dir=False, max_plane_ct=32,
                                   use_double_rounding=False, round_adjust=0):
    # make a set out of the planes to remove duplicates
    planes = list(set(tuple(plane) for plane in planes))
    lines_by_planes = {plane: [] for plane in planes}
    is_point_inside_form = (is_point_on_front_side_of_planes if plane_dir
                            else is_point_on_back_side_of_planes)

    if len(planes) > max_plane_ct:
        raise ValueError(
            "Provided more planes(%s) than the max plane count(%s)" %
            (len(planes), max_plane_ct))

    # Get intersection lines by crossing each plane with each other plane.
    for i in range(len(planes)):
        p0 = planes[i]
        for j in range(i + 1, len(planes)):
            p1 = planes[j]
            line = find_intersect_line_of_planes(p0, p1)
            if line is not None:
                # planes intersect and are not parallel
                lines_by_planes[p0].append(line)
                lines_by_planes[p1].append(line)

    verts = []
    vert_indices_by_raw_verts = {}
    edges_by_planes = {plane: set() for plane in planes}
    # Calculate the points of intersection for each planes edges
    # to determine their vertices, skipping any vertices that are
    # on the forward-facing side of any of the planes.
    for plane, lines in lines_by_planes.items():
        # loop over each line in the plane and find
        # two vertices where two lines intersect
        edges = edges_by_planes[plane]
        for i in range(len(lines)):
            v0_i = v1_i = None
            line = lines[i]

            for j in range(len(lines)):
                if i == j: continue
                intersect = find_intersect_point_of_lines(
                    line, lines[j], ignore_check=True)
                if intersect is None:
                    continue

                intersect = tuple(intersect)
                vert_index = vert_indices_by_raw_verts.get(intersect)
                if vert_index is None:
                    for point in vert_indices_by_raw_verts:
                        if are_points_equal(point, intersect):
                            #print("Found:\n%s\n%s" % (point, intersect))
                            vert_index = vert_indices_by_raw_verts[point]

                if vert_index is None:
                    # make sure the point is not outside the polyhedra
                    if not is_point_inside_form(intersect, planes, True):
                        #print("OUTSIDE: ", intersect)
                        continue
                    #print("INSIDE: ", intersect)
                    vert_index = len(verts)
                    verts.append(intersect)
                    vert_indices_by_raw_verts[intersect] = vert_index

                if v0_i is None:
                    v0_i = vert_index
                elif v1_i is None:
                    v1_i = vert_index
                    break

            #print(i, (v0_i, v1_i))
            if v0_i is None or v1_i is None or v0_i == v1_i:
                #print("FUCK! We couldn't find an intersection point.")
                continue

            # add the edge to this planes list of vert edges
            if v0_i > v1_i:
                v0_i, v1_i = v1_i, v0_i

            edge = (v0_i, v1_i)
            edges.add(edge)

    #print(verts)

    edge_loops = []
    # loop over each edge and put together an edge loop list
    # by visiting the edges shared by each vert index
    for plane, edges in edges_by_planes.items():
        if not edges:
            continue

        try:
            edge_loop = edges_to_edge_loop(edges)
        except Exception:
            continue
        if not edge_loop:
            continue

        # if the edge loop would construct triangles facing the
        # wrong direction, we need to reverse the edge loop
        v0 = verts[edge_loop[0]]
        v1 = verts[edge_loop[1]]
        v2 = verts[edge_loop[2]]
        if dot_product(vertex_cross_product(v0, v1, v2), plane[: 3]) < 0:
            edge_loop[:] = edge_loop[::-1]

        edge_loops.append(edge_loop)

    return verts, edge_loops


def edges_to_edge_loop(edges):
    edge_loop = []

    edges = set((min(edge), max(edge)) for edge in edges)
    edges_by_verts = {}
    for edge in edges:
        edges_by_verts.setdefault(edge[0], []).append(edge)
        edges_by_verts.setdefault(edge[1], []).append(edge)

    if len(edges_by_verts) < 3:
        return None

    curr_edge = next(iter(edges))
    v_i = curr_edge[1]
    edge_loop.append(curr_edge[0])
    edges_by_verts.pop(curr_edge[0])
    while edges_by_verts:
        vert_edges = edges_by_verts.pop(v_i, None)
        if vert_edges is None:
            break

        curr_edge = vert_edges[not vert_edges.index(curr_edge)]
        edge_loop.append(v_i)
        v_i = curr_edge[not curr_edge.index(v_i)]

    if len(edge_loop) < 3:
        return None

    return edge_loop


def line_from_verts(v0, v1):
    return tuple(b - a for a, b in zip(v0, v1))


def vertex_cross_product(v0, v1, v2):
    return cross_product(line_from_verts(v0, v1),
                         line_from_verts(v0, v2))


def cross_product(ray_a, ray_b):
    return ((ray_a[1]*ray_b[2] - ray_a[2]*ray_b[1],
             ray_a[2]*ray_b[0] - ray_a[0]*ray_b[2],
             ray_a[0]*ray_b[1] - ray_a[1]*ray_b[0]))


def dot_product(v0, v1):
    return sum(a*b for a, b in zip(v0, v1))


def euler_to_quaternion(y, p, r):
    '''Angles are expected to be in radians.'''
    c0, c1, c2 = cos(y / 2), cos(p / 2), cos(r / 2)
    s1, s2, s3 = sin(y / 2), sin(p / 2), sin(r / 2)
    return (s1*s2*c2*+ c0*c1*s3,
            s1*c1*c2 + c0*s2*s3,
            c0*s2*c2 - s1*c1*s3,
            c0*c1*c2 - s1*s2*s3)


def quaternion_to_euler(i, j, k, w):
    '''Angles returned are in radians.'''
    p_sin = 2*(i * j + k * w);
    # check for singularities at north and south poles
    if p_sin > 0.99999999999999:
        return 2 * atan2(i, w),   pi / 2, 0
    elif p_sin < -0.99999999999999:
        return -2 * atan2(i, w), -pi / 2, 0
    else:
        y = atan2(2*(j*w - i*k), 1 - 2*(j**2 - k**2));
        p = asin(p_sin);
        r = atan2(2*(i*w - j*k), 1 - 2*(i**2 - k**2))
        return y, p, r
    

def axis_angle_to_quaternion(x, y, z, a):
    '''Angle is expected to be in radians.'''
    a = a / 2
    return x * sin(a), y * sin(a), z * sin(a), cos(a)


def quaternion_to_axis_angle(i, j, k, w):
    assert w <= 1.0 and w >= -1.0
    length = sqrt(1 - w**2)
    return i / length, j / length, k / length, 2 * acos(w)


def multiply_quaternions(q0, q1):
    i =  q0[0] * q1[3] + q0[1] * q1[2] - q0[2] * q1[1] + q0[3] * q1[0]
    j = -q0[0] * q1[2] + q0[1] * q1[3] + q0[2] * q1[0] + q0[3] * q1[1]
    k =  q0[0] * q1[1] - q0[1] * q1[0] + q0[2] * q1[3] + q0[3] * q1[2]
    w = -q0[0] * q1[0] - q0[1] * q1[1] - q0[2] * q1[2] + q0[3] * q1[3]
    return type(q0)((i, j, k, w))


def quaternion_to_matrix(i, j, k, w):
    return Matrix([
        (2*(0.5 - j*j - k*k),   2*(i*j + k*w),         2*(i*k - j*w)),
        (2*(i*j - k*w),         2*(0.5 - k*k - i*i),   2*(j*k + i*w)),
        (2*(i*k + j*w),         2*(j*k - i*w),         2*(0.5 - i*i - j*j)),
    ])


def matrix_to_quaternion(matrix):
    m00, m10, m20 = matrix[0]
    m01, m11, m21 = matrix[1]
    m02, m12, m22 = matrix[2]
    tr = m00 + m11 + m22

    if tr > 0:
        s = sqrt(tr+1.0) * 2
        i = (m21 - m12) / s
        j = (m02 - m20) / s
        k = (m10 - m01) / s
        w = 0.25 * s
    elif m00 > m11 and m00 > m22:
        s = sqrt(1.0 + m00 - m11 - m22) * 2
        i = 0.25 * s
        j = (m01 + m10) / s
        k = (m02 + m20) / s
        w = (m21 - m12) / s
    elif m11 > m22:
        s = sqrt(1.0 + m11 - m00 - m22) * 2
        i = (m01 + m10) / s
        j = 0.25 * s
        k = (m12 + m21) / s
        w = (m02 - m20) / s
    else:
        s = sqrt(1.0 + m22 - m00 - m11) * 2
        i = (m02 + m20) / s
        j = (m12 + m21) / s
        k = 0.25 * s
        w = (m10 - m01) / s

    return i, j, k, w


# shorthand names
matrix_to_quat = matrix_to_quaternion
quat_to_matrix = quaternion_to_matrix
euler_to_quat = euler_to_quaternion
quat_to_euler = quaternion_to_euler
axis_angle_to_quat = axis_angle_to_quaternion
quat_to_axis_angle = quaternion_to_axis_angle
multiply_quats = multiply_quaternions


class FixedLengthList(list):
    __slots__ = ()
    def append(self, val): raise NotImplementedError
    def extend(self, vals): raise NotImplementedError
    def insert(self, index, val): raise NotImplementedError
    def pop(self): raise NotImplementedError
    def __delitem__(self): raise NotImplementedError
    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if start > stop:
                start, stop = stop, start
            if start == stop:
                return
            elif step < 0:
                step = -step

            slice_size = (stop - start) // step

            if slice_size != len(val):
                raise ValueError(("attempt to assign sequence of size %s to "
                                  "slice of size %s") % (len(val), slice_size))

        list.__setitem__(self, index, val)


class Vector(list):
    __slots__ = ()
    '''Implements the minimal methods required for messing with matrix rows'''
    def __neg__(self):
        return type(self)(-x for x in self)
    def __add__(self, other):
        new = type(self)(self)
        for i in range(len(other)): new[i] += other[i]
        return new
    def __sub__(self, other):
        new = type(self)(self)
        for i in range(len(other)): new[i] -= other[i]
        return new
    def __mul__(self, other):
        if isinstance(other, type(self)):
            return sum(self[i]*other[i] for i in range(len(self)))
        new = type(self)(self)
        for i in range(len(self)): new[i] *= other
        return new
    def __truediv__(self, other):
        if isinstance(other, type(self)):
            return cross_product(self, other)
        new = type(self)(self)
        for i in range(len(self)): new[i] /= other
        return new
    def __iadd__(self, other):
        for i in range(len(other)): self[i] += other[i]
        return self
    def __isub__(self, other):
        for i in range(len(other)): self[i] -= other[i]
        return self
    def __imul__(self, other):
        if isinstance(other, type(self)):
            raise NotImplementedError
        for i in range(len(self)): self[i] *= other
        return self
    def __itruediv__(self, other):
        if isinstance(other, type(self)):
            raise NotImplementedError
        for i in range(len(self)): self[i] /= other
        return self

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    

class Point(Vector):
    __slots__ = ()
    def __eq__(self, other):
        return are_points_equal(self, other)


class Ray(Vector):
    __slots__ = ()
    @property
    def is_zero(self): return not sum(bool(val) for val in self)
    @property
    def normalized(self):
        ray = Ray(self)
        ray.normalize()
        return ray
    @property
    def magnitude_sq(self): return sum(v**2 for v in self)
    @property
    def magnitude(self): return sqrt(sum(v**2 for v in self))
    mag_sq = magnitude_sq
    mag = magnitude

    @classmethod
    def cross(cls, v0, v1):
        assert len(v0) >= 3
        assert len(v1) >= 3
        return Ray(cross_product(v0, v1))
    @classmethod
    def dot(cls, v0, v1):
        assert len(v0) == len(v1)
        return dot_product(v0, v1)

    def normalize(self):
        div = self.magnitude
        if div:
            for i in range(len(self)): self[i] /= div


class Plane(FixedLengthList, Ray):
    __slots__ = ()
    def __init__(self, initializer=None):
        if initializer is None:
            initializer = (0, 0, 1, 0)
        assert len(initializer) == 4
        list.__init__(self, initializer)
    def __eq__(self, other):
        return are_planes_equal(self, other)
    @property
    def magnitude_sq(self): return self[3]**2
    @property
    def magnitude(self): return self[3]
    mag_sq = magnitude_sq
    mag = magnitude

    def normalize(self):
        div = self[3]
        if div:
            for i in range(len(self)): self[i] /= div

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


class Quaternion(FixedLengthList, Ray):
    __slots__ = ()
    def __init__(self, initializer=None):
        if initializer is None:
            initializer = (0, 0, 0, 1)
        assert len(initializer) == 4
        list.__init__(self, initializer)
    def __mul__(self, other):
        if isinstance(other, Quaternion):
            return sum(self[i]*other[i] for i in range(len(self)))
        new = Ray(self)
        for i in range(len(self)): new[i] *= other
        return new
    def __imul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(multiply_quaternions(self, other))
        for i in range(len(self)): self[i] *= other
        return self
    __rmul__ = __mul__

    @classmethod
    def to_euler(cls, self):
        return Vector(quaternion_to_euler(*self))
    @classmethod
    def to_axis_angle(cls, self):
        return Vector(quaternion_to_axis_angle(*self))
    @classmethod
    def to_matrix(cls, self):
        return quaternion_to_matrix(*self)


class MatrixRow(FixedLengthList, Vector):
    __slots__ = ()


class Matrix(list):
    width = 1
    height = 1

    def __init__(self, matrix=None, width=1, height=1, identity=False):
        if matrix is None:
            self.width = width
            self.height = height
            list.__init__(self, (MatrixRow((0,)*width) for i in range(height)))

            if identity and width <= height:
                # place the identity matrix into the inverse
                for i in range(self.width):
                    self[i][i] = 1.0
            return

        matrix_rows = []
        self.height = max(1, len(matrix))
        self.width = -1
        for row in matrix:
            if not hasattr(row, '__iter__'):
                row = [row]
            self.width = max(self.width, len(row))
            assert self.width and len(row) == self.width
            matrix_rows.append(MatrixRow(row[:]))
        list.__init__(self, matrix_rows)

    def __setitem__(self, index, new_row):
        assert len(new_row) == self.width
        list.__setitem__(self, index, MatrixRow(new_row))

    def __delitem__(self, index):
        self[index][:] = (0,)*self.width

    def __str__(self):
        matrix_str = "Matrix([\n%s])"
        insert_str = ''
        for row in self:
            insert_str += '%s,\n' % (row,)
        return matrix_str % insert_str

    def __neg__(self):
        return Matrix([-row for row in self])

    def __add__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        new = Matrix(self)
        for i in range(len(other)): new[i] += other[i]
        return new

    def __sub__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        new = Matrix(self)
        for i in range(len(other)): new[i] -= other[i]
        return new

    def __mul__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            new = Matrix(self)
            for row in new:
                row *= other
            return new

        assert self.width == other.height
        # transpose the matrix so its easier to work with
        new = Matrix(width=other.width, height=self.height)
        other = other.transpose

        # loop over each row in the new matrix
        for i in range(new.height):
            # loop over each column in the new matrix
            for j in range(new.width):
                # set the element equal to the dot product of the matrix rows
                new[i][j] = self[i]*other[j]

        return new

    def __truediv__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            new = Matrix(self)
            for row in new:
                row /= other
            return new
        assert self.width == other.height
        return self * other.inverse

    __repr__ = __str__
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def __iadd__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        for i in range(len(other)): self[i] += other[i]
        return self

    def __isub__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        for i in range(len(other)): self[i] -= other[i]
        return self

    def __imul__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            for row in self:
                row *= other
            return self

        assert self.width == other.height
        # transpose the matrix so its easier to work with
        new = Matrix(width=other.width, height=self.height)
        other = other.transpose

        # loop over each row in the new matrix
        for i in range(new.height):
            # loop over each column in the new matrix
            for j in range(new.width):
                # set the element equal to the dot product of the matrix rows
                new[i][j] = self[i]*other[j]

        # replace the values in this matrix with those in the new matrix
        self.width = 0
        self.height = new.height
        for i in range(self.height):
            self.width = len(self[i])
            self[i] = new[i]

        return self

    def __itruediv__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            for row in self:
                row /= other
            return self
        self *= other.inverse
        return self

    def to_quaternion(self):
        assert self.width == 3
        assert self.height == 3
        return Quaternion(matrix_to_quaternion(self))

    @property
    def determinant(self):
        assert self.width == self.height, "Non-square matrices do not have determinants."
        if self.width == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        d = 0
        sub_matrix = Matrix(width=self.width - 1, height=self.height - 1)
        for i in range(self.width):
            for j in range(sub_matrix.height):
                for k in range(sub_matrix.width):
                    sub_matrix[j][k] = self[j+1][(i + k + 1) % self.width]
            d += self[0][i] * sub_matrix.determinant
            
        return d

    @property
    def transpose(self):
        transpose = Matrix(width=self.height, height=self.width)
        for r in range(self.height):
            for c in range(self.width):
                transpose[c][r] = self[r][c]
        return transpose

    @property
    def inverse(self, find_best_inverse=True):
        # cannot invert non-square matrices. check for that
        if self.width != self.height:
            raise MatrixNotInvertable("Cannot invert non-square matrix.")
        elif not self.determinant:
            raise MatrixNotInvertable("Matrix is non-invertible.")

        regular, inverse = self.row_reduce(
            Matrix(width=self.width, height=self.height, identity=True),
            find_best_reduction=find_best_inverse
            )

        return inverse

    def row_reduce(self, other, find_best_reduction=True):
        # cant row-reduce if number of columns is greater than number of rows
        assert self.width <= self.height

        # WIDTH NOTE: We will loop over the width rather than height for
        #     several things here, as we do not care about any rows that
        #     don't intersect the columns at a diagonal. Essentially we're
        #     treating a potentially non-square matrix as square(we're
        #     ignoring the higher numbered rows) by rearranging the rows.

        new_row_order = self.get_row_reduce_order(find_best_reduction)
        if new_row_order is None:
            raise CannotRowReduce(
                "Impossible to rearrange rows to row-reduce:\n%s" % self)

        reduced = Matrix(self)
        orig_other = list(other)
        # rearrange rows so diagonals are all non-zero
        for i in range(len(new_row_order)):
            reduced[i] = self[new_row_order[i]]
            other[i] = orig_other[new_row_order[i]]

        orig_reduced = Matrix(reduced)  # TEMP
        for i in range(self.width):  # read note about looping over width
            # divide both matrices by their diagonal values
            div = reduced[i][i]
            if not div:
                raise CannotRowReduce("Impossible to row-reduce.")

            reduced[i] /= div
            other[i] /= div

            # make copies of the rows that we can multiply for subtraction
            reduced_diff = MatrixRow(reduced[i])
            other_diff = MatrixRow(other[i])

            # loop over the rows NOT intersecting the column at the diagonal
            for j in range(self.width):
                if i == j:
                    continue
                # get the value that needs to be subtracted from
                # where this row intersects the current column
                mul = reduced[j][i]

                # subtract the difference row from each of the
                # rows above it to set everything in the column
                # above an below the diagonal intersection to 0
                reduced[j] -= reduced_diff*mul
                other[j] -= other_diff*mul

        return reduced, other

    def get_row_reduce_order(self, find_best_reduction=True):
        nonzero_diag_row_indices = list(set() for i in range(self.width))
        valid_row_orders = {}

        # determine which rows have a nonzero value on each diagonal
        for i in range(self.height):
            for j in range(self.width):
                if self[i][j]:
                    nonzero_diag_row_indices[j].add(i)

        self._get_valid_diagonal_row_orders(
            nonzero_diag_row_indices, valid_row_orders, find_best_reduction)

        # get the highest weighted row order
        test_matrix = Matrix(width=self.width, height=self.width)
        for weight in sorted(valid_row_orders):
            for row_order in valid_row_orders[weight]:
                for i in range(len(row_order)):
                    test_matrix[i][:] = self[row_order[i]]

                # make sure the determinant of the matrix made from the
                # row order isn't zero. if it is, the matrix isnt solvable
                if test_matrix.determinant:
                    return row_order

        return None

    def _get_valid_diagonal_row_orders(self, row_indices, row_orders,
                                       choose_best=True, row_order=(),
                                       curr_column=0):
        row_order = list(row_order)
        column_count = len(row_indices)
        if not row_order:
            row_order = [None] * column_count

        # loop over each row with a non-zero value on this diagonal
        for i in row_indices[curr_column]:
            if row_orders and not choose_best:
                # found a valid row arrangement, don't keep checking
                break
            elif i in row_order:
                continue

            row_order[curr_column] = i
            if curr_column + 1 == column_count:
                weight = 1.0
                for j in range(len(row_order)):
                    weight *= abs(self[row_order[j]][j])

                # freeze this row order in place
                row_orders.setdefault(weight, []).append(tuple(row_order))
            else:
                # check the rest of the rows
                self._get_valid_diagonal_row_orders(
                    row_indices, row_orders, choose_best,
                    row_order, curr_column + 1)
