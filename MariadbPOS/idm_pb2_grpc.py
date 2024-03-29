# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import idm_pb2 as idm__pb2


class TokenAuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GenerateJwt = channel.unary_unary(
                '/TokenAuth/GenerateJwt',
                request_serializer=idm__pb2.InfoAuth.SerializeToString,
                response_deserializer=idm__pb2.TokenResponse.FromString,
                )


class TokenAuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GenerateJwt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TokenAuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GenerateJwt': grpc.unary_unary_rpc_method_handler(
                    servicer.GenerateJwt,
                    request_deserializer=idm__pb2.InfoAuth.FromString,
                    response_serializer=idm__pb2.TokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TokenAuth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TokenAuth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GenerateJwt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TokenAuth/GenerateJwt',
            idm__pb2.InfoAuth.SerializeToString,
            idm__pb2.TokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class TokenValidateStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateJwt = channel.unary_unary(
                '/TokenValidate/ValidateJwt',
                request_serializer=idm__pb2.TokenResponse.SerializeToString,
                response_deserializer=idm__pb2.MessageResponse.FromString,
                )


class TokenValidateServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ValidateJwt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TokenValidateServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateJwt': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateJwt,
                    request_deserializer=idm__pb2.TokenResponse.FromString,
                    response_serializer=idm__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TokenValidate', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TokenValidate(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ValidateJwt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TokenValidate/ValidateJwt',
            idm__pb2.TokenResponse.SerializeToString,
            idm__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class TokenDestroyStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DestroyJwt = channel.unary_unary(
                '/TokenDestroy/DestroyJwt',
                request_serializer=idm__pb2.TokenResponse.SerializeToString,
                response_deserializer=idm__pb2.MessageResponse.FromString,
                )


class TokenDestroyServicer(object):
    """Missing associated documentation comment in .proto file."""

    def DestroyJwt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TokenDestroyServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DestroyJwt': grpc.unary_unary_rpc_method_handler(
                    servicer.DestroyJwt,
                    request_deserializer=idm__pb2.TokenResponse.FromString,
                    response_serializer=idm__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TokenDestroy', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TokenDestroy(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def DestroyJwt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TokenDestroy/DestroyJwt',
            idm__pb2.TokenResponse.SerializeToString,
            idm__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
