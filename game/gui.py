import sys
# pyrefly: ignore [missing-import]
import pygame
from game.board import Board
from game.logic import GameLogic
from game.timer import Timer
from game import settings as S


STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2


class InputBox:


    def __init__(self, x, y, w, h, default=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = default
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                self.active = False
            elif event.unicode.isdigit() and len(self.text) < 4:
                self.text += event.unicode

    def draw(self, surf, font):
        bg = S.INPUT_ACTIVE_BG if self.active else S.INPUT_BG
        border = S.ACCENT if self.active else S.INPUT_BORDER
        pygame.draw.rect(surf, bg, self.rect, border_radius=6)
        pygame.draw.rect(surf, border, self.rect, 2, border_radius=6)
        txt = font.render(self.text, True, S.TEXT_COLOR)
        surf.blit(
            txt,
            (self.rect.x + 10, self.rect.y + (self.rect.h - txt.get_height()) // 2),
        )

    def value(self, fallback=0):
        try:
            return int(self.text)
        except ValueError:
            return fallback


class Button:


    def __init__(self, x, y, w, h, label, color=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.color = color or S.BUTTON_COLOR
        self.hovered = False

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, surf, font):
        c = S.BUTTON_HOVER if self.hovered else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=8)
        pygame.draw.rect(surf, S.ACCENT, self.rect, 1, border_radius=8)
        txt = font.render(self.label, True, S.BUTTON_TEXT)
        tx = self.rect.x + (self.rect.w - txt.get_width()) // 2
        ty = self.rect.y + (self.rect.h - txt.get_height()) // 2
        surf.blit(txt, (tx, ty))


class FruitboxGUI:


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (S.WINDOW_WIDTH, S.WINDOW_HEIGHT), pygame.RESIZABLE
        )
        pygame.display.set_caption("Fruitbox")
        self.clock = pygame.time.Clock()


        try:
            self.font_lg = pygame.font.SysFont(S.FONT_FAMILY, 42, bold=True)
            self.font_md = pygame.font.SysFont(S.FONT_FAMILY, 24)
            self.font_sm = pygame.font.SysFont(S.FONT_FAMILY, 18)
            self.font_xs = pygame.font.SysFont(S.FONT_FAMILY, 14)
        except Exception:
            self.font_lg = pygame.font.SysFont(S.FONT_FALLBACK, 42, bold=True)
            self.font_md = pygame.font.SysFont(S.FONT_FALLBACK, 24)
            self.font_sm = pygame.font.SysFont(S.FONT_FALLBACK, 18)
            self.font_xs = pygame.font.SysFont(S.FONT_FALLBACK, 14)

        self.state = STATE_MENU
        self._init_menu()


        self.board: Board | None = None
        self.logic: GameLogic | None = None
        self.timer: Timer | None = None


        self.sel_start = None
        self.sel_end = None
        self.dragging = False



    def _init_menu(self):
        cx = S.WINDOW_WIDTH // 2
        self.input_rows = InputBox(cx + 20, 300, 100, 40, str(S.DEFAULT_ROWS))
        self.input_cols = InputBox(cx + 20, 360, 100, 40, str(S.DEFAULT_COLS))
        self.btn_play = Button(cx - 120, 460, 240, 50, "Play Game")

    def _draw_menu(self):
        self.screen.fill(S.BG_COLOR)
        w, h = self.screen.get_size()
        cx = w // 2


        title = self.font_lg.render("FRUITBOX", True, S.ACCENT_LIGHT)
        self.screen.blit(title, (cx - title.get_width() // 2, 100))
        sub = self.font_md.render(
            "Select rectangles that sum to 10!", True, S.TEXT_DIM
        )
        self.screen.blit(sub, (cx - sub.get_width() // 2, 160))


        pygame.draw.line(self.screen, S.ACCENT, (cx - 150, 220), (cx + 150, 220), 2)


        lbl_r = self.font_sm.render("Rows:", True, S.TEXT_COLOR)
        lbl_c = self.font_sm.render("Cols:", True, S.TEXT_COLOR)
        self.screen.blit(lbl_r, (cx - 70, 308))
        self.screen.blit(lbl_c, (cx - 70, 368))


        self.input_rows.rect.x = cx + 20
        self.input_cols.rect.x = cx + 20
        self.btn_play.rect.x = cx - 120

        self.input_rows.draw(self.screen, self.font_sm)
        self.input_cols.draw(self.screen, self.font_sm)
        self.btn_play.draw(self.screen, self.font_md)

        hint = self.font_xs.render(
            f"Grid size: {S.MIN_GRID_SIZE}–{S.MAX_GRID_SIZE} rows/cols",
            True,
            S.TEXT_DIM,
        )
        self.screen.blit(hint, (cx - hint.get_width() // 2, 540))

    def _menu_event(self, event):
        self.input_rows.handle_event(event)
        self.input_cols.handle_event(event)
        if self.btn_play.handle_event(event):
            self._start_game()



    def _get_grid_size(self):
        rows = max(
            S.MIN_GRID_SIZE,
            min(S.MAX_GRID_SIZE, self.input_rows.value(S.DEFAULT_ROWS)),
        )
        cols = max(
            S.MIN_GRID_SIZE,
            min(S.MAX_GRID_SIZE, self.input_cols.value(S.DEFAULT_COLS)),
        )
        return rows, cols

    def _start_game(self):
        rows, cols = self._get_grid_size()
        self.board = Board(rows, cols)
        self.logic = GameLogic(self.board)
        self.timer = Timer(S.TIMER_SECONDS)
        self.timer.start()
        self.sel_start = self.sel_end = None
        self.dragging = False
        self.state = STATE_PLAYING



    def _grid_geometry(self):

        w, h = self.screen.get_size()
        header_h = 70
        footer_h = 50
        margin = 20
        avail_w = w - 2 * margin
        avail_h = h - header_h - footer_h - 2 * margin

        if self.board is None:
            return 0, 0, 40

        cell = min(
            avail_w // self.board.cols,
            avail_h // self.board.rows,
            S.MAX_CELL_SIZE,
        )
        cell = max(cell, S.MIN_CELL_SIZE)

        grid_w = cell * self.board.cols
        grid_h = cell * self.board.rows
        ox = (w - grid_w) // 2
        oy = header_h + margin + (avail_h - grid_h) // 2
        return ox, oy, cell

    def _pixel_to_cell(self, px, py):
        ox, oy, cell = self._grid_geometry()
        c = (px - ox) // cell
        r = (py - oy) // cell
        if 0 <= r < self.board.rows and 0 <= c < self.board.cols:
            return r, c
        return None



    def _get_cell_font(self, cell_size):
        sz = max(10, min(cell_size - 6, 28))
        return pygame.font.SysFont(S.FONT_FAMILY, sz, bold=True)

    def _draw_game(self):
        self.screen.fill(S.BG_COLOR)
        w, h = self.screen.get_size()
        ox, oy, cell = self._grid_geometry()


        pygame.draw.rect(self.screen, S.HEADER_BG, (0, 0, w, 65))
        title = self.font_md.render("FRUITBOX", True, S.ACCENT_LIGHT)
        self.screen.blit(title, (20, 18))

        score_txt = self.font_md.render(
            f"Score: {self.logic.score}", True, S.TEXT_COLOR
        )
        self.screen.blit(
            score_txt, (w // 2 - score_txt.get_width() // 2, 18)
        )

        if self.timer:
            timer_txt = self.font_md.render(
                self.timer.display(), True, S.TEXT_COLOR
            )
            self.screen.blit(
                timer_txt, (w - timer_txt.get_width() - 20, 18)
            )


        grid_rect = pygame.Rect(
            ox - 4,
            oy - 4,
            cell * self.board.cols + 8,
            cell * self.board.rows + 8,
        )
        pygame.draw.rect(self.screen, S.GRID_BG_COLOR, grid_rect, border_radius=8)


        font_cell = self._get_cell_font(cell)
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                x = ox + c * cell
                y = oy + r * cell
                val = self.board.get(r, c)
                cr = pygame.Rect(
                    x + S.CELL_PADDING,
                    y + S.CELL_PADDING,
                    cell - 2 * S.CELL_PADDING,
                    cell - 2 * S.CELL_PADDING,
                )
                if val == 0:
                    pygame.draw.rect(
                        self.screen, S.EMPTY_CELL_COLOR, cr, border_radius=S.CELL_RADIUS
                    )
                else:
                    color = S.DIGIT_COLORS.get(val, S.TEXT_COLOR)
                    bg = tuple(max(0, v // 4) for v in color)
                    pygame.draw.rect(self.screen, bg, cr, border_radius=S.CELL_RADIUS)
                    pygame.draw.rect(
                        self.screen, color, cr, 1, border_radius=S.CELL_RADIUS
                    )
                    if cell >= 16:
                        txt = font_cell.render(str(val), True, color)
                        tx = cr.x + (cr.w - txt.get_width()) // 2
                        ty = cr.y + (cr.h - txt.get_height()) // 2
                        self.screen.blit(txt, (tx, ty))


        self._draw_selection(ox, oy, cell)


        remaining = self.board.count_remaining()
        total = self.board.total_cells()
        hint = self.font_xs.render(
            f"Remaining: {remaining}/{total}  |  Drag to select a rectangle that sums to 10  |  ESC = menu",
            True,
            S.TEXT_DIM,
        )
        self.screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 30))

    def _draw_selection(self, ox, oy, cell):
        if self.sel_start is None or self.sel_end is None:
            return

        r1, c1 = self.sel_start
        r2, c2 = self.sel_end
        if r1 > r2:
            r1, r2 = r2, r1
        if c1 > c2:
            c1, c2 = c2, c1
        r1 = max(0, r1)
        c1 = max(0, c1)
        r2 = min(self.board.rows - 1, r2)
        c2 = min(self.board.cols - 1, c2)

        sx = ox + c1 * cell
        sy = oy + r1 * cell
        sw = (c2 - c1 + 1) * cell
        sh = (r2 - r1 + 1) * cell

        s = self.logic.rect_sum(r1, c1, r2, c2)
        valid = s == S.TARGET_SUM and self.logic.count_nonzero_in_rect(r1, c1, r2, c2) > 0
        color = S.SELECTION_VALID if valid else S.SELECTION_INVALID

        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((*color, S.OVERLAY_ALPHA))
        self.screen.blit(overlay, (sx, sy))
        pygame.draw.rect(self.screen, color, (sx, sy, sw, sh), 2, border_radius=2)

        sum_txt = self.font_sm.render(f"Sum={s}", True, color)
        self.screen.blit(sum_txt, (sx + sw + 6, sy))



    def _game_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = self._pixel_to_cell(*event.pos)
            if cell:
                self.sel_start = cell
                self.sel_end = cell
                self.dragging = True

        if event.type == pygame.MOUSEMOTION and self.dragging:
            cell = self._pixel_to_cell(*event.pos)
            if cell:
                self.sel_end = cell

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            if self.sel_start and self.sel_end:
                r1, c1 = self.sel_start
                r2, c2 = self.sel_end
                if r1 > r2:
                    r1, r2 = r2, r1
                if c1 > c2:
                    c1, c2 = c2, c1
                if self.logic.is_valid_move(r1, c1, r2, c2):
                    self.logic.apply_move(r1, c1, r2, c2)
            self.sel_start = self.sel_end = None

    def _check_game_over(self):
        if self.timer and self.timer.is_expired():
            self.state = STATE_GAME_OVER
            return
        if self.board.count_remaining() == 0:
            self.state = STATE_GAME_OVER
            return
        if not self.logic.has_valid_moves():
            self.state = STATE_GAME_OVER



    def _draw_game_over(self):
        self.screen.fill(S.BG_COLOR)
        w, h = self.screen.get_size()
        cx, cy = w // 2, h // 2

        title = self.font_lg.render("GAME OVER", True, S.ACCENT_LIGHT)
        self.screen.blit(title, (cx - title.get_width() // 2, cy - 120))

        total = self.board.total_cells()
        cleared = self.logic.score
        pct = round(cleared / total * 100, 1) if total else 0

        lines = [
            f"Score: {cleared} / {total}  ({pct}%)",
            f"Remaining: {self.board.count_remaining()}",
        ]
        for i, line in enumerate(lines):
            txt = self.font_md.render(line, True, S.TEXT_COLOR)
            self.screen.blit(txt, (cx - txt.get_width() // 2, cy - 30 + i * 40))

        hint = self.font_sm.render(
            "Press ENTER to return to menu", True, S.TEXT_DIM
        )
        self.screen.blit(hint, (cx - hint.get_width() // 2, cy + 120))



    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if self.state == STATE_MENU:
                    self._menu_event(event)
                elif self.state == STATE_PLAYING:
                    self._game_event(event)
                elif self.state == STATE_GAME_OVER:
                    if event.type == pygame.KEYDOWN and event.key in (
                        pygame.K_RETURN,
                        pygame.K_ESCAPE,
                    ):
                        self.state = STATE_MENU

                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        event.size, pygame.RESIZABLE
                    )


            if self.state == STATE_PLAYING:
                self._check_game_over()


            if self.state == STATE_MENU:
                self._draw_menu()
            elif self.state == STATE_PLAYING:
                self._draw_game()
            elif self.state == STATE_GAME_OVER:
                self._draw_game_over()

            pygame.display.flip()
            self.clock.tick(S.FPS)

        pygame.quit()
