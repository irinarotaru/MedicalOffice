from pydantic import BaseModel
from typing import List


class Investigation(BaseModel):
    id: int
    denumire: str
    durata_de_procesare: int
    rezultat: str


class MedicalRecord(BaseModel):
    id_pacient: str
    id_doctor: int
    data: str
    diagnostic: str
    investigatii: List[Investigation]
    links: List[dict]


class Consultation(BaseModel):
    consultations: List[MedicalRecord]


class Message(BaseModel):
    message: str
