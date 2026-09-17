# Water Jug Problem

`water_jug_problem.py` solves the water jug problem using:

- Breadth First Search (BFS)
- Depth First Search (DFS)
- Hill Climbing
- Best First Search
- A* Search

The example uses jugs of 4 and 3 litres to measure 2 litres. Run it with:

```bash
python3 water_jug_problem.py
```

Run the requested algorithms individually with:

```bash
python3 bfs.py
python3 dfs.py
python3 hill_climbing.py
```

Each search function returns a list of `(action, state)` pairs, so it can also
be imported and used by another program.