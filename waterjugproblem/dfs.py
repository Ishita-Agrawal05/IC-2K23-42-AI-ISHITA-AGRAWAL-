"""Run the water jug problem with Depth First Search."""

from water_jug_problem import depth_first_search, print_solution


if __name__ == "__main__":
    print_solution("DFS", depth_first_search(4, 3, 2))
