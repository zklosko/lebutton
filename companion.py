import asyncio
import logging

import httpx

log = logging.getLogger("companion")

class Companion:
    def __init__(self, cfg):
        self.base = cfg.base_url
        self.http = httpx.AsyncClient(timeout=cfg.timeout_s)
        self._tasks: set[asyncio.Task] = set()

    def _fire(self, path: str, **params):
        task = asyncio.create_task(self._post(path, params))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _post(self, path: str, params: dict):
        try:
            r = await self.http.post(f"{self.base}{path}", params=params)
            r.raise_for_status()
        except httpx.HTTPError as e:
            log.warning(f"companion {path} failed: {e}")

    def set_variable(self, name: str, value: str):
        self._fire(f"/api/custom-variable/{name}/value", value=str(value))

    def press(self, page: int, row: int, col: int):
        self._fire(f"/api/location/{page}/{row}/{col}/press")

    async def close(self):
        await self.http.aclose()