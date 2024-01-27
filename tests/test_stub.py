from __future__ import annotations

from asyncio import AbstractEventLoop
from concurrent.futures import Executor
from typing import TYPE_CHECKING

import grpc
import pytest
from google.protobuf.empty_pb2 import Empty

import sample_pb2_grpc

if TYPE_CHECKING:
    SampleStub = sample_pb2_grpc.SampleStub[grpc.Channel]
    AsyncSampleStub = sample_pb2_grpc.SampleStub[grpc.aio.Channel]


@pytest.mark.asyncio
async def test_unary_unary(
    event_loop: AbstractEventLoop, executor: Executor, sample_stub: SampleStub
) -> None:
    def main() -> None:
        stub = sample_stub

        call: Empty = stub.UU(request=Empty())
        assert isinstance(call, Empty)

    await event_loop.run_in_executor(executor, main)


@pytest.mark.asyncio
async def test_async_unary_unary(async_sample_stub: SampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.UnaryUnaryCall[Empty, Empty] = stub.UU(request=Empty())
    assert isinstance(call, grpc.aio.UnaryUnaryCall)

    respone: Empty = await call
    assert isinstance(respone, Empty)
