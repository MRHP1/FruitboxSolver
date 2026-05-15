import time
import heapq
from solver.graph import BoardGraph, apply_move_to_grid


def _grid_key(grid: list[list[int]]) -> tuple:
    """Convert grid to a hashable key for visited-state tracking."""
    return tuple(v for row in grid for v in row)


def solve_dijkstra(
    grid: list[list[int]],
    max_states: int = 5000,
    branch_limit: int = 15,
) -> dict:
    """
    Dijkstra-based solver for Fruitbox.

    The state space is modelled as a weighted directed graph where each node
    is a board configuration and each edge corresponds to applying one valid
    rectangle move.  Edge weight = –(cells cleared by that move), so the
    shortest (minimum-cost) path found by Dijkstra corresponds to the path
    that maximises total cells cleared.

    Parameters
    ----------
    grid        : 2-D list representing the current board.
    max_states  : hard cap on the number of states popped from the heap.
    branch_limit: maximum number of successor moves explored from each state.
    """
    t0 = time.perf_counter()
    grid_copy = [row[:] for row in grid]

    # Heap entry: (neg_cleared, state_id, grid, moves, cleared)
    # neg_cleared is used as the priority (min-heap → maximise cleared).
    start_key = _grid_key(grid_copy)
    counter = 0  # tie-breaker to avoid comparing grids directly

    # (priority, tie_breaker, current_grid, current_moves, current_cleared)
    heap: list = [(0, counter, grid_copy, [], 0)]

    visited: dict[tuple, int] = {start_key: 0}   # key → best neg_cleared seen

    best_moves: list = []
    best_cleared = 0
    states_explored = 0

    while heap and states_explored < max_states:
        neg_cleared, _, current_grid, current_moves, current_cleared = heapq.heappop(heap)
        states_explored += 1

        # Update global best
        if current_cleared > best_cleared:
            best_cleared = current_cleared
            best_moves = current_moves[:]

        bg = BoardGraph(current_grid)
        valid = bg.find_valid_rectangles()

        if not valid:
            continue

        # Sort by cells cleared descending so we explore the best moves first
        valid.sort(key=lambda m: m[4], reverse=True)

        for move in valid[:branch_limit]:
            r1, c1, r2, c2, cnt = move
            new_grid = apply_move_to_grid(current_grid, move)
            new_cleared = current_cleared + cnt
            new_neg = -(new_cleared)

            key = _grid_key(new_grid)
            # Only enqueue if we found a better (higher cleared) path to this state
            if key not in visited or visited[key] > new_neg:
                visited[key] = new_neg
                counter += 1
                new_moves = current_moves + [(r1, c1, r2, c2)]
                heapq.heappush(heap, (new_neg, counter, new_grid, new_moves, new_cleared))

    elapsed = (time.perf_counter() - t0) * 1000
    return {
        "algorithm": "Dijkstra",
        "moves": best_moves,
        "cleared": best_cleared,
        "states": states_explored,
        "time_ms": round(elapsed, 2),
    }
