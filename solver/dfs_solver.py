import sys
import time
from solver.graph import BoardGraph, apply_move_to_grid

sys.setrecursionlimit(20000)

def solve_dfs(
    grid: list[list[int]],
    max_states: int = 5000,
    branch_limit: int = 10,
) -> dict:
    t0 = time.perf_counter()
    grid_copy = [row[:] for row in grid]

    best: dict = {"moves": [], "cleared": 0}
    counter = {"states": 0}

    def dfs(current_grid, current_moves, current_cleared):
        if counter["states"] >= max_states:
            return
        counter["states"] += 1

        bg = BoardGraph(current_grid)
        valid = bg.find_valid_rectangles()

        if not valid:
            if current_cleared > best["cleared"]:
                best["cleared"] = current_cleared
                best["moves"] = current_moves[:]
            return

        if current_cleared > best["cleared"]:
            best["cleared"] = current_cleared
            best["moves"] = current_moves[:]

        valid.sort(key=lambda m: m[4], reverse=True)

        for move in valid[:branch_limit]:
            if counter["states"] >= max_states:
                return
            r1, c1, r2, c2, cnt = move
            new_grid = apply_move_to_grid(current_grid, move)
            current_moves.append((r1, c1, r2, c2))
            dfs(new_grid, current_moves, current_cleared + cnt)
            current_moves.pop()

    dfs(grid_copy, [], 0)

    elapsed = (time.perf_counter() - t0) * 1000
    return {
        "algorithm": "DFS",
        "moves": best["moves"],
        "cleared": best["cleared"],
        "states": counter["states"],
        "time_ms": round(elapsed, 2),
    }
