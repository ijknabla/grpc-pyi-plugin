from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator
from typing import TYPE_CHECKING

import grpc.aio
from google.protobuf.empty_pb2 import Empty

import sample_pb2_grpc

if TYPE_CHECKING:
    SampleStub = sample_pb2_grpc.SampleStub[grpc.Channel]
    AsyncSampleStub = sample_pb2_grpc.SampleStub[grpc.aio.Channel]
else:
    SampleStub = sample_pb2_grpc.SampleStub
    AsyncSampleStub = sample_pb2_grpc.SampleStub


class SampleServicer(sample_pb2_grpc.SampleServicer): ...


class AsyncSampleServicer(sample_pb2_grpc.SampleServicer):
    async def UU(self, request: Empty, context: grpc.aio.ServicerContext[Empty, Empty]) -> Empty:
        return Empty()

    async def US(
        self, request: Empty, context: grpc.aio.ServicerContext[Empty, Empty]
    ) -> AsyncIterator[Empty]:
        yield Empty()

    async def SU(
        self,
        request_iterator: AsyncIterable[Empty],
        context: grpc.aio.ServicerContext[Empty, Empty],
    ) -> Empty:
        async for _ in request_iterator:
            ...
        return Empty()

    async def SS(
        self,
        request_iterator: AsyncIterable[Empty],
        context: grpc.aio.ServicerContext[Empty, Empty],
    ) -> AsyncIterator[Empty]:
        async for empty in request_iterator:
            yield empty
