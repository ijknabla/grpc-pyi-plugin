from typing import Protocol, TypeVar

import grpc.aio

ChannelType = TypeVar("ChannelType", grpc.Channel, grpc.aio.Channel, covariant=True)
RequestType = TypeVar("RequestType", covariant=True)
ResponseType = TypeVar("ResponseType", covariant=True)


class GenericStub(Protocol[ChannelType]): ...


class UnaryUnaryProperty(Protocol[RequestType, ResponseType]): ...
