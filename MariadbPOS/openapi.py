import datetime

from pydantic import BaseModel
from typing import List, Union,Optional


class AppointmentInfo(BaseModel):
    id_pacient : str
    id_doctor: int
    data: datetime.date
    status: str
    links: List[dict]


class PatientInfo(BaseModel):
    cnp: str
    id_user: str
    nume: str
    prenume: str
    email: str
    telefon: str
    data_nasterii: datetime.date
    is_active: bool
    appointments: Union[List, str] = "query an appointment"
    links: Union[List[dict], None] = None


class Patient(BaseModel):
    patient: PatientInfo


class ChangeStatus(BaseModel):
    status: str


class Patients(BaseModel):
    patients: List[PatientInfo]
    links: List[dict]


class DoctorInfo(BaseModel):
    id_doctor: int
    id_user: str
    nume: str
    prenume: str
    email: str
    telefon: str
    specializare: str
    links: List[dict]


class Doctor(BaseModel):
    doctor: DoctorInfo


class Doctors(BaseModel):
    doctors: List[DoctorInfo]


class Appointment(BaseModel):
    appointments: List[AppointmentInfo]


class ResultInfo(BaseModel):
    id: int
    denumire: str
    durata_de_procesare: int
    rezultat: str


class Investigatii(BaseModel):
    investigatii: List[List[ResultInfo]]
    links: List[dict]


class Result(BaseModel):
    results: Investigatii


class Message(BaseModel):
    message: str
