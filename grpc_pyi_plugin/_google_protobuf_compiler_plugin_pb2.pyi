__all__ = (
    "CodeGeneratorRequest",
    "CodeGeneratorResponse",
)

import collections as _collections

import google as _google
from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse

class CodeGeneratorRequest(_google.protobuf.message.Message):
    source_file_descriptors: _collections.abc.Sequence[
        _google.protobuf.descriptor_pb2.FileDescriptorProto
    ]
