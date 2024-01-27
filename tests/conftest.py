from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

import grpc.aio
import pytest
import pytest_asyncio

from sample_pb2_grpc import SampleServicer, SampleStub, add_SampleServicer_to_server


@pytest_asyncio.fixture(scope="session")
async def _sample_address(host: str = "localhost") -> AsyncIterator[str]:
    server = grpc.aio.server()

    servicer = SampleServicer()
    add_SampleServicer_to_server(servicer, server)

    port = server.add_insecure_port(f"{host}:0")
    await server.start()
    try:
        yield f"{host}:{port}"
    finally:
        await server.stop(0)


@pytest.fixture(scope="session")
def sample_stub(_sample_address: str) -> Iterator[SampleStub[grpc.Channel]]:
    channel = grpc.insecure_channel(_sample_address)
    print(_sample_address)
    yield SampleStub(channel)


@pytest.fixture(scope="session")
def async_sample_stub(_sample_address: str) -> Iterator[SampleStub[grpc.aio.Channel]]:
    channel = grpc.aio.insecure_channel(_sample_address)
    yield SampleStub(channel)
