import peewee
from peewee import MySQLDatabase, CharField, IntegerField, DateField, BooleanField

db = MySQLDatabase(database='pos', user='user', password='pass', port=3306)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Idm(BaseModel):
    id = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    role = CharField()

    class Meta:
        db_table = "IDM"


class Pacienti(BaseModel):
    cnp = CharField(primary_key=True)
    id_user = CharField()
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    telefon = CharField()
    data_nasterii = DateField()
    is_active = BooleanField()

    class Meta:
        db_table = "Pacienti3"


class Doctori(BaseModel):
    id_doctor = IntegerField(primary_key=True)
    id_user = CharField()
    nume = CharField()
    prenume = CharField()
    email = CharField(unique=True)
    telefon = CharField()
    specializare = CharField()

    class Meta:
        db_table = "Doctori3"