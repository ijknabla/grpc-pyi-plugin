from __future__ import annotations

import sys
from asyncio.subprocess import Process, create_subprocess_exec
from collections.abc import AsyncIterator, Awaitable
from contextlib import AsyncExitStack, asynccontextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.mark.asyncio
async def test_protoc(
    sample_proto_path: Path,
) -> None:
    async with AsyncExitStack() as stack:
        aenter = stack.enter_async_context
        enter = stack.enter_context
        directory = Path(enter(TemporaryDirectory()))
        protoc = await aenter(
            terminating(
                create_subprocess_exec(
                    sys.executable,
                    "-mgrpc_tools.protoc",
                    f"-I{sample_proto_path.parent}",
                    f"{sample_proto_path.name}",
                    f"--grpc_pyi_out={directory}",
                )
            )
        )
        assert (await protoc.wait()) == 0


@asynccontextmanager
async def terminating(process: Process | Awaitable[Process]) -> AsyncIterator[Process]:
    if isinstance(process, Awaitable):
        process = await process

    try:
        yield process
    finally:
        if process.returncode is None:
            process.terminate()
            await process.wait()
