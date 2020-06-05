from peewee import *

from settings import db_path

# SQLite database using WAL journal mode and 64MB cache.
sqlite_db = SqliteDatabase(db_path, pragmas={'journal_mode': 'wal',
                                                       'cache_size': 10000, 
                                                       'foreign_keys': 1,
                                                       'ignore_check_constraints': 0,
                                                       'synchronous': 0})

class BaseModel(Model):
    """A base model that will use our Sqlite database."""
    class Meta:
        database = sqlite_db

class Sphere(BaseModel):
    """Сфера"""
    name = CharField(unique=True)

class Subject(BaseModel):
    """Предмет"""
    name = CharField(unique=True)

class Direction(BaseModel):
    """Направления"""
    idNSTU          = IntegerField(null = True)
    name            = CharField(max_length=200, unique=True)
    faculty         = CharField(max_length=200)
    keys_plus       = CharField(max_length=200)
    ball_k          = IntegerField(null = True)
    ball_b          = IntegerField(null = True)
    url             = TextField()
    active          = BooleanField(default=True)
    description     = TextField(null = True)
    profile_name    = CharField(max_length=200, null = True)
    RN              = IntegerField(null = True)

class DirectionSphere(BaseModel):
    direction = ForeignKeyField(Direction)
    sphere = ForeignKeyField(Sphere)

class DirectionSubject(BaseModel):
    direction = ForeignKeyField(Direction)
    subject = ForeignKeyField(Subject)


class Faculty(BaseModel):
    name = CharField(max_length=200, unique=True)
    url = CharField(max_length=200)

class User(BaseModel):
    id = IntegerField(primary_key=True)
    is_sub = BooleanField(default=False)
    lk_code = IntegerField(default=-1)


class Contex(BaseModel):
    user = ForeignKeyField(User, primary_key=True)
    faculty = ForeignKeyField(Faculty, null=True, default = None)
    direction = ForeignKeyField(Direction, null=True, default = None)
    last_intent = CharField(max_length=100, null=True, default=None)
    paginator_page = IntegerField(null=True, default=1)


class ContexSubject(BaseModel):
    contex = ForeignKeyField(Contex)
    subject = ForeignKeyField(Subject)

class ContexSphere(BaseModel):
    contex = ForeignKeyField(Contex)
    sphere = ForeignKeyField(Sphere)



def create_tables():
    with sqlite_db:
        sqlite_db.create_tables([User, Contex, ContexSubject, ContexSphere])

if __name__ == "__main__":
    create_tables()