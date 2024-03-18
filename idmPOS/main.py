import grpc
from fastapi.security import OAuth2PasswordBearer

import idm_pb2_grpc, idm_pb2
from fastapi import FastAPI, Depends
from database import db, Idm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


responses = {
    200: {"model": Message, "description": "Successful Request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"}
}

responses2 = {
    200: {"model": Message, "description": "Successful Request"},
    400: {"model": Message, "description": "Bad Request"},
    404: {"model": Message, "description": "Not found"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

channel = grpc.insecure_channel('localhost:50051')

stub_val = idm_pb2_grpc.TokenValidateStub(channel)
stub_gen = idm_pb2_grpc.TokenAuthStub(channel)
stub_dest = idm_pb2_grpc.TokenDestroyStub(channel)


def find_auth(authorization: str = Depends(oauth2_scheme)):
    print(authorization)

    if authorization.lower() == "bearer":
        message = {"message": "401 Unauthorized"}
        return JSONResponse(content=message, status_code=401)

    print("Token:", authorization)
    return authorization


@app.on_event("startup")
def startup():
    db.connect()


def validate_role(role):
    if role not in ["pacient", "doctor"]:
        raise ValueError("The role must 'pacient' or 'doctor'")


def validate_no_hash(text):
    if "#" in text:
        raise ValueError("Character # is not allowed.")


def validate_dict_no_hash(input_dict):
    for key, value in input_dict.items():
        if not isinstance(value, int):
            validate_no_hash(value)


@app.put("/api/medical_office/update_user", responses=responses)
async def update_user(u:dict):
    try:
        validate_no_hash(u['username'])
        validate_no_hash(u['new_username'])
        validate_no_hash(u['password'])
    except ValueError as e:
        message = {"message": "Your input was not a valid request." + str(e)}
        return JSONResponse(content=message, status_code=400)

    existing_user = Idm.get_or_none(Idm.username == u['username'])
    print(existing_user)

    if existing_user is None:
        message = {"message": "The user does not exist."}
        return JSONResponse(content=message, status_code=404)

    existing_user.username = u['new_username']
    existing_user.password = u['password']
    existing_user.save()

    message = {"message": "The user was modified"}
    return JSONResponse(content=message, status_code=200)


@app.post("/api/medical_office/login", responses=responses)
def login(u: dict):
    try:
        validate_no_hash(u['username'])
        validate_no_hash(u['password'])
    except ValueError as e:
        message = {"message": "Your content is not accepted. " + str(e)}
        return JSONResponse(content=message, status_code=400)
    print(u['username'])

    user = Idm.select().where((Idm.username == u['username']) & (Idm.password == u['password'])).dicts()

    if user.exists():
        user = user.get()
        print(user)
    else:
        message = {"message": "Wrong username or password."}
        return JSONResponse(content=message, status_code=401)

    info_auth = idm_pb2.InfoAuth(id=user['id'], role=user['role'], username=user['username'], password=user['password'])
    response = stub_gen.GenerateJwt(info_auth)
    token = response.token

    message = {"message": "Successfully connected.",
               "role": user['role'],
               "id": user['id'],
               'token': token}
    return JSONResponse(content=message, status_code=200)


@app.delete("/api/medical_office/logout")
def logout(authorization: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=authorization)
    stub_dest.DestroyJwt(token_response)
    message = {"message": "Successfully disconnected."}
    return JSONResponse(content=message, status_code=200)


@app.on_event("shutdown")
def shutdown():
    db.close()


def verify_token(token:str):
    resp = stub_val.ValidateJwt(token)
    return resp.response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)


