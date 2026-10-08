"""Vacuum cleaner problem solved with Breadth-First Search and Depth-First Search."""

from collections import deque

State = tuple[int, bool, bool]
Transition = tuple[str, State]


def is_goal(state: State) -> bool:
    """Return True when both rooms are already clean."""
    return not state[1] and not state[2]


def successors(state: State) -> list[Transition]:
    """Return the valid next states reachable from the current vacuum state."""
    location, room_a_dirty, room_b_dirty = state
    transitions: list[Transition] = []

    if location == 0:
        if room_a_dirty:
            transitions.append(("Suck Room A", (0, False, room_b_dirty)))
        transitions.append(("Move to Room B", (1, room_a_dirty, room_b_dirty)))
    else:
        if room_b_dirty:
            transitions.append(("Suck Room B", (1, room_a_dirty, False)))
        transitions.append(("Move to Room A", (0, room_a_dirty, room_b_dirty)))

    return [(action, next_state) for action, next_state in transitions if next_state != state]


def reconstruct(parent: dict[State, tuple[State, str]], state: State) -> list[tuple[str, State]]:
    """Rebuild the action path from the goal state back to the start state."""
    path: list[tuple[str, State]] = []
    while state in parent:
        previous, action = parent[state]
        path.append((action, state))
        state = previous
    return list(reversed(path))


def breadth_first_search(start: State = (0, True, True)) -> list[tuple[str, State]]:
    """Return the shortest sequence of actions that cleans both rooms."""
    queue = deque([start])
    parent: dict[State, tuple[State, str]] = {}
    visited = {start}

    while queue:
        state = queue.popleft()
        if is_goal(state):
            return reconstruct(parent, state)

        for action, next_state in successors(state):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (state, action)
                queue.append(next_state)

    return []


def depth_first_search(start: State = (0, True, True)) -> list[tuple[str, State]]:
    """Return any valid sequence of actions that cleans both rooms."""
    stack = [start]
    parent: dict[State, tuple[State, str]] = {}
    visited = {start}

    while stack:
        state = stack.pop()
        if is_goal(state):
            return reconstruct(parent, state)

        for action, next_state in reversed(successors(state)):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (state, action)
                stack.append(next_state)

    return []


def print_solution(name: str, path: list[tuple[str, State]]) -> None:
    print(f"{name}: {len(path)} step(s)")
    if not path:
        print("  No solution found.")
        return
    print("  Start: (0, True, True)")
    for action, state in path:
        print(f"  {action} -> {state}")


if __name__ == "__main__":
    algorithms = {
        "BFS": breadth_first_search,
        "DFS": depth_first_search,
    }
    for name, algorithm in algorithms.items():
        print_solution(name, algorithm())
