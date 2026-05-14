from game.board import Board
from game.settings import TARGET_SUM

class GameLogic:

    def __init__(self, board: Board):
        self.board = board
        self.score = 0
        self._build_prefix_sum()

    def _build_prefix_sum(self):
        R, C = self.board.rows, self.board.cols
        self.ps = [[0] * (C + 1) for _ in range(R + 1)]
        for i in range(R):
            for j in range(C):
                self.ps[i + 1][j + 1] = (
                    self.board.get(i, j)
                    + self.ps[i][j + 1]
                    + self.ps[i + 1][j]
                    - self.ps[i][j]
                )

    def rect_sum(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (
            self.ps[r2 + 1][c2 + 1]
            - self.ps[r1][c2 + 1]
            - self.ps[r2 + 1][c1]
            + self.ps[r1][c1]
        )

    def count_nonzero_in_rect(self, r1: int, c1: int, r2: int, c2: int) -> int:
        count = 0
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if self.board.get(r, c) != 0:
                    count += 1
        return count

    def is_valid_move(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        if r1 > r2 or c1 > c2:
            return False
        if r1 < 0 or c1 < 0 or r2 >= self.board.rows or c2 >= self.board.cols:
            return False
        s = self.rect_sum(r1, c1, r2, c2)
        if s != TARGET_SUM:
            return False
        return self.count_nonzero_in_rect(r1, c1, r2, c2) > 0

    def apply_move(self, r1: int, c1: int, r2: int, c2: int) -> int:
        cleared = self.board.clear_rect(r1, c1, r2, c2)
        self.score += cleared
        self._build_prefix_sum()
        return cleared

    def has_valid_moves(self) -> bool:
        R, C = self.board.rows, self.board.cols
        for r1 in range(R):
            for c1 in range(C):
                if self.board.is_empty(r1, c1):
                    continue
                for r2 in range(r1, R):
                    col_sum = self.rect_sum(r1, c1, r2, c1)
                    if col_sum > TARGET_SUM:
                        break
                    for c2 in range(c1, C):
                        s = self.rect_sum(r1, c1, r2, c2)
                        if s == TARGET_SUM:
                            if self.count_nonzero_in_rect(r1, c1, r2, c2) > 0:
                                return True
                        elif s > TARGET_SUM:
                            break
        return False

    def find_all_valid_moves(self) -> list[tuple[int, int, int, int, int]]:
        moves = []
        R, C = self.board.rows, self.board.cols
        for r1 in range(R):
            for c1 in range(C):
                if self.board.is_empty(r1, c1):
                    continue
                for r2 in range(r1, R):
                    col_sum = self.rect_sum(r1, c1, r2, c1)
                    if col_sum > TARGET_SUM:
                        break
                    for c2 in range(c1, C):
                        s = self.rect_sum(r1, c1, r2, c2)
                        if s == TARGET_SUM:
                            cnt = self.count_nonzero_in_rect(r1, c1, r2, c2)
                            if cnt > 0:
                                moves.append((r1, c1, r2, c2, cnt))
                        elif s > TARGET_SUM:
                            break
        return moves
