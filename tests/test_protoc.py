from __future__ import annotations

import sys
from asyncio.subprocess import Process, create_subprocess_exec
from collections.abc import AsyncIterator, Awaitable
from contextlib import AsyncExitStack, asynccontextmanager

import pytest


@pytest.mark.asyncio
async def test_protoc() -> None:
    async with AsyncExitStack() as stack:
        aenter = stack.enter_async_context
        protoc = await aenter(
            terminating(create_subprocess_exec(sys.executable, "-mgrpc_tools.protoc"))
        )
        assert (await protoc.wait()) == 0


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
