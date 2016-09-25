import problem_generator

num_copies = 5;
sizes = range(10, 110, 10)

for size in sizes:
    print 'Generating {} graphs of size {}...'.format(num_copies, size)
    for i in xrange(num_copies):
        graph = problem_generator.generate_graph(size)
        problem_generator.write_graph_to_file(
            'experiment_graph.size={}.copy={}.json'.format(size, i),
            graph
        )
