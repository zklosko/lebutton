import asyncio, httpx

class Companion:
    def __init__(self, cfg):
        self.base = cfg.base_url
        self.http = httpx.AsyncClient(timeout=cfg.timeout_s)

    async def _post(self, path: str, **params):
        try:
            await self.http.post(f"{self.base}{path}", params=params)
        except httpx.HTTPError as e:
            print(f"companion error: {e}")

    def set_variable(self, name: str, value: str):
        asyncio.create_task(self._post(f"/api/custom-variable/{name}/value"))

    def press(self, page: int, row: int, col: int):
        asyncio.create_task(self._post(f"/api/location/{page}/{row}/{col}"))