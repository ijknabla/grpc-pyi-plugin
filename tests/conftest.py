from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Generator, Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import grpc.aio
import pytest
import pytest_asyncio

from sample_pb2_grpc import add_SampleServicer_to_server

from . import AsyncSampleServicer, AsyncSampleStub, SampleServicer, SampleStub


# asyncio fixtures
@pytest.fixture(scope="module")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="module")
def sample_service_address(host: str = "localhost") -> Iterator[str]:
    with ThreadPoolExecutor() as executor:
        servicer = SampleServicer()
        server = grpc.server(executor)
        add_SampleServicer_to_server(servicer, server)
        port = server.add_insecure_port(f"{host}:0")
        server.start()
        try:
            yield f"{host}:{port}"
        finally:
            server.stop(grace=None)


@pytest_asyncio.fixture(scope="module")
async def async_sample_service_address(host: str = "localhost") -> AsyncIterator[str]:
    with ThreadPoolExecutor() as executor:
        servicer = AsyncSampleServicer()
        server = grpc.aio.server(executor)
        add_SampleServicer_to_server(servicer, server)
        port = server.add_insecure_port(f"{host}:0")
        await server.start()
        try:
            yield f"{host}:{port}"
        finally:
            await server.stop(grace=None)


@pytest.fixture(scope="module")
def sample_stub(sample_service_address: str) -> Iterator[SampleStub]:
    with grpc.insecure_channel(sample_service_address) as channel:
        yield SampleStub(channel=channel)


@pytest_asyncio.fixture(scope="module")
async def async_sample_stub(async_sample_service_address: str) -> AsyncIterator[AsyncSampleStub]:
    async with grpc.aio.insecure_channel(async_sample_service_address) as channel:
        yield AsyncSampleStub(channel=channel)
