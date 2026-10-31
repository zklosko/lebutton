from contextlib import asynccontextmanager
import time
from fastapi import FastAPI
from .config import load
from .buzzer import Buzzer
from .companion import Companion

cfg = load()
companion = Companion(cfg.companion)
players = {p.id: p for p in cfg.players}

def on_change(b: Buzzer):
    companion.set_variable("buzzer_state", b.state)
    if b.winner is not None:
        p = players[b.winner]
        companion.set_variable("first_buzzer", p.name)
        companion.press(*p.button)

buzzer = Buzzer(cfg.collect_window_ms / 1000, on_change)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #start input reader task here
    yield
    #cancel it here

app = FastAPI(lifespan=lifespan)

@app.post("/arm")
def arm(): buzzer.arm(); return {"state": buzzer.state}

@app.post("/reset")
def reset(): buzzer.reset; return {"state": buzzer.state}

@app.post("/debug/press/{player}")
def debug_press(player: int):
    buzzer.press(player, time.monotonic_ns())
    return {"state": buzzer.state}