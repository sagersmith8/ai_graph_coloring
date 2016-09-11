import unittest
from ai_graph_color.line import Line, point_distance


class TestLineObject(unittest.TestCase):
    def test_init_unequal_x(self):
        """
        Tests making a line with the same y and different x's
        """
        left_point = (0, 0)
        right_point = (10, 0)
        distance = 10
        deallocation_routines = []

        line = Line(
            right_point, left_point
        )

        self.assertEqual(left_point, line.left_point)
        self.assertEqual(right_point, line.right_point)
        self.assertEqual(distance, line.distance)
        self.assertEqual(deallocation_routines, line.deallocation_routines)

    def test_init_equal_x_unequal_y(self):
        """
        Tests making a line with the same x and different y's
        """
        left_point = (0, 0)
        right_point = (0, 10)
        distance = 10
        deallocation_routines = []

        line = Line(
            right_point, left_point
        )

        self.assertEqual(left_point, line.left_point)
        self.assertEqual(right_point, line.right_point)
        self.assertEqual(distance, line.distance)
        self.assertEqual(deallocation_routines, line.deallocation_routines)

    def test_init_equal_points(self):
        """
        Tests making a line with with the same points
        """
        point = (0, 0)
        distance = 0
        deallocation_routines = []

        line = Line(
            point, point
        )

        self.assertEqual(point, line.left_point)
        self.assertEqual(point, line.right_point)
        self.assertEqual(distance, line.distance)
        self.assertEqual(deallocation_routines, line.deallocation_routines)

    def test_add_reference_with_params(self):
        """
        Tests add reference_with_params and passes params
        """
        point = (0, 0)
        deallocation_routines = [(max, (0, 0))]

        line = Line(
            point, point
        )

        line.add_reference(max, 0, 0)
        self.assertEqual(deallocation_routines, line.deallocation_routines)

    def test_add_reference_without_params(self):
        """
        Tests add reference_with_params and doesn't pass params
        """
        point = (0, 0)
        deallocation_routines = [(max, ())]

        line = Line(
            point, point
        )

        line.add_reference(max)
        self.assertEqual(deallocation_routines, line.deallocation_routines)

    def free(self):
        """
        Tests that free calls the proper function
        """
        point = (0, 0)

        line = Line(
            point, point
        )

        expected = 10
        dictionary = {0: expected}

        line.add_reference(dictionary.get, 0)
        self.assertEqual(expected, line.free())


class TestLine(unittest.TestCase):
    def test_point_distance(self):
        """
        Tests that the distance is calculated correctly
        """
        points = [
            ((0, 0), (0, 0)),
            ((1, 0), (0, 0)),
            ((0, 1), (0, 0))
        ]

        expected_distances = [0, 1, 1]

        for i, points_to_check in enumerate(points):
            self.assertEqual(
                expected_distances[i],
                point_distance(*points_to_check)
            )
