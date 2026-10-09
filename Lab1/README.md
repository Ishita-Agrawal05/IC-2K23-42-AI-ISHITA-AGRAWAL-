# Lab 1: AI Environment, Production Systems, and Search Problems

This lab introduces rule-based reasoning and state-space problem solving.

## Activities
- AI environment setup: use `Experiment1.ipynb` to record environment checks and setup work.
- Production rule system: infer new facts by repeatedly applying matching rules.
- Rule-based decision making: select an action from facts using an ordered rule set.
- State-space representation: model states and transitions as a directed adjacency list.
- Water jug problem: find a shortest solution for 4- and 3-unit jugs with a 2-unit target.
- Missionaries and cannibals: cross the river without allowing cannibals to outnumber missionaries on either bank.
- Vacuum cleaner problem: clean two rooms by moving and sucking dirt.

## Run the demonstrations

Run all implemented activities from the repository root:

```bash
python3 Lab1/Experiment2.py
```

The script uses breadth-first search for the three problem-solving exercises. Its states are tuples, and each transition records an action and the resulting state.

`Experiment1.ipynb` checks the active Python interpreter and reports whether common optional packages are installed. The `outputs/` folder is reserved for generated results.
