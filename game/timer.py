import time

class Timer:

    def __init__(self, seconds: int):
        self.total = seconds
        self._start: float | None = None
        self._paused_remaining: float | None = None

    def start(self):
        self._start = time.time()
        self._paused_remaining = None

    def pause(self):
        if self._start is not None and self._paused_remaining is None:
            self._paused_remaining = self.remaining()

    def resume(self):
        if self._paused_remaining is not None:
            self._start = time.time() - (self.total - self._paused_remaining)
            self._paused_remaining = None

    def remaining(self) -> float:
        if self._paused_remaining is not None:
            return max(0.0, self._paused_remaining)
        if self._start is None:
            return float(self.total)
        elapsed = time.time() - self._start
        return max(0.0, self.total - elapsed)

    def is_expired(self) -> bool:
        return self.remaining() <= 0

    def display(self) -> str:
        rem = int(self.remaining())
        m, s = divmod(rem, 60)
        return f"{m}:{s:02d}"
