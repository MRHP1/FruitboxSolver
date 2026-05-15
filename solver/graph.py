from game.settings import TARGET_SUM


class BoardGraph:

    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.ps = self._build_prefix_sum()

    def _build_prefix_sum(self) -> list[list[int]]:
        R, C = self.rows, self.cols
        ps = [[0] * (C + 1) for _ in range(R + 1)]
        for i in range(R):
            for j in range(C):
                ps[i + 1][j + 1] = (
                    self.grid[i][j] + ps[i][j + 1] + ps[i + 1][j] - ps[i][j]
                )
        return ps

    def rect_sum(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (
            self.ps[r2 + 1][c2 + 1]
            - self.ps[r1][c2 + 1]
            - self.ps[r2 + 1][c1]
            + self.ps[r1][c1]
        )

    def find_valid_rectangles(
        self, target: int = TARGET_SUM
    ) -> list[tuple[int, int, int, int, int]]:
        moves = []
        R, C = self.rows, self.cols
        for r1 in range(R):
            for c1 in range(C):
                if self.grid[r1][c1] == 0:
                    continue
                for r2 in range(r1, R):
                    if self.rect_sum(r1, c1, r2, c1) > target:
                        break
                    for c2 in range(c1, C):
                        s = self.rect_sum(r1, c1, r2, c2)
                        if s == target:
                            cnt = sum(
                                1
                                for i in range(r1, r2 + 1)
                                for j in range(c1, c2 + 1)
                                if self.grid[i][j] != 0
                            )
                            if cnt > 0:
                                moves.append((r1, c1, r2, c2, cnt))
                        elif s > target:
                            break
        return moves

    @staticmethod
    def rects_overlap(a: tuple, b: tuple) -> bool:
        ar1, ac1, ar2, ac2 = a[:4]
        br1, bc1, br2, bc2 = b[:4]
        if ar2 < br1 or br2 < ar1:
            return False
        if ac2 < bc1 or bc2 < ac1:
            return False
        return True


def apply_move_to_grid(
    grid: list[list[int]], move: tuple
) -> list[list[int]]:
    r1, c1, r2, c2 = move[:4]
    new_grid = [row[:] for row in grid]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            new_grid[r][c] = 0
    return new_grid
