import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from buzzer import Buzzer
from companion import Companion
from config import load

logging.basicConfig(level=logging.INFO)

cfg = load()
companion = Companion(cfg.companion)
players = {p.id: p for p in cfg.players}

def describe_deltas(b: Buzzer):
    return [
        {
            "player": pid,
            "name": players[pid].name,
            "behind_winner_ms": round(delta_ns / 1_000_000, 3),
        }
        for pid, delta_ns in b.deltas
    ]

def on_change(b: Buzzer):
    companion.set_variable("buzzer_state", b.state)
    w = players[buzzer.winner].name if buzzer.winner is not None else None
    print(f"state={b.state} winner={w} deltas={describe_deltas(b)}")
    if b.winner is not None:
        p = players[b.winner]
        companion.set_variable("first_buzzer", p.name)
        companion.press(*p.button)

buzzer = Buzzer(cfg.collect_window_ms / 1000, on_change)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #start input reader task here
    yield
    await companion.close()

app = FastAPI(lifespan=lifespan)

@app.get("/status")
def status():
    w = players[buzzer.winner].name if buzzer.winner is not None else None
    return {"state": buzzer.state, "winner": w, "deltas": describe_deltas(buzzer)}

@app.get("/health")
def health():
    return {"ok": True, "players": [p.name for p in cfg.players]}

@app.post("/arm")
async def arm(): buzzer.arm(); return {"state": buzzer.state}

@app.post("/reset")
async def reset(): buzzer.reset(); return {"state": buzzer.state}

@app.post("/debug/press/{player}")
async def debug_press(player: int):
    if player not in players:
        raise HTTPException(404, f"unknown player {player}")
    buzzer.press(player, time.monotonic_ns())
    return {"state": buzzer.state}