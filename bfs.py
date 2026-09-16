"""Run the water jug problem with Breadth First Search."""

from water_jug_problem import breadth_first_search, print_solution


if __name__ == "__main__":
    print_solution("BFS", breadth_first_search(4, 3, 2))
