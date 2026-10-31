import asyncio

async def run_gpiomon(chip, lines, on_press):
    proc = await asyncio.create_subprocess_exec(
        "gpiomon", # check flags
        stdout=asyncio.subprocess.PIPE)
    async for raw in proc.stdout:
        ts_ns, line = parse(raw.decode()) # parse needs to be written
        on_press(line_to_player[line], ts_ns)