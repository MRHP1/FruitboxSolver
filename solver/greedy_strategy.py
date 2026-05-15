import time
from solver.graph import BoardGraph, apply_move_to_grid


def solve_greedy(
    grid: list[list[int]],
) -> dict:
    t0 = time.perf_counter()
    current = [row[:] for row in grid]
    moves: list[tuple] = []
    total_cleared = 0
    states = 0

    while True:
        bg = BoardGraph(current)
        valid = bg.find_valid_rectangles()
        states += 1

        if not valid:
            break

        best = max(valid, key=lambda m: m[4])
        r1, c1, r2, c2, cnt = best
        moves.append((r1, c1, r2, c2))
        total_cleared += cnt
        current = apply_move_to_grid(current, best)

    elapsed = (time.perf_counter() - t0) * 1000
    return {
        "algorithm": "Greedy",
        "moves": moves,
        "cleared": total_cleared,
        "states": states,
        "time_ms": round(elapsed, 2),
    }
