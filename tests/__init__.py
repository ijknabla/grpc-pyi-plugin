import grpc.aio
from google.protobuf.empty_pb2 import Empty

import sample_pb2_grpc


class SampleServicer(sample_pb2_grpc.SampleServicer):
    async def UU(self, request: Empty, context: grpc.aio.ServicerContext[Empty, Empty]) -> Empty:
        return Empty()
