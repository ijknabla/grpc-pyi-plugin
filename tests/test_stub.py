from __future__ import annotations

from asyncio import AbstractEventLoop
from collections.abc import Generator, Iterable, Iterator
from concurrent.futures import Executor
from typing import TYPE_CHECKING

import grpc
import pytest
from google.protobuf.empty_pb2 import Empty

from . import AsyncSampleStub, SampleStub


@pytest.mark.asyncio
async def test_unary_unary(
    event_loop: AbstractEventLoop, executor: Executor, sample_stub: SampleStub
) -> None:
    def main() -> None:
        stub = sample_stub

        response: Empty = stub.UU(request=Empty())
        assert isinstance(response, Empty)

    await event_loop.run_in_executor(executor, main)


@pytest.mark.asyncio
async def test_async_unary_unary(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.UnaryUnaryCall[Empty, Empty] = stub.UU(request=Empty())
    assert isinstance(call, grpc.aio.UnaryUnaryCall)

    response: Empty = await call
    assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_unary_stream(
    event_loop: AbstractEventLoop, executor: Executor, sample_stub: SampleStub
) -> None:
    def main() -> None:
        stub = sample_stub

        call: Iterator[Empty] = stub.US(request=Empty())
        assert isinstance(call, Iterable)
        assert isinstance(call, Iterator)
        assert not isinstance(call, Generator)

        response: Empty
        for response in call:
            assert isinstance(response, Empty)

    await event_loop.run_in_executor(executor, main)


@pytest.mark.asyncio
async def test_async_unary_stream(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.UnaryStreamCall[Empty, Empty] = stub.US(request=Empty())
    assert isinstance(call, grpc.aio.UnaryStreamCall)

    response: Empty
    async for response in call:
        assert isinstance(response, Empty)
