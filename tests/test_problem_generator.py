import unittest

from ai_graph_color import line, problem_generator


class TestProblemGenerator(unittest.TestCase):
    def test_generate_file_path(self):
        """
        Tests create file
        """
        file_names = ['test.json', '']
        for file_name in file_names:
            file_path = problem_generator.generate_file_path(file_name)
            self.assertEqual(type(''), type(file_path))
            self.assertEqual('problems/{}'.format(file_name), file_path)

    def test_read_and_write_graph_to_file(self):
        """
        Tests write graph to file
        """
        num_verts = [0, 5, 100]
        for index, num_vert in enumerate(num_verts):
            graph = problem_generator.generate_graph(num_vert)
            problem_generator.write_graph_to_file(
                'test{}.json'.format(index),
                graph
            )

            self.assertEqual(
                graph,
                problem_generator.read_graph_from_file(
                    'test{}.json'.format(index)
                )
            )

    def test_generate_graph(self):
        """
        Tests generate graph
        """
        num_verts = [0, 5, 100]
        for num_vert in num_verts:
            graph = problem_generator.generate_graph(num_vert)
            self.assertEquals(
                num_vert,
                len(graph)
            )
            for connections in graph:
                self.assertGreater(
                    len(connections),
                    0
                )

    def test_build_graph(self):
        """
        Tests build graph
        """
        points = [
            [(0, 0), (0, 0)],
            [],
            [(100, 100), (1000, 1000)]
        ]

        # This will need to change once build_graph is implemented
        for point in points:
            graph = problem_generator.build_graph(point)
            self.assertEquals(
                len(point),
                len(graph)
            )
            for connections in graph:
                self.assertGreater(
                    len(connections),
                    0
                )

    def test_scatter_points(self):
        """
        Tests scatter points
        """
        num_points = [0, 1, 100]
        for num_point in num_points:
            self.assertEqual(
                num_point,
                len(problem_generator.scatter_points(num_point))
            )

    def test_create_lines(self):
        """
        Tests certain properties hold for the lines-map on sample points:
        - The points indexed by a line's key are the same as the points
          listed in the line
        - The distance calculated in a mapped line matches the distance
          between the points indexed by that line's key
        - The line can be freed without exception
        """
        points = [(0.0, 0.0), (0.0, 3.0), (1.0, 1.0), (1.0, 5.0)]
        lines = problem_generator.create_lines(points)

        for pair, connecting_line in lines.items():
            distance = line.point_distance(
                *map(lambda i: points[i], pair)
            )

            self.assertAlmostEqual(distance, connecting_line.distance)
            self.assertEqual(
                frozenset(map(lambda i: points[i], pair)),
                frozenset([connecting_line.left_point,
                           connecting_line.right_point])
            )
            connecting_line.free()  # should not raise any errors

    def test_create_distance_list(self):
        """
        Tests certain properties hold for the distance list:
        - Lines in a linked-list are ordered by distance
        - Each line described in a list uses the correct indexes
        - Freeing a line removes it from the line-map and both of
          the linked-lists in the distance-list
        """
        points = [(0.0, 0.0), (0.0, 3.0), (1.0, 1.0), (1.0, 5.0)]
        lines = problem_generator.create_lines(points)
        distance_list = problem_generator.create_distance_list(
            lines, len(points)
        )

        for src_index, connections in enumerate(distance_list):
            distances = map(lambda i: i[1].distance, connections)
            self.assertTrue(all(
                distances[i] <= distances[i + 1]
                for i in xrange(len(distances) - 1)
            ))

            for dst_index, connecting_line in connections:
                self.assertEqual(
                    frozenset(map(lambda i: points[i],
                                  [src_index, dst_index])),
                    frozenset([connecting_line.left_point,
                               connecting_line.right_point])
                )

        for connections in distance_list:
            for other_index, connecting_line in connections:
                first_list_size = len(connections)
                other_list_size = len(distance_list[other_index])
                lines_size = len(lines)

                connecting_line.free()

                self.assertEqual(first_list_size - 1, len(connections))
                self.assertEqual(other_list_size - 1,
                                 len(distance_list[other_index]))
                self.assertEqual(lines_size - 1, len(lines))
            self.assertEquals(0, len(connections))
        self.assertEquals(0, len(lines))
