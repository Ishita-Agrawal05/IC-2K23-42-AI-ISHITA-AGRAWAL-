"""Solve the water jug problem using Breadth-First Search."""

from collections import deque


def breadth_first_search(capacity1: int, capacity2: int, target: int) -> list[tuple[str, tuple[int, int]]]:
    """Return the shortest sequence of operations that reaches target."""
    start = (0, 0)
    queue = deque([start])
    parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
    visited = {start}

    while queue:
        jug1, jug2 = queue.popleft()
        if jug1 == target or jug2 == target:
            path = []
            state = (jug1, jug2)
            while state != start:
                previous, action = parent[state]
                path.append((action, state))
                state = previous
            return list(reversed(path))

        next_states = [
            ("Fill Jug 1", (capacity1, jug2)),
            ("Fill Jug 2", (jug1, capacity2)),
            ("Empty Jug 1", (0, jug2)),
            ("Empty Jug 2", (jug1, 0)),
        ]

        amount = min(jug1, capacity2 - jug2)
        next_states.append(("Pour Jug 1 -> Jug 2", (jug1 - amount, jug2 + amount)))

        amount = min(jug2, capacity1 - jug1)
        next_states.append(("Pour Jug 2 -> Jug 1", (jug1 + amount, jug2 - amount)))

        for action, next_state in next_states:
            if next_state != (jug1, jug2) and next_state not in visited:
                visited.add(next_state)
                parent[next_state] = ((jug1, jug2), action)
                queue.append(next_state)

    return []


def print_solution(path: list[tuple[str, tuple[int, int]]]) -> None:
    print(f"BFS: {len(path)} step(s)")
    print("  Start: (0, 0)")
    for action, state in path:
        print(f"  {action} -> {state}")


if __name__ == "__main__":
    print_solution(breadth_first_search(4, 3, 2))
