def run(problem, setup, params):  
    num_values = params['colors']
    problem_size = len(problem)

    assignments = [{}]
    current_vars = []
    next_values = []

    current_var = choose_var(problem, assignments[-1], num_values)
    current_vars.append(current_var)

    next_values.append(
        order_values(problem, current_var, assignments[-1], num_values)
    )

    if setup.counter.increment():
        yield -1

    while len(current_vars) > 0:
        if len(next_values[-1]) > 0:
            current_assignment = assignments[-1]
            current_var = current_vars[-1]
            next_value = next_values[-1].pop()
            
            next_assignment = current_assignment.copy()
            next_assignment[current_var] = next_value

            if setup.counter.increment():
                yield -1

            if not valid_assignment(problem, next_assignment, current_var):
                continue

            if len(next_assignment) == problem_size:
                yield 0
                return

            next_var = choose_var(problem, next_assignment, num_values)
            next_ordering = order_values(problem, next_var, next_assignment, num_values)
            
            assignments.append(next_assignment)
            current_vars.append(next_var)
            next_values.append(next_ordering)
        else:
            assignments.pop()
            current_vars.pop()
            next_values.pop()
    
    yield 'Failed'


def choose_var(problem, assignment, num_values):
    available_values = [set(xrange(num_values)) for _ in range(len(problem))]
    degree = [len(adj_list) for adj_list in problem]

    for index, adj in enumerate(problem):
        if index not in assignment:
            for to_index in adj:
                if to_index in assignment:
                    available_values[index] -= {assignment[to_index]}

    max_item = min((len(available_values[i]), -degree[i], i) for i in range(len(available_values)) if not i in assignment)

    return max_item[2]


def order_values(problem, variable, assignment, num_values):
    count = [1 for i in xrange(num_values)]

    for to_variable in problem[variable]:
        for value in set(assignment.get(node) for node in problem[to_variable]):
            if value is not None:
                count[value] += 1

    return [count[1] for count in sorted((count[index], index) for index in xrange(num_values))]


def valid_assignment(problem, assignment, changed_var):
    for connected in problem[changed_var]:
        if connected in assignment and assignment[connected] == assignment[changed_var]:
            return False
    return True
