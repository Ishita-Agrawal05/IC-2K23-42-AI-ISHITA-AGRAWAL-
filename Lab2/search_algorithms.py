"""Lab 2: classic graph search algorithms."""

from collections import deque
from heapq import heappop, heappush


Graph = dict[str, list[tuple[str, int]]]


def bfs(graph: Graph, start: str, goal: str) -> list[str]:
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == goal:
            return reconstruct_path(parent, goal)
        for neighbor, _ in graph.get(node, []):
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
    return []


def dfs(graph: Graph, start: str, goal: str) -> list[str]:
    stack = [start]
    parent = {start: None}

    while stack:
        node = stack.pop()
        if node == goal:
            return reconstruct_path(parent, goal)
        for neighbor, _ in reversed(graph.get(node, [])):
            if neighbor not in parent:
                parent[neighbor] = node
                stack.append(neighbor)
    return []


def uniform_cost_search(graph: Graph, start: str, goal: str) -> list[str]:
    frontier: list[tuple[int, str]] = [(0, start)]
    parent = {start: None}
    cost = {start: 0}

    while frontier:
        current_cost, node = heappop(frontier)
        if current_cost > cost.get(node, float("inf")):
            continue
        if node == goal:
            return reconstruct_path(parent, goal)
        for neighbor, weight in graph.get(node, []):
            new_cost = current_cost + weight
            if new_cost < cost.get(neighbor, float("inf")):
                cost[neighbor] = new_cost
                parent[neighbor] = node
                heappush(frontier, (new_cost, neighbor))
    return []


def a_star(graph: Graph, start: str, goal: str) -> list[str]:
    heuristic = {
        "S": 6,
        "A": 5,
        "B": 4,
        "C": 3,
        "D": 2,
        "E": 2,
        "G": 0,
    }

    frontier: list[tuple[int, int, str]] = [(heuristic[start], 0, start)]
    parent = {start: None}
    g_cost = {start: 0}

    while frontier:
        _, current_cost, node = heappop(frontier)
        if current_cost > g_cost.get(node, float("inf")):
            continue
        if node == goal:
            return reconstruct_path(parent, goal)
        for neighbor, weight in graph.get(node, []):
            new_cost = current_cost + weight
            if new_cost < g_cost.get(neighbor, float("inf")):
                g_cost[neighbor] = new_cost
                parent[neighbor] = node
                priority = new_cost + heuristic.get(neighbor, 0)
                heappush(frontier, (priority, new_cost, neighbor))
    return []


def reconstruct_path(parent: dict[str, str | None], goal: str) -> list[str]:
    path: list[str] = []
    current = goal
    while current is not None:
        path.append(current)
        current = parent[current]
    return list(reversed(path))


def main() -> None:
    graph: Graph = {
        "S": [("A", 1), ("B", 2)],
        "A": [("C", 3), ("D", 4)],
        "B": [("D", 2), ("E", 5)],
        "C": [("G", 5)],
        "D": [("G", 1)],
        "E": [("G", 2)],
        "G": [],
    }

    print("Breadth-First Search:", bfs(graph, "S", "G"))
    print("Depth-First Search:", dfs(graph, "S", "G"))
    print("Uniform Cost Search:", uniform_cost_search(graph, "S", "G"))
    print("A* Search:", a_star(graph, "S", "G"))


if __name__ == "__main__":
    main()
