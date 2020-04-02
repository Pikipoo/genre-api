from peewee import *

DATABASE_FILE = 'db/genre_api.db'

sqlite_db = SqliteDatabase(DATABASE_FILE, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
})


class BaseModel(Model):
    class Meta:
        database = sqlite_db
