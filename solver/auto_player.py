from game.board import Board
from solver.greedy_strategy import solve_greedy
from solver.bfs_solver import solve_bfs
from solver.dfs_solver import solve_dfs
from solver.dijkstra_solver import solve_dijkstra


def solve(board: Board, algorithm: str = "greedy", **kwargs) -> dict:
    grid = board.get_grid_2d()
    if algorithm == "greedy":
        return solve_greedy(grid)
    elif algorithm == "bfs":
        return solve_bfs(grid, **kwargs)
    elif algorithm == "dfs":
        return solve_dfs(grid, **kwargs)
    elif algorithm == "dijkstra":
        return solve_dijkstra(grid, **kwargs)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def benchmark(board: Board, max_states: int = 5000) -> list[dict]:
    grid = board.get_grid_2d()
    results = [
        solve_greedy(grid),
        solve_bfs([row[:] for row in grid], max_states=max_states),
        solve_dfs([row[:] for row in grid], max_states=max_states),
        solve_dijkstra([row[:] for row in grid], max_states=max_states),
    ]
    total = board.total_cells()
    for r in results:
        r["pct"] = round(r["cleared"] / total * 100, 1) if total else 0
    return results
