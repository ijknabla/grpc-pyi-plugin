import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

import grpc_pyi_plugin as _plugin

class SampleStub(_plugin.GenericStub[_plugin.ChannelType]):
    UU: _plugin.UnaryUnaryProperty[
        google_dot_protobuf_dot_empty__pb2.Empty,
        google_dot_protobuf_dot_empty__pb2.Empty,
    ]
    US: _plugin.UnaryStreamProperty[
        google_dot_protobuf_dot_empty__pb2.Empty,
        google_dot_protobuf_dot_empty__pb2.Empty,
    ]
    SU: _plugin.StreamUnaryProperty[
        google_dot_protobuf_dot_empty__pb2.Empty,
        google_dot_protobuf_dot_empty__pb2.Empty,
    ]

class SampleServicer: ...

def add_SampleServicer_to_server(servicer: SampleServicer, server: grpc.aio.Server) -> None: ...
