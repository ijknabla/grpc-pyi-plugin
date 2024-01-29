from __future__ import annotations

from collections.abc import AsyncIterable, Iterable, Iterator
from typing import Generic, Protocol, TypeVar, overload

import grpc.aio

ChannelType = TypeVar("ChannelType", grpc.Channel, grpc.aio.Channel, covariant=True)

RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")

ArgumentType = TypeVar("ArgumentType", contravariant=True)
ReturnType = TypeVar("ReturnType", covariant=True)


class GenericStub(Generic[ChannelType]):
    def __init__(self, channel: ChannelType) -> None: ...


class UnaryUnaryProperty(Protocol[RequestType, ResponseType]):
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> UnaryCallable[
        RequestType,
        ResponseType,
    ]: ...

    @overload
    def __get__(
        property,
        self: GenericStub[grpc.aio.Channel],
        cls: type[GenericStub[grpc.aio.Channel]],
        /,
    ) -> UnaryCallable[
        RequestType,
        grpc.aio.UnaryUnaryCall[RequestType, ResponseType],
    ]: ...


class UnaryStreamProperty(Protocol[RequestType, ResponseType]):
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> UnaryCallable[
        RequestType,
        Iterator[ResponseType],
    ]: ...

    @overload
    def __get__(
        property,
        self: GenericStub[grpc.aio.Channel],
        cls: type[GenericStub[grpc.aio.Channel]],
        /,
    ) -> UnaryCallable[
        RequestType,
        grpc.aio.UnaryStreamCall[RequestType, ResponseType],
    ]: ...


class UnaryCallable(Protocol[ArgumentType, ReturnType]):
    @staticmethod
    def __call__(request: ArgumentType) -> ReturnType: ...


class StreamUnaryProperty(Protocol[RequestType, ResponseType]):
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> StreamCallable[
        Iterator[RequestType],
        ResponseType,
    ]: ...

    @overload
    def __get__(
        property,
        self: GenericStub[grpc.aio.Channel],
        cls: type[GenericStub[grpc.aio.Channel]],
        /,
    ) -> StreamCallable[
        Iterable[RequestType] | AsyncIterable[RequestType],
        grpc.aio.StreamUnaryCall[RequestType, ResponseType],
    ]: ...


class StreamStreamProperty(Protocol[RequestType, ResponseType]):
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> StreamCallable[
        Iterator[RequestType],
        Iterator[ResponseType],
    ]: ...

    @overload
    def __get__(
        property,
        self: GenericStub[grpc.aio.Channel],
        cls: type[GenericStub[grpc.aio.Channel]],
        /,
    ) -> StreamCallable[
        Iterable[RequestType] | AsyncIterable[RequestType],
        grpc.aio.StreamStreamCall[RequestType, ResponseType],
    ]: ...


class StreamCallable(Protocol[ArgumentType, ReturnType]):
    @staticmethod
    def __call__(request_iterator: ArgumentType) -> ReturnType: ...
