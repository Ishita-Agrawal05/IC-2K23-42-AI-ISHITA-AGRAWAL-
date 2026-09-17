"""Run the water jug problem with Hill Climbing."""

from water_jug_problem import hill_climbing, print_solution


if __name__ == "__main__":
    print_solution("Hill Climbing", hill_climbing(4, 3, 2))
