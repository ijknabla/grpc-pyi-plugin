from __future__ import annotations

from asyncio import CancelledError
from collections.abc import AsyncIterator, Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

import grpc
import pytest
from google.protobuf.empty_pb2 import Empty

from . import AsyncSampleStub, SampleStub

T = TypeVar("T")


def test_unary_unary(sample_stub: SampleStub) -> None:
    stub = sample_stub

    response: Empty

    response = stub.UU(request=Empty())
    assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_async_unary_unary(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.UnaryUnaryCall[Empty, Empty]
    response: Empty

    call = stub.UU(request=Empty())
    assert isinstance(call, grpc.aio.UnaryUnaryCall)

    response = await call
    assert isinstance(response, Empty)


def test_unary_stream(sample_stub: SampleStub) -> None:
    stub = sample_stub

    call: Iterator[Empty]
    response: Empty

    call = stub.US(request=Empty())
    assert isinstance(call, Iterable)
    assert isinstance(call, Iterator)
    assert not isinstance(call, Generator)

    for response in call:
        assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_async_unary_stream(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.UnaryStreamCall[Empty, Empty]
    response: Empty

    call = stub.US(request=Empty())
    assert isinstance(call, grpc.aio.UnaryStreamCall)

    async for response in call:
        assert isinstance(response, Empty)


def test_stream_unary(sample_stub: SampleStub) -> None:
    stub = sample_stub

    response: Empty

    with pytest.raises(grpc.RpcError):
        response = stub.SU(request_iterator=Empty())  # type: ignore[arg-type]

    with pytest.raises(grpc.RpcError):
        response = stub.SU(request_iterator=[Empty()])  # type: ignore[arg-type]

    response = stub.SU(request_iterator=iter([Empty()]))
    assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_async_stream_unary(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.StreamUnaryCall[Empty, Empty]
    response: Empty

    # T
    call = stub.SU(request_iterator=Empty())  # type: ignore[arg-type]
    assert isinstance(call, grpc.aio.StreamUnaryCall)
    with pytest.raises(CancelledError):
        response = await call

    # Iterable[T]
    call = stub.SU(request_iterator=[Empty()])
    assert isinstance(call, grpc.aio.StreamUnaryCall)
    response = await call
    assert isinstance(response, Empty)

    # Iterator[T]
    call = stub.SU(request_iterator=iter([Empty()]))
    assert isinstance(call, grpc.aio.StreamUnaryCall)
    response = await call
    assert isinstance(response, Empty)

    # AsyncIterable[T]
    call = stub.SU(request_iterator=AsyncIteration([Empty()]))
    assert isinstance(call, grpc.aio.StreamUnaryCall)
    response = await call
    assert isinstance(response, Empty)

    # AsyncIterator[T]
    call = stub.SU(request_iterator=aiter(AsyncIteration([Empty()])))
    assert isinstance(call, grpc.aio.StreamUnaryCall)
    response = await call
    assert isinstance(response, Empty)


def test_stream_strem(sample_stub: SampleStub) -> None:
    stub = sample_stub

    call: Iterator[Empty]
    response: Empty

    # with pytest.raises(grpc.RpcError):
    call = stub.SS(request_iterator=Empty())  # type: ignore[arg-type]
    assert isinstance(call, Iterable)
    assert isinstance(call, Iterator)
    assert not isinstance(call, Generator)
    with pytest.raises(grpc.RpcError):
        for response in call:
            assert isinstance(response, Empty)

    call = stub.SS(request_iterator=[Empty()])  # type: ignore[arg-type]
    assert isinstance(call, Iterable)
    assert isinstance(call, Iterator)
    assert not isinstance(call, Generator)
    with pytest.raises(grpc.RpcError):
        for response in call:
            assert isinstance(response, Empty)

    call = stub.SS(request_iterator=iter([Empty()]))
    assert isinstance(call, Iterable)
    assert isinstance(call, Iterator)
    assert not isinstance(call, Generator)
    for response in call:
        assert isinstance(response, Empty)


@pytest.mark.asyncio
async def test_async_stream_stream(async_sample_stub: AsyncSampleStub) -> None:
    stub = async_sample_stub

    call: grpc.aio.StreamStreamCall[Empty, Empty]
    response: Empty

    # T
    call = stub.SS(request_iterator=Empty())  # type: ignore[arg-type]
    assert isinstance(call, grpc.aio.StreamStreamCall)
    with pytest.raises(CancelledError):
        async for response in call:
            assert isinstance(response, Empty)

    # Iterable[T]
    call = stub.SS(request_iterator=[Empty()])
    assert isinstance(call, grpc.aio.StreamStreamCall)
    async for response in call:
        assert isinstance(response, Empty)

    # Iterator[T]
    call = stub.SS(request_iterator=iter([Empty()]))
    assert isinstance(call, grpc.aio.StreamStreamCall)
    async for response in call:
        assert isinstance(response, Empty)

    # AsyncIterable[T]
    call = stub.SS(request_iterator=AsyncIteration([Empty()]))
    assert isinstance(call, grpc.aio.StreamStreamCall)
    async for response in call:
        assert isinstance(response, Empty)

    # AsyncIterator[T]
    call = stub.SS(request_iterator=aiter(AsyncIteration([Empty()])))
    assert isinstance(call, grpc.aio.StreamStreamCall)
    async for response in call:
        assert isinstance(response, Empty)


@dataclass(frozen=True)
class AsyncIteration(Generic[T]):
    iterable: Iterable[T]

    async def __aiter__(self) -> AsyncIterator[T]:
        for item in self.iterable:
            yield item
