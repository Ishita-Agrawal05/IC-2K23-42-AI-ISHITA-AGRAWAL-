from collections import deque


def water_jug(capacity1,   capacity2, target):
    queue = deque()
    visited = set()
    # Initial state: both jugs are empty
    queue.append((0, 0, []))
    while queue:
        jug1, jug2, path = queue.popleft()

        # If target   is achieved
        if jug1 == target or jug2 == target:
            print(" Solution found:")
            for step in path:
                print (step)
            print(f"Final State: ({jug1}, {jug2})")
            return

        # Avoid visiting the same state again
        if (jug1, jug2) in visited:
            continue

        visited.add((jug1, jug2))
        # 1. Fill  Jug 1
        new_state = (capacity1, jug2)
        if new_state not in visited:
            queue.append((
                capacity1,
                jug2,
                path + [f"Fill Jug 1 -> ({capacity1}, {jug2})"]
            ))

        # 2. Fill Jug 2
        new_state = (jug1, capacity2)
        if new_state not in visited:
            queue.append((
                jug1,
                capacity2,
                path + [f"Fill Jug 2 -> ({jug1}, {capacity2})"]
            ))
        # 3. Empty Jug 1
        new_state =   (0, jug2)
        if new_state not in visited:
            queue.append((
                0,
                jug2,
                path  + [f"Empty Jug 1 -> (0, {jug2})"]
            )) 

        # 4. Empty Jugg  2
        new_state = (jug1,  0)
        if new_state not in visited:
            queue.append((
                jug1,
                0,
                path + [f"Empty   Jug 2 -> ({jug1}, 0)"]
            ))

        # 5. Pour Jug 1 ->    Jug 2
        amount = min(jug1, capacity2 - jug2)
        new_jug1 = jug1 - amount
        new_jug2 = jug2 + amount

        new_state = (new_jug1, new_jug2)
        if new_state not   in visited:
            queue.append((
                new_jug1,
                new_jug2 ,
                path + [
                    f"Pour Jug 1 -> Jug 2 -> ({new_jug1}, {new_jug2})"
                ]
            ))

        # 6. Pour Jug 2 -> Jug 1
        amount = min(jug2, capacity1 - jug1)
        new_jug1 = jug1 + amount
        new_jug2 = jug2 - amount
        new_state = (new_jug1, new_jug2)
        if new_state  not in visited:
            queue.append((
                new_jug1,
                new_jug2,
                path + [
                    f"Pour Jug 2 -> Jug 1 -> ({new_jug1}, {new_jug2})"
                ]
            ))

    print("No solution  exists.")


# Example:
# Jug 1 = 4 litres
# Jug 2 = 3 litres
# Target = 2 litres

water_jug(4, 3, 2)