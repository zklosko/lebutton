import pytest
import asyncio
from buzzer import Buzzer, State

@pytest.mark.asyncio
async def test_lowest_timestamp_wins_inside_window():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.arm()
    b.press(2, 1_000_500)
    b.press(1, 1_000_000)
    await asyncio.sleep(0.01)
    assert b.state is State.LOCKED and b.winner == 1