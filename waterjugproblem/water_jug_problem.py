"""Water jug problem solved with common uninformed and informed searches."""

from collections import deque
from heapq import heappop, heappush
from math import gcd

State = tuple[int, int]
Transition = tuple[str, State]


def validate_problem(capacity1: int, capacity2: int, target: int) -> None:
    if capacity1 <= 0 or capacity2 <= 0:
        raise ValueError("Jug capacities must be positive.")
    if target < 0 or target > max(capacity1, capacity2):
        raise ValueError("Target must be between zero and the largest capacity.")
    if target and target % gcd(capacity1, capacity2) != 0:
        raise ValueError("This target cannot be measured with these jug sizes.")


def is_goal(state: State, target: int) -> bool:
    return state[0] == target or state[1] == target


def successors(state: State, capacity1: int, capacity2: int) -> list[Transition]:
    jug1, jug2 = state
    transitions = [
        ("Fill Jug 1", (capacity1, jug2)),
        ("Fill Jug 2", (jug1, capacity2)),
        ("Empty Jug 1", (0, jug2)),
        ("Empty Jug 2", (jug1, 0)),
    ]
    amount = min(jug1, capacity2 - jug2)
    transitions.append(("Pour Jug 1 -> Jug 2", (jug1 - amount, jug2 + amount)))
    amount = min(jug2, capacity1 - jug1)
    transitions.append(("Pour Jug 2 -> Jug 1", (jug1 + amount, jug2 - amount)))
    return [(action, next_state) for action, next_state in transitions if next_state != state]


def reconstruct(parent: dict[State, tuple[State, str]], state: State) -> list[tuple[str, State]]:
    path = []
    while state in parent:
        previous, action = parent[state]
        path.append((action, state))
        state = previous
    return list(reversed(path))


def heuristic(state: State, target: int) -> int:
    return min(abs(state[0] - target), abs(state[1] - target))


def breadth_first_search(capacity1: int, capacity2: int, target: int) -> list[tuple[str, State]]:
    validate_problem(capacity1, capacity2, target)
    start = (0, 0)
    queue = deque([start])
    parent = {}
    visited = {start}
    while queue:
        state = queue.popleft()
        if is_goal(state, target):
            return reconstruct(parent, state)
        for action, next_state in successors(state, capacity1, capacity2):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (state, action)
                queue.append(next_state)
    return []


def depth_first_search(capacity1: int, capacity2: int, target: int) -> list[tuple[str, State]]:
    validate_problem(capacity1, capacity2, target)
    start = (0, 0)
    stack = [start]
    parent = {}
    visited = {start}
    while stack:
        state = stack.pop()
        if is_goal(state, target):
            return reconstruct(parent, state)
        for action, next_state in reversed(successors(state, capacity1, capacity2)):
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (state, action)
                stack.append(next_state)
    return []


def hill_climbing(capacity1: int, capacity2: int, target: int) -> list[tuple[str, State]]:
    validate_problem(capacity1, capacity2, target)
    def climb(state: State, visited: set[State]) -> list[tuple[str, State]] | None:
        if is_goal(state, target):
            return []
        current_score = heuristic(state, target)
        candidates = sorted(
            (
                heuristic(next_state, target),
                action,
                next_state,
            )
            for action, next_state in successors(state, capacity1, capacity2)
            if next_state not in visited
        )
        for score, action, next_state in candidates:
            if score > current_score:
                continue
            result = climb(next_state, visited | {next_state})
            if result is not None:
                return [(action, next_state)] + result
        return None

    return climb((0, 0), {(0, 0)}) or []


def best_first_search(capacity1: int, capacity2: int, target: int) -> list[tuple[str, State]]:
    validate_problem(capacity1, capacity2, target)
    start = (0, 0)
    frontier = [(heuristic(start, target), start)]
    parent = {}
    visited = set()
    while frontier:
        _, state = heappop(frontier)
        if state in visited:
            continue
        visited.add(state)
        if is_goal(state, target):
            return reconstruct(parent, state)
        for action, next_state in successors(state, capacity1, capacity2):
            if next_state not in visited:
                parent.setdefault(next_state, (state, action))
                heappush(frontier, (heuristic(next_state, target), next_state))
    return []


def a_star_search(capacity1: int, capacity2: int, target: int) -> list[tuple[str, State]]:
    validate_problem(capacity1, capacity2, target)
    start = (0, 0)
    frontier = [(heuristic(start, target), 0, start)]
    parent = {}
    costs = {start: 0}
    while frontier:
        _, cost, state = heappop(frontier)
        if cost != costs[state]:
            continue
        if is_goal(state, target):
            return reconstruct(parent, state)
        for action, next_state in successors(state, capacity1, capacity2):
            next_cost = cost + 1
            if next_cost < costs.get(next_state, float("inf")):
                costs[next_state] = next_cost
                parent[next_state] = (state, action)
                priority = next_cost + heuristic(next_state, target)
                heappush(frontier, (priority, next_cost, next_state))
    return []


def print_solution(name: str, path: list[tuple[str, State]]) -> None:
    print(f"{name}: {len(path)} step(s)")
    if not path:
        print("  No solution found.")
        return
    print("  Start: (0, 0)")
    for action, state in path:
        print(f"  {action} -> {state}")


if __name__ == "__main__":
    capacity1, capacity2, target = 4, 3, 2
    algorithms = {
        "BFS": breadth_first_search,
        "DFS": depth_first_search,
        "Hill Climbing": hill_climbing,
        "Best First Search": best_first_search,
        "A*": a_star_search,
    }
    for name, algorithm in algorithms.items():
        print_solution(name, algorithm(capacity1, capacity2, target))