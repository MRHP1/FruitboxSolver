import time
from collections import deque
from solver.graph import BoardGraph, apply_move_to_grid


def solve_bfs(
    grid: list[list[int]],
    max_states: int = 5000,
    beam_width: int = 15,
) -> dict:
    t0 = time.perf_counter()
    grid_copy = [row[:] for row in grid]

    queue: deque[tuple] = deque()
    queue.append((grid_copy, [], 0))

    best_moves: list = []
    best_cleared = 0
    states_explored = 0

    while queue and states_explored < max_states:
        level_size = len(queue)
        next_level: list[tuple] = []

        for _ in range(level_size):
            if states_explored >= max_states:
                break
            current_grid, current_moves, current_cleared = queue.popleft()
            states_explored += 1

            bg = BoardGraph(current_grid)
            valid = bg.find_valid_rectangles()

            if not valid:
                if current_cleared > best_cleared:
                    best_cleared = current_cleared
                    best_moves = current_moves
                continue

            if current_cleared > best_cleared:
                best_cleared = current_cleared
                best_moves = current_moves

            valid.sort(key=lambda m: m[4], reverse=True)

            for move in valid[:beam_width]:
                r1, c1, r2, c2, cnt = move
                new_grid = apply_move_to_grid(current_grid, move)
                new_moves = current_moves + [(r1, c1, r2, c2)]
                new_cleared = current_cleared + cnt
                next_level.append((new_grid, new_moves, new_cleared))

        next_level.sort(key=lambda x: x[2], reverse=True)
        for item in next_level[:beam_width]:
            queue.append(item)

    while queue:
        g, m, c = queue.popleft()
        if c > best_cleared:
            best_cleared = c
            best_moves = m

    elapsed = (time.perf_counter() - t0) * 1000
    return {
        "algorithm": "BFS (Beam)",
        "moves": best_moves,
        "cleared": best_cleared,
        "states": states_explored,
        "time_ms": round(elapsed, 2),
    }
