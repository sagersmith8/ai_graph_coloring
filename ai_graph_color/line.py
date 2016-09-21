class Line:
    def __init__(self, point_a, point_b):
        """
        Make a new line from two points.

        :param point_a: one of the points on the line
        :type point_a: tuple(float, float)
        :param point_b: one of the points on the line
        :type point_b: tuple(float, float)
        """
        self.left_point = min(point_a, point_b)
        self.right_point = max(point_a, point_b)
        self.distance = point_distance(point_a, point_b)
        self.deallocation_routines = []

    def add_reference(self, deallocation_routine, *params):
        """
        Add a deallocation routine for when resources associated with this line

        :param deallocation_routine: the function to call to free a specific
            resource
        :type deallocation_routine: function
        :param params: parameters to the deallocation_routine
        :type params: tuple

        :return: Nothing
        """
        self.deallocation_routines.append((deallocation_routine, params))

    def free(self):
        """
        Call the deallocation routines specified for when this line is freed.

        :return: Nothing
        """
        for routine, params in self.deallocation_routines:
            routine(*params)

    def intersects(self, other_line):
        """
        Determines whether this line intersects another line.

        :param other_line: the other line
        :type other_line: Line
        :rtype: boolean
        :return: whether this line intersects the other line
        """
        return self.straddles(other_line) and other_line.straddles(self)

    def straddles(self, other_line):
        """
        Determines whether this line straddles another line.
        That is, the points of this line are on opposite sides of
        the other line.

        :param other_line: the other line
        :type other_line: Line
        :rtype: boolean
        :return: whether this line straddles the other line
        """
        return (side_of_line(other_line, self.left_point) *
                side_of_line(other_line, self.right_point) == -1)


def side_of_line(line, point):
    """
    Computes a sign representing which side of the line a point is on.

    :param line: the line
    :type line: Line
    :param point: the point
    :type point: tuple
    :rtype: integer
    :return: the side of the line the point is
    """
    return sign(cross_product(vector(line.left_point, line.right_point),
                              vector(line.left_point, point)))


def vector(point_a, point_b):
    """
    Compute the vector difference between two 2D points.

    :param point_a: the first point
    :type point_a: tuple
    :param point_b: the other point
    :type point_b: tuple
    :rtype: tuple
    :return: difference between two points
    """
    return (point_b[0] - point_a[0], point_b[1] - point_a[1])


def sign(num):
    """
    Compute the sign of a given number.

    :param num: the number to extract the sign from
    :type num: number
    :rtype: integer (one of -1, 0, or 1)
    :return: the sign of the number
    """
    if num == 0:
        return 0
    if num < 0:
        return -1
    if num > 0:
        return 1


def cross_product(vector_a, vector_b):
    """
    Compute the size of the cross product between two vectors.

    :param vector_a: the first vector
    :type vector_a: tuple
    :param vector_a: the second vector
    :type vector_a: tuple
    :rtype: number
    :return: the signed area between the two vectors
    """
    return vector_a[0] * vector_b[1] - vector_a[1] * vector_b[0]


def point_distance(point_a, point_b):
    """
    Compute the euclidean distance between two points.

    :param point_a: one of the two points to measure distance between
    :type point_a: tuple(float, float)
    :param point_b: the other of the two points to measure distance between
    :type point_b: tuple(float, float)
    :rtype: float
    :return: the distance between point_a and point_b
    """
    return ((point_a[0] - point_b[0]) ** 2 +
            (point_a[1] - point_b[1]) ** 2) ** 0.5
