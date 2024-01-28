from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Generator, Iterator
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import Any

import grpc.aio
import pytest
import pytest_asyncio

from sample_pb2_grpc import add_SampleServicer_to_server

from . import AsyncSampleStub, SampleServicer, SampleStub


# asyncio fixtures
@pytest.fixture(scope="module")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="module")
async def grpc_addr(host: str = "localhost") -> AsyncIterator[str]:
    with ThreadPoolExecutor() as executor:
        servicer = SampleServicer()
        server = grpc.aio.server(executor)
        add_SampleServicer_to_server(servicer, server)
        port = server.add_insecure_port(f"{host}:0")
        await server.start()
        try:
            yield f"{host}:{port}"
        finally:
            await server.stop(grace=None)


@pytest.fixture(scope="module")
def sample_stub(grpc_addr: str) -> Iterator[SampleStub]:
    with grpc.insecure_channel(grpc_addr) as channel:
        yield SampleStub(channel=channel)


@pytest_asyncio.fixture(scope="module")
async def async_sample_stub(grpc_addr: str) -> AsyncIterator[AsyncSampleStub]:
    async with grpc.aio.insecure_channel(grpc_addr) as channel:
        yield AsyncSampleStub(channel=channel)
