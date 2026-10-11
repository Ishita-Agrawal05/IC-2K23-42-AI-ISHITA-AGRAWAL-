"""Lab 1 demonstrations: production rules and classic AI state spaces."""

from collections import deque
from dataclasses import dataclass
from typing import Callable, Hashable, TypeVar

StateT = TypeVar("StateT", bound=Hashable)
Transition = tuple[str, StateT]


def breadth_first_search(
	start: StateT,
	is_goal: Callable[[StateT], bool],
	successors: Callable[[StateT], list[Transition]],
) -> list[Transition]:
	"""Find a shortest path in an unweighted state space."""
	queue = deque([start])
	parent: dict[StateT, tuple[StateT, str]] = {}
	visited = {start}

	while queue:
		state = queue.popleft()
		if is_goal(state):
			path: list[Transition] = []
			while state in parent:
				previous, action = parent[state]
				path.append((action, state))
				state = previous
			return list(reversed(path))

		for action, next_state in successors(state):
			if next_state not in visited:
				visited.add(next_state)
				parent[next_state] = (state, action)
				queue.append(next_state)

	return []


@dataclass(frozen=True)
class Rule:
	name: str
	conditions: frozenset[str]
	conclusion: str


def run_production_system(
	initial_facts: set[str], rules: list[Rule]
) -> tuple[set[str], list[str]]:
	"""Apply matching production rules until no new facts can be inferred."""
	facts = set(initial_facts)
	applied: list[str] = []
	changed = True

	while changed:
		changed = False
		for rule in rules:
			if rule.conditions <= facts and rule.conclusion not in facts:
				facts.add(rule.conclusion)
				applied.append(rule.name)
				changed = True

	return facts, applied


def production_system_demo() -> None:
	rules = [
		Rule("detect rain", frozenset({"cloudy", "rain_sensor_on"}), "raining"),
		Rule("protect equipment", frozenset({"raining"}), "equipment_needs_cover"),
		Rule("close windows", frozenset({"raining"}), "windows_should_close"),
	]
	facts, applied = run_production_system({"cloudy", "rain_sensor_on"}, rules)
	print("Production system:")
	print(f"  Fired rules: {', '.join(applied)}")
	print(f"  Inferred facts: {', '.join(sorted(facts))}")


def rule_based_decision_demo() -> None:
	facts = {"room_dirty", "vacuum_in_room_a", "battery_charged"}
	rules = [
		Rule("clean current room", frozenset({"room_dirty", "vacuum_in_room_a"}), "Suck"),
		Rule("move to room B", frozenset({"room_clean", "vacuum_in_room_a"}), "Move to Room B"),
		Rule("recharge", frozenset({"battery_low"}), "Recharge"),
	]
	decision = next(
		(rule.conclusion for rule in rules if rule.conditions <= facts),
		"No action available",
	)
	print("Rule-based decision:")
	print(f"  Facts: {', '.join(sorted(facts))}")
	print(f"  Selected action: {decision}")


def water_jug_successors(state: tuple[int, int]) -> list[Transition]:
	jug_a, jug_b = state
	capacity_a, capacity_b = 4, 3
	moves = [
		("Fill jug A", (capacity_a, jug_b)),
		("Fill jug B", (jug_a, capacity_b)),
		("Empty jug A", (0, jug_b)),
		("Empty jug B", (jug_a, 0)),
	]
	amount = min(jug_a, capacity_b - jug_b)
	moves.append(("Pour A into B", (jug_a - amount, jug_b + amount)))
	amount = min(jug_b, capacity_a - jug_a)
	moves.append(("Pour B into A", (jug_a + amount, jug_b - amount)))
	return [(action, next_state) for action, next_state in moves if next_state != state]


def water_jug_demo() -> None:
	path = breadth_first_search((0, 0), lambda state: 2 in state, water_jug_successors)
	print("Water jug problem (capacities 4 and 3; target 2):")
	print("  State format: (amount in jug A, amount in jug B)")
	for action, state in path:
		print(f"  {action} -> {state}")


def missionaries_successors(state: tuple[int, int, int]) -> list[Transition]:
	missionaries_left, cannibals_left, boat = state
	moves: list[Transition] = []
	for missionaries, cannibals in ((2, 0), (0, 2), (1, 1), (1, 0), (0, 1)):
		direction = -1 if boat == 0 else 1
		next_state = (
			missionaries_left + direction * missionaries,
			cannibals_left + direction * cannibals,
			1 - boat,
		)
		next_missionaries, next_cannibals, _ = next_state
		if not (0 <= next_missionaries <= 3 and 0 <= next_cannibals <= 3):
			continue
		missionaries_right = 3 - next_missionaries
		cannibals_right = 3 - next_cannibals
		left_is_safe = next_missionaries == 0 or next_missionaries >= next_cannibals
		right_is_safe = missionaries_right == 0 or missionaries_right >= cannibals_right
		if left_is_safe and right_is_safe:
			moves.append((f"Move {missionaries} missionary/missionaries and {cannibals} cannibal(s)", next_state))
	return moves


def missionaries_and_cannibals_demo() -> None:
	start = (3, 3, 0)
	goal = lambda state: state == (0, 0, 1)
	path = breadth_first_search(start, goal, missionaries_successors)
	print("Missionaries and cannibals:")
	print("  State format: (missionaries left, cannibals left, boat side; 0=left, 1=right)")
	for action, state in path:
		print(f"  {action} -> {state}")


def vacuum_successors(state: tuple[int, bool, bool]) -> list[Transition]:
	location, room_a_dirty, room_b_dirty = state
	if location == 0:
		moves = [("Suck Room A", (0, False, room_b_dirty))] if room_a_dirty else []
		moves.append(("Move to Room B", (1, room_a_dirty, room_b_dirty)))
	else:
		moves = [("Suck Room B", (1, room_a_dirty, False))] if room_b_dirty else []
		moves.append(("Move to Room A", (0, room_a_dirty, room_b_dirty)))
	return [(action, next_state) for action, next_state in moves if next_state != state]


def vacuum_cleaner_demo() -> None:
	path = breadth_first_search(
		(0, True, True),
		lambda state: not state[1] and not state[2],
		vacuum_successors,
	)
	print("Vacuum cleaner problem:")
	print("  State format: (location; 0=Room A, 1=Room B; Room A dirty; Room B dirty)")
	for action, state in path:
		print(f"  {action} -> {state}")


def state_space_demo() -> None:
	graph = {
		"Start": ["A", "B"],
		"A": ["Goal"],
		"B": ["A", "Goal"],
		"Goal": [],
	}
	print("State-space representation (directed adjacency list):")
	for state, neighbors in graph.items():
		print(f"  {state} -> {neighbors}")


def main() -> None:
	production_system_demo()
	rule_based_decision_demo()
	state_space_demo()
	water_jug_demo()
	missionaries_and_cannibals_demo()
	vacuum_cleaner_demo()


if __name__ == "__main__":
	main()
