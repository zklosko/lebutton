import asyncio

import pytest

from buzzer import Buzzer, State


@pytest.mark.asyncio
async def test_lowest_timestamp_wins_inside_window():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.arm()
    b.press(2, 1_000_500)
    b.press(1, 1_000_000)
    await asyncio.sleep(0.01)
    assert b.state is State.LOCKED and b.winner == 1

@pytest.mark.asyncio
async def test_button_ignore_when_idle():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.press(1, 1_000_000)
    await asyncio.sleep(0.01)
    assert b.state is State.IDLE and b.winner is None

@pytest.mark.asyncio
async def test_press_after_window_is_ignored():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.arm()
    b.press(2, 1_000_500)
    b.press(1, 1_000_000)
    await asyncio.sleep(0.01)
    b.press(3, 900_500)
    assert b.state is State.LOCKED and b.winner == 1

@pytest.mark.asyncio
async def test_locked_out_player_ignore():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.locked_out.add(1)
    b.arm()
    b.press(1, 1_000_000)
    b.press(2, 1_000_500)
    await asyncio.sleep(0.01)
    assert b.state is State.LOCKED and b.winner == 2

@pytest.mark.asyncio
async def test_arm_and_reset_rules():
    b = Buzzer(window_s=0.005, on_change=lambda _: None)
    b.arm()
    b.arm() # intentional
    assert b.state is State.ARMED
    b.press(1, 1_000_000)
    b.reset()
    await asyncio.sleep(0.01)
    assert b.state is State.IDLE
