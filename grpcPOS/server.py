import grpc
from concurrent import futures
import time

import idm_pb2
import idm_pb2_grpc

import auth


class TokenAuthServicer(idm_pb2_grpc.TokenAuthServicer):
    def GenerateJwt(self, request, context):
        response = idm_pb2.TokenResponse()
        response.token = auth.generate_token(request)
        return response


class TokenValidateServicer(idm_pb2_grpc.TokenValidateServicer):
    def ValidateJwt(self, request, context):
        response = idm_pb2.MessageResponse()
        response.response = auth.validate_token(request)
        return response


class TokenDestroyServicer(idm_pb2_grpc.TokenDestroyServicer):
    def DestroyJwt(self, request, context):
        response = idm_pb2.MessageResponse()
        response.response = auth.destroy_token(request)
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

idm_pb2_grpc.add_TokenAuthServicer_to_server(TokenAuthServicer(), server)
idm_pb2_grpc.add_TokenValidateServicer_to_server(TokenValidateServicer(), server)
idm_pb2_grpc.add_TokenDestroyServicer_to_server(TokenDestroyServicer(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
