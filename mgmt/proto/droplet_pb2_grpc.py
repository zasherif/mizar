# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import droplet_pb2 as droplet__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class DropletServiceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDropletInfo = channel.unary_unary(
                '/DropletService/GetDropletInfo',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=droplet__pb2.Droplet.FromString,
                )


class DropletServiceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetDropletInfo(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DropletServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetDropletInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDropletInfo,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=droplet__pb2.Droplet.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DropletService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DropletService(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetDropletInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DropletService/GetDropletInfo',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            droplet__pb2.Droplet.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
