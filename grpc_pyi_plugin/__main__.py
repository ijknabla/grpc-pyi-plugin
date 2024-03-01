from __future__ import annotations

import sys
from pathlib import Path

from ._google_protobuf_compiler_plugin_pb2 import CodeGeneratorRequest, CodeGeneratorResponse


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
