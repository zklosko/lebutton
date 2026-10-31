import asyncio
from enum import StrEnum

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
        self.locked_out: set[int] = set()

    def arm(self):
        # Refuse unless idle, clear pending/winner

    def reset(self):
        # Back to idle

    def press(self, player_id: int, ts_ns: int):
        if player_id in self.locked_out:
            return  # maybe log this at some point
        if self.state is State.ARMED:
            self.pending.append((ts_ns, player_id))
            self.state = State.COLLECTING
            asyncio.create_task(self._resolve())
        elif self.state is State.COLLECTING:
            self.pending.append((ts_ns, player_id))
        elif self.state is State.IDLE:
            # false start from player

    async def _resolve(self):
        await asyncio.sleep(self.window_s)
        ts, winner = min(self.pending)
        self.winner, self.state = winner, State.LOCKED
        self.on_change(self)