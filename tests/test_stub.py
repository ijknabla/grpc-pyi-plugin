from __future__ import annotations

from typing import TYPE_CHECKING

import grpc
import pytest
from google.protobuf.empty_pb2 import Empty

import sample_pb2_grpc

if TYPE_CHECKING:
    SampleStub = sample_pb2_grpc.SampleStub[grpc.Channel]
    AsyncSampleStub = sample_pb2_grpc.SampleStub[grpc.aio.Channel]


# def test_unary_unary(sample_stub: SampleStub):
#     stub = sample_stub
#     call: Empty = stub.UU(Empty())
#     assert isinstance(call, Empty)


@pytest.mark.asyncio
async def test_async_unary_unary(async_sample_stub: SampleStub):
    stub = async_sample_stub

    call: grpc.aio.UnaryUnaryCall[Empty, Empty] = stub.UU(Empty())
    assert isinstance(call, grpc.aio.UnaryUnaryCall)

    respone: Empty = await call
    assert isinstance(respone, Empty)
