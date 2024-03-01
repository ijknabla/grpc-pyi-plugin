from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorResponse
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.message import Message

if not TYPE_CHECKING:
    from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest
else:

    class CodeGeneratorRequest(Message):
        source_file_descriptors: Sequence[FileDescriptorProto]


def main() -> None:
    request = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())
    print(request, file=sys.stderr)

    response = CodeGeneratorResponse()

    for descriptor in request.source_file_descriptors:
        source = Path(descriptor.name)
        response.file.append(CodeGeneratorResponse.File(name=f"{source.stem}_pb2_grpc.pyi"))

    sys.stdout.buffer.write(response.SerializeToString())


if __name__ == "__main__":
    main()
