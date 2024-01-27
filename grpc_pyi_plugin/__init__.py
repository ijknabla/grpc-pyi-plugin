from typing import Generic, TypeVar

import grpc.aio

ChannelType = TypeVar("ChannelType", grpc.Channel, grpc.aio.Channel, covariant=True)
RequestType = TypeVar("RequestType", covariant=True)
ResponseType = TypeVar("ResponseType", covariant=True)


class GenericStub(Generic[ChannelType]):
    def __init__(self, channel: ChannelType) -> None: ...


class UnaryUnaryProperty(Generic[RequestType, ResponseType]): ...
