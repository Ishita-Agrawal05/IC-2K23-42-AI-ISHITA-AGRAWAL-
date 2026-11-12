# AI Search Problems

This repository contains classic AI search examples, including:

- Water jug problem (BFS, DFS, Hill Climbing, Best First Search, A*)
- Vacuum cleaner problem (BFS and DFS)

## Water Jug Problem

The water jug implementation is stored in the `waterjugproblem` folder and can be run with:

```bash
python3 waterjugproblem/water_jug_problem.py
```

## Vacuum Cleaner Problem

The vacuum cleaner implementation is stored in the `vacuum_cleaner_problem` folder and can be run with:

```bash
python3 vacuum_cleaner_problem/vacuum_cleaner_problem.py
```

Each search function returns a list of `(action, state)` pairs, so each solver can also be imported and reused in another program.