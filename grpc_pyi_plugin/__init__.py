from __future__ import annotations

from collections.abc import Iterator
from typing import Generic, Protocol, TypeVar, overload

import grpc.aio

ChannelType = TypeVar("ChannelType", grpc.Channel, grpc.aio.Channel, covariant=True)
InvariantRequestType = TypeVar("InvariantRequestType")
InvariantResponseType = TypeVar("InvariantResponseType")
ContravariantRequestType = TypeVar("ContravariantRequestType", contravariant=True)
CovariantResponseType = TypeVar("CovariantResponseType", covariant=True)


class GenericStub(Generic[ChannelType]):
    def __init__(self, channel: ChannelType) -> None: ...


class UnaryUnaryProperty(Protocol[InvariantRequestType, InvariantResponseType]):
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> UnaryCallable[InvariantRequestType, InvariantResponseType]: ...
    @overload
    def __get__(
        property,
        self: GenericStub[grpc.aio.Channel],
        cls: type[GenericStub[grpc.aio.Channel]],
        /,
    ) -> UnaryCallable[
        InvariantRequestType, grpc.aio.UnaryUnaryCall[InvariantRequestType, InvariantResponseType]
    ]: ...


class UnaryStreamProperty(Protocol[ContravariantRequestType, CovariantResponseType]):
    def __get__(
        property,
        self: GenericStub[grpc.Channel],
        cls: type[GenericStub[grpc.Channel]],
        /,
    ) -> UnaryCallable[ContravariantRequestType, Iterator[CovariantResponseType]]: ...


class UnaryCallable(Protocol[ContravariantRequestType, CovariantResponseType]):
    @staticmethod
    def __call__(request: ContravariantRequestType) -> CovariantResponseType: ...
