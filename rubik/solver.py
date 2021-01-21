import rubik

from collections import deque

GODS_NUMBER = 14


def shortest_path(start, end):
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
                    forward_dq.append(next_state)

            current_backward = backward_dq.popleft()
            for twist in rubik.quarter_twists:
                next_state = rubik.perm_apply(twist, current_backward)
                if next_state not in backward_parents:
                    backward_parents[next_state] = (current_backward, twist)
                    backward_dq.append(next_state)

                if next_state in forward_parents:
                    forward_path = path(next_state, forward_parents)
                    backward_path = path(next_state, backward_parents)
                    backward_path.reverse()

                    return forward_path + map(rubik.perm_inverse, backward_path)


def path(position, parents):
    path = []
    while True:
        position = parents[position]
        if position is None:
            path.reverse()
            return path
        path.append(position[1])
        position = position[0]
