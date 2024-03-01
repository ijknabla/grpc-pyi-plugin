from __future__ import annotations

from asyncio.subprocess import Process
from collections.abc import AsyncIterator, Awaitable
from contextlib import asynccontextmanager


@asynccontextmanager
async def terminating(process: Process | Awaitable[Process]) -> AsyncIterator[Process]:
    if isinstance(process, Awaitable):
        process = await process

    try:
        yield process
    finally:
        if process.returncode is not None:
            return

        process.terminate()
        await process.wait()
