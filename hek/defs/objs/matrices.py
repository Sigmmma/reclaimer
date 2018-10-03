'''
This module implements some basic matrix classes
'''
from math import log, sqrt, cos, sin, atan2, asin, acos, pi


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

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__


class Matrix(list):
    width = 1
    height = 1

    def __init__(self, matrix=None, width=1, height=1):
        if matrix is None:
            self.width = width
            self.height = height
            list.__init__(self, (MatrixRow((0,)*width) for i in range(height)))
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
    def transpose(self):
        transpose = Matrix(width=self.height, height=self.width)
        for r in range(self.height):
            for c in range(self.width):
                transpose[c][r] = self[r][c]
        return transpose

    @property
    def inverse(self):
        # cannot invert non-square matrices. check for that
        assert self.width == self.height
        regular = Matrix(self)
        inverse = Matrix(width=self.width, height=self.height)

        # place the identity matrix into the inverse
        for i in range(inverse.width):
            inverse[i][i] = 1.0

        # IN THE FUTURE I NEED TO REARRANGE THE MATRIX SO THE VALUES
        # ALONG THE DIAGONAL ARE GUARANTEED TO BE NON-ZERO. IF THAT
        # CANT BE ACCOMPLISHED FOR ANY COLUMN, ITS COMPONENT IS ZERO.

        for i in range(self.height):
            # divide both matrices by their diagonal values
            # THIS DOES NOT MAKE SURE THAT THE DIAGONALS ARE NON-ZERO
            div = regular[i][i]
            regular[i] /= div
            inverse[i] /= div

            # make copies of the rows that we can multiply for subtraction
            reg_diff = MatrixRow(regular[i])
            inv_diff = MatrixRow(inverse[i])

            # loop over the rows NOT intersecting the column at the diagonal
            for j in range(self.width):
                if i == j:
                    continue
                # get the value that needs to be subtracted from
                # where this row intersects the current column
                mul = regular[j][i]

                # subtract the difference row from each of the
                # rows above it to set everything in the column
                # above an below the diagonal intersection to 0
                regular[j] -= reg_diff*mul
                inverse[j] -= inv_diff*mul

        return inverse

