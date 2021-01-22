import rubik
import random
import timeit

from collections import deque

GODS_NUMBER = 14

def shortest_path(start, end):
    visited_nodes = 0
    if start == end:
        return []

    forward_parents = {start: None}
    backward_parents = {end: None}

    forward_dq = deque([start, None])
    backward_dq = deque([end])

    graph_radius = GODS_NUMBER / 2
    for i in range(graph_radius):
        while True:
            current_forward = forward_dq.popleft()
            if current_forward is None:
                forward_dq.append(None)
                break

            for twist in rubik.quarter_twists:
                next_state = rubik.perm_apply(twist, current_forward)
                if next_state not in forward_parents:
                    forward_parents[next_state] = (current_forward, twist)
                    visited_nodes += 1
                    forward_dq.append(next_state)

            current_backward = backward_dq.popleft()
            for twist in rubik.quarter_twists:
                next_state = rubik.perm_apply(twist, current_backward)
                if next_state not in backward_parents:
                    backward_parents[next_state] = (current_backward, twist)
                    visited_nodes += 1
                    backward_dq.append(next_state)

                if next_state in forward_parents:
                    forward_path = path(next_state, forward_parents)
                    backward_path = path(next_state, backward_parents)
                    backward_path.reverse()

                    print('2 BFS, visited nodes number: ', visited_nodes)
                    return forward_path + map(rubik.perm_inverse, backward_path)


def shortest_path_bfs(start, end):
    visited_nodes = 0
    if start == end:
        return []

    forward_parents = {start: None}

    forward_dq = deque([start, None])

    for i in range(GODS_NUMBER):
        while True:
            current_forward = forward_dq.popleft()
            if current_forward is None:
                forward_dq.append(None)
                break

            for twist in rubik.quarter_twists:
                next_state = rubik.perm_apply(twist, current_forward)
                if next_state not in forward_parents:
                    forward_parents[next_state] = (current_forward, twist)
                    visited_nodes += 1
                    forward_dq.append(next_state)

                if next_state == end:
                    print('BFS, visited nodes number: ', visited_nodes)
                    return path(next_state, forward_parents)


def path(position, parents):
    twists = []
    while True:
        position = parents[position]
        if position is None:
            twists.reverse()
            return twists
        twists.append(position[1])
        position = position[0]


def random_state():
    state = rubik.I
    for i in range(GODS_NUMBER):
        index = random.randint(0, 5)
        twist = rubik.quarter_twists[index]
        state = rubik.perm_apply(twist, state)
    return (rubik.I, state)


states = []
for i in range(10):
    states.append(random_state())

start_time = timeit.default_timer()
for state in states:
    result = shortest_path_bfs(state[0], state[1])
print('BFS implementation:')
print(timeit.default_timer() - start_time)

start_time = timeit.default_timer()
for state in states:
    result2 = shortest_path(state[0], state[1])
print('2 BFS implementation:')
print(timeit.default_timer() - start_time)

