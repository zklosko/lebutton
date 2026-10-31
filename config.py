from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    gpio_line: int
    button: tuple[int, int, int]

class CompanionCfg(BaseModel):
    base_url: str
    timeout_s: float = 0.5

class Config(BaseModel):
    collect_window_ms: float = 4
    input: Literal["fake", "gpiomon"] = "fake"
    gpiomon_chip: str = "gpiochip0"
    companion: CompanionCfg
    players: list[Player]

def load(path: str = "config.yml") -> Config:
    return Config.model_validate(yaml.safe_load(Path(path).read_text()))