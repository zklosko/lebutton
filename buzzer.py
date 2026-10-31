import asyncio
import logging
from enum import StrEnum

log = logging.getLogger("buzzer")

class State(StrEnum):
    IDLE = "idle"
    ARMED = "armed"
    COLLECTING = "collecting" # first press seen
    LOCKED = "locked"

class Buzzer:
    def __init__(self, window_s: float, on_change):
        self.window_s = window_s
        self.on_change = on_change
        self.state = State.IDLE
        self.pending: list[tuple[int, int]] = []
        self.winner: int | None = None
        self.deltas: list[tuple[int, int]] = []
        self.locked_out: set[int] = set()
        self._task: asyncio.Task | None = None

    def arm(self):
        # Refuse unless idle, clear pending/winner
        if self.state != State.IDLE:
            return
        self._clear()
        self.state = State.ARMED
        self.on_change(self)

    def reset(self):
        # Back to idle
        if self._task:
            self._task.cancel()
            self._task = None
        self._clear()
        self.state = State.IDLE
        self.on_change(self)

    def _clear(self):
        self.winner = None
        self.pending = []
        self.deltas = []

    def press(self, player_id: int, ts_ns: int):
        if player_id in self.locked_out:
            log.info("ignored press from locked-out player %s", player_id)
            return  # maybe log this at some point
        if self.state is State.ARMED:
            self.pending.append((ts_ns, player_id))
            self.state = State.COLLECTING
            asyncio.create_task(self._resolve())
        elif self.state is State.COLLECTING:
            self.pending.append((ts_ns, player_id))
        elif self.state is State.IDLE:
            # false start from player
            log.info("press while idle: player %s at %s", player_id, ts_ns)
            return

    async def _resolve(self):
        await asyncio.sleep(self.window_s)
        self.pending.sort()
        win_ts, self.winner = self.pending[0]
        self.deltas = [(pid, ts - win_ts) for ts, pid in self.pending]
        self.state = State.LOCKED
        self._task = None
        self.on_change(self)