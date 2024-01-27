from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Callable, Generator, Sequence
from concurrent import futures
from typing import Any

import grpc.aio
import pytest
import pytest_asyncio

from sample_pb2_grpc import SampleServicer, SampleStub, add_SampleServicer_to_server


# asyncio fixtures
@pytest.fixture(scope="module")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


# gRPC fixtures
@pytest.fixture(scope="module")
def _grpc_server(
    request: pytest.FixtureRequest,
    grpc_addr: str,
    grpc_interceptors: Sequence[grpc.aio.ServerInterceptor[Any, Any]] | None,
) -> Generator[grpc.aio.Server, None, None]:
    max_workers = request.config.getoption("grpc-max-workers")
    try:
        max_workers = max(request.module.grpc_max_workers, max_workers)
    except AttributeError:
        pass
    pool = futures.ThreadPoolExecutor(max_workers=max_workers)
    # if request.config.getoption('grpc-fake'):
    #     server = FakeServer(pool)
    #     yield server
    if True:
        server = grpc.aio.server(pool, interceptors=grpc_interceptors)
        yield server
    pool.shutdown(wait=False)


@pytest.fixture(scope="module")
def grpc_servicer() -> Generator[SampleServicer, None, None]:
    yield SampleServicer()


@pytest_asyncio.fixture(scope="module")
async def grpc_server(
    _grpc_server: grpc.aio.Server,
    grpc_addr: str,
    grpc_add_to_server: Callable[[SampleServicer, grpc.aio.Server], None],
    grpc_servicer: SampleServicer,
) -> AsyncGenerator[grpc.aio.Server, None]:
    grpc_add_to_server(grpc_servicer, _grpc_server)
    _grpc_server.add_insecure_port(grpc_addr)
    await _grpc_server.start()
    try:
        yield _grpc_server
    finally:
        await _grpc_server.stop(grace=None)


@pytest.fixture(scope="module")
def grpc_add_to_server() -> Callable[[SampleServicer, grpc.aio.Server], None]:
    return add_SampleServicer_to_server


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


@pytest.fixture(scope="session")
def sample_stub(_sample_address: str) -> Iterator[SampleStub[grpc.Channel]]:
    channel = grpc.insecure_channel(_sample_address)
    print(_sample_address)
    yield SampleStub(channel)


@pytest.fixture(scope="session")
def async_sample_stub(_sample_address: str) -> Iterator[SampleStub[grpc.aio.Channel]]:
    channel = grpc.aio.insecure_channel(_sample_address)
    yield SampleStub(channel)
