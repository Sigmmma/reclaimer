'''
This module implements some basic matrix classes
'''
from math import log, sqrt, cos, sin, atan2, asin, acos, pi
from sys import float_info


def is_point_on_forward_side_of_plane(plane, point, mantissa_len=23):
    # return True if point is on forward side of plane, otherwise False
    # take into account rounding errors for 32bit floats
    delta_max = 2**(
        int(log(abs(plane[3] + float_info.epsilon), 2)) -
        mantissa_len)

    delta = dot_product(plane[:3], point) - plane[3]
    if abs(delta) < delta_max:
        # point lies on plane
        return False
    return delta > 0


def is_point_on_forward_side_of_planes(planes, point):
    for plane in planes:
        if is_point_on_forward_side_of_plane(plane, point):
            return True
    return False


def find_intersect_line_of_planes(plane_0, plane_1):
    # returns an arbitrary point where the provided planes intersect.
    # if they do not intersect, None will be returned instead.
    line_point = [0, 0, 0]
    line_dir = cross_product(plane_0[:3], plane_1[:3])

    if not (line_dir[0] or line_dir[1] or line_dir[2]):
        # parallel planes. ignore
        return None

    return line_point, line_dir


def find_intersect_point_of_lines(line_0, line_1, mantissa_len=23):
    # returns an arbitrary point where the provided lines intersect.
    # if they do not intersect, None will be returned instead.
    v0, d0 = tuple(MatrixRow(v) for v in line_0)
    v1, d1 = tuple(MatrixRow(v) for v in line_1)
    assert len(v0) == len(v1)
    assert len(d0) == len(d1)
    if not((max(d0) or min(d0)) and (max(d1) or min(d1))):
       # one or both vectors are the zero-vector
        return None

    if d0.normalized == d1.normalized:
        # if the directions are the same, normalize their verts
        # and use those as the interesects. if they're on the
        # same line, they'll normalize to the same point.
        v0.normalize()
        v1.normalize()
        intersect_a, intersect_b = v0, v1
    else:
        # Goal: find the point where these equations hold true:
        #    v0_a + d0_a*t0 == v1_a + d1_a*t1
        #    v0_b + d0_b*t0 == v1_b + d1_b*t1

        lines_matrix = Matrix(list((v0, v1) for v0, v1 in zip(d0, d1)))
        reduced, result = lines_matrix.row_reduce(Matrix(v1 - v0))
        #print(lines_matrix)
        #print(reduced)
        #print(result)
        t0 = result[0][0]
        t1 = result[1][0]

        #print("T0: ", t0)
        #print("T1: ", t1)
        intersect_a = v0 + d0 * t0
        intersect_b = v1 - d1 * t1

    #print("A:", intersect_a)
    #print("B:", intersect_b)
    intersect_diff = intersect_b - intersect_a

    for val_0, val_1, diff in zip(intersect_b, intersect_a, intersect_diff):
        # take into account rounding errors for 32bit floats
        val = max(abs(val_0), abs(val_1))
        delta_max = 2**(int(log(val + float_info.epsilon, 2)) - mantissa_len)
        if abs(diff) > delta_max:
            return None

    # point lies on both lines
    return list(intersect_a + intersect_diff / 2)


def planes_to_verts_and_edge_loops(planes, max_plane_ct=32):
    # make a set out of the planes to remove duplicates
    planes = list(set(tuple(plane) for plane in planes))
    lines_by_planes = {}

    if len(planes) > max_plane_ct:
        raise ValueError(
            "Provided more planes(%s) than the max plane count(%s)" %
            (len(planes), max_plane_ct))

    # Get the edge lines for each plane by crossing the plane with
    # each other plane. If they are parallel, their cross product
    # will be the zero vector and should be ignored.
    for i in range(len(planes)):
        p0 = planes[i]
        for j in range(len(planes)):
            if i == j: continue

            line = find_intersect_line_of_planes(p0, planes[j])
            if line is not None:
                # planes intersect and are not parallel
                lines_by_planes.setdefault(p0, []).append(line)

    verts = []
    vert_indices_by_raw_verts = {}
    edges_by_planes = {plane: [] for plane in planes}
    edges_by_verts_by_planes = {plane: [] for plane in planes}
    # Calculate the points of intersection for each planes edges
    # to determine their vertices, skipping any vertices that are
    # on the forward-facing side of any of the planes.
    for plane, lines in lines_by_planes.items():
        # loop over each line in the plane and find
        # two vertices where two lines intersect
        for i in range(len(lines)):
            v0_i = v1_i = None
            line = lines[i]
            for j in range(i + 1, len(lines)):
                intersect = tuple(find_intersect_point_of_lines(
                    line, lines[j]))

                if intersect in vert_indices_by_raw_verts:
                    vert_index = vert_indices_by_raw_verts[intersect]
                elif intersect is not None:
                    # make sure the point is not outside the polyhedra
                    if is_point_on_forward_side_of_planes(planes, intersect):
                        continue
                    vert_index = len(verts)
                    verts.append(intersect)
                    vert_indices_by_raw_verts[intersect] = vert_index
                else:
                    continue

                if   v0_i is None: v0_i = vert_index
                elif v1_i is None: v1_i = vert_index
                else: break

            if v0_i is None or v1_i is None:
                #print("FUCK! We couldn't find an intersection point.")
                continue

            # add the edge to this planes list of vert edges
            edge = (v0_i, v1_i)
            edges_by_planes[plane].append(edge)
            edges_by_verts_by_planes[plane].setdefault(v0_i, []).append(edge)
            edges_by_verts_by_planes[plane].setdefault(v1_i, []).append(edge)


    edge_loops = []
    # loop over each edge and put together an edge loop list
    # by visiting the edges shared by each vert index
    for plane, edges in edges_by_planes.items():
        edge_loop = []
        edge_loops.append(edge_loop)
        edges_by_verts = edges_by_verts_by_planes[plane]

        curr_edge = edges[0]
        edge_loop.append(curr_edge[0])
        edges_by_verts.pop(curr_edge[0])
        v_i = curr_edge[1]
        while edges_by_verts:
            vert_edges = edges_by_verts.pop(v_i, None)
            if vert_edges is None:
                break

            curr_edge = vert_edges[not vert_edges.index(curr_edge)]
            edge_loop.append(v_i)
            v_i = curr_edge[not curr_edge.index(v_i)]

        # if the edge loop would construct triangles facing the
        # wrong direction, we need to reverse the edge loop
        v0 = verts[edge_loop[0]]
        v1 = verts[edge_loop[1]]
        v2 = verts[edge_loop[2]]
        if dot_product(vertex_cross_product(v0, v1, v2), plane[: 3]) < 0:
            edge_loop[:] = edge_loop[::-1]

    return verts, edge_loops


def line_from_verts(v0, v1):
    return tuple(b - a for a, b in zip(v0, v1))


def vertex_cross_product(v0, v1, v2):
    return cross_product(line_from_verts(v0, v1),
                         line_from_verts(v0, v2))


def cross_product(ray_a, ray_b):
    return [ray_a[1]*ray_b[2] - ray_a[2]*ray_b[1],
            ray_a[2]*ray_b[0] - ray_a[0]*ray_b[2],
            ray_a[0]*ray_b[1] - ray_a[1]*ray_b[0]]


def dot_product(v0, v1):
    assert len(v0) == len(v1)
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
    assert len(q0) == 4
    assert len(q1) == 4
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


class MatrixRow(list):
    '''Implements the minimal methods required for messing with matrix rows'''
    def __neg__(self):
        return MatrixRow(-x for x in self)
    def __add__(self, other):
        new = MatrixRow(self)
        for i in range(len(other)): new[i] += other[i]
        return new
    def __sub__(self, other):
        new = MatrixRow(self)
        for i in range(len(other)): new[i] -= other[i]
        return new
    def __mul__(self, other):
        if isinstance(other, MatrixRow):
            return sum(self[i]*other[i] for i in range(len(self)))
        new = MatrixRow(self)
        for i in range(len(self)): new[i] *= other
        return new
    def __truediv__(self, other):
        if isinstance(other, MatrixRow):
            return sum(self[i]/other[i] for i in range(len(self)))
        new = MatrixRow(self)
        for i in range(len(self)): new[i] /= other
        return new
    def __iadd__(self, other):
        for i in range(len(other)): self[i] += other[i]
        return self
    def __isub__(self, other):
        for i in range(len(other)): self[i] -= other[i]
        return self
    def __imul__(self, other):
        if isinstance(other, MatrixRow):
            return sum(self[i]*other[i] for i in range(len(self)))
        for i in range(len(self)): self[i] *= other
        return self
    def __itruediv__(self, other):
        if isinstance(other, MatrixRow):
            return sum(self[i]/other[i] for i in range(len(self)))
        for i in range(len(self)): self[i] /= other
        return self
    def normalize(self):
        div = self.magnitude
        if div:
            for i in range(len(self)): self[i] /= div
    @property
    def normalized(self):
        vector = MatrixRow(self)
        vector.normalize()
        return vector
    @property
    def magnitude_sq(self): return sum(v**2 for v in self)
    @property
    def magnitude(self): return sqrt(sum(v**2 for v in self))
    mag_sq = magnitude_sq
    mag = magnitude

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__


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
        assert self.width == self.height, "Cannot invert non-square matrix."
        assert self.determinant != 0, "Matrix is non-invertible."

        regular, inverse = self.row_reduce(
            Matrix(width=self.width, height=self.height, identity=True),
            find_best_reduction=find_best_inverse
            )

        return inverse

    def row_reduce(self, other, find_best_reduction=True):
        # cant row-reduce if number of columns is greater than number of rows
        assert self.width <= self.height

        # IN THE FUTURE I NEED TO REARRANGE THE MATRIX SO THE VALUES
        # ALONG THE DIAGONAL ARE GUARANTEED TO BE NON-ZERO. IF THAT
        # CANT BE ACCOMPLISHED FOR ANY COLUMN, ITS COMPONENT IS ZERO.
        # EDIT: It's the future now
        rearrange_rows = False

        # WIDTH NOTE: We will loop over the width rather than height for
        #     several things here, as we do not care about any rows that
        #     don't intersect the columns at a diagonal. Essentially we're
        #     treating a potentially non-square matrix as square(we're
        #     ignoring the higher numbered rows) by rearranging the rows.

        # determine if rows need to be rearranged to calculate inverse
        for i in range(self.width):  # read note about looping over width
            largest = max(abs(self[i][j]) for j in range(self.width))
            if abs(self[i][i]) < largest:
                rearrange_rows = True
                break

        reduced = Matrix(self)
        if rearrange_rows:
            new_row_order = self.get_row_reduce_order(find_best_reduction)
            # rearrange rows so diagonals are all non-zero
            orig_other = list(other)
            for i in range(len(new_row_order)):
                reduced[i] = self[new_row_order[i]]
                other[i] = orig_other[new_row_order[i]]

        for i in range(self.width):  # read note about looping over width
            # divide both matrices by their diagonal values
            div = reduced[i][i]
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

        if not valid_row_orders:
            raise ValueError("Impossible to rearrange rows to row-reduce.")

        # get the highest weighted row order
        return valid_row_orders[max(valid_row_orders)]

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
                row_orders[weight] = tuple(row_order)
            else:
                # check the rest of the rows
                self._get_valid_diagonal_row_orders(
                    row_indices, row_orders, choose_best,
                    row_order, curr_column + 1)
