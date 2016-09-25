import glob
import json
import os

import problem_generator

def check(graph, coloring):
    if len(coloring) < len(graph):
        print 'Incomplete coloring'
        return False
    for from_index, adj_list in enumerate(graph):
        for to_index in adj_list:
            if coloring[str(from_index)] == coloring[str(to_index)]:
                return False
    return True


for result_path in glob.iglob('results/*'):
    result_file_name = os.path.split(result_path)[-1]
    result_name = os.path.splitext(result_file_name)[0]

    result = json.load(open(result_path))
    graph = problem_generator.read_graph_from_file(
        '.'.join(result_name.split('.')[:-1]) + '.json'
    )
    
    history = result['history'][:3]
    history = [run[0] for run in history]
    history = [[item for item in run if item] for run in history]
    history = [run[-1] if len(run) > 0 else None for run in history]

    for i, coloring in enumerate(history):
        #print coloring
        if coloring:
            if check(graph, coloring):
                print 'Verified result: {}, alg {}'.format(result_name, i)
