from __future__ import annotations

from typing import TYPE_CHECKING

import grpc
from google.protobuf.empty_pb2 import Empty

import sample_pb2_grpc

if TYPE_CHECKING:
    SampleStub = sample_pb2_grpc.SampleStub[grpc.Channel]
    AsyncSampleStub = sample_pb2_grpc.SampleStub[grpc.aio.Channel]


def test_unary_unary(sample_stub: SampleStub):
    stub = sample_stub
    call = stub.UU(Empty())
    assert isinstance(call, Empty)
