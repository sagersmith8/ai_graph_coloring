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
            print routine, params
            routine(*params)


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
