from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db, Pacienti, Doctori
from fastapi.responses import JSONResponse

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


@app.on_event("startup")
def startup():
    db.connect()


@app.on_event("shutdown")
def shutdown():
    db.close()


@app.get('/get_cnp/{id}')
def get_doctor(id:str):
    print(id)

    user = Pacienti.select().where(Pacienti.id_user == id).dicts()

    if user.exists():
        user = user.get()
        cnp = user['cnp']
        message = {"cnp": cnp}
        return JSONResponse(content=message, status_code=200)

    else:
        message = {"message": "The endpoint was not found."}
        return JSONResponse(content=message, status_code=404)


@app.get('/get_id_doctor/{id}')
def get_doctor(id:str):
    print(id)
    user = Doctori.select().where(Doctori.id_user == id).dicts()

    if user.exists():
        user = user.get()
        id_doctor = user['id_doctor']
        message = {"id_doctor": id_doctor}
        return JSONResponse(content=message, status_code=200)

    else:
        message = {"message": "The endpoint was not found."}
        return JSONResponse(content=message, status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8003)