import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

import grpc_pyi_plugin as _plugin

_UU = _plugin.UnaryUnaryProperty[
    google_dot_protobuf_dot_empty__pb2.Empty,
    google_dot_protobuf_dot_empty__pb2.Empty,
]
_US = _plugin.UnaryStreamProperty[
    google_dot_protobuf_dot_empty__pb2.Empty,
    google_dot_protobuf_dot_empty__pb2.Empty,
]
_SU = _plugin.StreamUnaryProperty[
    google_dot_protobuf_dot_empty__pb2.Empty,
    google_dot_protobuf_dot_empty__pb2.Empty,
]
_SS = _plugin.StreamStreamProperty[
    google_dot_protobuf_dot_empty__pb2.Empty,
    google_dot_protobuf_dot_empty__pb2.Empty,
]

class SampleStub(_plugin.GenericStub[_plugin.ChannelType]):
    UU: _UU
    US: _US
    SU: _SU
    SS: _SS

class SampleServicer(_plugin.GenericServicer[_plugin.ServerType]): ...

def add_SampleServicer_to_server(
    servicer: SampleServicer[_plugin.ServerType],
    server: _plugin.ServerType,
) -> None: ...
