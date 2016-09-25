import json
import sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

plot_file, = sys.argv[1:]

results = json.load(open(plot_file))
iterations = results['iterations']
history = [run[:2] for run in results['history']]

fig = plt.figure()
ax = Axes3D(fig)


new_history = [[[], []] for i in xrange(len(history)/10)]

duplication = 10
for index, (run, iterations) in enumerate(history):
    new_history[index % duplication][0].extend(run)
    new_history[index % duplication][1].extend(iterations)

for index, (run_set, iteration_set) in enumerate(new_history):
    ax.scatter(iteration_set, run_set, [index]*len(run_set), label=str(index))
    
ax.legend(loc='upper right')
plt.show()
