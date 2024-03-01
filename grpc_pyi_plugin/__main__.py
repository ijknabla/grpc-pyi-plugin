import sys

from google.protobuf.compiler.plugin_pb2 import CodeGeneratorRequest


def main() -> None:
    request = CodeGeneratorRequest.FromString(sys.stdin.buffer.read())
    print(request, file=sys.stderr)


if __name__ == "__main__":
    main()
