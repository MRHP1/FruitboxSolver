import random


class Board:

    def __init__(self, rows: int, cols: int, grid=None):
        self.rows = rows
        self.cols = cols
        if grid is not None:
            self.grid = [row[:] for row in grid]
        else:
            self.grid = self._generate()

    def _generate(self) -> list[list[int]]:
        return [
            [random.randint(1, 9) for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def get(self, r: int, c: int) -> int:
        return self.grid[r][c]

    def set(self, r: int, c: int, val: int):
        self.grid[r][c] = val

    def is_empty(self, r: int, c: int) -> bool:
        return self.grid[r][c] == 0

    def clear_rect(self, r1: int, c1: int, r2: int, c2: int) -> int:
        cleared = 0
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if self.grid[r][c] != 0:
                    cleared += 1
                    self.grid[r][c] = 0
        return cleared

    def count_remaining(self) -> int:
        return sum(
            1 for r in range(self.rows) for c in range(self.cols)
            if self.grid[r][c] != 0
        )

    def total_cells(self) -> int:
        return self.rows * self.cols

    def copy(self) -> "Board":
        return Board(self.rows, self.cols, grid=self.grid)

    def to_tuple(self) -> tuple:
        return tuple(tuple(row) for row in self.grid)

    def get_grid_2d(self) -> list[list[int]]:
        return [row[:] for row in self.grid]

    def __repr__(self):
        lines = []
        for row in self.grid:
            lines.append(" ".join(str(v) if v != 0 else "." for v in row))
        return "\n".join(lines)
