import unittest

from ai_graph_color import problem_generator


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
            # This will need to change when generate graph is finished
            self.assertIsNone(
                problem_generator.generate_graph(num_vert)
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
            self.assertIsNone(
                problem_generator.build_graph(point)
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
