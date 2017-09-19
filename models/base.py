import peewee
import peewee_async
import peewee_asyncext
from playhouse.postgres_ext import *
from playhouse.signals import Model, post_save
import datetime

# http://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database
# http://docs.peewee-orm.com/en/latest/peewee/api.html#Database.init

psql_db = peewee_asyncext.PooledPostgresqlExtDatabase(None)

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db

class CurrencyField(DecimalField):
    pass
