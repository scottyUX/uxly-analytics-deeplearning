from peewee import SqliteDatabase, Model
import os

from utils.custom_keys import CustomKeys as ck

database = os.getenv(ck.DATABASE_URL)
# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(database, pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db
