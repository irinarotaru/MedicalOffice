import grpc
import uuid

import idm_pb2
import idm_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

stub = idm_pb2_grpc.TokenAuthStub(channel)
stub2 = idm_pb2_grpc.TokenValidateStub(channel)
stub3 = idm_pb2_grpc.TokenDestroyStub(channel)

info_auth = idm_pb2.InfoAuth(id=str(uuid.uuid4()), role="pacient", username="anapopa", password="parola")

response = stub.GenerateJwt(info_auth)
print(response.token)
token_response = idm_pb2.TokenResponse(token=response.token)
response2 = stub2.ValidateJwt(token_response)
print(response2.response)
response3 = stub3.DestroyJwt(token_response)
print(response3.response)
response2 = stub2.ValidateJwt(token_response)
print(response2.response)


