from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Callable, Generator, Iterator, Sequence
from concurrent import futures
from typing import Any

import grpc.aio
import pytest
import pytest_asyncio

from sample_pb2_grpc import SampleStub, add_SampleServicer_to_server

from . import SampleServicer


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
async def grpc_server(
    grpc_addr: str,
) -> AsyncGenerator[grpc.aio.Server, None]:
    with futures.ThreadPoolExecutor() as executor:
        servicer = SampleServicer()
        server = grpc.aio.server(executor)
        add_SampleServicer_to_server(servicer, server)
        server.add_insecure_port(grpc_addr)
        await server.start()
        try:
            yield server
        finally:
            await server.stop(grace=None)


@pytest.fixture(scope="module")
def grpc_create_channel(
    request: pytest.FixtureRequest,
    grpc_addr: str,
    grpc_server: grpc.aio.Server,
) -> Callable[..., grpc.aio.Channel]:
    def _create_channel(
        credentials: grpc.ChannelCredentials | None = None, options: Any = None
    ) -> grpc.aio.Channel:
        # if request.config.getoption('grpc-fake'):
        #     return FakeChannel(grpc_server, credentials)
        if credentials is not None:
            return grpc.aio.secure_channel(grpc_addr, credentials, options)
        return grpc.aio.insecure_channel(grpc_addr, options)

    return _create_channel


@pytest_asyncio.fixture(scope="module")
async def grpc_channel(
    grpc_create_channel: Callable[..., grpc.aio.Channel]
) -> AsyncGenerator[grpc.aio.Channel, None]:
    async with grpc_create_channel() as channel:
        yield channel


@pytest.fixture(scope="module")
def grpc_stub_cls() -> type[SampleStub[grpc.aio.Channel]]:
    return SampleStub


@pytest.fixture(scope="module")
def sample_stub(grpc_addr: str) -> SampleStub[grpc.Channel]:
    channel = grpc.insecure_channel(grpc_addr)
    return SampleStub(channel)


@pytest.fixture(scope="module")
def async_sample_stub(grpc_addr: str) -> SampleStub[grpc.aio.Channel]:
    channel = grpc.aio.insecure_channel(grpc_addr)
    return SampleStub(channel)
