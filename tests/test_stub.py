from __future__ import annotations

from typing import TYPE_CHECKING

import grpc
from google.protobuf.empty_pb2 import Empty
import pytest

import sample_pb2_grpc

if TYPE_CHECKING:
    SampleStub = sample_pb2_grpc.SampleStub[grpc.Channel]
    AsyncSampleStub = sample_pb2_grpc.SampleStub[grpc.aio.Channel]


@pytest.mark.asyncio
async def test_unary_unary(grpc_stub: SampleStub):
    stub = grpc_stub
    call = await stub.UU(Empty())
    assert isinstance(call, Empty)
