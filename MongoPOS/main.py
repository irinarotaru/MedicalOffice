from pymongo import MongoClient
from fastapi import FastAPI, Depends
from openapi import Consultation, Message
import requests
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import idm_pb2,idm_pb2_grpc
import grpc

app = FastAPI()
mongodb_uri = "mongodb://root:password@localhost:27017"
client = MongoClient(mongodb_uri)
db = client["pos"]
consultatii = db["consultatii"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
channel = grpc.insecure_channel('localhost:50051')
stub = idm_pb2_grpc.TokenValidateStub(channel)

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

responses = {
    200: {"model": Consultation, "description": "Successful response"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    404: {"model": Message, "description": "Not Found"}
}

responses3 = {
    201: {"model": Message, "description": "Resource created"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    405: {"model": Message, "description": "Method not allowed"},
    422: {"model": Message, "description": "Unprocessable content"}
}

responses4 = {
    200: {"model": Message, "description": "Successful response"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    422: {"model": Message, "description": "Unprocessable content"}
}


def validate_no_hash(text):
    if "#" in text:
        raise ValueError("Character # is not allowed.")


def validate_dict_no_hash(input_dict):
    for key, value in input_dict.items():
        if not isinstance(value, int):
            validate_no_hash(value)


def find_auth(authorization: str = Depends(oauth2_scheme)):
    if authorization.lower() == "bearer":
        message = {"message": "You must be logged in."}
        return JSONResponse(content=message, status_code=401)

    return authorization


@app.post('/api/medical_office/consult', responses=responses3)
def consult(c: dict, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)
    print(c)

    if "Validarea" in val.response and "doctor" in val.response:
        try:
            validate_dict_no_hash(c)
            required_keys = ['id_pacient', 'id_doctor', 'data', 'diagnostic', 'investigatii']

            if not all(key in c for key in required_keys) or not isinstance(c['id_doctor'], int) or not c['id_pacient'].isdigit():
                message = {"message": "Your content is not valid."}
                return JSONResponse(content=message, status_code=422)

            else:
                for investigatie in c['investigatii']:
                    required_inv_keys = ["id", "denumire", "durata_de_procesare", "rezultat"]
                    if not all(key in investigatie for key in required_inv_keys):
                        message = {"message": "Your content is not valid."}
                        return JSONResponse(content=message, status_code=422)

            criterii_cautare = {
                "id_doctor": c['id_doctor'],
                "id_pacient": c['id_pacient'],
                "data": c['data']
            }

            cons = consultatii.find_one(criterii_cautare)
            if cons:
                message = {"message": "There is already a consultation, please update that one."}
                return JSONResponse(content=message, status_code=405)

            headers = {'Authorization': f'Bearer {auth}'}
            pat = c['id_pacient']
            doct = int(c['id_doctor'])
            url = f"http://127.0.0.1:8000/api/medical_office/physicians/{doct}/patients"
            response = requests.get(url, headers=headers)
            info = response.json()

            if response.status_code == 200:
                cnp_values = [patient['id_pacient'] for patient in info.get('appointments', [])]
                print(cnp_values)
                print(pat)
                if pat in cnp_values:
                    result = consultatii.insert_one(c)
                    print(result.inserted_id)
                    response = {'links': [{"self": {"href": "/api/medical_office/consult", "type": "POST"}},
                                {"parent": {"href": f"/api/medical_office/physicians/{doct}", "type": "GET"}},
                              {"see_consult": {"href": f"/api/medical_office/physicians/{doct}/consult", "type": "GET"}},
                              {"update_consult": {"href": "/api/medical_office/updateconsult/#", "type": "PUT"}}
                              ]}
                    return JSONResponse(content=response, status_code=201)

                else:
                    message = {"message": "You are not allowed to do this method."}
                    return JSONResponse(content=message, status_code=405)
            else:
                return response.status_code
        except ValueError as e:
            message = {"message": "Your input was not a valid request." + str(e)}
            return JSONResponse(content=message, status_code=400)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.patch('/api/medical_office/consultation', responses=responses4)
def consult(c: dict, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "doctor" in val.response:
        try:
            validate_dict_no_hash(c)
            required_keys = ['id_pacient', 'id_doctor', 'data', 'diagnostic', 'investigatii']

            if not all(key in c for key in required_keys) or not isinstance(c['id_doctor'], int) or not c['id_pacient'].isdigit():
                message = {"message": "Your content is not valid."}
                return JSONResponse(content=message, status_code=422)

            else:
                for investigatie in c['investigatii']:
                    required_inv_keys = ["id", "denumire", "durata_de_procesare", "rezultat"]
                    if not all(key in investigatie for key in required_inv_keys):
                        message = {"message": "Your content is not valid."}
                        return JSONResponse(content=message, status_code=422)

            criterii_cautare = {
                "id_doctor": c['id_doctor'],
                "id_pacient": c['id_pacient'],
                "data": c['data']
            }

            cons = consultatii.find_one(criterii_cautare)

            update_data = {"$set": {"diagnostic": c['diagnostic'],
                                    "investigatii": c['investigatii']}}

            if cons:
                consultatii.update_one(criterii_cautare, update_data)
                response = {'links': [{"self": {"href": f"/api/medical_office/consultation", "type": "PATCH"}},
                                      {"parent": {"href": f"/api/medical_office/physicians/{c['id_doctor']}/consult", "type": "GET"}},
                                      {"add_consult": {"href": f"/api/medical_office/consult", "type": "POST"}}
                                      ]}
                return response

            else:
                message = {"message": "The consulation was not found"}
                return JSONResponse(content=message, status_code=404)
        except ValueError as e:
            message = {"message": "Your input was not a valid request." + str(e)}
            return JSONResponse(content=message, status_code=400)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/physicians/{id}/consult', response_model=Consultation, responses=responses)
def see_consult(id: str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response:
        resp = []

        if not id.isdigit():
            message = {"message": "400 Bad Request - id is not a number"}
            return JSONResponse(content=message, status_code=400)
        cons = consultatii.find({"id_doctor": int(id)})

        if cons is not None:
            for c in cons:
                print(c)
                c.pop('_id', None)
                c["links"] = [{"self": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                                          {"parent": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                                          {"add_consult": {"href": f"/api/medical_office/consult", "type": "POST"}},
                                          {"update_consult": {"href": f"/api/medical_office/updateconsult/{id}", "type": "PUT"}}]
                resp.append(c)
            print(resp)
            return {'consultations': resp}

        else:
            message = {"message": "The endpoint was not found."}
            return JSONResponse(content=message, status_code=404)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.on_event("shutdown")
def shutdown():
    client.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)

