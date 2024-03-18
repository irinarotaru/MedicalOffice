from datetime import datetime
import uuid

from fastapi import FastAPI, Depends
from typing import Optional
from database import db, Pacienti, Doctori, Programari, Idm
import requests
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from openapi import Patient, Doctor, Appointment, Result, Doctors, ChangeStatus, Message, Patients
import grpc
import idm_pb2_grpc, idm_pb2

app = FastAPI()
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.connect()


@app.on_event("shutdown")
def shutdown():
    db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

channel = grpc.insecure_channel('localhost:50051')
stub = idm_pb2_grpc.TokenValidateStub(channel)


def find_auth(authorization: str = Depends(oauth2_scheme)):
    if authorization.lower() == "bearer":
        message = {"message": "You must be logged in."}
        return JSONResponse(content=message, status_code=401)

    print("Token:", authorization)
    return authorization


def validate_no_hash(text):
    if "#" in text:
        raise ValueError("Character # is not allowed.")


def validate_dict_no_hash(input_dict):
    for key, value in input_dict.items():
        if not isinstance(value, int):
            validate_no_hash(value)


@app.put("/api/medical_office/patient", responses={
    201: {"model": Message, "description": "Resource created"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    409: {"model": Message, "description": "Conflict"},
    422: {"model": Message, "description": "Unprocessable content"}
})
def create_pacient(u: dict):
    try:
        validate_dict_no_hash(u)
        id = uuid.uuid4()

        required_keys = ['cnp', 'nume', 'prenume', 'email', 'telefon', 'data_nasterii', 'username', 'password']

        if not all(key in u for key in required_keys) \
                or not (len(u['telefon']) == 10 and u['telefon'].startswith('0') and u['telefon'].isdigit()):
            message = {"message": "Your content is not valid."}
            return JSONResponse(content=message, status_code=422)

        data_nasterii = datetime.strptime(u['data_nasterii'], '%Y-%m-%d')
        diferenta_ani = datetime.now() - data_nasterii
        if diferenta_ani.days < 365 * 18:
            message = {"message": "Your must be 18 years old to create an account."}
            return JSONResponse(content=message, status_code=403)

        existing_user = Idm.get_or_none(Idm.username == u['username'])
        if existing_user:
            message = {"message": "An user with this username already exists."}
            return JSONResponse(content=message, status_code=409)

        Pacienti.create(cnp=u['cnp'], id_user=id, nume=u['nume'], prenume=u['prenume'], email=u['email'],
                        telefon=u['telefon'], data_nasterii=u['data_nasterii'], is_active=True)

        Idm.create(id=id, username=u['username'], password=u['password'], role='pacient')

        message = {"message": "Pacient created"}
        return JSONResponse(content=message, status_code=201)
    except ValueError as e:
        message = {"message": "Your input was not a valid request." + str(e)}
        return JSONResponse(content=message, status_code=400)


@app.post("/api/medical_office/appointment", responses={
    201: {"model": Message, "description": "Resource created"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    422: {"model": Message, "description": "Unprocessable content"}
})
def create_app(u: dict, auth:str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)

    if "Validarea" in val.response and "pacient" in val.response:
        try:
            validate_dict_no_hash(u)
            required_keys = ['id_pacient', 'id_doctor', 'data']
            print(u['data'])
            if not all(key in u for key in required_keys) or datetime.strptime(u['data'], '%Y-%m-%d') < datetime.now():
                message = {"message": "Your content is not valid."}
                return JSONResponse(content=message, status_code=422)
            pat = Pacienti.select().where(Pacienti.cnp == u['id_pacient']).dicts()
            pat = pat.get()
            doct = Doctori.select().where(Doctori.id_doctor == int(u['id_doctor'])).dicts()
            doct = doct.get()

            if pat and doct:
                Programari.create(id_pacient=u['id_pacient'], id_doctor=u['id_doctor'], data=u['data'], status='onorata')
                message = {"message": "Appointment created"}
                return JSONResponse(content=message, status_code=201)
            else:
                message = {"message": "Your input was not a valid request."}
                return JSONResponse(content=message, status_code=400)

        except ValueError as e:
            message = {"message": "Your input was not a valid request. " + str(e)}
            return JSONResponse(content=message, status_code=400)

    if "doctor" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/patients/{id}', response_model=Patient, responses={
    200: {"model": Patient, "description": "Successful response"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not Found"}
})
def get_patient(id: str, auth: str = Depends(find_auth), date: Optional[str] = None, type: Optional[str] = None):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "pacient" in val.response:
        pat = []
        patient = Pacienti.select().where(Pacienti.cnp == id).dicts()

        if not id.isdigit():
            message = {"message": "CNP does not respect the rule."}
            return JSONResponse(content=message, status_code=400)

        if date and patient:
            patient = patient.get()

            if type == "month":
                ap = Programari.select().where((Programari.data.month == date) & (Programari.id_pacient == id)).dicts()
                for a in ap:
                    pat.append(a)

            elif type == "day":
                ap = Programari.select().where((Programari.data.day == date) & (Programari.id_pacient == id)).dicts()
                for a in ap:
                    pat.append(a)

            else:
                ap = Programari.select().where((Programari.data == date) & (Programari.id_pacient == id)).dicts()
                for a in ap:
                    pat.append(a)

            patient["appointments"] = pat
            patient["links"] = [{"self": {"href": f"/api/medical_office/patients/{id}", "type": "GET"}},
                                {"parent": {"href": "/api/medical_office/patients", "type": "GET"}},
                                {"appointments": {"href": f"/api/medical_office/patients/{id}/physicians", "type": "GET"}},
                                {"results": {"href": f"/api/medical_office/patients/{id}/results", "type": "GET"}},
                                {"create_appointment":{"href": f"/api/medical_office/appointment", "type": "POST"}}
                                ]
            return {'patient': patient}

        if patient:
            patient = patient.get()
            print(patient['id_user'])
            patient["links"] = [{"self": {"href": f"/api/medical_office/patients/{id}", "type": "GET"}},
                                {"parent": {"href": "/api/medical_office/patients", "type": "GET"}},
                                {"appointments": {"href": f"/api/medical_office/patients/{id}/physicians", "type": "GET"}},
                                {"results": {"href": f"/api/medical_office/results/patients/{id}", "type": "GET"}}
                                ]
            return {'patient': patient}
        else:
            message = {"message": "The endpoint was not found"}
            return JSONResponse(content=message, status_code=404)

    if "doctor" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/physicians/{id}', response_model=Doctor, responses={
    200: {"model": Doctor, "description": "Successful response"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not Found"}
})
def get_doctor(id:str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "doctor" in val.response:
        if not id.isdigit():
            message = {"message": "400 Bad Request - id is not a number"}
            return JSONResponse(content=message, status_code=400)

        doctor = Doctori.select().where(Doctori.id_doctor == int(id)).dicts()

        if doctor:
            doctor = doctor.get()
            doctor["links"] = [{"self": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                               {"parent": {"href": f"/api/medical_office/physicians", "type": "GET"}},
                               {"appointments": {"href": f"/api/medical_office/physicians/{id}/appointments", "type": "GET"}},
                               {"see_patients": {"href": f"/api/medical_office/physicians/{id}/patients", "type": "GET"}},
                               {"add_consult": {"href": "/api/medical_office/consult", "type": "POST"}},
                               {"see_consult": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                               {"update_consult": {"href": f"/api/medical_office/physicians/{id}/consultation", "type": "PATCH"}}]
            return {'doctor': doctor}

        else:
            message = {"message": "The endpoint was not found"}
            return JSONResponse(content=message, status_code=404)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/physicians/{id}/appointments', response_model=Appointment, responses={
    200: {"model": Appointment, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def get_app_doctor(id: str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "doctor" in val.response:
        if not id.isdigit():
            message = {"message": "Id is not a number"}
            return JSONResponse(content=message, status_code=400)
        appt = Programari.select().where(Programari.id_doctor == int(id)).dicts()
        appoint = []

        for a in appt:
            a["links"] = [{"self": {"href": f"/api/medical_office/physicians/{id}/appointments", "type": "GET"}},
                           {"parent": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                          {"see_patients": {"href": f"/api/medical_office/physicians/{id}/patients", "type": "GET"}},
                          {"add_consult": {"href": "/api/medical_office/consult", "type": "POST"}},
                          {"see_consult": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                          {"update_consult": {"href": f"/api/medical_office/physicians/{id}/consultation", "type": "PATCH"}}
                          ]
            appoint.append(a)

        if appoint or Doctori.select().where(Doctori.id_doctor == int(id)):
            return {'appointments': appoint}

        else:
            message = {"message": "The endpoint was not found."}
            return JSONResponse(content=message, status_code=404)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)
    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/patients/{id}/physicians', response_model=Appointment, responses={
    200: {"model": Appointment, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def get_app_patient(id: str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "pacient" in val.response:
        if not id.isdigit():
            message = {"message": "CNP does not respect the rule"}
            return JSONResponse(content=message, status_code=400)
        appt = Programari.select().where(Programari.id_pacient == id).dicts()
        doct = []

        for a in appt:
            a["links"] = [{"self": {"href": f"/api/medical_office/patients/{id}/physicians", "type": "GET"}},
                          {"parent": {"href": f"/api/medical_office/patients/{id}", "type": "GET"}},
                          {"create_appointment": {"href": f"/api/medical_office/appointment", "type": "POST"}},
                          {"results": {"href": f"/api/medical_office/patients/{id}/results", "type": "GET"}}]
            doct.append(a)

        if Pacienti.select().where(Pacienti.cnp == id):
            return {'appointments': doct}

        else:
            message = {"message": "The endpoint was not found."}
            return JSONResponse(content=message, status_code=404)

    if "doctor" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/physicians', response_model=Doctors, responses={
    200: {"model": Doctors, "description": "Successful request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def get_doctors(auth: str = Depends(find_auth), specialization: Optional[str] = None, name: Optional[str] = None, page: Optional[int] = None, items_per_page: Optional[int] = None):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "pacient" in val.response:
        doct = []
        if specialization:
            doctori = Doctori.select().where(Doctori.specializare == specialization).dicts()
            for d in doctori:
                d["links"] = [{"self": {"href": f"/api/medical_office/physicians", "type": "GET"}}]
                doct.append(d)

        elif name:
            doctori = Doctori.select().where(Doctori.nume.startswith(name)).dicts()
            for d in doctori:
                d["links"] = [{"self": {"href": "/api/medical_office/physicians", "type": "GET"}}]
                doct.append(d)

        elif page:
            if items_per_page:
                number = items_per_page
            else:
                number = 2
            start = (page-1) * number
            stop = start + number
            doct = Doctori.select().dicts()[start:stop]
            for d in doct:
                d["links"] = [{"self": {"href": "/api/medical_office/physicians", "type": "GET"}}]

        else:
            for doctor in Doctori.select().dicts():
                doctor["links"] = [{"self": {"href": "/api/medical_office/physicians", "type": "GET"}}]
                doct.append(doctor)

        if doct:
            return {'doctors': doct}

        else:
            message = {"message": "The endpoint was not found."}
            return JSONResponse(content=message, status_code=404)

    if "doctor" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/patients/{id}/results', response_model=Result, responses={
    200: {"model": Result, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def get_app(id: str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "pacient" in val.response:
        res = []
        if not id.isdigit():
            message = {"message": "CNP does not respect the rule"}
            return JSONResponse(content=message, status_code=400)

        if Pacienti.select().where(Pacienti.cnp == id):
            ap = Programari.select().where(Programari.id_pacient == id).dicts()
            for a in ap:
                print(a)
                doct = int(a['id_doctor'])
                print(doct)
                url = f"http://127.0.0.1:8001/api/medical_office/physicians/{doct}/consult"
                headers = {
                    'Authorization': f'Bearer {auth}'
                }
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    info = response.json()

                    for c in info['consultations']:
                        print(c['data'])
                        print(str(a['data']))
                        print(c['id_pacient'])
                        if c['data'] == str(a['data']) and c['id_pacient'] == id:
                            res.append(c['investigatii'])
                    print(res)

            return {'results': {'investigatii': res,
                                'links': [{"self": {"href": f"/api/medical_office/results/patients/{id}",
                                                                    "type": "GET"}},
                                                    {"parent": {"href": f"/api/medical_office/patients/{id}",
                                                                       "type": "GET"}},
                                                    {"appointments": {
                                                              "href": f"/api/medical_office/patients/{id}/physicians",
                                                              "type": "GET"}},
                                                    {"create_appointment": {"href": f"/api/medical_office/appointment",
                                                                  "type": "POST"}}
                                          ]}}

        message = {"message": "The endpoint was not found."}
        return JSONResponse(content=message, status_code=404)

    if "doctor" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.get('/api/medical_office/physicians/{id}/patients', response_model=Patients, responses={
    200: {"model": Patients, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def see_patients(id:str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)

    if "Validarea" in val.response and "doctor" in val.response:
        pat = []
        if not id.isdigit():
            message = {"message": "Id must be a number"}
            return JSONResponse(content=message, status_code=400)

        if Doctori.select().where(Doctori.id_doctor == int(id)):
            app = Programari.select().where(Programari.id_doctor == int(id)).dicts()
            if app:
                for a in app:
                    c = Pacienti.select().where(Pacienti.cnp == a['id_pacient']).dicts()
                    print(c.get())
                    c = c.get()
                    if c not in pat:
                        pat.append(c)
            print(pat)
            return {'patients': pat, 'links': [{"self": {"href": f"/api/medical_office/physicians/{id}/patients", "type": "GET"}},
                      {"parent": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                      {"appointments": {"href": f"/api/medical_office/physicians/{id}/appointments", "type": "GET"}},
                      {"add_consult": {"href": "/api/medical_office/consult", "type": "POST"}},
                      {"see_consult": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                      {"update_consult": {"href": f"/api/medical_office/physicians/{id}/consultation","type": "PATCH"}}
                      ]}

        else:
            message = {"message": "The endpoint was not found."}
            return JSONResponse(content=message, status_code=404)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.post("/api/medical_office/physician", responses={
    201: {"model": Message, "description": "Resource created"},
    400: {"model": Message, "description": "Bad Request"},
    409: {"model": Message, "description": "Conflict"},
    422: {"model": Message, "description": "Unprocessable content"}
})
def create_doctor(u: dict):
    try:
        validate_dict_no_hash(u)
        id = uuid.uuid4()
        required_keys = ['id_doctor', 'nume', 'prenume', 'email', 'telefon', 'specializare', 'username', 'password']
        allowed_specializari = ['Alergologie', 'Infectioase', 'Cardiologie', 'Radiologie', 'Chirurgie']

        if not all(key in u for key in required_keys) or not isinstance(u['id_doctor'], int) \
                or u['specializare'] not in allowed_specializari or not (len(u['telefon']) == 10 and u['telefon'].startswith('0')):
            message = {"message": "Your content is not valid."}
            return JSONResponse(content=message, status_code=422)

        existing_user = Idm.get_or_none(Idm.username == u['username'])
        if existing_user:
            message = {"message": "An user with this username already exists."}
            return JSONResponse(content=message, status_code=409)

        if u['specializare'] not in allowed_specializari:
            raise ValueError(f'Specializarea trebuie să fie una din: {", ".join(allowed_specializari)}.')
        Doctori.create(id_doctor=u['id_doctor'], id_user=id, nume=u['nume'], prenume=u['prenume'], email=u['email'], telefon=u['telefon'], specializare=u['specializare'])

        Idm.create(id=id, username=u['username'], password=u['password'], role='doctor')

        message = {"message": "Doctor created."}
        return JSONResponse(content=message, status_code=201)
    except ValueError as e:
        message = {"message": "Your input was not a valid request." + str(e)}
        return JSONResponse(content=message, status_code=400)


@app.patch('/api/medical_office/physicians/{id}/patients/{cnp}', responses={
    200: {"model": Patient, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def make_inactive(id:str, cnp:str, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)
    print(val.response)

    if "Validarea" in val.response and "doctor" in val.response:
        if not id.isdigit() or not cnp.isdigit():
            message = {"message": "Id or CNP are not the correct format."}
            return JSONResponse(content=message, status_code=400)
        pat = Pacienti.get_or_none(Pacienti.cnp == cnp)
        if pat:
            Pacienti.update(is_active=False).where(Pacienti.cnp == cnp).execute()
            pat = Pacienti.get_or_none(Pacienti.cnp == cnp)
            return {'patients': pat, 'links': [{"self": {"href": f"/api/medical_office/physicians/{id}/patients/{cnp}", "type": "PATCH"}},
                      {"parent": {"href": f"/api/medical_office/physicians/{id}/patients", "type": "GET"}},
                      {"profile": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                      {"add_consult": {"href": "/api/medical_office/consult", "type": "POST"}},
                      {"see_consult": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                      {"update_consult": {"href": f"/api/medical_office/physicians/{id}/consultation", "type": "PATCH"}}
                      ]}

        else:
            message = {"message": "The patient was not found."}
            return JSONResponse(content=message, status_code=404)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)


@app.patch('/api/medical_office/physicians/{id}/appointment/{cnp}/{data}', responses={
    200: {"model": Patient, "description": "Successful request"},
    400: {"model": Message, "description": "Bad Request"},
    401: {"model": Message, "description": "Unauthorized"},
    403: {"model": Message, "description": "Forbidden"},
    404: {"model": Message, "description": "Not found"}
})
def change_status(id: str, cnp: str, data: str, status: ChangeStatus, auth: str = Depends(find_auth)):
    token_response = idm_pb2.TokenResponse(token=auth)
    val = stub.ValidateJwt(token_response)

    if "Validarea" in val.response and "doctor" in val.response:
        if not id.isdigit() or not cnp.isdigit():
            message = {"message": "Id or CNP are not the correct format."}
            return JSONResponse(content=message, status_code=400)

        app = Programari.get_or_none((Programari.id_doctor == id) & (Programari.id_pacient == cnp) & (Programari.data == data))

        if app:
            Programari.update(status=status.status).where(Programari.id_doctor == id and Programari.id_pacient == cnp and Programari.data == data).execute()
            app = Programari.get_or_none((Programari.id_doctor == id) & (Programari.id_pacient == cnp) & (Programari.data == data))
            return {'appointments': app, 'links': [{"self": {"href":f'/api/medical_office/physicians/{id}/appointment/{cnp}/{data}', "type": "PATCH"}},
                      {"parent": {"href": f"/api/medical_office/physicians/{id}/appointments", "type": "GET"}},
                      {"profile": {"href": f"/api/medical_office/physicians/{id}", "type": "GET"}},
                      {"add_consult": {"href": "/api/medical_office/consult", "type": "POST"}},
                      {"see_consult": {"href": f"/api/medical_office/physicians/{id}/consult", "type": "GET"}},
                      {"update_consult": {"href": f"/api/medical_office/physicians/{id}/consultation", "type": "PATCH"}}
                      ]}

        else:
            message = {"message": "The appointment was not found."}
            return JSONResponse(content=message, status_code=404)

    if "pacient" in val.response:
        message = {"message": "You cannot access this resource."}
        return JSONResponse(content=message, status_code=403)

    message = {"message": "You must be logged in."}
    return JSONResponse(content=message, status_code=401)
