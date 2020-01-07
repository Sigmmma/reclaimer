#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
This module implements some basic matrix classes
'''
from math import log, sqrt, cos, sin, atan2, asin, acos, pi
from sys import float_info


class CannotRowReduce(ValueError): pass
class MatrixNotInvertable(ValueError): pass
class QuaternionNotInvertable(ValueError): pass


def are_vectors_equal(vector_0, vector_1, use_double_rounding=False,
                      round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23)
    for val_0, val_1 in zip(vector_0, vector_1):
        # take into account rounding errors for 32bit floats
        val = max(abs(val_0), abs(val_1))
        delta_max = 2**(
            int(log(val + float_info.epsilon, 2)) -
            mantissa_len) + abs(round_adjust)
        if abs(val_1 - val_0) > delta_max:
            return False
    return True


def vertex_cross_product(v0, v1, v2):
    return cross_product(line_from_verts(v0, v1),
                         line_from_verts(v0, v2))


def cross_product(ray_a, ray_b):
    return ((ray_a[1]*ray_b[2] - ray_a[2]*ray_b[1],
             ray_a[2]*ray_b[0] - ray_a[0]*ray_b[2],
             ray_a[0]*ray_b[1] - ray_a[1]*ray_b[0]))


def dot_product(v0, v1):
    return sum(a*b for a, b in zip(v0, v1))


def line_from_verts(v0, v1):
    return tuple(b - a for a, b in zip(v0, v1))


def euler_2d_to_vector_3d(y, p):
    '''Angles are expected to be in radians.'''
    return (cos(y) * cos(p),
            sin(y) * cos(p),
            sin(p))


def euler_to_quaternion(y, p, r):
    '''Angles are expected to be in radians.'''
    c0, c1, c2 = cos(y / 2), cos(p / 2), cos(r / 2)
    s0, s1, s2 = sin(y / 2), sin(p / 2), sin(r / 2)
    return (s0*s1*c2 + c0*c1*s2, s0*c1*c2 + c0*s1*s2,
            c0*s1*c2 - s0*c1*s2, c0*c1*c2 - s0*s1*s2)


def quaternion_to_euler(i, j, k, w):
    '''Angles returned are in radians.'''
    p_sin = 2*(i * j + k * w)
    # check for singularities at north and south poles
    if p_sin > 0.999999999999:
        return 2 * atan2(i, w),   pi / 2, 0
    elif p_sin < -0.999999999999:
        return -2 * atan2(i, w), -pi / 2, 0
    else:
        y = atan2(2*(j*w - i*k), 1 - 2*(j**2 + k**2))
        p = asin(p_sin)
        r = atan2(2*(i*w - j*k), 1 - 2*(i**2 + k**2))
        return y, p, r


def axis_angle_to_quaternion(x, y, z, a):
    '''Angle is expected to be in radians.'''
    a /= 2
    sa = sin(a)
    return x * sa, y * sa, z * sa, cos(a)


def quaternion_to_axis_angle(i, j, k, w):
    ray_len = sqrt(i**2 + j**2 + k**2 + w**2)
    i /= ray_len
    j /= ray_len
    k /= ray_len
    w /= ray_len

    length = sqrt(1 - w**2)
    if length == 0.0:
        return i, j, k, 0
    return i / length, j / length, k / length, 2 * acos(w)


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


def multiply_quaternions(q0, q1):
    i =  q0[0] * q1[3] + q0[1] * q1[2] - q0[2] * q1[1] + q0[3] * q1[0]
    j = -q0[0] * q1[2] + q0[1] * q1[3] + q0[2] * q1[0] + q0[3] * q1[1]
    k =  q0[0] * q1[1] - q0[1] * q1[0] + q0[2] * q1[3] + q0[3] * q1[2]
    w = -q0[0] * q1[0] - q0[1] * q1[1] - q0[2] * q1[2] + q0[3] * q1[3]
    div = i**2 + j**2 + k**2 + w**2
    if not div:
        # not sure if we should raise an error.
        # this multiplication makes no sense.
        i = j = k = 0.0
        w = 1.0
    else:
        div = sqrt(div)
        i /= div
        j /= div
        k /= div
        w /= div

    return type(q0)((i, j, k, w))


# shorthand names
matrix_to_quat = matrix_to_quaternion
quat_to_matrix = quaternion_to_matrix
euler_to_quat = euler_to_quaternion
quat_to_euler = quaternion_to_euler
axis_angle_to_quat = axis_angle_to_quaternion
quat_to_axis_angle = quaternion_to_axis_angle
multiply_quats = multiply_quaternions


def clip_angle_to_bounds(angle, step=pi):
    angle -= step * 2 * int(angle / (2 * step))

    if angle < -step:
        return angle + step * 2
    elif angle > step:
        return angle - step * 2
    return angle


def lerp_blend_vectors(v0, v1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - r1
    return [a*r0 + b*r1 for a, b in zip(v0, v1)]


def nlerp_blend_quaternions(q0, q1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - ratio

    i0, j0, k0, w0 = q0
    i1, j1, k1, w1 = q1

    cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        r1 = -r1

    return [i0*r0 + i1*r1, j0*r0 + j1*r1, k0*r0 + k1*r1, w0*r0 + w1*r1]


def slerp_blend_quaternions(q0, q1, ratio):
    ratio = max(0.0, min(1.0, ratio))

    i0, j0, k0, w0 = q0
    i1, j1, k1, w1 = q1

    cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
    half_theta = acos(cos_half_theta) if abs(cos_half_theta) < 1.0 else 0.0

    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        cos_half_theta = -cos_half_theta
        i1 = -i1
        j1 = -j1
        k1 = -k1
        w1 = -w1

    # angle is not well defined in floating point at this point
    if cos_half_theta > 0.9999999:
        r0 = 1.0 - ratio
        r1 = ratio
    else:
        sin_half_theta = sqrt(max(1 - cos_half_theta**2, 0))
        r0 = sin((1.0 - ratio) * half_theta) / sin_half_theta
        r1 = sin(ratio * half_theta) / sin_half_theta

    return [i0*r0 + i1*r1, j0*r0 + j1*r1, k0*r0 + k1*r1, w0*r0 + w1*r1]


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
    def __eq__(self, other):
        return are_vectors_equal(self, other)
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


class Ray(Vector):
    __slots__ = ()
    @property
    def is_zero(self): return not sum(bool(val) for val in self)
    @property
    def normalized(self):
        ray = type(self)(self)
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


class Quaternion(FixedLengthList, Ray):
    __slots__ = ()
    def __init__(self, initializer=(0, 0, 0, 1)):
        assert len(initializer) == 4
        list.__init__(self, initializer)
    def __mul__(self, other):
        if isinstance(other, Quaternion):
            new = Quaternion(multiply_quaternions(self, other))
        else:
            new = Ray(self)
            for i in range(len(self)): new[i] *= other
        return new
    def __imul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(multiply_quaternions(self, other))
        for i in range(len(self)): self[i] *= other
        return self
    __rmul__ = __mul__

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
    def w(self): return self[3]
    @w.setter
    def w(self, new_val): self[3] = float(new_val)

    @property
    def to_euler(self):
        return Vector(quaternion_to_euler(*self))
    @property
    def to_axis_angle(self):
        return Vector(quaternion_to_axis_angle(*self))
    @property
    def to_matrix(self):
        return quaternion_to_matrix(*self)
    @property
    def inverse(self):
        copy = Quaternion(self)
        copy.invert()
        return copy

    def invert(self):
        div = self.i**2 + self.j**2 + self.k**2 + self.w**2
        if not div:
            raise QuaternionNotInvertable("%s is not invertable." % self)

        div = sqrt(div)
        self.i = -self.i / div
        self.j = -self.j / div
        self.k = -self.k / div
        self.w =  self.w / div


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
        for weight in reversed(sorted(valid_row_orders)):
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
