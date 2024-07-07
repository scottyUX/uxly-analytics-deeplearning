from peewee import SqliteDatabase, Model

# Ensure foreign-key constraints are enforced.
db = SqliteDatabase('airdrops.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db
