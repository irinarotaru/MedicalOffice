import peewee
from peewee import MySQLDatabase, Model, CharField, BooleanField, DateField, IntegerField, ForeignKeyField, Check, CompositeKey

db = MySQLDatabase(database='pos', user='user', password='pass', port=3306)


class BaseModel(peewee.Model):
    class Meta:
        database = db


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


class Programari(BaseModel):
    id_pacient = ForeignKeyField(model=Pacienti, column_name="id_pacient", to_field='cnp')
    id_doctor = ForeignKeyField(Doctori, column_name="id_doctor")
    data = DateField()
    status = CharField()

    class Meta:
        db_table = "Programari2"
        primary_key = CompositeKey('id_pacient', 'id_doctor', 'data')


class Idm(BaseModel):
    id = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    role = CharField()

    class Meta:
        db_table = "IDM"
